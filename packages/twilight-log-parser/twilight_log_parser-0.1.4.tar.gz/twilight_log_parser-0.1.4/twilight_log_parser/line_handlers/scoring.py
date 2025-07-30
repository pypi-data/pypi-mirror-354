from typing import Dict

from .. import constants
from ..core import Game
from .base import LineHandler


class ScoreHandler(LineHandler):
    def __init__(self) -> None:
        """Initialize handler for score lines"""
        super().__init__(
            pattern=(
                rf"(?!Turn \d+, Cleanup: : )(?!: : )(?!Turn \d+, "
                rf"(?:{constants.Side.US.value}|{constants.Side.USSR.value}) AR\d+:)"
                rf"(?:.*Score is (?P<player>{constants.Side.US.value}|"
                rf"{constants.Side.USSR.value}) "
                rf"(?P<score>\d+)|.*Score is even)"
            )
        )

    def handle(self, game: Game, data: Dict[str, str], _: str) -> None:
        """Handle score updates by calculating and setting new score"""
        # handling "Score is even"
        if not data["player"]:
            updated_score = 0
        else:
            updated_score = (
                -int(data["score"])
                if data["player"] == constants.Side.US
                else int(data["score"])
            )
        game.current_play.updated_score = updated_score
        game.score = updated_score


class FinalScoreHandler(LineHandler):
    def __init__(self) -> None:
        """Initialize handler for final score lines"""
        super().__init__(
            pattern=(
                rf"(?:: : (?:{constants.Side.US.value}|"
                rf"{constants.Side.USSR.value}) gains \d+ VP\. "
                rf"Score is (?P<player>{constants.Side.US.value}|"
                rf"{constants.Side.USSR.value}) "
                rf"(?P<score>\d+)\.|: : )"
            )
        )

    def handle(self, game: Game, data: Dict[str, str], _: str) -> None:
        """Handle final scoring by calculating final score and creating final play"""
        updated_score = None
        score = data.get("score")
        player = data.get("player")
        if score is not None and player is not None:
            updated_score = -int(score) if player == constants.Side.US else int(score)
            game.score = updated_score

        game.create_new_play(
            turn=11,
            action_round=0,
            order_in_ar=None,
            ar_owner=None,
            action_executor=None,
            play_type=constants.PlayType.FINAL_SCORING,
            card=None,
            updated_score=updated_score,
        )
