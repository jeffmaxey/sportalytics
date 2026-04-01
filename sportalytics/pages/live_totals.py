import dash
import dash_mantine_components as dmc

from sportalytics.services.live_totals import get_live_games

dash.register_page(__name__, path="/live-totals", title="Live Totals", name="Live Totals")

REC_COLORS = {"Over": "green", "Under": "red"}


def live_game_card(game: dict) -> dmc.Card:
    color = REC_COLORS.get(game["recommendation"], "blue")
    pace_pct = (
        min((game["current_total"] / game["opening_total"]) * 100, 100)
        if game["opening_total"]
        else 50
    )
    return dmc.Card(
        withBorder=True,
        radius="md",
        mb="sm",
        children=[
            dmc.Group(
                justify="space-between",
                mb="xs",
                children=[
                    dmc.Group(
                        children=[
                            dmc.Badge(game["sport"], color="blue", variant="light"),
                            dmc.Badge("LIVE", color="red", variant="filled"),
                        ]
                    ),
                    dmc.Text(f"{game['period']} | {game['time_remaining']}", size="sm", c="dimmed"),
                ],
            ),
            dmc.Text(game["matchup"], fw=700, mb="xs"),
            dmc.Group(
                mb="sm",
                children=[
                    dmc.Text(f"Score: {game['home_score']}-{game['away_score']}", fw=600),
                    dmc.Text(f"Current: {game['current_total']} pts", size="sm"),
                    dmc.Text(f"Projected: {game['projected_total']}", size="sm"),
                ],
            ),
            dmc.Group(
                mb="xs",
                children=[
                    dmc.Text("Total Line:", size="sm"),
                    dmc.Text(str(game["current_line"]), fw=600),
                    dmc.Badge(game["recommendation"], color=color, variant="filled"),
                ],
            ),
            dmc.Progress(
                value=pace_pct,
                color="blue",
                size="sm",
                mb="xs",
            ),
            dmc.Text(f"Pace Factor: {game['pace_factor']:.2f}x", size="xs", c="dimmed"),
        ],
    )


def layout():
    games = get_live_games()
    return dmc.Container(
        fluid=True,
        children=[
            dmc.Title("Live Totals", order=2, mb="md"),
            dmc.Text(
                "Real-time pace tracking and projected totals for live games.", c="dimmed", mb="lg"
            ),
            dmc.Grid(
                children=[
                    dmc.GridCol(live_game_card(g), span={"base": 12, "md": 6, "lg": 4})
                    for g in games
                ]
            )
            if games
            else dmc.Alert("No live games currently.", color="blue"),
        ],
    )
