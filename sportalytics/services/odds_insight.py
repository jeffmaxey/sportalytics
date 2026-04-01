SPORTSBOOKS = [
    "DraftKings", "FanDuel", "BetMGM", "Caesars",
    "PointsBet", "BetRivers", "WynnBet",
]

SAMPLE_ODDS = [
    {
        "game_id": "nba-001",
        "sport": "NBA",
        "matchup": "Lakers vs Celtics",
        "market": "moneyline",
        "lines": {
            "DraftKings": {"home": 145, "away": -165},
            "FanDuel": {"home": 150, "away": -172},
            "BetMGM": {"home": 140, "away": -160},
            "Caesars": {"home": 145, "away": -168},
            "PointsBet": {"home": 155, "away": -175},
            "BetRivers": {"home": 142, "away": -162},
            "WynnBet": {"home": 148, "away": -170},
        },
        "best_home": "PointsBet",
        "best_away": "BetMGM",
        "consensus_home": 146,
        "consensus_away": -167,
    },
    {
        "game_id": "nfl-001",
        "sport": "NFL",
        "matchup": "Chiefs vs Bills",
        "market": "spread",
        "lines": {
            "DraftKings": {"home": -3.0, "away": 3.0},
            "FanDuel": {"home": -3.5, "away": 3.5},
            "BetMGM": {"home": -3.0, "away": 3.0},
            "Caesars": {"home": -3.5, "away": 3.5},
            "PointsBet": {"home": -3.0, "away": 3.0},
            "BetRivers": {"home": -3.5, "away": 3.5},
            "WynnBet": {"home": -3.0, "away": 3.0},
        },
        "best_home": "FanDuel",
        "best_away": "DraftKings",
        "consensus_home": -3.2,
        "consensus_away": 3.2,
    },
]


def get_odds_comparison(sport: str | None = None) -> list[dict]:
    odds = list(SAMPLE_ODDS)
    if sport:
        odds = [o for o in odds if o["sport"] == sport]
    return odds


def get_line_movement(game_id: str) -> list[dict]:
    return [
        {"timestamp": "2024-01-10T08:00:00", "sportsbook": "DraftKings", "home": 140, "away": -160},
        {"timestamp": "2024-01-10T10:00:00", "sportsbook": "DraftKings", "home": 143, "away": -163},
        {"timestamp": "2024-01-10T12:00:00", "sportsbook": "DraftKings", "home": 145, "away": -165},
        {"timestamp": "2024-01-10T14:00:00", "sportsbook": "DraftKings", "home": 142, "away": -162},
        {"timestamp": "2024-01-10T16:00:00", "sportsbook": "DraftKings", "home": 145, "away": -165},
    ]
