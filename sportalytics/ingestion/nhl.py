from sportalytics.ingestion.base import BaseIngester, IngestionResult


class NHLIngester(BaseIngester):
    sport = "NHL"

    def fetch_schedule(self, season: str) -> list[dict]:
        return [
            {
                "game_id": "nhl-20240110-bos-nyr",
                "home_team": "Bruins",
                "away_team": "Rangers",
                "scheduled_at": "2024-01-10T19:00:00",
                "season": season,
            }
        ]

    def fetch_player_stats(self, game_id: str) -> list[dict]:
        return [
            {
                "player_id": "p020", "player_name": "David Pastrnak",
                "goals": 1, "assists": 2, "shots": 5,
            },
            {
                "player_id": "p021", "player_name": "Artemi Panarin",
                "goals": 0, "assists": 1, "shots": 3,
            },
        ]

    def fetch_team_stats(self, season: str) -> list[dict]:
        return [
            {"team": "Bruins", "wins": 30, "losses": 12, "gpg": 3.2, "opp_gpg": 2.4},
            {"team": "Rangers", "wins": 28, "losses": 14, "gpg": 3.0, "opp_gpg": 2.6},
        ]

    def _run_impl(self, result: IngestionResult) -> None:
        schedule = self.fetch_schedule("2023-24")
        result.records_fetched = len(schedule)
        result.records_inserted = len(schedule)
