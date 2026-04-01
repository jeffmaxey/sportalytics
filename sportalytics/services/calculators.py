"""
Betting calculator utilities for Sportalytics.

Provides pure-function helpers for converting odds formats, computing
implied probabilities, identifying arbitrage opportunities, and
calculating expected value.  All functions are stateless and have no
external dependencies beyond the standard library.
"""

from fractions import Fraction


def american_to_implied(odds: float) -> float:
    """
    Convert American odds to implied probability.

    Parameters
    ----------
    odds : float
        American odds value.  Positive values represent underdogs;
        negative values represent favourites.

    Returns
    -------
    float
        Implied win probability in the range ``(0, 1)``.

    Examples
    --------
    >>> round(american_to_implied(100), 4)
    0.5
    >>> round(american_to_implied(-110), 4)
    0.5238
    """
    if odds > 0:
        return 100 / (odds + 100)
    return abs(odds) / (abs(odds) + 100)


def american_to_decimal(odds: float) -> float:
    """
    Convert American odds to decimal odds.

    Parameters
    ----------
    odds : float
        American odds value.

    Returns
    -------
    float
        Decimal odds (always ≥ 1.0).

    Examples
    --------
    >>> american_to_decimal(100)
    2.0
    >>> american_to_decimal(-200)
    1.5
    """
    if odds > 0:
        return (odds / 100) + 1
    return (100 / abs(odds)) + 1


def decimal_to_american(decimal: float) -> float:
    """
    Convert decimal odds to American odds.

    Parameters
    ----------
    decimal : float
        Decimal odds value (must be > 1.0).

    Returns
    -------
    float
        American odds.  Values ≥ 2.0 produce positive American odds;
        values < 2.0 produce negative (favourite) odds.

    Examples
    --------
    >>> decimal_to_american(2.0)
    100.0
    >>> decimal_to_american(1.5)
    -200.0
    """
    if decimal >= 2.0:
        return (decimal - 1) * 100
    return -100 / (decimal - 1)


def decimal_to_fractional(decimal: float) -> str:
    """
    Convert decimal odds to a fractional string representation.

    Parameters
    ----------
    decimal : float
        Decimal odds value (must be > 1.0).

    Returns
    -------
    str
        Fractional odds string, e.g. ``'5/2'`` or ``'1/1'``.

    Examples
    --------
    >>> decimal_to_fractional(2.0)
    '1/1'
    >>> decimal_to_fractional(3.5)
    '5/2'
    """
    frac = Fraction(decimal - 1).limit_denominator(100)
    return f"{frac.numerator}/{frac.denominator}"


def implied_to_american(prob: float) -> float:
    """
    Convert an implied probability to American odds.

    Parameters
    ----------
    prob : float
        Win probability in the range ``(0, 1)`` exclusive.

    Returns
    -------
    float
        American odds corresponding to the implied probability.

    Raises
    ------
    ValueError
        If *prob* is not strictly between 0 and 1.

    Examples
    --------
    >>> round(implied_to_american(0.5), 1)
    100.0
    """
    if prob <= 0 or prob >= 1:
        raise ValueError("Probability must be between 0 and 1 (exclusive).")
    if prob < 0.5:
        return (100 / prob) - 100
    return -(prob * 100) / (1 - prob)


def calculate_arbitrage(odds1_american: float, odds2_american: float) -> dict:
    """
    Calculate whether an arbitrage opportunity exists between two sides.

    Parameters
    ----------
    odds1_american : float
        American odds for side 1.
    odds2_american : float
        American odds for side 2.

    Returns
    -------
    dict
        A result dict with the following keys:

        * ``'arb_pct'`` *(float)* — percentage margin.  Positive means
          an arb exists; negative means over-round.
        * ``'has_arb'`` *(bool)* — ``True`` when total implied < 100 %.
        * ``'total_implied'`` *(float)* — sum of implied probabilities
          as a percentage.
        * ``'prob1'`` *(float)* — side 1 implied probability (%).
        * ``'prob2'`` *(float)* — side 2 implied probability (%).

    Examples
    --------
    >>> result = calculate_arbitrage(-110, -110)
    >>> result["has_arb"]
    False
    >>> result["total_implied"] > 100
    True
    """
    prob1 = american_to_implied(odds1_american)
    prob2 = american_to_implied(odds2_american)
    total = prob1 + prob2
    arb_pct = (1 - total) * 100
    return {
        "arb_pct": round(arb_pct, 4),
        "has_arb": total < 1.0,
        "total_implied": round(total * 100, 4),
        "prob1": round(prob1 * 100, 4),
        "prob2": round(prob2 * 100, 4),
    }


def calculate_arbitrage_stakes(
    odds1: float, odds2: float, total_stake: float
) -> dict:
    """
    Calculate the optimal stake split for an arbitrage bet.

    Parameters
    ----------
    odds1 : float
        American odds for side 1.
    odds2 : float
        American odds for side 2.
    total_stake : float
        Total stake amount in dollars.

    Returns
    -------
    dict
        A result dict with keys:

        * ``'stake1'`` *(float)* — optimal stake on side 1 (USD).
        * ``'stake2'`` *(float)* — optimal stake on side 2 (USD).
        * ``'profit'`` *(float)* — guaranteed profit (USD).

    Examples
    --------
    >>> res = calculate_arbitrage_stakes(200, -110, 100)
    >>> res["stake1"] + res["stake2"]
    100.0
    """
    prob1 = american_to_implied(odds1)
    prob2 = american_to_implied(odds2)
    total_prob = prob1 + prob2
    stake1 = total_stake * (prob1 / total_prob)
    stake2 = total_stake * (prob2 / total_prob)
    dec1 = american_to_decimal(odds1)
    dec2 = american_to_decimal(odds2)
    profit = min(stake1 * dec1, stake2 * dec2) - total_stake
    return {
        "stake1": round(stake1, 2),
        "stake2": round(stake2, 2),
        "profit": round(profit, 2),
    }


def calculate_ev(odds_american: float, win_prob: float, stake: float) -> dict:
    """
    Calculate the expected value of a bet.

    Parameters
    ----------
    odds_american : float
        American odds for the bet.
    win_prob : float
        Estimated win probability in the range ``[0, 1]``.
    stake : float
        Bet stake in USD.

    Returns
    -------
    dict
        A result dict with keys:

        * ``'ev'`` *(float)* — expected value in USD.
        * ``'payout'`` *(float)* — net profit if bet wins (USD).
        * ``'roi_pct'`` *(float)* — return on investment as a percentage.

    Examples
    --------
    >>> res = calculate_ev(-110, 0.6, 100)
    >>> res["ev"] > 0
    True
    """
    if odds_american > 0:
        payout = stake * odds_american / 100
    else:
        payout = stake * 100 / abs(odds_american)
    ev = (win_prob * payout) - ((1 - win_prob) * stake)
    roi = (ev / stake) * 100 if stake > 0 else 0
    return {
        "ev": round(ev, 4),
        "payout": round(payout, 4),
        "roi_pct": round(roi, 4),
    }


def convert_odds(value: float, from_format: str) -> dict:
    """
    Convert odds from any supported format to all other formats.

    Parameters
    ----------
    value : float
        Odds value in the source format.
    from_format : str
        Source format identifier.  Must be one of:
        ``'american'``, ``'decimal'``, ``'implied'``.

    Returns
    -------
    dict
        A result dict with keys:

        * ``'american'`` *(float)* — American odds.
        * ``'decimal'`` *(float)* — Decimal odds.
        * ``'fractional'`` *(str)* — Fractional odds string.
        * ``'implied'`` *(float)* — Implied probability (%).

    Raises
    ------
    ValueError
        If *from_format* is not one of the recognised format strings.

    Examples
    --------
    >>> res = convert_odds(-110, "american")
    >>> res["decimal"]
    1.9091
    """
    if from_format == "american":
        american = value
        decimal = american_to_decimal(value)
    elif from_format == "decimal":
        decimal = value
        american = decimal_to_american(value)
    elif from_format == "implied":
        prob = value / 100
        american = implied_to_american(prob)
        decimal = american_to_decimal(american)
    else:
        raise ValueError(f"Unknown format: {from_format!r}")
    implied = american_to_implied(american) * 100
    fractional = decimal_to_fractional(decimal)
    return {
        "american": round(american, 2),
        "decimal": round(decimal, 4),
        "fractional": fractional,
        "implied": round(implied, 4),
    }
