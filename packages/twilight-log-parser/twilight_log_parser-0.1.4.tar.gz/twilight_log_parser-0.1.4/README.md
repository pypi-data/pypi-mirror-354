[![PyPI version](https://badge.fury.io/py/twilight-log-parser.svg)](https://badge.fury.io/py/twilight-log-parser)
[![Python Support](https://img.shields.io/pypi/pyversions/twilight-log-parser.svg)](https://pypi.org/project/twilight-log-parser/)

# twilight-log-parser

twilight-log-parser is a Python package that parses Twilight Struggle game logs into a structured format for analysis or other uses.

## Installation

Install twilight-log-parser using pip:

```
pip install twilight-log-parser
```

## Usage

An example of how to use the package to ingest a single log file can be found in [src/ingest_log.py](src/ingest_log.py).

To parse a single log file and output to CSVs (plays and board states) you can run the following command:

```
python -m twilight_log_parser.ingest_log test_logs/<pick-a-log-file>.txt [--output-dir <output-dir>]
```

## Current Features

- CSV output of plays and board states
- Tracked objects during each play include
    - Board state (influence)
    - Defcon changes
    - Space Race changes
    - Headline changes
    - VP Track
    - MilOps
    - Revealed Cards
    - Deck Status (cannot track known cards in hand)
    - Dice Rolls
    - Active Effects per Play
    - Influence Changes
    - Targets Country(s) - Coup, War, Realignment
- Determines winner and win type
- API for accessing the above


## Roadmap
- [ ] Add real unit tests
- [ ] SQLAlchemy DB integration tooling (for easier analysis)
- [ ] Log Validation
- [ ] Improved error handling


## Contributions

Maintaining twilight-log-parser is a community effort, and we'd love to have help! You can support the project by
reporting bugs, requesting features, writing documentation, helping to narrow down issues, and submitting code.

Especially if you have unique game situations, we'd like to work on validating them and adding them to a test suite!

## License

This project is licensed under the GNU General Public License v3 or later (GPLv3+) - see the [LICENSE](LICENSE) file for details.