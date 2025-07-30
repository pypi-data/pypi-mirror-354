"""
Twilight Struggle game log parser.
Parses and analyzes game logs from Twilight Struggle digital edition.
"""

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from . import constants
from . import line_handlers as line_handlers
from .core.game import Game
from .utils import helpers


@dataclass
class LogParser:
    """Parser for Twilight Struggle game log files"""

    def __init__(self) -> None:
        # Initialize all handlers
        self.handlers: Dict[str, line_handlers.LineHandler] = {
            "PlayerSetupLine": line_handlers.PlayerSetupHandler(),
            "HandicapLine": line_handlers.HandicapHandler(),
            "ScenarioLine": line_handlers.ScenarioHandler(),
            "OptionalCardsLine": line_handlers.OptionalCardsHandler(),
            "TimerLine": line_handlers.TimerHandler(),
            "ARLine": line_handlers.ARHandler(),
            "NonARPlayLine": line_handlers.NonARPlayHandler(),
            "HeadlineLine": line_handlers.HeadlineHandler(),
            "HeadlineDetailsLine": line_handlers.HeadlineDetailsHandler(),
            "ScoreLine": line_handlers.ScoreHandler(),
            "FinalScoringLine": line_handlers.FinalScoreHandler(),
            "CleanupLine": line_handlers.CleanupHandler(),
            "DefconLine": line_handlers.DefconHandler(),
            "SpaceRaceLine": line_handlers.SpaceRaceHandler(),
            "PlaysCardLine": line_handlers.PlaysCardHandler(),
            "GrainSalesReturned": line_handlers.GrainSalesReturnedHandler(),
            "RevealsLine": line_handlers.RevealsHandler(),
            "DiscardsLine": line_handlers.DiscardsHandler(),
            "MilOpsLine": line_handlers.MilOpsHandler(),
            "TargetCountryLine": line_handlers.TargetCountryHandler(),
            "RollLine": line_handlers.RollHandler(),
            "InfluenceChangeLine": line_handlers.UpdateInfluenceHandler(),
            "InPlayLine": line_handlers.InPlayHandler(),
            "ReshuffleLine": line_handlers.ReshuffleHandler(),
        }
        self.handlers["CleanupLine"].parser = self

    def parse_game_log(
        self,
        log_location: str,
        output_csv: Optional[str] = None,
        write_on_failure=False,
    ) -> Game:
        """Parse the Twilight Struggle game log and return a
        fully built Game object.

        Reads the log file line by line, processes each line
        through appropriate handlers,
        and builds up the game state. Can output results to CSV.
        """
        game = Game()

        try:
            with open(log_location, "r") as file:
                line_group: List[Dict[str, Any]] = []
                for line in file:
                    line = helpers.fix_oas_founded(line)
                    handler_name, data = self._identify_line(line)
                    # If line is None, skip it
                    if handler_name is None:
                        continue

                    # If a particular line signals the end of a chunk,
                    # flush the line_group
                    if handler_name in constants.CHUNK_END_LINES:
                        self._update_situation(line_group, game)
                        line_group = []

                    line_group.append(
                        {"handler_name": handler_name, "data": data, "line": line}
                    )
        except Exception as e:
            if output_csv and write_on_failure:
                game.output_all_plays_to_csv(location=output_csv)
            raise e

        self._update_situation(line_group, game)

        if output_csv is not None:
            game.output_all_plays_to_csv(location=output_csv)

        game.determine_win_type()
        return game

    def _parse_with_regex(
        self, line: str, pattern: str
    ) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Try to match a line against a regex pattern. Returns whether there was a match
        and any captured groups from the pattern.
        """
        match = re.match(pattern, line)
        if match:
            return True, match.groupdict()
        return False, None

    def _identify_line(
        self, line: str
    ) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
        """
        Identify the type of log line and extract its data. Tries each handler's pattern
        in turn until a match is found.
        """
        for handler_name, handler in self.handlers.items():
            matched, data = self._parse_with_regex(line, handler.pattern)
            if matched:
                return handler_name, data

        # if len(line) > 10:
        #     print(f'could not match: {line}')
        return None, None

    def _update_situation(self, line_group: List[Dict[str, Any]], game: Game) -> None:
        """
        Process a group of related log lines and update the game state.
        Applies each line's
        handler in sequence and sorts the plays after each update.
        """
        for line in line_group:
            handler = self.handlers[line["handler_name"]]
            handler.handle(game, line["data"], line["line"])

            # Sort plays after each update
            game.plays.sort(
                key=lambda x: (
                    x.turn if x.turn is not None else float("-inf"),
                    x.action_round if x.action_round is not None else float("-inf"),
                    x.ar_owner[::-1] if x.ar_owner else "",
                    x.order_in_ar if x.order_in_ar is not None else float("-inf"),
                ),
            )

        self._validate_and_cleanup_line_group(line_group, game)

    def _validate_and_cleanup_line_group(
        self, line_group: List[Dict[str, Any]], game: Game
    ) -> None:
        """
        Validates and cleans up a group of plays after processing.
        Ensures the action round owner
        is properly credited with plays and fixes any misattributed die rolls.
        """
        if 0 <= game.current_ar <= 8:
            line_group_plays = game.get_all_plays_from_current_ar()
            if line_group_plays is not None and len(line_group_plays) > 0:
                did_owner_get_play = False
                for play in line_group_plays:
                    if play.ar_owner == play.action_executor:
                        did_owner_get_play = True

                if not did_owner_get_play:
                    original_executor = line_group_plays[-1].action_executor
                    line_group_plays[-1].action_executor = line_group_plays[-1].ar_owner
                    if original_executor == constants.Side.US:
                        line_group_plays[-1].ussr_die_rolls = line_group_plays[
                            -1
                        ].us_die_rolls
                        line_group_plays[-1].us_die_rolls = []
                    else:
                        line_group_plays[-1].us_die_rolls = line_group_plays[
                            -1
                        ].ussr_die_rolls
                        line_group_plays[-1].ussr_die_rolls = []

                # if its a sticky if card, and it got evented in headline,
                # we need to check that it actually got evented
                for play in line_group_plays:
                    if play.card in constants.SpecialCards.STICKY_IF_CARDS:
                        sticky_card_evented = False
                        if play.play_type == constants.PlayType.EVENT and (
                            play.action_round == 0
                        ):
                            for line in line_group:
                                if (
                                    line.get("data")
                                    and line["data"].get("play_type")
                                    == constants.PlayType.EVENT
                                ):
                                    sticky_card_evented = True
                        if sticky_card_evented:
                            for play_to_cleanup in line_group_plays:
                                play_to_cleanup.discarded_cards.add(play.card)
                                play_to_cleanup.removed_cards.discard(play.card)
