import copy
from typing import Dict

from .. import constants
from ..core import Game
from ..utils.card_state import update_card_state
from .base import LineHandler


class RevealsHandler(LineHandler):
    def __init__(self) -> None:
        """Initialize handler for card reveal lines"""
        super().__init__(
            pattern=(
                rf"(?P<action_executor>{constants.Side.US.value}|"
                rf"{constants.Side.USSR.value}) "
                rf"reveals (?P<card>.+?)(?=(?: from hand)?$)"
            )
        )

    def handle(self, game: Game, data: Dict[str, str], _: str) -> None:
        """Handle card reveals by updating revealed cards and card locations"""
        if data["card"] not in game.current_play.revealed_cards:
            game.current_play.revealed_cards.append(data["card"])

        card_state_data = update_card_state(
            data["card"],
            play_type=constants.PlayType.REVEALS,
            discarded_cards=game.current_play.discarded_cards,
            removed_cards=game.current_play.removed_cards,
            possible_draw_cards=game.current_play.possible_draw_cards,
            cards_in_hands=game.current_play.cards_in_hands,
        )

        game.current_play.discarded_cards = card_state_data["discarded_cards"]
        game.current_play.removed_cards = card_state_data["removed_cards"]
        game.current_play.possible_draw_cards = card_state_data["possible_draw_cards"]
        game.current_play.cards_in_hands = card_state_data["cards_in_hands"]


class DiscardsHandler(LineHandler):
    def __init__(self) -> None:
        """Initialize handler for card discard lines"""
        super().__init__(
            pattern=(
                rf"(?P<action_executor>{constants.Side.US.value}|"
                rf"{constants.Side.USSR.value}) "
                rf"discards (?P<card>.*)"
            )
        )

    def handle(self, game: Game, data: Dict[str, str], _: str) -> None:
        """Handle card discards by updating discard pile and card locations"""
        prior_play_rec = game.current_play

        # For US cards, the game logs that FYP discards it
        # but it also plays the event, which is effectively a discard
        # we don't want to get confused about whether or not this card
        # is in the discard pile, so instead we should skip the discard
        # record in that case.
        if prior_play_rec.card == "Five Year Plan":
            if game.is_us_card(data["card"]):
                return

        prior_play_rec = game.get_copy_of_current_play_cleaned_up()
        data = {**vars(prior_play_rec), **data}

        if data["order_in_ar"] is not None:
            data["order_in_ar"] += 1

        data["play_type"] = constants.PlayType.DISCARD
        data.update(
            update_card_state(
                data["card"],
                play_type=constants.PlayType.DISCARD.value,
                discarded_cards=game.current_play.discarded_cards,
                removed_cards=game.current_play.removed_cards,
                possible_draw_cards=game.current_play.possible_draw_cards,
                cards_in_hands=game.current_play.cards_in_hands,
            )
        )

        game.create_new_play(**data)


class ReshuffleHandler(LineHandler):
    def __init__(self) -> None:
        """Initialize handler for deck reshuffle lines"""
        super().__init__(
            pattern=r"\*RESHUFFLE\*",  # noqa: W605
        )

    def handle(self, game: Game, data: Dict[str, str], _: str) -> None:
        """Handle deck reshuffles by moving cards between appropriate piles"""
        # TODO: not sure how this handles a mid-turn reshuffle from kennedy/OMIT

        # Reshuffle line appears after headline plays, requiring special handling
        is_headline = False
        if game.current_play.action_round == 0 and game.current_play.order_in_ar == 0:
            is_headline = True
            # Check if headlined cards were in discard pile at end of previous turn
            headline_plays = game.get_all_plays_from_current_ar()

            headline_discard_cards = []
            headline_removed_cards = []
            for play in headline_plays:
                if play.card in game.current_play.discarded_cards:
                    headline_discard_cards.append(play.card)
                    play.discarded_cards.remove(play.card)

                if play.card in game.current_play.removed_cards:
                    headline_removed_cards.append(play.card)
                    play.removed_cards.remove(play.card)

        # Move draw pile into cards in hands
        cards_in_hands = copy.deepcopy(game.current_play.cards_in_hands).union(
            game.current_play.possible_draw_cards
        )
        possible_draw_cards = set()

        # Move discard pile into possible draw pile
        possible_draw_cards = possible_draw_cards.union(
            game.current_play.discarded_cards
        )
        discarded_cards = set()

        # Create a new play for the reshuffle
        game.create_new_play(
            play_type=constants.PlayType.RESHUFFLE,
            action_round=-1 if is_headline else game.current_play.action_round,
            order_in_ar=0 if is_headline else (game.current_play.order_in_ar or 0) + 1,
            turn=game.current_turn,
            card=None,
            ar_owner=None,
            action_executor=None,
            cards_in_hands=cards_in_hands,
            possible_draw_cards=possible_draw_cards,
            discarded_cards=discarded_cards,
        )

        if is_headline:
            for play in headline_plays:
                play.cards_in_hands = copy.deepcopy(cards_in_hands)
                play.possible_draw_cards = copy.deepcopy(possible_draw_cards)
                play.discarded_cards = copy.deepcopy(discarded_cards).union(
                    headline_discard_cards
                )
                play.removed_cards = copy.deepcopy(play.removed_cards).union(
                    headline_removed_cards
                )

            game.current_play = headline_plays[1]
            game.current_turn = headline_plays[1].turn
            game.current_ar = headline_plays[1].action_round
            game.current_event = headline_plays[1].card
