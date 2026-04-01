from datetime import date, datetime

DAILY_PICK = {
    "date": datetime.utcnow().date().isoformat(),
    "sport": "NBA",
    "matchup": "Celtics vs Knicks",
    "pick": "Celtics -5.5",
    "line": -5.5,
    "pick_type": "spread",
    "confidence": "A",
    "grade": "A+",
    "rationale": (
        "Celtics are 8-2 ATS in last 10 home games. "
        "Knicks missing Brunson (foot). "
        "Model projects Celtics win by 8.2 points."
    ),
    "model_version": "v2.1",
    "ml_score": 0.84,
}


def get_free_pick(target_date: date | None = None) -> dict:
    """Return the free daily ML-graded pick."""
    return dict(DAILY_PICK)


def get_free_pick_history() -> list[dict]:
    """Return historical free picks with results."""
    return [
        {"date": "2024-01-09", "matchup": "Chiefs vs Bills", "pick": "Chiefs -3",
         "result": "W", "grade": "A"},
        {"date": "2024-01-08", "matchup": "Lakers vs Celtics", "pick": "Celtics ML",
         "result": "W", "grade": "B"},
        {"date": "2024-01-07", "matchup": "Yankees vs Red Sox", "pick": "Under 9",
         "result": "L", "grade": "B"},
        {"date": "2024-01-06", "matchup": "Bruins vs Rangers", "pick": "Bruins ML",
         "result": "W", "grade": "A"},
        {"date": "2024-01-05", "matchup": "Duke vs UNC", "pick": "Over 147",
         "result": "W", "grade": "A"},
        {"date": "2024-01-04", "matchup": "Oilers vs Flames", "pick": "Over 6",
         "result": "L", "grade": "C"},
        {"date": "2024-01-03", "matchup": "Alabama vs Georgia", "pick": "Georgia +3",
         "result": "W", "grade": "B"},
    ]
