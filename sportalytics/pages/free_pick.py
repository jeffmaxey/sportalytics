import dash
import dash_mantine_components as dmc

from sportalytics.services.free_pick import get_free_pick, get_free_pick_history

dash.register_page(__name__, path="/free-pick", title="Free Daily Pick", name="Free Pick")

RESULT_COLORS = {"W": "green", "L": "red"}


def layout():
    pick = get_free_pick()
    history = get_free_pick_history()
    recent_record = (
        f"{sum(1 for h in history if h['result'] == 'W')}-"
        f"{sum(1 for h in history if h['result'] == 'L')}"
    )
    return dmc.Container(
        fluid=True,
        children=[
            dmc.Title("Free Daily Pick", order=2, mb="md"),
            dmc.Alert(
                "Today's ML-graded pick — no signup required!",
                color="blue",
                mb="lg",
            ),
            dmc.Card(
                withBorder=True,
                radius="md",
                mb="xl",
                p="xl",
                children=[
                    dmc.Group(
                        justify="space-between",
                        mb="md",
                        children=[
                            dmc.Badge(pick["sport"], color="blue", size="lg"),
                            dmc.Badge(f"Grade: {pick['grade']}", color="green", size="lg"),
                        ],
                    ),
                    dmc.Title(pick["matchup"], order=3, mb="xs"),
                    dmc.Group(
                        mb="md",
                        children=[
                            dmc.Text("Pick:", fw=600),
                            dmc.Text(pick["pick"], size="xl", fw=700, c="blue"),
                            dmc.Text(f"({pick['pick_type']})", c="dimmed"),
                        ],
                    ),
                    dmc.Progress(
                        value=pick["ml_score"] * 100,
                        color="green",
                        size="lg",
                        mb="xs",
                    ),
                    dmc.Text(
                        f"ML Confidence Score: {pick['ml_score']:.0%}",
                        size="sm",
                        c="dimmed",
                        mb="md",
                    ),
                    dmc.Alert(pick["rationale"], color="blue", variant="light"),
                ],
            ),
            dmc.Title(f"Recent History ({recent_record})", order=3, mb="md"),
            dmc.Table(
                data={
                    "head": ["Date", "Matchup", "Pick", "Grade", "Result"],
                    "body": [
                        [
                            h["date"],
                            h["matchup"],
                            h["pick"],
                            h["grade"],
                            dmc.Badge(h["result"], color=RESULT_COLORS.get(h["result"], "gray")),
                        ]
                        for h in history
                    ],
                }
            ),
        ],
    )
