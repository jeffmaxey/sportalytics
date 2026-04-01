"""
AI/ML Predictions page for Sportalytics.

Displays daily model-generated picks in a filterable, responsive grid.
Picks are colour-coded by confidence tier and sport.
"""

import dash
import dash_mantine_components as dmc

from sportalytics.components import page_header, pick_card
from sportalytics.services.predictions import SPORTS, get_daily_picks

dash.register_page(__name__, path="/predictions", title="AI Predictions", name="AI Predictions")


def layout() -> dmc.Container:
    """
    Render the AI Predictions page layout.

    Returns
    -------
    dmc.Container
        A fluid container with a page header, sport/tier filter controls,
        and a responsive :class:`dmc.Grid` of :func:`pick_card` tiles.

    Notes
    -----
    Picks are fetched at render time via :func:`get_daily_picks`.
    Server-side callback filtering is not yet implemented; the filter
    selects are reserved for a future callback.
    """
    picks = get_daily_picks()
    return dmc.Container(
        fluid=True,
        children=[
            page_header(
                "AI/ML Predictions",
                subtitle="Today's model-generated picks, graded by confidence tier",
                right_content=dmc.Group(
                    gap="sm",
                    children=[
                        dmc.Select(
                            id="predictions-sport-filter",
                            label="Sport",
                            placeholder="All Sports",
                            data=[{"value": s, "label": s} for s in SPORTS],
                            clearable=True,
                            w=160,
                        ),
                        dmc.Select(
                            id="predictions-tier-filter",
                            label="Confidence Tier",
                            placeholder="All Tiers",
                            data=[
                                {"value": "A", "label": "Tier A — Best"},
                                {"value": "B", "label": "Tier B"},
                                {"value": "C", "label": "Tier C"},
                            ],
                            clearable=True,
                            w=180,
                        ),
                    ],
                ),
            ),
            dmc.Grid(
                children=[
                    dmc.GridCol(pick_card(p), span={"base": 12, "md": 6, "lg": 4})
                    for p in picks
                ],
                gutter="md",
            ),
        ],
    )
