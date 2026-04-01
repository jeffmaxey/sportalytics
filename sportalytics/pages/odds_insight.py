"""
Odds Insight page for Sportalytics.

Compares lines across multiple sportsbooks in real time, highlighting
the best available odds for each side of a game.
"""

import dash
import dash_mantine_components as dmc

from sportalytics.components import odds_table_card, page_header
from sportalytics.services.odds_insight import SPORTSBOOKS, get_odds_comparison

dash.register_page(__name__, path="/odds-insight", title="Odds Insight", name="Odds Insight")


def layout() -> dmc.Container:
    """
    Render the Odds Insight page layout.

    Returns
    -------
    dmc.Container
        A fluid container with a page header and a vertical list of
        :func:`odds_table_card` components — one per game.

    Notes
    -----
    Best-value cells in each table are highlighted in teal via
    :func:`~sportalytics.components.odds_table_card`.  The number of
    sportsbooks compared is reported in the page subtitle.
    """
    games = get_odds_comparison()
    return dmc.Container(
        fluid=True,
        children=[
            page_header(
                "Odds Insight",
                subtitle=f"Comparing lines across {len(SPORTSBOOKS)} sportsbooks in real time",
            ),
            *[odds_table_card(g) for g in games],
        ],
    )
