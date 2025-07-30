import copy
from typing import Dict

from .. import constants
from ..core import Game, InfluenceChange
from .base import LineHandler


class CleanupHandler(LineHandler):
    def __init__(self) -> None:
        """Initialize handler for cleanup phase lines"""
        super().__init__(pattern=r"Turn \d+, Cleanup: : (?P<cleanup_details>.*)")
        self.parser = None

    def handle(self, game: Game, data: Dict[str, str], _: str) -> None:
        """Handle cleanup phase by processing cleanup details and updating game state"""
        game.defcon += 1
        game.create_new_play(
            turn=game.current_turn,
            action_round=9,
            order_in_ar=None,
            ar_owner=None,
            action_executor=None,
            play_type=constants.PlayType.CLEANUP,
            card=None,
            updated_defcon=game.defcon,
            updated_us_mil_ops=0,
            updated_ussr_mil_ops=0,
        )

        cleanup_details_line = data["cleanup_details"]
        if self.parser:  # Only process if parser has been set
            handler_name, handler_data = self.parser._identify_line(
                cleanup_details_line
            )
            if handler_name and handler_name in self.parser.handlers:
                self.parser.handlers[handler_name].handle(
                    game, handler_data, cleanup_details_line
                )

        if game.current_turn == 3:
            game.current_play.possible_draw_cards.update(
                {
                    card.name
                    for card in game.CARDS.values()
                    if card.name != constants.SpecialCards.THE_CHINA_CARD
                    and card.war == constants.War.MID
                }
            )
        if game.current_turn == 7:
            game.current_play.possible_draw_cards.update(
                {
                    card.name
                    for card in game.CARDS.values()
                    if card.name != constants.SpecialCards.THE_CHINA_CARD
                    and card.war == constants.War.LATE
                }
            )


class DefconHandler(LineHandler):
    def __init__(self) -> None:
        """Initialize handler for DEFCON change lines"""
        super().__init__(pattern=r"DEFCON (?:degrades|improves) to (?P<defcon>\d)")

    def handle(self, game: Game, data: Dict[str, str], _: str) -> None:
        """Handle DEFCON changes by updating DEFCON level"""
        prior_play_rec = game.current_play
        new_defcon = int(data["defcon"])
        prior_play_rec.updated_defcon = new_defcon
        game.defcon = new_defcon


class MilOpsHandler(LineHandler):
    def __init__(self) -> None:
        """Initialize handler for military operations lines"""
        super().__init__(
            pattern=(
                rf"(?P<player>{constants.Side.US.value}|{constants.Side.USSR.value}) "
                rf"Military Ops to (?P<mil_ops>\d+)"
            )
        )

    def handle(self, game: Game, data: Dict[str, str], _: str) -> None:
        """Handle military operations by updating mil ops levels"""
        player = data["player"]
        mil_ops = int(data["mil_ops"])

        current_play = game.current_play

        if player == constants.Side.US:
            current_play.updated_us_mil_ops = mil_ops
        else:
            current_play.updated_ussr_mil_ops = mil_ops


class UpdateInfluenceHandler(LineHandler):
    def __init__(self) -> None:
        """Initialize handler for influence update lines"""
        super().__init__(
            pattern=(
                rf"(?P<player>{constants.Side.US.value}|{constants.Side.USSR.value}) "
                rf"(?P<direction>[+-])(?P<change>\d+) in (?P<country>.+?) "
                rf"\[(?P<us_inf>\d+)\]\[(?P<ussr_inf>\d+)\]"
            )
        )

    def handle(self, game: Game, data: Dict[str, str], _: str) -> None:
        """Handle influence updates by modifying board state and recording changes"""
        country = data["country"]
        direction = data["direction"]
        change = int(data["change"])
        player = data["player"]
        expected_us_inf = int(data["us_inf"])
        expected_ussr_inf = int(data["ussr_inf"])

        # Update the game state influence values
        if direction == "+":
            game.board_state.add_influence(country, player, change)
        else:
            game.board_state.remove_influence(country, player, change)

        # Validate that the stored influence matches what's expected from the log
        actual_us_inf = game.board_state.country_statuses[country].us_influence
        actual_ussr_inf = game.board_state.country_statuses[country].ussr_influence

        if actual_us_inf != expected_us_inf or actual_ussr_inf != expected_ussr_inf:
            raise ValueError(
                f"Influence mismatch in {country}: "
                f"Expected US={expected_us_inf}, USSR={expected_ussr_inf} "
                f"but got US={actual_us_inf}, USSR={actual_ussr_inf}"
            )

        # handle creating a play for placing initial influence
        if (
            game.current_turn == 0
            and game.current_play.ar_owner == constants.Side.USSR
            and player == constants.Side.US
        ):
            game.create_new_play(
                turn=game.current_turn,
                action_round=game.current_ar,
                order_in_ar=game.current_play.order_in_ar + 1,
                ar_owner=constants.Side.US,
                action_executor=constants.Side.US,
                play_type=constants.PlayType.INITIAL_SETUP,
                board_state=copy.deepcopy(game.board_state),
                card=None,
            )

        current_play = game.current_play

        if (
            current_play.action_round == 0
            and game.current_event != game.current_play.card
        ):
            current_play = game.get_last_play_for_kwargs(
                turn=game.current_turn,
                card=game.current_event,
            )

        current_play.board_state = copy.deepcopy(game.board_state)

        current_play.influence_changes.append(
            InfluenceChange(
                country=country, side=player, change=int(direction + str(change))
            )
        )


class InPlayHandler(LineHandler):
    def __init__(self) -> None:
        """Initialize handler for card in/out of play lines"""
        super().__init__(
            pattern=(
                r"^(?!Turn \d+, US AR\d+:)"
                r"(?P<card>.*?) is (?P<status>now|no longer) in play\.$"
            )
        )

    def handle(self, game: Game, data: Dict[str, str], _: str) -> None:
        """Handle cards entering/leaving play by updating effect lists"""
        effect_card = data["card"]
        if data["status"] == constants.CardStatus.IN_PLAY:
            if game.is_us_card(effect_card):
                game.current_play.us_effects.append(effect_card)
            elif game.is_ussr_card(effect_card):
                game.current_play.ussr_effects.append(effect_card)
            else:
                if effect_card in constants.SpecialCards.BOTH_EFFECT_NEUTRAL:
                    game.current_play.us_effects.append(effect_card)
                    game.current_play.ussr_effects.append(effect_card)
                elif effect_card in constants.SpecialCards.OPPONENT_EFFECT_NEUTRAL:
                    if game.current_play.action_executor == constants.Side.US:
                        game.current_play.ussr_effects.append(effect_card)
                    else:
                        game.current_play.us_effects.append(effect_card)
            if game.current_play.headline_order == 0:
                second_headline_play = game.get_last_play_for_kwargs(
                    turn=game.current_turn,
                    action_round=game.current_ar,
                    headline_order=1,
                )
                second_headline_play.us_effects = game.current_play.us_effects
                second_headline_play.ussr_effects = game.current_play.ussr_effects

        elif data["status"] == constants.CardStatus.OUT_OF_PLAY:
            if game.is_us_card(effect_card):
                if effect_card in game.current_play.us_effects:
                    game.current_play.us_effects.remove(effect_card)
            elif game.is_ussr_card(effect_card):
                if effect_card in game.current_play.ussr_effects:
                    game.current_play.ussr_effects.remove(effect_card)
            else:
                if effect_card in constants.SpecialCards.BOTH_EFFECT_NEUTRAL:
                    if effect_card in game.current_play.us_effects:
                        game.current_play.us_effects.remove(effect_card)
                    if effect_card in game.current_play.ussr_effects:
                        game.current_play.ussr_effects.remove(effect_card)
                elif effect_card in constants.SpecialCards.OPPONENT_EFFECT_NEUTRAL:
                    if game.current_play.action_executor == constants.Side.US:
                        if effect_card in game.current_play.ussr_effects:
                            game.current_play.ussr_effects.remove(effect_card)
                    else:
                        if effect_card in game.current_play.us_effects:
                            game.current_play.us_effects.remove(effect_card)
            if game.current_play.headline_order == 0:
                second_headline_play = game.get_last_play_for_kwargs(
                    turn=game.current_turn,
                    action_round=game.current_ar,
                    headline_order=1,
                )
                second_headline_play.us_effects = game.current_play.us_effects
                second_headline_play.ussr_effects = game.current_play.ussr_effects
        else:
            raise ValueError(f'Invalid status in in_play line: {data["status"]}')
