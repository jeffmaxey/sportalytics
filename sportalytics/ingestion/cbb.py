from sportalytics.ingestion.base import BaseIngester, IngestionResult


class CBBIngester(BaseIngester):
    sport = "CBB"

    def fetch_schedule(self, season: str) -> list[dict]:
        return [
            {
                "game_id": "cbb-20240206-duk-unc",
                "home_team": "Duke",
                "away_team": "UNC",
                "scheduled_at": "2024-02-06T21:00:00",
                "season": season,
            }
        ]

    def fetch_player_stats(self, game_id: str) -> list[dict]:
        return [
            {
                "player_id": "p060", "player_name": "Kyle Filipowski",
                "points": 22, "rebounds": 8, "assists": 3,
            },
            {
                "player_id": "p061", "player_name": "Armando Bacot",
                "points": 18, "rebounds": 11, "assists": 2,
            },
        ]

    def fetch_team_stats(self, season: str) -> list[dict]:
        return [
            {"team": "Duke", "wins": 22, "losses": 5, "ppg": 82.4, "opp_ppg": 68.1},
            {"team": "UNC", "wins": 19, "losses": 8, "ppg": 79.8, "opp_ppg": 71.3},
        ]

    def _run_impl(self, result: IngestionResult) -> None:
        schedule = self.fetch_schedule("2023-24")
        result.records_fetched = len(schedule)
        result.records_inserted = len(schedule)
