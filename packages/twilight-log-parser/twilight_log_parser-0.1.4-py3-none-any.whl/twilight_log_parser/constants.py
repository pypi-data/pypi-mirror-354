from enum import Enum
from pathlib import Path


class Side(str, Enum):
    US = "US"
    USSR = "USSR"


class War(str, Enum):
    EARLY = "Early"
    MID = "Mid"
    LATE = "Late"


class PlayType(str, Enum):
    EVENT = "Event"
    PLACE_INFLUENCE = "Place Influence"
    SPACE_RACE = "Space Race"
    DISCARD = "Discard"
    RETURN_TO_HAND = "Return to Hand"
    AWAITING_GRAIN_SALES_ACTION = "Awaiting Grain Sales Action"
    FINAL_SCORING = "Final Scoring"
    CLEANUP = "Cleanup"
    INITIAL_SETUP = "Initial Setup"
    COUP = "Coup"
    REALIGNMENT = "Realignment"
    RESHUFFLE = "Reshuffle"
    REVEALS = "Reveals"


class CardStatus(str, Enum):
    IN_PLAY = "now"
    OUT_OF_PLAY = "no longer"


class FileConfig:
    CSV_DELIMITER = "|"
    CSV_ESCAPE_CHAR = "\\"
    DATA_DIR = Path(__file__).parent / "data"
    CARDS_FILE = DATA_DIR / "cards.csv"
    COUNTRIES_FILE = DATA_DIR / "countries.csv"


class SpecialCards:
    SALT_NEGOTIATIONS = "SALT Negotiations*"
    LATIN_AMERICAN_DEATH_SQUADS = "Latin American Death Squads"
    RED_SCARE_PURGE = "Red Scare/Purge"
    CUBAN_MISSILE_CRISIS = "Cuban Missile Crisis*"
    OAS_FOUNDED_WRONG = "OAS Founded"
    BOTH_EFFECT_NEUTRAL = [SALT_NEGOTIATIONS, LATIN_AMERICAN_DEATH_SQUADS]
    OPPONENT_EFFECT_NEUTRAL = [RED_SCARE_PURGE, CUBAN_MISSILE_CRISIS]
    THE_CHINA_CARD = "The China Card"
    GRAIN_SALES_TO_SOVIETS = "Grain Sales To Soviets"
    DEFECTORS = "Defectors"
    MISSILE_ENVY = "Missile Envy"
    UN_INTERVENTION = "UN Intervention"
    STAR_WARS = "Star Wars*"
    WARGAMES = "Wargames*"
    OUR_MAN_IN_TEHRAN = "Our Man in Tehran*"
    NATO = "NATO*"
    KITCHEN_DEBATES = "Kitchen Debates*"
    STICKY_IF_CARDS = [STAR_WARS, WARGAMES, OUR_MAN_IN_TEHRAN, NATO, KITCHEN_DEBATES]


CHUNK_END_LINES = ("HeadlineLine", "ARLine", "FinalScoringLine", "CleanupLine")
