from sportalytics.ingestion.base import BaseIngester, IngestionResult


class NFLIngester(BaseIngester):
    sport = "NFL"

    def fetch_schedule(self, season: str) -> list[dict]:
        return [
            {
                "game_id": "nfl-20240107-kc-buf",
                "home_team": "Chiefs",
                "away_team": "Bills",
                "scheduled_at": "2024-01-07T18:30:00",
                "season": season,
            }
        ]

    def fetch_player_stats(self, game_id: str) -> list[dict]:
        return [
            {
                "player_id": "p010",
                "player_name": "Patrick Mahomes",
                "passing_yards": 305,
                "touchdowns": 3,
                "interceptions": 0,
            },
            {
                "player_id": "p011",
                "player_name": "Josh Allen",
                "passing_yards": 287,
                "touchdowns": 2,
                "interceptions": 1,
            },
        ]

    def fetch_team_stats(self, season: str) -> list[dict]:
        return [
            {"team": "Chiefs", "wins": 11, "losses": 6, "ppg": 25.3, "opp_ppg": 19.8},
            {"team": "Bills", "wins": 11, "losses": 6, "ppg": 27.1, "opp_ppg": 22.4},
        ]

    def _run_impl(self, result: IngestionResult) -> None:
        schedule = self.fetch_schedule("2023")
        result.records_fetched = len(schedule)
        result.records_inserted = len(schedule)
