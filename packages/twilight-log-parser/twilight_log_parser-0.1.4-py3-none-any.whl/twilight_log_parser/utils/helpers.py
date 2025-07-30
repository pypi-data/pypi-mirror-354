import re
from typing import Dict, Optional

from .. import constants

TIME_UNIT_CONVERSIONS: Dict[str, int] = {
    "minute": 1,
    "hour": 60,
    "day": 1440,
    "week": 10080,
    "month": 43800,
    "year": 525600,
}


def convert_play_time_text_to_minutes(play_time_text: str) -> int:
    """
    Convert a text description of time (e.g. '2 hours 30 minutes') into total minutes.
    Supports units: minute, hour, day, week, month, year.
    Returns the total number of minutes.
    """
    pattern = r"(\d+)\s*(minute|hour|day|week|month|year)s?"

    # Find matches in the time_text
    matches = re.findall(pattern, play_time_text, re.IGNORECASE)
    total_minutes = 0

    # Iterate over matches and calculate total minutes
    for value, unit in matches:
        total_minutes += int(value) * TIME_UNIT_CONVERSIONS[unit.lower()]

    return total_minutes


def str_to_bool(s: str) -> Optional[bool]:
    """
    Convert a string representation to a boolean value.
    Returns None if empty string, True for 'true', False for 'false'.
    Raises ValueError for invalid values.
    """
    s = s.lower()
    if s == "":
        return None
    if s == "true":
        return True
    if s == "false":
        return False
    raise ValueError(f'Cannot convert string value "{s}" to boolean')


def clean_card_name(name: str) -> str:
    """
    Clean card name by properly handling escaped quotes.
    Returns the cleaned card name with proper quote handling.
    """
    # Replace \" with " if present
    if f'{constants.FileConfig.CSV_ESCAPE_CHAR}"' in name:
        return name.replace(f'{constants.FileConfig.CSV_ESCAPE_CHAR}"', '"')
    return name


def fix_oas_founded(log_line: str) -> str:
    """
    Fix OAS Founded card name in log lines.
    OAS Founded is a play-once card (suffixed with *) but
    appears without the suffix in logs.
    Returns the log line with corrected OAS Founded card name.
    """
    return log_line.replace(
        constants.SpecialCards.OAS_FOUNDED_WRONG,
        f"{constants.SpecialCards.OAS_FOUNDED_WRONG}*",
    )
