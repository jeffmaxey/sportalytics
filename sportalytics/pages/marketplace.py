"""
Expert Marketplace page for Sportalytics.

Browse verified expert cappers with transparent, auditable track records
and subscription pricing.
"""

import dash
import dash_mantine_components as dmc

from sportalytics.components import expert_card, page_header
from sportalytics.services.marketplace import get_experts

dash.register_page(__name__, path="/marketplace", title="Marketplace", name="Marketplace")


def layout() -> dmc.Container:
    """
    Render the Expert Marketplace page layout.

    Returns
    -------
    dmc.Container
        A fluid container with a page header and a responsive
        :class:`dmc.Grid` of :func:`expert_card` tiles.

    Notes
    -----
    Experts are fetched at render time via :func:`get_experts`.  Each
    card shows win rate, ROI, last-5 results, and subscription price.
    """
    experts = get_experts()
    return dmc.Container(
        fluid=True,
        children=[
            page_header(
                "Expert Marketplace",
                subtitle="Browse verified cappers with transparent, auditable track records",
            ),
            dmc.Grid(
                children=[
                    dmc.GridCol(expert_card(e), span={"base": 12, "md": 6, "lg": 4})
                    for e in experts
                ],
                gutter="md",
            ),
        ],
    )
