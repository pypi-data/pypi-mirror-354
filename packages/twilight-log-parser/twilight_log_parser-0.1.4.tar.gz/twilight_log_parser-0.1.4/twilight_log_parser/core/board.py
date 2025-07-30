from dataclasses import dataclass
from typing import Dict

from .. import constants
from .country import Country


@dataclass
class CountryStatus:
    """Tracks the influence levels of both sides in a country"""

    us_influence: int = 0
    ussr_influence: int = 0

    def add_influence(self, player: str, amount: int) -> None:
        """Add influence for the specified player"""
        if player == constants.Side.US:
            self.us_influence += amount
        elif player == constants.Side.USSR:
            self.ussr_influence += amount

    def remove_influence(self, player: str, amount: int) -> None:
        """Remove influence for the specified player, ensuring it doesn't go below 0"""
        if player == constants.Side.US:
            self.us_influence -= amount
        elif player == constants.Side.USSR:
            self.ussr_influence -= amount
        if self.us_influence < 0 or self.ussr_influence < 0:
            raise ValueError(f"Cannot reduce {player} influence below 0 in {self.name}")


class Board:
    """Represents the game board and tracks influence in all countries"""

    def __init__(self, countries_data: Dict[str, Country]) -> None:
        self.country_statuses: Dict[str, CountryStatus] = {}
        self.countries_data = countries_data
        self._load_countries()

    def _load_countries(self) -> None:
        """Initialize countries with their starting influence levels"""
        for country_name, country_data in self.countries_data.items():
            us_influence = country_data.starting_us_influence
            ussr_influence = country_data.starting_ussr_influence
            if us_influence > 0 or ussr_influence > 0:
                self.country_statuses[country_name] = CountryStatus(
                    us_influence=us_influence, ussr_influence=ussr_influence
                )

    def add_influence(self, country_name: str, player: str, amount: int) -> None:
        """Add influence to a country for the specified player"""
        if (
            country_name not in self.country_statuses
            and country_name in self.countries_data.keys()
        ):
            self.country_statuses[country_name] = CountryStatus()
        self.country_statuses[country_name].add_influence(player, amount)

    def remove_influence(self, country_name: str, player: str, amount: int) -> None:
        """Remove influence from a country for the specified player"""
        if country_name in self.country_statuses:
            self.country_statuses[country_name].remove_influence(player, amount)
        else:
            raise ValueError(f"Country {country_name} not found")
