"""
Model Tracker page for Sportalytics.

Shows overall win/loss record, ROI by sport and confidence tier, and a
monthly ROI bar chart powered by the model-performance service.
"""

import dash
import dash_mantine_components as dmc
import plotly.graph_objects as go
from dash import dcc

from sportalytics.components import page_header, section_title, stat_grid, styled_table
from sportalytics.services.model_tracker import get_model_performance, get_monthly_roi
from sportalytics.theme import PLOTLY_LAYOUT_DEFAULTS

dash.register_page(__name__, path="/model-tracker", title="Model Tracker", name="Model Tracker")


def roi_chart() -> dcc.Graph:
    """
    Build the monthly ROI bar chart.

    Returns
    -------
    dcc.Graph
        A :class:`dcc.Graph` containing a Plotly bar chart of monthly
        ROI percentages.  Positive bars are rendered in green; negative
        bars in red.  Layout tokens are imported from
        :data:`~sportalytics.theme.PLOTLY_LAYOUT_DEFAULTS` for visual
        consistency with the Mantine theme.
    """
    monthly = get_monthly_roi()
    months = [m["month"] for m in monthly]
    rois = [m["roi"] for m in monthly]

    fig = go.Figure(
        go.Bar(
            x=months,
            y=rois,
            marker_color=["#40c057" if r > 0 else "#fa5252" for r in rois],
        )
    )
    fig.update_layout(
        title="Monthly ROI (%)",
        xaxis_title="Month",
        yaxis_title="ROI %",
        **PLOTLY_LAYOUT_DEFAULTS,
    )
    return dcc.Graph(figure=fig)


def layout() -> dmc.Container:
    """
    Render the Model Tracker page layout.

    Returns
    -------
    dmc.Container
        A fluid container with summary KPI tiles, a monthly ROI chart,
        and performance breakdown tables by sport and confidence tier.

    Notes
    -----
    All data is fetched from :func:`get_model_performance` and
    :func:`get_monthly_roi` at render time.
    """
    perf = get_model_performance()
    overall = perf["overall"]
    by_sport = perf["by_sport"]
    by_tier = perf["by_tier"]

    return dmc.Container(
        fluid=True,
        children=[
            page_header(
                "Model Tracker",
                subtitle="Historical pick accuracy, ROI, and confidence-tier breakdown",
            ),
            stat_grid([
                {"label": "Overall Record", "value": overall["record"]},
                {"label": "Win Rate",       "value": f"{overall['win_rate']:.1%}", "color": "blue"},
                {"label": "ROI",            "value": f"{overall['roi']}%",         "color": "teal"},
                {"label": "Total Picks",    "value": str(overall["total_picks"])},
            ]),
            roi_chart(),
            section_title("Performance by Sport"),
            styled_table(
                head=["Sport", "Record", "Win Rate", "ROI", "Picks"],
                body=[
                    [
                        s["sport"],
                        s["record"],
                        f"{s['win_rate']:.1%}",
                        f"{s['roi']}%",
                        s["picks"],
                    ]
                    for s in by_sport
                ],
            ),
            section_title("Performance by Confidence Tier"),
            styled_table(
                head=["Tier", "Record", "Win Rate", "ROI", "Picks"],
                body=[
                    [t["tier"], t["record"], f"{t['win_rate']:.1%}", f"{t['roi']}%", t["picks"]]
                    for t in by_tier
                ],
            ),
        ],
    )
