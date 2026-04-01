import dash
import dash_mantine_components as dmc

from sportalytics.services.player_props import get_player_props
from sportalytics.services.predictions import SPORTS

dash.register_page(__name__, path="/player-props", title="Player Props", name="Player Props")

GRADE_COLORS = {"A": "green", "B": "yellow", "C": "orange", "D": "red"}


def prop_card(prop: dict) -> dmc.Card:
    grade = prop["grade"]
    color = GRADE_COLORS.get(grade, "blue")
    return dmc.Card(
        withBorder=True,
        radius="md",
        mb="sm",
        children=[
            dmc.Group(
                justify="space-between",
                children=[
                    dmc.Text(prop["player_name"], fw=700),
                    dmc.Badge(f"Grade: {grade}", color=color, variant="filled"),
                ],
            ),
            dmc.Text(f"{prop['team']} — {prop['game']}", size="sm", c="dimmed"),
            dmc.Divider(my="sm"),
            dmc.Group(
                children=[
                    dmc.Stack(
                        gap=2,
                        children=[
                            dmc.Text("Prop", size="xs", c="dimmed"),
                            dmc.Text(prop["prop_type"].replace("_", " ").title(), fw=500),
                        ],
                    ),
                    dmc.Stack(
                        gap=2,
                        children=[
                            dmc.Text("Line", size="xs", c="dimmed"),
                            dmc.Text(str(prop["line"]), fw=500),
                        ],
                    ),
                    dmc.Stack(
                        gap=2,
                        children=[
                            dmc.Text("Pick", size="xs", c="dimmed"),
                            dmc.Text(prop["recommendation"], fw=600, c="blue"),
                        ],
                    ),
                    dmc.Stack(
                        gap=2,
                        children=[
                            dmc.Text("Hit Rate (L10)", size="xs", c="dimmed"),
                            dmc.Text(f"{prop['hit_rate_last_10']:.0%}", fw=500),
                        ],
                    ),
                ]
            ),
        ],
    )


def layout():
    props = get_player_props()
    return dmc.Container(
        fluid=True,
        children=[
            dmc.Title("Player Props", order=2, mb="md"),
            dmc.Select(
                id="props-sport-filter",
                label="Sport",
                placeholder="All Sports",
                data=[{"value": s, "label": s} for s in SPORTS],
                clearable=True,
                w=200,
                mb="md",
            ),
            dmc.Grid(
                children=[
                    dmc.GridCol(prop_card(p), span={"base": 12, "md": 6, "lg": 4})
                    for p in props
                ]
            ),
        ],
    )
