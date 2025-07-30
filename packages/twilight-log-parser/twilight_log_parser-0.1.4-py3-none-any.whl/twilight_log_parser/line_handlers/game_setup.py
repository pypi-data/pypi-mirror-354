from typing import Dict

from .. import constants
from ..core import Game
from ..utils import helpers
from .base import LineHandler


class PlayerSetupHandler(LineHandler):
    def __init__(self) -> None:
        """Initialize handler for player setup lines"""
        super().__init__(
            pattern=(
                r"^(?:SETUP: : )?(?P<playdek_id>.+?)\s+will play as "
                rf"(?P<player>{constants.Side.US.value}(?:A)?|"
                rf"{constants.Side.USSR.value})\.$"
            ),
        )

    def handle(self, game: Game, data: Dict, _: str) -> None:
        """Handle player setup by setting player IDs"""
        if data["player"] == constants.Side.USSR:
            game.ussr_player = data["playdek_id"].strip()
        if data["player"] in (constants.Side.US, constants.Side.US + "A"):
            game.us_player = data["playdek_id"].strip()


class HandicapHandler(LineHandler):
    def __init__(self) -> None:
        """Initialize handler for handicap lines"""
        super().__init__(
            pattern=(
                rf"Handicap influence: (?P<player>{constants.Side.US.value}|"
                rf"{constants.Side.USSR.value}) (?P<handicap>[+|-]\d+)"
            )
        )

    def handle(self, game: Game, data: Dict, _: str) -> None:
        """Handle handicap by setting game handicap"""
        game.handicap = f"{data['player']}: {data['handicap']}"


class ScenarioHandler(LineHandler):
    def __init__(self) -> None:
        """Initialize handler for scenario lines"""
        super().__init__(pattern=r"Scenario: (?P<scenario>.*)")

    def handle(self, game: Game, data: Dict, _: str) -> None:
        """Handle scenario by setting game scenario"""
        game.scenario = data["scenario"]


class OptionalCardsHandler(LineHandler):
    def __init__(self) -> None:
        """Initialize handler for optional cards lines"""
        super().__init__(pattern=r"Optional Cards Added")

    def handle(self, game: Game, data: Dict, _: str) -> None:
        """Handle optional cards by setting flag"""
        game.optional_cards = True


class TimerHandler(LineHandler):
    def __init__(self) -> None:
        """Initialize handler for timer lines"""
        super().__init__(pattern=r"Time per Player: (?P<play_time_text>.*)s{0,1}")

    def handle(self, game: Game, data: Dict, _: str) -> None:
        """Handle timer by converting and setting play time"""
        play_time_minutes = helpers.convert_play_time_text_to_minutes(
            data["play_time_text"]
        )
        game.play_time_minutes = int(play_time_minutes)
