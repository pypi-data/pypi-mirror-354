"""Basic parser tests."""

import pathlib
import traceback
import unittest

from twilight_log_parser import log_parser


class TestGameParser(unittest.TestCase):
    """Test suite for game log parsing."""

    def setUp(self):
        """Set up test logs directory and files."""
        self.test_logs_dir = pathlib.Path(__file__).parent / "test_logs"
        self.log_files = list(self.test_logs_dir.glob("*.txt"))

    def test_can_parse_all_logs(self) -> None:
        """Test that all log files can be parsed without errors."""
        self.assertTrue(len(self.log_files) > 0, "No log files found in test directory")

        for log_file in self.log_files:
            try:
                parser = log_parser.LogParser()
                game = parser.parse_game_log(
                    log_location=str(log_file), output_csv=None
                )

                # Basic sanity checks
                self.assertIsNotNone(game.game_id, "Game ID not set")
                self.assertGreaterEqual(game.current_turn, 0, "Turn number not set")
                self.assertIsInstance(game.score, int, "Score should be an integer")
                self.assertTrue(
                    1 <= game.defcon <= 5, "DEFCON should be between 1 and 5"
                )
                self.assertGreater(len(game.plays), 0, "Game has no plays")
                self.assertIsNotNone(game.winning_side, "Game has no winner")
                self.assertIsNotNone(game.win_type, "Game has no win type")

            except Exception as e:
                self.fail(
                    f"Failed to parse log file: {log_file}\n"
                    f"Error: {str(e)}\n"
                    f"Traceback:\n{traceback.format_exc()}"
                )


if __name__ == "__main__":
    unittest.main()
