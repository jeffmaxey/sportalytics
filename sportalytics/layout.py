"""
Application shell layout for Sportalytics.

Provides :func:`create_header`, :func:`create_navbar`, and
:func:`create_layout` which assemble the persistent
:class:`dmc.AppShell` structure shared by every page.
"""

import dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import dcc

NAV_ITEMS = [
    {"label": "Free Pick",      "href": "/free-pick",    "icon": "mdi:trophy-outline"},
    {"label": "AI Predictions", "href": "/predictions",  "icon": "mdi:robot-outline"},
    {"label": "Player Props",   "href": "/player-props", "icon": "mdi:basketball"},
    {"label": "Model Tracker",  "href": "/model-tracker","icon": "mdi:chart-line"},
    {"label": "Odds Insight",   "href": "/odds-insight", "icon": "mdi:chart-areaspline"},
    {"label": "Marketplace",    "href": "/marketplace",  "icon": "mdi:storefront-outline"},
    {
        "label": "Live Totals", "href": "/live-totals",  "icon": "mdi:lightning-bolt",
        "badge": "LIVE",        "badge_color": "red",
    },
    {"label": "Calculators",    "href": "/calculators",  "icon": "mdi:calculator-variant-outline"},
    {
        "label": "EV+",         "href": "/calculators",  "icon": "mdi:target",
        "badge": "SOON",        "badge_color": "gray",
    },
]

UTILITY_NAV = [
    {"label": "Home",     "href": "/",         "icon": "mdi:home-outline"},
    {"label": "Profile",  "href": "/profile",  "icon": "mdi:account-outline"},
    {"label": "Settings", "href": "/settings", "icon": "mdi:cog-outline"},
    {"label": "Help",     "href": "/help",     "icon": "mdi:help-circle-outline"},
]


def _nav_link(item: dict) -> dmc.NavLink:
    right_section = None
    if item.get("badge"):
        right_section = dmc.Badge(
            item["badge"],
            color=item["badge_color"],
            variant="filled",
            size="xs",
            radius="sm",
        )
    return dmc.NavLink(
        label=item["label"],
        leftSection=DashIconify(icon=item["icon"], width=16),
        href=item["href"],
        rightSection=right_section,
        style={"borderRadius": "8px"},
    )


def create_navbar() -> dmc.AppShellNavbar:
    """
    Build the persistent left-hand navigation sidebar with main nav,
    utility links, and a user section at the bottom.
    """
    main_links = [_nav_link(item) for item in NAV_ITEMS]

    return dmc.AppShellNavbar(
        p="md",
        style={"display": "flex", "flexDirection": "column", "gap": "0"},
        children=[
            # ── main navigation ──────────────────────────────────────────
            dmc.Stack(
                gap="xs",
                style={"flex": "1 1 auto", "overflowY": "auto"},
                children=main_links,
            ),
            # ── bottom section ───────────────────────────────────────────
            dmc.Stack(
                gap="xs",
                mt="md",
                children=[
                    dmc.Divider(),
                    # Utility icon row
                    dmc.Group(
                        gap=4,
                        justify="center",
                        children=[
                            dmc.Tooltip(
                                label=item["label"],
                                children=dmc.Anchor(
                                    href=item["href"],
                                    style={"textDecoration": "none"},
                                    children=dmc.ActionIcon(
                                        DashIconify(icon=item["icon"], width=16),
                                        variant="subtle",
                                        size="lg",
                                        radius="md",
                                    ),
                                ),
                            )
                            for item in UTILITY_NAV
                        ],
                    ),
                    dmc.Divider(),
                    # User card
                    dmc.Card(
                        withBorder=True,
                        radius="md",
                        p="sm",
                        children=dmc.Group(
                            gap="sm",
                            wrap="nowrap",
                            children=[
                                dmc.Avatar(
                                    "S",
                                    size="sm",
                                    radius="xl",
                                    color="green",
                                ),
                                dmc.Stack(
                                    gap=0,
                                    style={"flex": 1, "minWidth": 0},
                                    children=[
                                        dmc.Text(
                                            "sportalytics_user",
                                            size="xs",
                                            fw=600,
                                            style={"overflow": "hidden", "textOverflow": "ellipsis", "whiteSpace": "nowrap"},
                                        ),
                                        dmc.Text("Free Plan", size="xs", c="dimmed"),
                                    ],
                                ),
                            ],
                        ),
                    ),
                    dmc.NavLink(
                        label="Sign Out",
                        leftSection=DashIconify(icon="mdi:logout", width=16),
                        href="/",
                        style={"borderRadius": "8px"},
                        c="red",
                    ),
                ],
            ),
        ],
    )


def create_header() -> dmc.AppShellHeader:
    """
    Build the persistent top application header with branding and
    a dark-mode toggle.
    """
    return dmc.AppShellHeader(
        p="md",
        children=dmc.Group(
            justify="space-between",
            h="100%",
            children=[
                dmc.Group(
                    gap="xs",
                    children=[
                        DashIconify(icon="mdi:lightning-bolt", width=18, color="#51cf66"),
                        dmc.Text("Sportalytics", fw=700, size="xl", c="green"),
                    ],
                ),
                dmc.Group(
                    gap="xs",
                    children=[
                        DashIconify(icon="mdi:white-balance-sunny", width=16),
                        dmc.Switch(
                            id="theme-toggle",
                            size="md",
                            color="green",
                            checked=True,
                        ),
                        DashIconify(icon="mdi:moon-waning-crescent", width=16),
                    ],
                ),
            ],
        ),
    )


def create_layout() -> dmc.AppShell:
    """
    Assemble the full :class:`dmc.AppShell` application shell.
    """
    return dmc.AppShell(
        [
            create_header(),
            create_navbar(),
            dmc.AppShellMain(
                children=[
                    dcc.Store(id="theme-store", data="dark"),
                    dash.page_container,
                ]
            ),
        ],
        navbar={"width": 260, "breakpoint": "sm", "collapsed": {"mobile": True}},
        header={"height": 60},
        padding="md",
    )
