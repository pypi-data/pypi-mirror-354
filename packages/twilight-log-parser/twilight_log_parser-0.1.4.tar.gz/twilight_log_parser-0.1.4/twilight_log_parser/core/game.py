import copy
import csv
import uuid
from typing import Any, Dict, List, Optional, Set

from frozendict import frozendict

from .. import constants
from ..utils import helpers
from .board import Board
from .card import Card
from .country import Country
from .play import Play


class Game:
    """Main game class that manages game state and progression."""

    def __init__(self, game_id: Optional[str] = None) -> None:
        # Load card data from CSV as immutable tuple of Card objects
        # Load card data from CSV as immutable tuple of Card objects
        with open(constants.FileConfig.CARDS_FILE) as cards_file:
            self.CARDS: frozendict[str, Card] = frozendict(
                {
                    helpers.clean_card_name(row["card_name"]): Card(
                        name=helpers.clean_card_name(row["card_name"]),
                        ops=int(row["ops_value"]),
                        war=row["war"],
                        side=row["side"],
                        is_scoring=row["is_scoring"].upper() == "TRUE",
                        is_optional=row["is_optional"].upper() == "TRUE",
                        is_permanent=False if row["card_name"].endswith("*") else True,
                    )
                    for row in csv.DictReader(
                        cards_file,
                        delimiter=constants.FileConfig.CSV_DELIMITER,
                    )
                }
            )

        # Load country data from CSV as immutable tuple of Country objects
        with open(constants.FileConfig.COUNTRIES_FILE) as countries_file:
            self.COUNTRIES: frozendict[str, Country] = frozendict(
                {
                    row["country"]: Country(
                        name=row["country"],
                        region=row["region"],
                        is_battleground=row["is_battleground"].upper() == "TRUE",
                        stability=int(row["stability"]),
                        is_sea=row["is_sea"].upper() == "TRUE",
                        is_west_europe=row["is_west_europe"].upper() == "TRUE",
                        is_east_europe=row["is_east_europe"].upper() == "TRUE",
                        touches_us=row["touches_us"].upper() == "TRUE",
                        touches_ussr=row["touches_ussr"].upper() == "TRUE",
                        starting_ussr_influence=int(row["starting_ussr_influence"]),
                        starting_us_influence=int(row["starting_us_influence"]),
                    )
                    for row in csv.DictReader(
                        countries_file,
                        delimiter=constants.FileConfig.CSV_DELIMITER,
                    )
                }
            )
        if game_id is not None:
            self.game_id = game_id
        else:
            self.game_id = uuid.uuid4()
        self.us_player: Optional[str] = None
        self.ussr_player: Optional[str] = None
        self.handicap: Optional[int] = None
        self.scenario: Optional[str] = None
        self.optional_cards: Optional[bool] = None
        self.play_time_minutes: Optional[int] = None
        self.winning_side: Optional[str] = None
        self.win_type: Optional[str] = None
        self.current_turn: int = 0
        self.current_ar: int = 0
        self.score: int = 0
        self.defcon: int = 5
        self.board_state: Board = Board(countries_data=self.COUNTRIES)
        self.current_event: Optional[str] = None
        self._current_possible_draw_cards: Set[str] = {
            card.name
            for card in self.CARDS.values()
            if card.name != constants.SpecialCards.THE_CHINA_CARD
            and card.war == constants.War.EARLY
        }
        self._current_discard_cards: Set[str] = set()
        self._current_removed_cards: Set[str] = set()
        self._current_cards_in_hands: Set[str] = set()
        self.current_play: Play = Play(
            turn=self.current_turn,
            action_round=self.current_ar,
            order_in_ar=0,
            ar_owner=constants.Side.USSR,
            action_executor=constants.Side.USSR,
            card=None,
            play_type=constants.PlayType.INITIAL_SETUP,
            board_state=self.board_state,
            possible_draw_cards={
                card.name
                for card in self.CARDS.values()
                if card.name != constants.SpecialCards.THE_CHINA_CARD
                and card.war == constants.War.EARLY
            },
            discarded_cards=set(),
            removed_cards=set(),
            cards_in_hands=set(),
        )
        self.plays: List[Play] = [self.current_play]

    def create_new_play(self, **kwargs: Any) -> Play:
        """Creates a new play record with the given parameters, copying over state from
        current play if not specified."""
        if "board_state" not in kwargs:
            kwargs["board_state"] = copy.deepcopy(self.board_state)
        if "us_effects" not in kwargs:
            kwargs["us_effects"] = copy.deepcopy(self.current_play.us_effects)
        if "ussr_effects" not in kwargs:
            kwargs["ussr_effects"] = copy.deepcopy(self.current_play.ussr_effects)
        if "possible_draw_cards" not in kwargs:
            kwargs["possible_draw_cards"] = copy.deepcopy(
                self.current_play.possible_draw_cards
            )
        if "discarded_cards" not in kwargs:
            kwargs["discarded_cards"] = copy.deepcopy(self.current_play.discarded_cards)
        if "removed_cards" not in kwargs:
            kwargs["removed_cards"] = copy.deepcopy(self.current_play.removed_cards)
        if "cards_in_hands" not in kwargs:
            kwargs["cards_in_hands"] = copy.deepcopy(self.current_play.cards_in_hands)
        play = Play(**kwargs)

        self.plays.append(play)
        self.current_turn = play.turn
        self.current_ar = play.action_round
        self.current_play = play
        if play.play_type == constants.PlayType.EVENT:
            self.current_event = play.card
        return play

    def get_copy_of_current_play_cleaned_up(self) -> Play:
        """Returns a copy of current play with transient state cleared."""
        copied_play = copy.deepcopy(self.current_play)
        copied_play.headline_order = None
        copied_play.revealed_cards = []
        copied_play.updated_score = None
        copied_play.updated_defcon = None
        copied_play.updated_space_position = None
        copied_play.updated_us_mil_ops = None
        copied_play.updated_ussr_mil_ops = None
        copied_play.target_countries = []
        copied_play.us_die_rolls = []
        copied_play.ussr_die_rolls = []
        copied_play.influence_changes = []

        return copied_play

    def get_last_play_for_kwargs(self, **kwargs: Any) -> Play:
        """Finds the most recent play matching the given criteria."""
        # iterate backwards over list of plays
        # to try to find the play associated with the **kwargs
        filters = kwargs.items()
        for play in self.plays[::-1]:
            match = True
            for key, value in filters:
                if type(value) in (tuple, list, set):
                    if getattr(play, key, None) not in value:
                        match = False
                else:
                    if getattr(play, key, None) != value:
                        match = False
                if match is True:
                    return play

        raise ValueError(f"Cannot find play record for kwargs: {kwargs}")

    def get_last_non_discard_play_record(self, ar_owner: Optional[str] = None) -> Play:
        """Gets the most recent play that wasn't a discard, optionally filtered by
        ar_owner."""
        if ar_owner is None:
            return self.get_last_play_for_kwargs(
                play_type=(
                    constants.PlayType.COUP,
                    constants.PlayType.PLACE_INFLUENCE,
                    constants.PlayType.EVENT,
                    constants.PlayType.SPACE_RACE,
                    constants.PlayType.REALIGNMENT,
                )
            )
        return self.get_last_play_for_kwargs(
            play_type=(
                constants.PlayType.COUP,
                constants.PlayType.PLACE_INFLUENCE,
                constants.PlayType.EVENT,
                constants.PlayType.SPACE_RACE,
                constants.PlayType.REALIGNMENT,
            ),
            ar_owner=ar_owner,
        )

    def get_ussr_headline(self) -> Play:
        """Gets the USSR headline play for the current turn."""
        return self.get_last_play_for_kwargs(
            turn=self.current_turn,
            ar_owner=constants.Side.USSR,
            action_round=0,
            order_in_ar=0,
        )

    def get_first_headline_play(self) -> Play:
        """Gets the first headline play for the current turn."""
        return self.get_last_play_for_kwargs(
            turn=self.current_turn,
            action_round=0,
            headline_order=0,
        )

    def get_all_plays_from_last_ar(self) -> List[Play]:
        """Gets all plays from the most recently completed action round."""
        plays_in_ar: List[Play] = []
        if len(self.plays) > 0:
            last_ar_owner = self.plays[-1].ar_owner
        else:
            return []
        for play in self.plays[::-1]:
            if (
                play.turn != self.current_turn
                or play.action_round != self.current_ar
                or play.ar_owner != last_ar_owner
            ):
                return list(reversed(plays_in_ar))
            plays_in_ar.append(play)

    def get_all_plays_from_current_ar(self) -> List[Play]:
        """Gets all plays from the current action round."""
        plays_in_ar: List[Play] = []
        if len(self.plays) == 0:
            return []
        for play in self.plays[::-1]:
            if play.turn == self.current_turn and play.action_round == self.current_ar:
                plays_in_ar.append(play)
        return plays_in_ar

    def output_all_plays_to_csv(self, location: str = "test.csv") -> None:
        """Outputs all plays and board states to CSV files for analysis."""
        # Write plays CSV
        play_headers = [h for h in vars(self.plays[0]).keys() if h != "board_state"]
        plays_location = location
        states_location = location.replace(".csv", "_states.csv")

        # Sort plays by turn, action_round, order_in_ar
        sorted_plays = sorted(
            self.plays,
            key=lambda x: (
                x.turn if x.turn is not None else float("-inf"),
                x.action_round if x.action_round is not None else float("-inf"),
                x.ar_owner[::-1] if x.ar_owner else None,
                x.order_in_ar if x.order_in_ar is not None else float("-inf"),
            ),
        )

        with open(plays_location, mode="w", newline="") as plays_file:
            plays_writer = csv.DictWriter(
                plays_file,
                fieldnames=play_headers,
                delimiter=constants.FileConfig.CSV_DELIMITER,
            )
            plays_writer.writeheader()

            with open(states_location, mode="w", newline="") as states_file:
                states_writer = csv.writer(
                    states_file, delimiter=constants.FileConfig.CSV_DELIMITER
                )
                states_writer.writerow(
                    [
                        "turn",
                        "action_round",
                        "order_in_ar",
                        "ar_owner",
                        "country",
                        "us_influence",
                        "ussr_influence",
                    ]
                )

                for play in sorted_plays:
                    # Write play record without board state, and convert
                    # influence_changes to list of dicts
                    play_dict: Dict[str, Any] = {}
                    for k, v in vars(play).items():
                        if k == "board_state":
                            continue
                        elif k == "influence_changes":
                            play_dict[k] = [
                                {
                                    "country": ic.country,
                                    "side": ic.side,
                                    "change": ic.change,
                                }
                                for ic in v
                            ]
                        elif isinstance(v, set) and len(v) == 0:
                            play_dict[k] = "null"
                        else:
                            play_dict[k] = v
                    plays_writer.writerow(play_dict)

                    # Write board state with play identifier
                    for country, state in play.board_state.country_statuses.items():
                        states_writer.writerow(
                            [
                                play.turn,
                                play.action_round,
                                play.order_in_ar,
                                play.ar_owner,
                                country,
                                state.us_influence,
                                state.ussr_influence,
                            ]
                        )

    def check_region_control(self, region: str) -> Optional[str]:
        """Returns US, USSR, or None based on who controls all battlegrounds in a
        region."""
        # Read countries data to get battlegrounds and stability
        battleground_stabilities = {
            country: data.stability
            for country, data in self.COUNTRIES.items()
            if data.region == region and data.is_battleground
        }

        # Check control of each battleground
        us_controls = 0
        ussr_controls = 0

        for country in battleground_stabilities:
            country_status = self.board_state.country_statuses[country]

            # Control requires influence >= stability + opponent influence
            if (
                country_status.us_influence
                >= battleground_stabilities[country] + country_status.ussr_influence
            ):
                us_controls += 1
            elif (
                country_status.ussr_influence
                >= battleground_stabilities[country] + country_status.us_influence
            ):
                ussr_controls += 1

        # Return controlling power if they control all battlegrounds
        if us_controls == len(battleground_stabilities):
            return constants.Side.US
        elif ussr_controls == len(battleground_stabilities):
            return constants.Side.USSR
        return None

    def is_us_card(self, card: str) -> bool:
        """Checks if a card belongs to the US side."""
        card_details = self.CARDS.get(card, None)
        if card_details is None:
            raise ValueError(f"Card '{card}' does not exist")
        return card_details.side == constants.Side.US

    def is_ussr_card(self, card: str) -> bool:
        """Checks if a card belongs to the USSR side."""
        card_details = self.CARDS.get(card, None)
        if card_details is None:
            raise ValueError(f"Card '{card}' does not exist")
        return card_details.side == constants.Side.USSR

    def determine_win_type(self) -> None:
        """Determine and write win type based on game state. Possible win types:

        - DEFCON: Game ends when DEFCON drops to 1
        - Europe Control: Controlling all battlegrounds in Europe
        - VP +20: Reaching 20 VP lead
        - Final: Game ends after final scoring
        - CMC: Cuban Missile Crisis in effect and opponent coups
        - Forfiet: Not possible to calculate, left as "unknown"
        - "unknown": Not possible to determine win type, left as "unknown"
        """
        self.win_type = "unknown"
        self.winning_side = "unknown"

        if self.defcon == 1:
            self.win_type = "DEFCON"
            self.winning_side = (
                constants.Side.USSR
                if self.current_play.ar_owner == constants.Side.US
                else constants.Side.US
            )
            return

        if (
            "Cuban Missile Crisis*" in self.current_play.us_effects
            and self.current_play.play_type == constants.PlayType.COUP
            and self.action_executor == constants.Side.US
        ):
            self.win_type = "Cuban Missile Crisis"
            self.winning_side = constants.Side.USSR
            return

        if (
            "Cuban Missile Crisis*" in self.current_play.ussr_effects
            and self.current_play.play_type == constants.PlayType.COUP
            and self.current_play.action_executor == constants.Side.USSR
        ):
            self.win_type = "Cuban Missile Crisis"
            self.winning_side = constants.Side.US
            return

        europe_controller = self.check_region_control("Europe")
        if europe_controller is not None and (
            self.current_play.card == "Europe Scoring" or self.current_turn > 10
        ):
            self.win_type = "Europe Control"
            self.winning_side = europe_controller
            return

        if self.current_turn > 10:
            self.win_type = "Final"
            self.winning_side = (
                constants.Side.USSR if self.score >= 0 else constants.Side.US
            )
            return

        if self.score >= 20 or self.score <= -20:
            self.win_type = "vp_20"
            self.winning_side = (
                constants.Side.USSR if self.score >= 0 else constants.Side.US
            )
            return
