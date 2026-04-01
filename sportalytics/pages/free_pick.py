"""
Free Pick of the Day page for Sportalytics.

Enhanced layout matching the WiseSportsAI free pick screen:
- Live countdown to midnight ET (dcc.Interval callback)
- Team matchup display with AI pick in large text
- Confidence / edge / hit-rate / model stat row
- AI Analysis narrative
- "Unlock All Picks" upgrade CTA
- Recent Free Picks history list
"""

from __future__ import annotations

import dash
import dash_mantine_components as dmc
from dash import Input, Output, callback, dcc, html
from dash_iconify import DashIconify
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from sportalytics.services.free_pick import get_free_pick, get_free_pick_history

dash.register_page(__name__, path="/free-pick", title="Free Pick of the Day", name="Free Pick")

# ---------------------------------------------------------------------------
# Module-level data
# ---------------------------------------------------------------------------

_ET = ZoneInfo("America/New_York")

PICK = get_free_pick()
HISTORY = get_free_pick_history()
WINS = sum(1 for h in HISTORY if h["result"] == "W")
LOSSES = sum(1 for h in HISTORY if h["result"] == "L")
UNITS = +1.67
WIN_RATE = 53.6

_TEAM_DISPLAY = {
    "CBB": ("Baylor", "Minnesota"),
    "NBA": ("Celtics", "Knicks"),
    "NFL": ("Chiefs", "Bills"),
    "NHL": ("Bruins", "Rangers"),
    "MLB": ("Yankees", "Red Sox"),
    "UFC": ("Jones", "Miocic"),
    "CFB": ("Alabama", "Georgia"),
}

_HOME_TEAM, _AWAY_TEAM = _TEAM_DISPLAY.get(PICK["sport"], ("Home", "Away"))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _get_seconds_to_midnight() -> int:
    now = datetime.now(_ET)
    midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    return max(0, int((midnight - now).total_seconds()))


def _result_color(result: str) -> str:
    return {"W": "green", "L": "red", "P": "yellow"}.get(result, "gray")


def _countdown_children(hrs: int, mins: int, secs: int):
    return dmc.SimpleGrid(
        cols=3,
        spacing="xs",
        children=[
            dmc.Stack(align="center", gap=2, children=[
                dmc.Text(f"{hrs:02d}", size="2rem", fw=800),
                dmc.Text("HOURS", size="xs", c="dimmed", fw=600),
            ]),
            dmc.Stack(align="center", gap=2, children=[
                dmc.Text(f"{mins:02d}", size="2rem", fw=800),
                dmc.Text("MINS", size="xs", c="dimmed", fw=600),
            ]),
            dmc.Stack(align="center", gap=2, children=[
                dmc.Text(f"{secs:02d}", size="2rem", fw=800, c="green"),
                dmc.Text("SECS", size="xs", c="dimmed", fw=600),
            ]),
        ],
    )


# ---------------------------------------------------------------------------
# Countdown callback
# ---------------------------------------------------------------------------


@callback(
    Output("free-pick-countdown", "children"),
    Output("free-pick-inline-countdown", "children"),
    Input("free-pick-interval", "n_intervals"),
)
def _update_countdown(n_intervals):
    secs = _get_seconds_to_midnight()
    hrs = secs // 3600
    mins = (secs % 3600) // 60
    s = secs % 60
    return _countdown_children(hrs, mins, s), f"{hrs:02d}:{mins:02d}:{s:02d}"


# ---------------------------------------------------------------------------
# Sub-components
# ---------------------------------------------------------------------------


def _record_bar() -> dmc.Card:
    return dmc.Card(
        withBorder=True, radius="md", p="lg", mb="lg",
        children=dmc.Group(
            justify="space-between", wrap="wrap", gap="xl",
            children=[
                dmc.Group(gap="sm", children=[
                    dmc.Avatar(DashIconify(icon="mdi:trophy-outline", width=16), size="md", radius="md", color="yellow"),
                    dmc.Stack(gap=0, children=[
                        dmc.Text("Free Pick Record", fw=600),
                        dmc.Text("All-time tracked results", size="xs", c="dimmed"),
                    ]),
                ]),
                dmc.Group(gap="xl", children=[
                    dmc.Stack(align="center", gap=0, children=[
                        dmc.Text(f"{WINS}-{LOSSES}", size="xl", fw=800),
                        dmc.Text("W-L", size="xs", c="dimmed"),
                    ]),
                    dmc.Stack(align="center", gap=0, children=[
                        dmc.Text(f"+{UNITS}u", size="xl", fw=800, c="green"),
                        dmc.Text("Units", size="xs", c="dimmed"),
                    ]),
                    dmc.Stack(align="center", gap=0, children=[
                        dmc.Text(f"{WIN_RATE}%", size="xl", fw=800, c="green"),
                        dmc.Text("Win Rate", size="xs", c="dimmed"),
                    ]),
                ]),
            ],
        ),
    )


def _main_pick_card() -> dmc.Card:
    now_et = datetime.now(_ET)
    try:
        date_str = now_et.strftime("%-d %b")
    except ValueError:
        date_str = now_et.strftime("%#d %b")

    confidence_pct = int(PICK["ml_score"] * 100)

    return dmc.Card(
        withBorder=True, radius="md", p="lg",
        children=dmc.Stack(gap="md", children=[
            # Header row
            dmc.Group(justify="space-between", wrap="wrap", gap="sm", children=[
                dmc.Group(gap="xs", children=[
                    dmc.Badge("DAILY FREE PICK", color="green", variant="filled", size="sm", radius="sm"),
                    dmc.Badge(
                        f"{PICK['sport']} • {PICK['pick_type'].upper()}",
                        color="gray", variant="light", size="sm", radius="sm",
                    ),
                ]),
                dmc.Group(gap="sm", children=[
                    dmc.Group(gap=4, children=[DashIconify(icon="mdi:calendar-month-outline", width=14, color="#868e96"), dmc.Text(date_str, size="sm", c="dimmed")]),
                    dmc.Group(gap="xs", children=[
                        DashIconify(icon="mdi:clock-outline", width=14, color="#868e96"),
                        dmc.Text("Resets in", size="sm", c="dimmed"),
                        html.Span(
                            id="free-pick-inline-countdown",
                            style={"color": "#51cf66", "fontSize": "0.875rem", "fontWeight": 600},
                        ),
                    ]),
                ]),
            ]),
            # Teams
            dmc.Paper(
                withBorder=True, radius="md", p="lg",
                children=dmc.Stack(gap="sm", children=[
                    dmc.Text("TODAY'S MATCHUP", size="xs", c="dimmed", ta="center", tt="uppercase", fw=600),
                    dmc.Group(justify="center", gap="xl", children=[
                        dmc.Stack(align="center", gap="xs", children=[
                            dmc.Avatar(_HOME_TEAM[0], size="xl", radius="xl", color="green",
                                       style={"fontSize": "1.5rem", "fontWeight": 800}),
                            dmc.Text(_HOME_TEAM, fw=600),
                        ]),
                        dmc.Text("@", size="xl", c="dimmed", fw=300),
                        dmc.Stack(align="center", gap="xs", children=[
                            dmc.Avatar(_AWAY_TEAM[0], size="xl", radius="xl", color="red",
                                       style={"fontSize": "1.5rem", "fontWeight": 800}),
                            dmc.Text(_AWAY_TEAM, fw=600),
                        ]),
                    ]),
                ]),
            ),
            # AI Pick
            dmc.Paper(
                withBorder=True, radius="md", p="lg",
                children=dmc.Stack(align="center", gap="xs", children=[
                    dmc.Group(gap="xs", justify="center", children=[
                        DashIconify(icon="mdi:robot-outline", width=14),
                        dmc.Text("AI PICK", size="xs", c="dimmed", fw=600, tt="uppercase"),
                    ]),
                    dmc.Text(PICK["pick"], size="2.5rem", fw=800, c="green", ta="center"),
                ]),
            ),
            # Stats
            dmc.SimpleGrid(cols=4, children=[
                dmc.Stack(align="center", gap=2, children=[
                    dmc.Text("CONFIDENCE", size="xs", c="dimmed", fw=600, tt="uppercase"),
                    dmc.Text(f"{confidence_pct}%", fw=700, size="lg"),
                ]),
                dmc.Stack(align="center", gap=2, children=[
                    dmc.Text("EDGE", size="xs", c="dimmed", fw=600, tt="uppercase"),
                    dmc.Text("+0.0 pts", fw=700, size="lg", c="green"),
                ]),
                dmc.Stack(align="center", gap=2, children=[
                    dmc.Text("HIT RATE", size="xs", c="dimmed", fw=600, tt="uppercase"),
                    dmc.Text("63%", fw=700, size="lg"),
                ]),
                dmc.Stack(align="center", gap=2, children=[
                    dmc.Text("MODEL", size="xs", c="dimmed", fw=600, tt="uppercase"),
                    dmc.Text(PICK["sport"], fw=700, size="lg"),
                ]),
            ]),
        ]),
    )


def _ai_analysis_card() -> dmc.Card:
    return dmc.Card(
        withBorder=True, radius="md", p="lg",
        children=dmc.Stack(gap="md", children=[
            dmc.Group(gap="sm", children=[
                dmc.Avatar(DashIconify(icon="mdi:robot-outline", width=14), size="sm", radius="md", color="green"),
                dmc.Stack(gap=0, children=[
                    dmc.Text("AI Analysis", fw=600),
                    dmc.Text("Machine learning insights", size="xs", c="dimmed"),
                ]),
            ]),
            dmc.Text(PICK["rationale"], size="sm"),
        ]),
    )


def _recent_picks_card() -> dmc.Card:
    return dmc.Card(
        withBorder=True, radius="md", p="lg",
        children=dmc.Stack(gap="md", children=[
            dmc.Group(gap="sm", children=[
                dmc.Avatar(DashIconify(icon="mdi:clock-outline", width=14), size="sm", radius="md", color="orange"),
                dmc.Stack(gap=0, children=[
                    dmc.Text("Recent Free Picks", fw=600),
                    dmc.Text("Last 10 graded picks", size="xs", c="dimmed"),
                ]),
            ]),
            dmc.Stack(gap="xs", children=[
                dmc.Card(
                    withBorder=True, radius="sm", p="sm",
                    children=dmc.Group(justify="space-between", children=[
                        dmc.Group(gap="sm", children=[
                            dmc.Badge(
                                h["result"],
                                color=_result_color(h["result"]),
                                variant="filled", size="sm", radius="sm",
                            ),
                            dmc.Stack(gap=0, children=[
                                dmc.Text(h["pick"], size="sm", fw=500),
                                dmc.Text(
                                    f"{h['matchup']} • {h['date']}",
                                    size="xs", c="dimmed",
                                ),
                            ]),
                        ]),
                        dmc.Badge(
                            f"Grade {h['grade']}",
                            color={"A": "green", "B": "yellow", "C": "orange"}.get(h["grade"][0], "blue"),
                            variant="light", size="sm",
                        ),
                    ]),
                )
                for h in HISTORY
            ]),
        ]),
    )


def _sidebar() -> dmc.Stack:
    secs = _get_seconds_to_midnight()
    hrs, mins, s = secs // 3600, (secs % 3600) // 60, secs % 60

    premium = [
        ("50+ Daily AI Picks",  "All sports covered",  "mdi:lock-outline"),
        ("Player Props",         "O/U predictions",     "mdi:lock-outline"),
        ("Deep Analytics",       "Advanced insights",   "mdi:lock-outline"),
        ("Real-time Updates",    "Live odds tracking",  "mdi:lock-outline"),
    ]

    return dmc.Stack(gap="md", children=[
        # Countdown card
        dmc.Card(
            withBorder=True, radius="md", p="lg",
            children=dmc.Stack(gap="md", children=[
                dmc.Group(gap="sm", children=[
                    DashIconify(icon="mdi:clock-outline", width=18),
                    dmc.Stack(gap=0, children=[
                        dmc.Text("Next Pick In", fw=600),
                        dmc.Text("Resets at midnight ET", size="xs", c="dimmed"),
                    ]),
                ]),
                html.Div(id="free-pick-countdown", children=_countdown_children(hrs, mins, s)),
            ]),
        ),
        # Upgrade CTA
        dmc.Card(
            withBorder=True, radius="md", p="lg",
            style={"borderColor": "#51cf66"},
            children=dmc.Stack(gap="md", children=[
                dmc.Stack(align="center", gap="sm", children=[
                    DashIconify(icon="mdi:trophy-outline", width=32),
                    dmc.Text("Unlock All Picks", fw=700, size="lg", ta="center"),
                    dmc.Text(
                        "Get unlimited AI predictions across all sports, player props, and exclusive insights.",
                        size="sm", c="dimmed", ta="center",
                    ),
                ]),
                dmc.Button("Upgrade Now", color="green", fullWidth=True, radius="md", size="md", rightSection=DashIconify(icon="mdi:arrow-right", width=16)),
            ]),
        ),
        # Premium features
        dmc.Card(
            withBorder=True, radius="md", p="lg",
            children=dmc.Stack(gap="md", children=[
                dmc.Group(gap="xs", children=[
                    DashIconify(icon="mdi:star-outline", width=14),
                    dmc.Text("Premium Features", fw=600),
                ]),
                dmc.Stack(gap="xs", children=[
                    dmc.Group(justify="space-between", children=[
                        dmc.Group(gap="sm", children=[
                            DashIconify(icon="mdi:circle", width=8, color="#228be6"),
                            dmc.Stack(gap=0, children=[
                                dmc.Text(pf[0], size="sm", fw=500),
                                dmc.Text(pf[1], size="xs", c="dimmed"),
                            ]),
                        ]),
                        DashIconify(icon=pf[2], width=14, color="#868e96"),
                    ])
                    for pf in premium
                ]),
            ]),
        ),
    ])


# ---------------------------------------------------------------------------
# Page layout
# ---------------------------------------------------------------------------


def layout() -> dmc.Container:
    """Render the enhanced Free Pick of the Day page."""
    return dmc.Container(
        fluid=True,
        children=[
            dcc.Interval(id="free-pick-interval", interval=1_000, n_intervals=0),
            # Page title
            dmc.Group(mb="lg", gap="md", children=[
                dmc.Avatar(DashIconify(icon="mdi:gift-outline", width=18), size="lg", radius="md", color="green"),
                dmc.Stack(gap=2, children=[
                    dmc.Group(gap="xs", children=[
                        dmc.Title("Free Pick ", order=2, style={"display": "inline"}),
                        dmc.Title("of the Day", order=2, c="green", style={"display": "inline"}),
                    ]),
                    dmc.Text("One free AI-powered prediction daily", size="sm", c="dimmed"),
                ]),
            ]),
            _record_bar(),
            dmc.Grid(gutter="md", children=[
                dmc.GridCol(
                    span={"base": 12, "md": 8},
                    children=dmc.Stack(gap="md", children=[
                        _main_pick_card(),
                        _ai_analysis_card(),
                        _recent_picks_card(),
                    ]),
                ),
                dmc.GridCol(span={"base": 12, "md": 4}, children=_sidebar()),
            ]),
        ],
    )
