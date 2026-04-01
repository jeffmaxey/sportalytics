from fractions import Fraction


def american_to_implied(odds: float) -> float:
    """Convert American odds to implied probability."""
    if odds > 0:
        return 100 / (odds + 100)
    else:
        return abs(odds) / (abs(odds) + 100)


def american_to_decimal(odds: float) -> float:
    """Convert American odds to decimal odds."""
    if odds > 0:
        return (odds / 100) + 1
    else:
        return (100 / abs(odds)) + 1


def decimal_to_american(decimal: float) -> float:
    """Convert decimal odds to American odds."""
    if decimal >= 2.0:
        return (decimal - 1) * 100
    else:
        return -100 / (decimal - 1)


def decimal_to_fractional(decimal: float) -> str:
    """Convert decimal odds to fractional string like '5/2'."""
    frac = Fraction(decimal - 1).limit_denominator(100)
    return f"{frac.numerator}/{frac.denominator}"


def implied_to_american(prob: float) -> float:
    """Convert implied probability to American odds."""
    if prob <= 0 or prob >= 1:
        raise ValueError("Probability must be between 0 and 1")
    if prob < 0.5:
        return (100 / prob) - 100
    else:
        return -(prob * 100) / (1 - prob)


def calculate_arbitrage(odds1_american: float, odds2_american: float) -> dict:
    """Calculate arbitrage opportunity between two sides."""
    prob1 = american_to_implied(odds1_american)
    prob2 = american_to_implied(odds2_american)
    total = prob1 + prob2
    arb_pct = (1 - total) * 100
    has_arb = total < 1.0
    return {
        "arb_pct": round(arb_pct, 4),
        "has_arb": has_arb,
        "total_implied": round(total * 100, 4),
        "prob1": round(prob1 * 100, 4),
        "prob2": round(prob2 * 100, 4),
    }


def calculate_arbitrage_stakes(odds1: float, odds2: float, total_stake: float) -> dict:
    """Calculate optimal stake split for arbitrage."""
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
    """Calculate expected value of a bet."""
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
    """Convert odds from any format to all formats."""
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
        raise ValueError(f"Unknown format: {from_format}")
    implied = american_to_implied(american) * 100
    fractional = decimal_to_fractional(decimal)
    return {
        "american": round(american, 2),
        "decimal": round(decimal, 4),
        "fractional": fractional,
        "implied": round(implied, 4),
    }
