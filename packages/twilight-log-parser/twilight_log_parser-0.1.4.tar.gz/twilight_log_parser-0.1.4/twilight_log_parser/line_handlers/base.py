import re
from abc import ABC, abstractmethod
from typing import Dict, Pattern

from ..core import Game


class LineHandler(ABC):
    def __init__(self, pattern: str) -> None:
        """Initialize line handler with regex pattern"""
        self.pattern: Pattern = re.compile(pattern)

    @abstractmethod
    def handle(self, game: Game, data: Dict, line: str) -> None:
        """Process the matched line and update the game state"""
        pass
