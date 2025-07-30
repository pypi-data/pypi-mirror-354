from dataclasses import dataclass


@dataclass(frozen=True)
class Card:
    """Represents a card in the game with its properties"""

    name: str
    ops: int
    war: str
    side: str
    is_scoring: bool
    is_optional: bool
    is_permanent: bool
