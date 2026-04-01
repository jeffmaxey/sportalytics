import dash
import dash_mantine_components as dmc

from sportalytics.services.predictions import SPORTS, get_daily_picks

dash.register_page(__name__, path="/predictions", title="AI Predictions", name="AI Predictions")

TIER_COLORS = {"A": "green", "B": "yellow", "C": "orange"}


def pick_card(pick: dict) -> dmc.Card:
    tier = pick["confidence"]
    color = TIER_COLORS.get(tier, "blue")
    return dmc.Card(
        withBorder=True,
        radius="md",
        mb="sm",
        children=[
            dmc.Group(
                justify="space-between",
                children=[
                    dmc.Group(
                        children=[
                            dmc.Badge(pick["sport"], color="blue", variant="light"),
                            dmc.Badge(f"Tier {tier}", color=color, variant="filled"),
                        ]
                    ),
                    dmc.Text(pick["model_version"], size="xs", c="dimmed"),
                ],
            ),
            dmc.Text(pick["matchup"], fw=600, mt="sm"),
            dmc.Text(f"Pick: {pick['selection']} ({pick['pick_type']})", size="sm"),
            dmc.Text(f"Line: {pick['line']}", size="sm", c="dimmed"),
            dmc.Divider(my="sm"),
            dmc.Text(pick["rationale"], size="sm", c="dimmed"),
        ],
    )


def layout():
    picks = get_daily_picks()
    return dmc.Container(
        fluid=True,
        children=[
            dmc.Title("AI/ML Predictions", order=2, mb="md"),
            dmc.Group(
                mb="md",
                children=[
                    dmc.Select(
                        id="predictions-sport-filter",
                        label="Sport",
                        placeholder="All Sports",
                        data=[{"value": s, "label": s} for s in SPORTS],
                        clearable=True,
                        w=200,
                    ),
                    dmc.Select(
                        id="predictions-tier-filter",
                        label="Confidence Tier",
                        placeholder="All Tiers",
                        data=[
                            {"value": "A", "label": "Tier A (Best)"},
                            {"value": "B", "label": "Tier B"},
                            {"value": "C", "label": "Tier C"},
                        ],
                        clearable=True,
                        w=200,
                    ),
                ],
            ),
            dmc.Grid(
                children=[
                    dmc.GridCol(pick_card(p), span={"base": 12, "md": 6, "lg": 4})
                    for p in picks
                ],
            ),
        ],
    )
