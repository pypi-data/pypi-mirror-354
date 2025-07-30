from dataclasses import dataclass


@dataclass(frozen=True)
class Country:
    """Represents a country on the game board with its properties"""

    name: str
    region: str
    is_battleground: bool
    stability: int
    is_sea: bool
    is_west_europe: bool
    is_east_europe: bool
    touches_us: bool
    touches_ussr: bool
    starting_ussr_influence: int
    starting_us_influence: int
