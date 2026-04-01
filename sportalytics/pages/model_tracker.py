import dash
import dash_mantine_components as dmc
import plotly.graph_objects as go
from dash import dcc

from sportalytics.services.model_tracker import get_model_performance, get_monthly_roi

dash.register_page(__name__, path="/model-tracker", title="Model Tracker", name="Model Tracker")


def roi_chart() -> dcc.Graph:
    monthly = get_monthly_roi()
    months = [m["month"] for m in monthly]
    rois = [m["roi"] for m in monthly]
    fig = go.Figure(
        go.Bar(
            x=months,
            y=rois,
            marker_color=["green" if r > 0 else "red" for r in rois],
        )
    )
    fig.update_layout(
        title="Monthly ROI (%)",
        xaxis_title="Month",
        yaxis_title="ROI %",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return dcc.Graph(figure=fig)


def layout():
    perf = get_model_performance()
    overall = perf["overall"]
    by_sport = perf["by_sport"]
    by_tier = perf["by_tier"]
    return dmc.Container(
        fluid=True,
        children=[
            dmc.Title("Model Tracker", order=2, mb="md"),
            dmc.SimpleGrid(
                cols={"base": 1, "sm": 4},
                mb="lg",
                children=[
                    dmc.Card(
                        withBorder=True,
                        children=[
                            dmc.Text("Overall Record", size="sm", c="dimmed"),
                            dmc.Text(overall["record"], fw=700, size="xl"),
                        ],
                    ),
                    dmc.Card(
                        withBorder=True,
                        children=[
                            dmc.Text("Win Rate", size="sm", c="dimmed"),
                            dmc.Text(f"{overall['win_rate']:.1%}", fw=700, size="xl"),
                        ],
                    ),
                    dmc.Card(
                        withBorder=True,
                        children=[
                            dmc.Text("ROI", size="sm", c="dimmed"),
                            dmc.Text(f"{overall['roi']}%", fw=700, size="xl", c="green"),
                        ],
                    ),
                    dmc.Card(
                        withBorder=True,
                        children=[
                            dmc.Text("Total Picks", size="sm", c="dimmed"),
                            dmc.Text(str(overall["total_picks"]), fw=700, size="xl"),
                        ],
                    ),
                ],
            ),
            roi_chart(),
            dmc.Title("Performance by Sport", order=3, mt="lg", mb="md"),
            dmc.Table(
                data={
                    "head": ["Sport", "Record", "Win Rate", "ROI", "Picks"],
                    "body": [
                        [
                            s["sport"], s["record"],
                            f"{s['win_rate']:.1%}", f"{s['roi']}%", s["picks"],
                        ]
                        for s in by_sport
                    ],
                }
            ),
            dmc.Title("Performance by Confidence Tier", order=3, mt="lg", mb="md"),
            dmc.Table(
                data={
                    "head": ["Tier", "Record", "Win Rate", "ROI", "Picks"],
                    "body": [
                        [t["tier"], t["record"], f"{t['win_rate']:.1%}", f"{t['roi']}%", t["picks"]]
                        for t in by_tier
                    ],
                }
            ),
        ],
    )
