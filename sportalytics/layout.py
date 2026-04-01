import dash
import dash_mantine_components as dmc
from dash import dcc

NAV_ITEMS = [
    {"label": "AI Predictions", "href": "/predictions", "icon": "🤖"},
    {"label": "Player Props", "href": "/player-props", "icon": "🏀"},
    {"label": "Model Tracker", "href": "/model-tracker", "icon": "📊"},
    {"label": "Odds Insight", "href": "/odds-insight", "icon": "📈"},
    {"label": "Marketplace", "href": "/marketplace", "icon": "🏪"},
    {"label": "Free Pick", "href": "/free-pick", "icon": "🎁"},
    {"label": "Live Totals", "href": "/live-totals", "icon": "⚡"},
    {"label": "Calculators", "href": "/calculators", "icon": "🧮"},
]


def create_navbar():
    return dmc.AppShellNavbar(
        p="md",
        children=[
            dmc.Stack(
                gap="xs",
                children=[
                    dmc.NavLink(
                        label=f"{item['icon']} {item['label']}",
                        href=item["href"],
                        style={"borderRadius": "8px"},
                    )
                    for item in NAV_ITEMS
                ],
            )
        ],
    )


def create_header():
    return dmc.AppShellHeader(
        p="md",
        children=dmc.Group(
            justify="space-between",
            h="100%",
            children=[
                dmc.Group(
                    children=[
                        dmc.Text("⚡ Sportalytics", fw=700, size="xl", c="blue"),
                    ]
                ),
                dmc.Group(
                    children=[
                        dmc.Text("🌙", size="sm"),
                        dmc.Switch(
                            id="theme-toggle",
                            size="md",
                            color="blue",
                        ),
                        dmc.Text("☀️", size="sm"),
                    ]
                ),
            ],
        ),
    )


def create_layout():
    return dmc.AppShell(
        [
            create_header(),
            create_navbar(),
            dmc.AppShellMain(
                children=[
                    dcc.Store(id="theme-store", data="light"),
                    dash.page_container,
                ]
            ),
        ],
        navbar={"width": 250, "breakpoint": "sm", "collapsed": {"mobile": True}},
        header={"height": 60},
        padding="md",
    )
