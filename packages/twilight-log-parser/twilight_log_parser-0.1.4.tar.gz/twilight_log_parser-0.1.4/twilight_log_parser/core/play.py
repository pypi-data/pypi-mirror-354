from dataclasses import dataclass
from typing import List, Optional, Set

from .board import Board


@dataclass
class InfluenceChange:
    """Represents a change in influence in a country"""

    country: str
    side: str
    change: int


class Play:
    """Represents a single play/action in the game with its full state"""

    def __init__(
        self,
        turn: int,
        action_round: int,
        order_in_ar: int,
        ar_owner: str,
        action_executor: str,
        card: Optional[str],
        play_type: str,
        board_state: "Board",
        cards_in_hands: Set[str],
        removed_cards: Set[str],
        discarded_cards: Set[str],
        possible_draw_cards: Set[str],
        updated_score: Optional[int] = None,
        updated_defcon: Optional[int] = None,
        updated_space_position: Optional[int] = None,
        revealed_cards: Optional[List[str]] = None,
        headline_order: Optional[int] = None,
        updated_us_mil_ops: Optional[int] = None,
        updated_ussr_mil_ops: Optional[int] = None,
        target_countries: Optional[List[str]] = None,
        us_die_rolls: Optional[List[int]] = None,
        ussr_die_rolls: Optional[List[int]] = None,
        ussr_effects: Optional[List[str]] = None,
        us_effects: Optional[List[str]] = None,
        influence_changes: Optional[List[InfluenceChange]] = None,
    ) -> None:
        self.turn = turn
        self.action_round = action_round
        self.order_in_ar = order_in_ar
        self.ar_owner = ar_owner
        self.action_executor = action_executor
        self.headline_order = headline_order
        self.card = card
        self.play_type = play_type
        self.board_state = board_state
        self.updated_score = updated_score
        self.updated_defcon = updated_defcon
        self.updated_space_position = updated_space_position
        self.updated_us_mil_ops = updated_us_mil_ops
        self.updated_ussr_mil_ops = updated_ussr_mil_ops
        self.revealed_cards = revealed_cards if revealed_cards is not None else []
        self.target_countries = [] if target_countries is None else target_countries
        self.us_die_rolls = [] if us_die_rolls is None else us_die_rolls
        self.ussr_die_rolls = [] if ussr_die_rolls is None else ussr_die_rolls
        self.ussr_effects = [] if ussr_effects is None else ussr_effects
        self.us_effects = [] if us_effects is None else us_effects
        self.influence_changes = [] if influence_changes is None else influence_changes
        self.possible_draw_cards = possible_draw_cards
        self.discarded_cards = discarded_cards
        self.removed_cards = removed_cards
        self.cards_in_hands = cards_in_hands
