import dash
import dash_mantine_components as dmc

from sportalytics.services.marketplace import get_experts

dash.register_page(__name__, path="/marketplace", title="Marketplace", name="Marketplace")

RESULT_COLORS = {"W": "green", "L": "red", "P": "yellow"}


def expert_card(expert: dict) -> dmc.Card:
    verified_badge = (
        dmc.Badge("✓ Verified", color="blue", variant="light") if expert["verified"] else None
    )
    children_group = [dmc.Text(expert["display_name"], fw=700)]
    if verified_badge is not None:
        children_group.append(verified_badge)
    return dmc.Card(
        withBorder=True,
        radius="md",
        mb="sm",
        children=[
            dmc.Group(
                justify="space-between",
                children=[
                    dmc.Group(children=children_group),
                    dmc.Text(f"${expert['monthly_price']}/mo", fw=700, c="blue"),
                ],
            ),
            dmc.Text(expert["bio"], size="sm", c="dimmed", mt="xs"),
            dmc.Divider(my="sm"),
            dmc.Group(
                children=[
                    dmc.Stack(
                        gap=2,
                        children=[
                            dmc.Text("Win Rate", size="xs", c="dimmed"),
                            dmc.Text(f"{expert['win_rate']:.1%}", fw=600),
                        ],
                    ),
                    dmc.Stack(
                        gap=2,
                        children=[
                            dmc.Text("ROI", size="xs", c="dimmed"),
                            dmc.Text(f"{expert['roi']}%", fw=600, c="green"),
                        ],
                    ),
                    dmc.Stack(
                        gap=2,
                        children=[
                            dmc.Text("Total Picks", size="xs", c="dimmed"),
                            dmc.Text(str(expert["total_picks"]), fw=600),
                        ],
                    ),
                    dmc.Stack(
                        gap=2,
                        children=[
                            dmc.Text("Last 5", size="xs", c="dimmed"),
                            dmc.Group(
                                gap=4,
                                children=[
                                    dmc.Badge(r, color=RESULT_COLORS.get(r, "gray"), size="sm")
                                    for r in expert["last_5"]
                                ],
                            ),
                        ],
                    ),
                ]
            ),
            dmc.Group(
                mt="sm",
                children=[
                    dmc.Badge(s, variant="dot", size="sm") for s in expert["sports"]
                ],
            ),
        ],
    )


def layout():
    experts = get_experts()
    return dmc.Container(
        fluid=True,
        children=[
            dmc.Title("Expert Marketplace", order=2, mb="md"),
            dmc.Text(
                "Browse verified expert cappers with transparent track records.",
                c="dimmed",
                mb="lg",
            ),
            dmc.Grid(
                children=[
                    dmc.GridCol(expert_card(e), span={"base": 12, "md": 6, "lg": 4})
                    for e in experts
                ]
            ),
        ],
    )
