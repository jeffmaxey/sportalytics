from sportalytics.services.calculators import american_to_implied
from sportalytics.services.free_pick import get_free_pick, get_free_pick_history
from sportalytics.services.live_totals import get_live_games
from sportalytics.services.marketplace import get_expert_picks, get_experts
from sportalytics.services.model_tracker import get_model_performance, get_monthly_roi
from sportalytics.services.odds_insight import SPORTSBOOKS, get_odds_comparison
from sportalytics.services.player_props import get_player_history, get_player_props
from sportalytics.services.predictions import SPORTS, get_daily_picks


def test_get_daily_picks_returns_list():
    picks = get_daily_picks()
    assert isinstance(picks, list)
    assert len(picks) > 0


def test_get_daily_picks_filtered_by_sport():
    picks = get_daily_picks(sport="NBA")
    for pick in picks:
        assert pick["sport"] == "NBA"


def test_get_daily_picks_unknown_sport():
    picks = get_daily_picks(sport="XYZ")
    assert picks == []


def test_sports_list_completeness():
    required = {"NBA", "NFL", "NHL", "MLB", "UFC", "CFB", "CBB"}
    assert required.issubset(set(SPORTS))


def test_get_player_props_returns_list():
    props = get_player_props()
    assert isinstance(props, list)
    assert len(props) > 0


def test_get_player_props_filtered_by_sport():
    props = get_player_props(sport="NBA")
    for prop in props:
        assert prop["sport"] == "NBA"


def test_get_player_history_returns_list():
    history = get_player_history("p001")
    assert isinstance(history, list)


def test_get_model_performance():
    perf = get_model_performance()
    assert "overall" in perf
    assert "by_sport" in perf
    assert "by_tier" in perf
    assert "monthly" in perf


def test_get_monthly_roi():
    roi = get_monthly_roi()
    assert isinstance(roi, list)
    assert len(roi) > 0


def test_sportsbooks_count():
    assert len(SPORTSBOOKS) >= 7


def test_get_odds_comparison():
    odds = get_odds_comparison()
    assert isinstance(odds, list)


def test_get_experts_returns_list():
    experts = get_experts()
    assert isinstance(experts, list)
    assert len(experts) > 0


def test_get_experts_verified_filter():
    experts = get_experts(verified_only=True)
    for e in experts:
        assert e["verified"] is True


def test_get_expert_picks():
    picks = get_expert_picks("e001")
    assert isinstance(picks, list)


def test_get_free_pick():
    pick = get_free_pick()
    assert "pick" in pick
    assert "ml_score" in pick
    assert "sport" in pick


def test_get_free_pick_history():
    history = get_free_pick_history()
    assert isinstance(history, list)
    assert len(history) > 0


def test_get_live_games():
    games = get_live_games()
    assert isinstance(games, list)


def test_get_live_games_filtered():
    games = get_live_games(sport="NBA")
    for g in games:
        assert g["sport"] == "NBA"
