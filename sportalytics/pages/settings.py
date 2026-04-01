"""
Settings page for Sportalytics.

Four-tab settings panel: Account, Security, Notifications, Appearance —
mirroring the WiseSportsAI settings screen.
"""

import dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify

dash.register_page(__name__, path="/settings", title="Settings", name="Settings")


# ---------------------------------------------------------------------------
# Tab panels
# ---------------------------------------------------------------------------


def _account_tab() -> dmc.Stack:
    return dmc.Stack(
        gap="lg",
        pt="md",
        children=[
            # Top info row
            dmc.SimpleGrid(
                cols={"base": 1, "sm": 3},
                children=[
                    dmc.Card(
                        withBorder=True,
                        radius="md",
                        p="lg",
                        children=[
                            DashIconify(icon="mdi:email-outline", width=20),
                            dmc.Text("EMAIL ADDRESS", size="xs", c="dimmed", tt="uppercase", mt="xs", fw=500),
                            dmc.Text("user@sportalytics.com", fw=600),
                        ],
                    ),
                    dmc.Card(
                        withBorder=True,
                        radius="md",
                        p="lg",
                        children=[
                            DashIconify(icon="mdi:calendar-month-outline", width=20),
                            dmc.Text("MEMBER SINCE", size="xs", c="dimmed", tt="uppercase", mt="xs", fw=500),
                            dmc.Text("Mar 31, 2026", fw=600),
                        ],
                    ),
                    dmc.Card(
                        withBorder=True,
                        radius="md",
                        p="lg",
                        children=[
                            DashIconify(icon="mdi:crown-outline", width=20),
                            dmc.Text("PLAN", size="xs", c="dimmed", tt="uppercase", mt="xs", fw=500),
                            dmc.Text("Free", fw=600),
                            dmc.Text("Limited access", size="xs", c="dimmed"),
                        ],
                    ),
                ],
            ),
            # Subscription + Connected Accounts
            dmc.SimpleGrid(
                cols={"base": 1, "sm": 2},
                children=[
                    # Subscription
                    dmc.Card(
                        withBorder=True,
                        radius="md",
                        p="lg",
                        children=dmc.Stack(
                            gap="md",
                            children=[
                                dmc.Group(
                                    gap="xs",
                                    children=[
                                        DashIconify(icon="mdi:credit-card-outline", width=20),
                                        dmc.Stack(
                                            gap=0,
                                            children=[
                                                dmc.Text("Subscription", fw=600),
                                                dmc.Text("Manage your plan", size="xs", c="dimmed"),
                                            ],
                                        ),
                                    ],
                                ),
                                dmc.Card(
                                    withBorder=True,
                                    radius="md",
                                    p="md",
                                    children=dmc.Group(
                                        gap="sm",
                                        children=[
                                            dmc.Avatar(DashIconify(icon="mdi:lightning-bolt", width=16), size="md", radius="md", color="gray"),
                                            dmc.Stack(
                                                gap=0,
                                                children=[
                                                    dmc.Text("Free Plan", fw=600),
                                                    dmc.Text("Upgrade to unlock all features", size="xs", c="dimmed"),
                                                ],
                                            ),
                                        ],
                                    ),
                                ),
                                dmc.Button(
                                    "Upgrade to Pro",
                                    color="green",
                                    fullWidth=True,
                                    radius="md",
                                    leftSection=DashIconify(icon="mdi:lightning-bolt", width=16),
                                ),
                            ],
                        ),
                    ),
                    # Connected accounts
                    dmc.Card(
                        withBorder=True,
                        radius="md",
                        p="lg",
                        children=dmc.Stack(
                            gap="md",
                            children=[
                                dmc.Group(
                                    gap="xs",
                                    children=[
                                        DashIconify(icon="mdi:link-variant", width=20),
                                        dmc.Stack(
                                            gap=0,
                                            children=[
                                                dmc.Text("Connected Accounts", fw=600),
                                                dmc.Text("Link external services", size="xs", c="dimmed"),
                                            ],
                                        ),
                                    ],
                                ),
                                dmc.Card(
                                    withBorder=True,
                                    radius="md",
                                    p="md",
                                    children=dmc.Group(
                                        justify="space-between",
                                        children=[
                                            dmc.Group(
                                                gap="sm",
                                                children=[
                                                    dmc.Avatar(DashIconify(icon="mdi:chat-outline", width=14), size="sm", radius="md", color="blue"),
                                                    dmc.Stack(
                                                        gap=0,
                                                        children=[
                                                            dmc.Text("Discord", size="sm", fw=600),
                                                            dmc.Text("Not connected", size="xs", c="dimmed"),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                            dmc.Button(
                                                "Connect",
                                                size="xs",
                                                color="blue",
                                                variant="filled",
                                                radius="md",
                                            ),
                                        ],
                                    ),
                                ),
                            ],
                        ),
                    ),
                ],
            ),
            # Delete account
            dmc.Card(
                withBorder=True,
                radius="md",
                p="lg",
                children=dmc.Group(
                    justify="space-between",
                    children=[
                        dmc.Group(
                            gap="sm",
                            children=[
                                dmc.Avatar(DashIconify(icon="mdi:delete-outline", width=14), size="sm", radius="md", color="red"),
                                dmc.Stack(
                                    gap=0,
                                    children=[
                                        dmc.Text("Delete Account", fw=600),
                                        dmc.Text("Permanently remove your account and data", size="xs", c="dimmed"),
                                    ],
                                ),
                            ],
                        ),
                        dmc.Button("Delete", color="red", variant="subtle", radius="md"),
                    ],
                ),
            ),
        ],
    )


def _security_tab() -> dmc.Stack:
    return dmc.Stack(
        gap="lg",
        pt="md",
        children=[
            dmc.SimpleGrid(
                cols={"base": 1, "sm": 2},
                children=[
                    # Password
                    dmc.Card(
                        withBorder=True,
                        radius="md",
                        p="lg",
                        children=dmc.Stack(
                            gap="md",
                            children=[
                                dmc.Group(
                                    gap="xs",
                                    children=[
                                        DashIconify(icon="mdi:key-outline", width=20),
                                        dmc.Stack(
                                            gap=0,
                                            children=[
                                                dmc.Text("Password", fw=600),
                                                dmc.Text("Change your password", size="xs", c="dimmed"),
                                            ],
                                        ),
                                    ],
                                ),
                                dmc.Card(
                                    withBorder=True,
                                    radius="md",
                                    p="md",
                                    children=dmc.Stack(
                                        gap="xs",
                                        children=[
                                            dmc.Group(
                                                gap="sm",
                                                children=[
                                                    DashIconify(icon="mdi:lock-outline", width=14),
                                                    dmc.Text("Current Password", size="sm", fw=500),
                                                ],
                                            ),
                                            dmc.Text(
                                                "••••••••••••",
                                                size="sm",
                                                c="dimmed",
                                                fw=700,
                                                style={"letterSpacing": "0.2em"},
                                            ),
                                            dmc.Text(
                                                "We'll send a verification code to your email",
                                                size="xs",
                                                c="dimmed",
                                            ),
                                        ],
                                    ),
                                ),
                                dmc.Button(
                                    "Change Password",
                                    variant="default",
                                    fullWidth=True,
                                    radius="md",
                                    leftSection=DashIconify(icon="mdi:lock-outline", width=14),
                                ),
                            ],
                        ),
                    ),
                    # Right column: 2FA + Active Sessions
                    dmc.Stack(
                        gap="md",
                        children=[
                            # Two-Factor Auth
                            dmc.Card(
                                withBorder=True,
                                radius="md",
                                p="lg",
                                children=dmc.Stack(
                                    gap="md",
                                    children=[
                                        dmc.Group(
                                            gap="xs",
                                            children=[
                                                DashIconify(icon="mdi:cellphone", width=20),
                                                dmc.Stack(
                                                    gap=0,
                                                    children=[
                                                        dmc.Text("Two-Factor Auth", fw=600),
                                                        dmc.Text("Extra security layer", size="xs", c="dimmed"),
                                                    ],
                                                ),
                                            ],
                                        ),
                                        dmc.Card(
                                            withBorder=True,
                                            radius="md",
                                            p="md",
                                            children=dmc.Group(
                                                justify="space-between",
                                                children=[
                                                    dmc.Group(
                                                        gap="sm",
                                                        children=[
                                                            dmc.Avatar(DashIconify(icon="mdi:shield-outline", width=14), size="sm", radius="md", color="yellow"),
                                                            dmc.Stack(
                                                                gap=0,
                                                                children=[
                                                                    dmc.Text("2FA Status", size="sm", fw=600),
                                                                    dmc.Text("Not enabled", size="xs", c="dimmed"),
                                                                ],
                                                            ),
                                                        ],
                                                    ),
                                                    dmc.Badge("SOON", color="gray", variant="filled", size="sm"),
                                                ],
                                            ),
                                        ),
                                    ],
                                ),
                            ),
                            # Active Sessions
                            dmc.Card(
                                withBorder=True,
                                radius="md",
                                p="lg",
                                children=dmc.Stack(
                                    gap="md",
                                    children=[
                                        dmc.Group(
                                            gap="xs",
                                            children=[
                                                DashIconify(icon="mdi:monitor", width=20),
                                                dmc.Stack(
                                                    gap=0,
                                                    children=[
                                                        dmc.Text("Active Sessions", fw=600),
                                                        dmc.Text("Devices logged in", size="xs", c="dimmed"),
                                                    ],
                                                ),
                                            ],
                                        ),
                                        dmc.Card(
                                            withBorder=True,
                                            radius="md",
                                            p="md",
                                            children=dmc.Group(
                                                justify="space-between",
                                                children=[
                                                    dmc.Group(
                                                        gap="sm",
                                                        children=[
                                                            dmc.Avatar(DashIconify(icon="mdi:monitor", width=14), size="sm", radius="md"),
                                                            dmc.Stack(
                                                                gap=0,
                                                                children=[
                                                                    dmc.Text("Current Device", size="sm", fw=600),
                                                                    dmc.Text("Active now", size="xs", c="dimmed"),
                                                                ],
                                                            ),
                                                        ],
                                                    ),
                                                    dmc.Badge([DashIconify(icon="mdi:circle", width=8), " Active"], color="green", size="sm"),
                                                ],
                                            ),
                                        ),
                                    ],
                                ),
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


def _notifications_tab() -> dmc.Stack:
    def _toggle_row(label: str, desc: str, default: bool = True) -> dmc.Group:
        return dmc.Group(
            justify="space-between",
            children=[
                dmc.Stack(
                    gap=0,
                    children=[
                        dmc.Text(label, size="sm", fw=500),
                        dmc.Text(desc, size="xs", c="dimmed"),
                    ],
                ),
                dmc.Switch(checked=default, color="green", size="md"),
            ],
        )

    return dmc.Stack(
        gap="lg",
        pt="md",
        children=[
            # Summary pills
            dmc.SimpleGrid(
                cols={"base": 2, "sm": 4},
                children=[
                    dmc.Card(withBorder=True, radius="md", p="md", children=[
                        dmc.Group(gap="xs", children=[DashIconify(icon="mdi:email-outline", width=14), dmc.Stack(gap=0, children=[dmc.Text("EMAIL", size="xs", c="dimmed", tt="uppercase"), dmc.Text("On", fw=700, c="green")])]),
                    ]),
                    dmc.Card(withBorder=True, radius="md", p="md", children=[
                        dmc.Group(gap="xs", children=[DashIconify(icon="mdi:bell-outline", width=14), dmc.Stack(gap=0, children=[dmc.Text("PUSH", size="xs", c="dimmed", tt="uppercase"), dmc.Text("On", fw=700, c="green")])]),
                    ]),
                    dmc.Card(withBorder=True, radius="md", p="md", children=[
                        dmc.Group(gap="xs", children=[DashIconify(icon="mdi:lightning-bolt", width=14), dmc.Stack(gap=0, children=[dmc.Text("PICK ALERTS", size="xs", c="dimmed", tt="uppercase"), dmc.Text("On", fw=700, c="green")])]),
                    ]),
                    dmc.Card(withBorder=True, radius="md", p="md", children=[
                        dmc.Group(gap="xs", children=[DashIconify(icon="mdi:volume-high", width=14), dmc.Stack(gap=0, children=[dmc.Text("SOUND", size="xs", c="dimmed", tt="uppercase"), dmc.Text("On", fw=700, c="green")])]),
                    ]),
                ],
            ),
            # Detail cards
            dmc.SimpleGrid(
                cols={"base": 1, "sm": 2},
                children=[
                    # Email notifications
                    dmc.Card(
                        withBorder=True,
                        radius="md",
                        p="lg",
                        children=dmc.Stack(
                            gap="md",
                            children=[
                                dmc.Group(gap="xs", children=[
                                    DashIconify(icon="mdi:email-outline", width=20),
                                    dmc.Stack(gap=0, children=[
                                        dmc.Text("Email Notifications", fw=600),
                                        dmc.Text("Updates sent to your inbox", size="xs", c="dimmed"),
                                    ]),
                                ]),
                                dmc.Stack(gap="sm", children=[
                                    _toggle_row("Email Notifications", "Important updates", True),
                                    dmc.Divider(),
                                    _toggle_row("Pick Alerts", "New picks available", True),
                                    dmc.Divider(),
                                    _toggle_row("Promotions", "Offers and deals", False),
                                ]),
                            ],
                        ),
                    ),
                    # Push + Sound
                    dmc.Stack(
                        gap="md",
                        children=[
                            dmc.Card(
                                withBorder=True,
                                radius="md",
                                p="lg",
                                children=dmc.Stack(
                                    gap="md",
                                    children=[
                                        dmc.Group(gap="xs", children=[
                                            DashIconify(icon="mdi:bell-outline", width=20),
                                            dmc.Stack(gap=0, children=[
                                                dmc.Text("Push Notifications", fw=600),
                                                dmc.Text("Browser alerts", size="xs", c="dimmed"),
                                            ]),
                                        ]),
                                        _toggle_row("Push Notifications", "Desktop & mobile", True),
                                    ],
                                ),
                            ),
                            dmc.Card(
                                withBorder=True,
                                radius="md",
                                p="lg",
                                children=dmc.Stack(
                                    gap="md",
                                    children=[
                                        dmc.Group(gap="xs", children=[
                                            DashIconify(icon="mdi:volume-high", width=20),
                                            dmc.Stack(gap=0, children=[
                                                dmc.Text("Sound", fw=600),
                                                dmc.Text("Audio alerts", size="xs", c="dimmed"),
                                            ]),
                                        ]),
                                        _toggle_row("Notification Sounds", "Play alert sounds", True),
                                    ],
                                ),
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


def _appearance_tab() -> dmc.Stack:
    themes = [
        {"icon": "mdi:moon-waning-crescent", "label": "Dark",   "desc": "Easy on the eyes",  "value": "dark"},
        {"icon": "mdi:white-balance-sunny", "label": "Light",  "desc": "Bright and clean",  "value": "light"},
        {"icon": "mdi:monitor", "label": "System", "desc": "Match device",      "value": "system"},
    ]
    return dmc.Stack(
        gap="lg",
        pt="md",
        children=[
            # Theme selector
            dmc.Card(
                withBorder=True,
                radius="md",
                p="lg",
                children=dmc.Stack(
                    gap="md",
                    children=[
                        dmc.Group(gap="xs", children=[
                            DashIconify(icon="mdi:palette-outline", width=20),
                            dmc.Stack(gap=0, children=[
                                dmc.Text("Theme", fw=600),
                                dmc.Text("Choose your preferred look", size="xs", c="dimmed"),
                            ]),
                        ]),
                        dmc.SimpleGrid(
                            cols=3,
                            children=[
                                dmc.Card(
                                    withBorder=True,
                                    radius="md",
                                    p="md",
                                    style={
                                        "cursor": "pointer",
                                        "borderColor": "#51cf66" if t["value"] == "dark" else None,
                                        "borderWidth": 2 if t["value"] == "dark" else 1,
                                        "textAlign": "center",
                                    },
                                    children=dmc.Stack(
                                        align="center",
                                        gap="xs",
                                        children=[
                                            DashIconify(icon=t["icon"], width=28),
                                            dmc.Text(t["label"], fw=600, size="sm"),
                                            dmc.Text(t["desc"], size="xs", c="dimmed"),
                                        ],
                                    ),
                                )
                                for t in themes
                            ],
                        ),
                        dmc.Text(
                            "Note: Only dark theme is currently available",
                            size="xs",
                            c="dimmed",
                            ta="center",
                        ),
                    ],
                ),
            ),
            # Display + Language
            dmc.SimpleGrid(
                cols={"base": 1, "sm": 2},
                children=[
                    # Display
                    dmc.Card(
                        withBorder=True,
                        radius="md",
                        p="lg",
                        children=dmc.Stack(
                            gap="md",
                            children=[
                                dmc.Group(gap="xs", children=[
                                    DashIconify(icon="mdi:aspect-ratio", width=20),
                                    dmc.Stack(gap=0, children=[
                                        dmc.Text("Display", fw=600),
                                        dmc.Text("Visual preferences", size="xs", c="dimmed"),
                                    ]),
                                ]),
                                dmc.Group(
                                    justify="space-between",
                                    children=[
                                        dmc.Stack(gap=0, children=[
                                            dmc.Text("Compact Mode", size="sm", fw=500),
                                            dmc.Text("Reduce spacing", size="xs", c="dimmed"),
                                        ]),
                                        dmc.Switch(checked=True, color="green", size="md"),
                                    ],
                                ),
                                dmc.Divider(),
                                dmc.Group(
                                    justify="space-between",
                                    children=[
                                        dmc.Stack(gap=0, children=[
                                            dmc.Text("Animations", size="sm", fw=500),
                                            dmc.Text("UI transitions", size="xs", c="dimmed"),
                                        ]),
                                        dmc.Switch(checked=True, color="green", size="md"),
                                    ],
                                ),
                            ],
                        ),
                    ),
                    # Language & Region
                    dmc.Card(
                        withBorder=True,
                        radius="md",
                        p="lg",
                        children=dmc.Stack(
                            gap="md",
                            children=[
                                dmc.Group(gap="xs", children=[
                                    DashIconify(icon="mdi:earth", width=20),
                                    dmc.Stack(gap=0, children=[
                                        dmc.Text("Language & Region", fw=600),
                                        dmc.Text("Localization settings", size="xs", c="dimmed"),
                                    ]),
                                ]),
                                dmc.Card(
                                    withBorder=True,
                                    radius="md",
                                    p="md",
                                    children=dmc.Group(
                                        justify="space-between",
                                        children=[
                                            dmc.Group(gap="sm", children=[
                                                DashIconify(icon="mdi:flag", width=16),
                                                dmc.Stack(gap=0, children=[
                                                    dmc.Text("English (US)", size="sm", fw=600),
                                                    dmc.Text("Default language", size="xs", c="dimmed"),
                                                ]),
                                            ]),
                                            dmc.Badge("ONLY", color="green", variant="light", size="sm"),
                                        ],
                                    ),
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        ],
    )


# ---------------------------------------------------------------------------
# Page layout
# ---------------------------------------------------------------------------


def layout() -> dmc.Container:
    """Render the Settings page with four tabs."""
    return dmc.Container(
        fluid=True,
        children=[
            # Page header
            dmc.Group(
                mb="xl",
                gap="md",
                children=[
                    dmc.Avatar(DashIconify(icon="mdi:cog-outline", width=18), size="lg", radius="md", color="green"),
                    dmc.Stack(
                        gap=2,
                        children=[
                            dmc.Title("Settings", order=2),
                            dmc.Text("Manage your account and preferences", size="sm", c="dimmed"),
                        ],
                    ),
                ],
            ),
            # Tabs
            dmc.Tabs(
                value="account",
                children=[
                    dmc.TabsList(
                        mb="md",
                        children=[
                            dmc.TabsTab([DashIconify(icon="mdi:account-outline", width=14), " Account"], value="account"),
                            dmc.TabsTab([DashIconify(icon="mdi:lock-outline", width=14), " Security"], value="security"),
                            dmc.TabsTab([DashIconify(icon="mdi:bell-outline", width=14), " Notifications"], value="notifications"),
                            dmc.TabsTab([DashIconify(icon="mdi:palette-outline", width=14), " Appearance"], value="appearance"),
                        ],
                    ),
                    dmc.TabsPanel(_account_tab(),       value="account"),
                    dmc.TabsPanel(_security_tab(),      value="security"),
                    dmc.TabsPanel(_notifications_tab(), value="notifications"),
                    dmc.TabsPanel(_appearance_tab(),    value="appearance"),
                ],
            ),
            # Footer
            dmc.Group(
                justify="space-between",
                mt="xl",
                children=[
                    dmc.Group(gap="sm", children=[
                        DashIconify(icon="mdi:lightning-bolt", width=14, color="#868e96"),
                        dmc.Text("Sportalytics", size="sm", c="dimmed"),
                        dmc.Text("v2.0", size="sm", c="dimmed"),
                    ]),
                ],
            ),
        ],
    )

