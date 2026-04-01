from sportalytics.services.calculators import (
    american_to_decimal,
    american_to_implied,
    calculate_arbitrage,
    calculate_ev,
    decimal_to_american,
    decimal_to_fractional,
)


def test_american_to_implied_positive():
    assert abs(american_to_implied(100) - 0.5) < 0.001


def test_american_to_implied_negative():
    assert abs(american_to_implied(-110) - 0.5238) < 0.001


def test_calculate_arbitrage_no_arb():
    result = calculate_arbitrage(-110, -110)
    assert result["has_arb"] is False


def test_calculate_arbitrage_with_arb():
    result = calculate_arbitrage(200, -110)
    assert "total_implied" in result
    assert "has_arb" in result


def test_calculate_ev_positive():
    result = calculate_ev(-110, 0.6, 100)
    assert result["ev"] > 0


def test_calculate_ev_negative():
    result = calculate_ev(-110, 0.4, 100)
    assert result["ev"] < 0


def test_american_to_decimal_positive():
    assert abs(american_to_decimal(100) - 2.0) < 0.001


def test_american_to_decimal_negative():
    assert abs(american_to_decimal(-200) - 1.5) < 0.001


def test_decimal_to_american_favorite():
    assert abs(decimal_to_american(2.0) - 100) < 0.001


def test_decimal_to_american_underdog():
    assert abs(decimal_to_american(1.5) - (-200)) < 0.001


def test_decimal_to_fractional():
    result = decimal_to_fractional(2.0)
    assert result == "1/1"


def test_arb_pct_calculation():
    result = calculate_arbitrage(-110, -110)
    assert result["total_implied"] > 100


def test_calculate_ev_returns_payout():
    result = calculate_ev(100, 0.5, 100)
    assert abs(result["payout"] - 100.0) < 0.001
