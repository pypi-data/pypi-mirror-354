import copy
from typing import Dict, Optional, Set

from .. import constants


def update_card_state(
    card: str,
    *,
    play_type: Optional[str] = None,
    discarded_cards: Set[str] = None,
    removed_cards: Set[str] = None,
    possible_draw_cards: Set[str] = None,
    cards_in_hands: Set[str] = None,
    is_defectors_discard: bool = False,
) -> Dict[str, Set[str]]:
    """Update card collections based on a played card.

    Args:
        card: The card being played
        play_type: Type of play (event, space race, etc)
        discarded_cards: Current set of discarded cards
        removed_cards: Current set of removed cards
        possible_draw_cards: Current set of possible draw cards
        cards_in_hands: Current set of cards in hands

    Returns:
        Dict containing updated card collections
    """
    # Skip The China Card since it has special handling
    if card == "The China Card":
        return {
            "discarded_cards": discarded_cards or set(),
            "removed_cards": removed_cards or set(),
            "possible_draw_cards": possible_draw_cards or set(),
            "cards_in_hands": cards_in_hands or set(),
        }

    # Make defensive copies of input sets
    discarded_cards = (
        copy.deepcopy(discarded_cards) if discarded_cards is not None else set()
    )
    removed_cards = copy.deepcopy(removed_cards) if removed_cards is not None else set()
    possible_draw_cards = (
        copy.deepcopy(possible_draw_cards) if possible_draw_cards is not None else set()
    )
    cards_in_hands = (
        copy.deepcopy(cards_in_hands) if cards_in_hands is not None else set()
    )

    if play_type == constants.PlayType.REVEALS:
        # For reveals, add to cards_in_hands and remove from discard, if its there
        # happens with SALT, probably Star Wars
        cards_in_hands.add(card)
        discarded_cards.discard(card)

    # Handle card state based on play type
    elif play_type == constants.PlayType.EVENT:
        # For events, starred cards are removed, others are discarded
        if card.endswith("*"):
            removed_cards.add(card)
            discarded_cards.discard(card)
        else:
            discarded_cards.add(card)
        cards_in_hands.discard(card)
    else:
        if is_defectors_discard:
            discarded_cards.add(card)
            removed_cards.discard(card)
            cards_in_hands.discard(card)
        # For non-events (space race, influence, etc),
        # card goes to discard unless it's already removed
        else:
            if card not in removed_cards:
                discarded_cards.add(card)
            cards_in_hands.discard(card)

    # Always remove from possible draws and hands
    possible_draw_cards.discard(card)

    return {
        "discarded_cards": discarded_cards,
        "removed_cards": removed_cards,
        "possible_draw_cards": possible_draw_cards,
        "cards_in_hands": cards_in_hands,
    }
