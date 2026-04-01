"""
Live Totals page for Sportalytics.

Real-time pace tracking and projected total overlays for in-progress
games across all supported sports.
"""

import dash
import dash_mantine_components as dmc

from sportalytics.components import live_game_card, page_header
from sportalytics.services.live_totals import get_live_games

dash.register_page(__name__, path="/live-totals", title="Live Totals", name="Live Totals")


def layout() -> dmc.Container:
    """
    Render the Live Totals page layout.

    Returns
    -------
    dmc.Container
        A fluid container with a page header and either a responsive
        :class:`dmc.Grid` of :func:`live_game_card` tiles or an
        informational alert when no live games are available.

    Notes
    -----
    Live games are fetched at render time via :func:`get_live_games`.
    Each card shows the current score, projected total, live line,
    and an Over/Under recommendation with pace progress bar.
    """
    games = get_live_games()
    return dmc.Container(
        fluid=True,
        children=[
            page_header(
                "Live Totals",
                subtitle="Real-time pace tracking and projected totals for in-progress games",
            ),
            (
                dmc.Grid(
                    children=[
                        dmc.GridCol(live_game_card(g), span={"base": 12, "md": 6, "lg": 4})
                        for g in games
                    ],
                    gutter="md",
                )
                if games
                else dmc.Alert("No live games at the moment. Check back soon!", color="blue")
            ),
        ],
    )
