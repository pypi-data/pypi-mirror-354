import copy
from typing import Dict

from .. import constants
from ..core import Game
from .base import LineHandler


class GrainSalesReturnedHandler(LineHandler):
    def __init__(self) -> None:
        """Initialize handler for Grain Sales return lines"""
        super().__init__(
            pattern=(
                rf"(?P<action_executor>{constants.Side.US.value}|"
                rf"{constants.Side.USSR.value}) "
                rf"returns (?P<card>.*) to ({constants.Side.US.value}|"
                rf"{constants.Side.USSR.value})"
            )
        )

    def handle(self, game: Game, data: Dict[str, str], _: str) -> None:
        """Handle Grain Sales returns by updating state when card returned"""
        prior_play_rec = game.get_last_play_for_kwargs(
            turn=game.current_turn,
        )

        if (
            prior_play_rec.card != constants.SpecialCards.GRAIN_SALES_TO_SOVIETS
            and prior_play_rec.play_type != constants.PlayType.EVENT
        ):
            raise ValueError("Issue with Grain Sales log - something is not right.")

        data = {**vars(prior_play_rec), **data}
        data["order_in_ar"] += 1
        data["play_type"] = constants.PlayType.RETURN_TO_HAND
        data["revealed_cards"] = []

        data["cards_in_hands"] = copy.deepcopy(game.current_play.cards_in_hands).union(
            {data["card"]}
        )
        data["possible_draw_cards"] = copy.deepcopy(
            game.current_play.possible_draw_cards
        ).difference({data["card"]})

        game.create_new_play(**data)
