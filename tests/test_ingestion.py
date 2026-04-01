from sportalytics.ingestion.base import IngestionResult
from sportalytics.ingestion.cbb import CBBIngester
from sportalytics.ingestion.cfb import CFBIngester
from sportalytics.ingestion.mlb import MLBIngester
from sportalytics.ingestion.nba import NBAIngester
from sportalytics.ingestion.nfl import NFLIngester
from sportalytics.ingestion.nhl import NHLIngester
from sportalytics.ingestion.ufc import UFCIngester


def test_ingestion_result_defaults():
    r = IngestionResult(sport="NBA")
    assert r.records_fetched == 0
    assert r.records_inserted == 0
    assert r.errors == []
    assert r.completed_at is None


def test_nba_ingester_run():
    ingester = NBAIngester()
    result = ingester.run()
    assert isinstance(result, IngestionResult)
    assert result.sport == "NBA"
    assert result.completed_at is not None


def test_nba_ingester_fetch_schedule():
    ingester = NBAIngester()
    schedule = ingester.fetch_schedule("2023-24")
    assert isinstance(schedule, list)
    assert len(schedule) > 0


def test_nba_ingester_fetch_player_stats():
    ingester = NBAIngester()
    stats = ingester.fetch_player_stats("nba-20240101-lal-bos")
    assert isinstance(stats, list)


def test_nba_ingester_fetch_team_stats():
    ingester = NBAIngester()
    teams = ingester.fetch_team_stats("2023-24")
    assert isinstance(teams, list)


def test_all_ingesters_run():
    ingesters = [
        NBAIngester(), NFLIngester(), NHLIngester(), MLBIngester(),
        UFCIngester(), CFBIngester(), CBBIngester(),
    ]
    for ingester in ingesters:
        result = ingester.run()
        assert isinstance(result, IngestionResult)
        assert result.completed_at is not None
        assert len(result.errors) == 0, f"{ingester.sport} had errors: {result.errors}"


def test_ingestion_result_has_sport():
    for sport in ["NBA", "NFL", "NHL", "MLB", "UFC", "CFB", "CBB"]:
        r = IngestionResult(sport=sport)
        assert r.sport == sport
