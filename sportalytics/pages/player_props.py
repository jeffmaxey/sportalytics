"""
Player Props page for Sportalytics.

Displays AI-graded player prop recommendations in a filterable
responsive grid, with hit-rate statistics and model edge data.
"""

import dash
import dash_mantine_components as dmc

from sportalytics.components import page_header, prop_card
from sportalytics.services.player_props import get_player_props
from sportalytics.services.predictions import SPORTS

dash.register_page(__name__, path="/player-props", title="Player Props", name="Player Props")


def layout() -> dmc.Container:
    """
    Render the Player Props page layout.

    Returns
    -------
    dmc.Container
        A fluid container with a page header, sport filter, and a
        responsive :class:`dmc.Grid` of :func:`prop_card` tiles.

    Notes
    -----
    Props are fetched at render time via :func:`get_player_props`.
    The sport filter select is reserved for a future server-side
    callback.
    """
    props = get_player_props()
    return dmc.Container(
        fluid=True,
        children=[
            page_header(
                "Player Props",
                subtitle="Model-graded player prop recommendations with historical hit rates",
                right_content=dmc.Select(
                    id="props-sport-filter",
                    label="Sport",
                    placeholder="All Sports",
                    data=[{"value": s, "label": s} for s in SPORTS],
                    clearable=True,
                    w=160,
                ),
            ),
            dmc.Grid(
                children=[
                    dmc.GridCol(prop_card(p), span={"base": 12, "md": 6, "lg": 4})
                    for p in props
                ],
                gutter="md",
            ),
        ],
    )
