from sportalytics.ingestion.base import BaseIngester, IngestionResult


class CFBIngester(BaseIngester):
    sport = "CFB"

    def fetch_schedule(self, season: str) -> list[dict]:
        return [
            {
                "game_id": "cfb-20240108-ala-uga",
                "home_team": "Alabama",
                "away_team": "Georgia",
                "scheduled_at": "2024-01-08T20:00:00",
                "season": season,
            }
        ]

    def fetch_player_stats(self, game_id: str) -> list[dict]:
        return [
            {
                "player_id": "p050",
                "player_name": "Jalen Milroe",
                "passing_yards": 242,
                "rushing_yards": 88,
                "touchdowns": 3,
            },
            {
                "player_id": "p051",
                "player_name": "Carson Beck",
                "passing_yards": 284,
                "rushing_yards": 12,
                "touchdowns": 2,
            },
        ]

    def fetch_team_stats(self, season: str) -> list[dict]:
        return [
            {"team": "Alabama", "wins": 12, "losses": 2, "ppg": 38.5, "opp_ppg": 18.2},
            {"team": "Georgia", "wins": 13, "losses": 1, "ppg": 41.2, "opp_ppg": 16.8},
        ]

    def _run_impl(self, result: IngestionResult) -> None:
        schedule = self.fetch_schedule("2023")
        result.records_fetched = len(schedule)
        result.records_inserted = len(schedule)
