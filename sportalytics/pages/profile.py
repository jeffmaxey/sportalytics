"""
User Profile / Dashboard page for Sportalytics.

Displays account overview, subscription status, quick actions,
referral program, and recent activity — mirroring the WiseSportsAI
profile dashboard.
"""

import dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify

dash.register_page(__name__, path="/profile", title="Profile", name="Profile")

# ---------------------------------------------------------------------------
# Demo user data
# ---------------------------------------------------------------------------

USER = {
    "username": "sportalytics_user",
    "email": "user@sportalytics.com",
    "plan": "Free",
    "plan_label": "Limited",
    "member_since": "Mar 31, 2026",
    "referrals": 0,
    "rewards": 0.00,
    "referral_code": "sport3l4b9c2f",
    "email_verified": True,
    "account_active": True,
    "two_fa_enabled": False,
}


# ---------------------------------------------------------------------------
# Sub-components
# ---------------------------------------------------------------------------


def _profile_header() -> dmc.Group:
    return dmc.Group(
        mb="xl",
        gap="lg",
        align="flex-start",
        children=[
            dmc.Avatar(
                USER["username"][0].upper(),
                size="xl",
                radius="xl",
                color="green",
                style={"fontSize": "1.5rem"},
            ),
            dmc.Stack(
                gap=4,
                children=[
                    dmc.Text(USER["username"], fw=700, size="xl"),
                    dmc.Text(USER["email"], c="dimmed", size="sm"),
                ],
            ),
        ],
    )


def _stat_cards() -> dmc.SimpleGrid:
    return dmc.SimpleGrid(
        cols={"base": 2, "sm": 4},
        mb="xl",
        children=[
            dmc.Card(
                withBorder=True,
                radius="md",
                p="lg",
                children=[
                    DashIconify(icon="mdi:calendar-month-outline", width=24),
                    dmc.Text("MEMBER SINCE", size="xs", c="dimmed", mt="xs", tt="uppercase", fw=500),
                    dmc.Text(USER["member_since"], fw=700, size="md"),
                ],
            ),
            dmc.Card(
                withBorder=True,
                radius="md",
                p="lg",
                children=[
                    DashIconify(icon="mdi:crown-outline", width=24),
                    dmc.Text("PLAN", size="xs", c="dimmed", mt="xs", tt="uppercase", fw=500),
                    dmc.Text(USER["plan"], fw=700, size="md"),
                    dmc.Text(USER["plan_label"], size="xs", c="dimmed"),
                ],
            ),
            dmc.Card(
                withBorder=True,
                radius="md",
                p="lg",
                children=[
                    DashIconify(icon="mdi:account-group-outline", width=24),
                    dmc.Text("REFERRALS", size="xs", c="dimmed", mt="xs", tt="uppercase", fw=500),
                    dmc.Text("N/A" if USER["referrals"] == 0 else str(USER["referrals"]), fw=700, size="md"),
                    dmc.Text("friends invited", size="xs", c="dimmed"),
                ],
            ),
            dmc.Card(
                withBorder=True,
                radius="md",
                p="lg",
                children=[
                    DashIconify(icon="mdi:cash-multiple", width=24),
                    dmc.Text("REWARDS", size="xs", c="dimmed", mt="xs", tt="uppercase", fw=500),
                    dmc.Text(f"${USER['rewards']:.2f}", fw=700, size="md"),
                    dmc.Text("total earned", size="xs", c="dimmed"),
                ],
            ),
        ],
    )


def _subscription_card() -> dmc.Card:
    return dmc.Card(
        withBorder=True,
        radius="md",
        p="lg",
        h="100%",
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
                                dmc.Text("Subscription", fw=600, size="md"),
                                dmc.Text("Your current plan", size="xs", c="dimmed"),
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
                                    dmc.Text("Upgrade for full access", size="xs", c="dimmed"),
                                ],
                            ),
                        ],
                    ),
                ),
                dmc.Button(
                    "Upgrade",
                    color="green",
                    fullWidth=True,
                    radius="md",
                    size="md",
                    leftSection=DashIconify(icon="mdi:lightning-bolt", width=16),
                ),
            ],
        ),
    )


def _account_status_card() -> dmc.Card:
    return dmc.Card(
        withBorder=True,
        radius="md",
        p="lg",
        h="100%",
        children=dmc.Stack(
            gap="md",
            children=[
                dmc.Group(
                    gap="xs",
                    children=[
                        DashIconify(icon="mdi:lightning-bolt", width=20),
                        dmc.Stack(
                            gap=0,
                            children=[
                                dmc.Text("Account Status", fw=600, size="md"),
                                dmc.Text("Your account health", size="xs", c="dimmed"),
                            ],
                        ),
                    ],
                ),
                dmc.Stack(
                    gap="sm",
                    children=[
                        dmc.Group(
                            justify="space-between",
                            children=[
                                dmc.Group(gap="xs", children=[
                                    DashIconify(icon="mdi:check-bold", width=14, color="#51cf66"),
                                    dmc.Text("Email Verified", size="sm"),
                                ]),
                                dmc.Badge(DashIconify(icon="mdi:circle", width=8), color="green", size="sm", radius="xl"),
                            ],
                        ),
                        dmc.Divider(),
                        dmc.Group(
                            justify="space-between",
                            children=[
                                dmc.Group(gap="xs", children=[
                                    DashIconify(icon="mdi:circle", width=10, color="#51cf66"),
                                    dmc.Text("Account Active", size="sm"),
                                ]),
                                dmc.Badge("Online", color="green", variant="light", size="sm"),
                            ],
                        ),
                        dmc.Divider(),
                        dmc.Group(
                            justify="space-between",
                            children=[
                                dmc.Group(gap="xs", children=[
                                    DashIconify(icon="mdi:lock-outline", width=14),
                                    dmc.Text("2FA", size="sm"),
                                ]),
                                dmc.Text("Not enabled", size="sm", c="dimmed"),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    )


def _quick_actions_card() -> dmc.Card:
    actions = [
        {"icon": "mdi:chart-areaspline", "label": "Predictions", "desc": "View today's picks", "href": "/predictions"},
        {"icon": "mdi:storefront-outline", "label": "Marketplace", "desc": "Browse expert cappers", "href": "/marketplace"},
        {"icon": "mdi:cog-outline", "label": "Settings",    "desc": "Account preferences",  "href": "/settings"},
        {"icon": "mdi:chat-outline", "label": "Discord",      "desc": "Connect account",       "href": "/help"},
    ]
    return dmc.Card(
        withBorder=True,
        radius="md",
        p="lg",
        h="100%",
        children=dmc.Stack(
            gap="md",
            children=[
                dmc.Group(
                    gap="xs",
                    children=[
                        DashIconify(icon="mdi:lightning-bolt", width=20),
                        dmc.Stack(
                            gap=0,
                            children=[
                                dmc.Text("Quick Actions", fw=600, size="md"),
                                dmc.Text("Navigate quickly", size="xs", c="dimmed"),
                            ],
                        ),
                    ],
                ),
                dmc.Stack(
                    gap=4,
                    children=[
                        dmc.NavLink(
                            label=dmc.Group(
                                gap="sm",
                                children=[
                                    DashIconify(icon=a["icon"], width=16),
                                    dmc.Stack(
                                        gap=0,
                                        children=[
                                            dmc.Text(a["label"], size="sm", fw=500),
                                            dmc.Text(a["desc"], size="xs", c="dimmed"),
                                        ],
                                    ),
                                ],
                            ),
                            href=a["href"],
                            style={"borderRadius": "8px"},
                        )
                        for a in actions
                    ],
                ),
            ],
        ),
    )


def _referral_card() -> dmc.Card:
    return dmc.Card(
        withBorder=True,
        radius="md",
        p="lg",
        children=dmc.Stack(
            gap="md",
            children=[
                dmc.Group(
                    gap="xs",
                    children=[
                        DashIconify(icon="mdi:gift-outline", width=20),
                        dmc.Stack(
                            gap=0,
                            children=[
                                dmc.Text("Referral Program", fw=600, size="md"),
                                dmc.Text("Earn rewards by inviting friends", size="xs", c="dimmed"),
                            ],
                        ),
                    ],
                ),
                dmc.Text(
                    "Share your code and earn when friends subscribe!",
                    size="sm",
                    c="dimmed",
                ),
                dmc.Group(
                    gap="sm",
                    children=[
                        dmc.Code(
                            USER["referral_code"],
                            style={
                                "fontSize": "1rem",
                                "padding": "8px 16px",
                                "color": "#51cf66",
                                "flex": 1,
                                "letterSpacing": "0.05em",
                            },
                        ),
                        dmc.Button("Copy", variant="default", radius="md", size="sm", leftSection=DashIconify(icon="mdi:content-copy", width=14)),
                    ],
                ),
                dmc.SimpleGrid(
                    cols=2,
                    children=[
                        dmc.Stack(
                            align="center",
                            gap=2,
                            children=[
                                dmc.Text("0", size="2rem", fw=800),
                                dmc.Text("FRIENDS INVITED", size="xs", c="dimmed", fw=500),
                            ],
                        ),
                        dmc.Stack(
                            align="center",
                            gap=2,
                            children=[
                                dmc.Text("$0.00", size="2rem", fw=800, c="green"),
                                dmc.Text("TOTAL EARNED", size="xs", c="dimmed", fw=500),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    )


def _recent_activity_card() -> dmc.Card:
    return dmc.Card(
        withBorder=True,
        radius="md",
        p="lg",
        children=dmc.Stack(
            gap="md",
            children=[
                dmc.Group(
                    gap="xs",
                    children=[
                        DashIconify(icon="mdi:clock-outline", width=20),
                        dmc.Stack(
                            gap=0,
                            children=[
                                dmc.Text("Recent Activity", fw=600, size="md"),
                                dmc.Text("Your latest actions", size="xs", c="dimmed"),
                            ],
                        ),
                    ],
                ),
                dmc.Card(
                    withBorder=True,
                    radius="md",
                    p="sm",
                    children=dmc.Group(
                        gap="sm",
                        children=[
                            DashIconify(icon="mdi:check-bold", width=16, color="#51cf66"),
                            dmc.Stack(
                                gap=0,
                                children=[
                                    dmc.Text("Logged in", size="sm", fw=500),
                                    dmc.Text("Just now", size="xs", c="dimmed"),
                                ],
                            ),
                        ],
                    ),
                ),
                dmc.Card(
                    withBorder=True,
                    radius="md",
                    p="sm",
                    children=dmc.Group(
                        gap="sm",
                        children=[
                            DashIconify(icon="mdi:eye-outline", width=16),
                            dmc.Stack(
                                gap=0,
                                children=[
                                    dmc.Text("Viewed Free Pick", size="sm", fw=500),
                                    dmc.Text("2 minutes ago", size="xs", c="dimmed"),
                                ],
                            ),
                        ],
                    ),
                ),
            ],
        ),
    )


# ---------------------------------------------------------------------------
# Page layout
# ---------------------------------------------------------------------------


def layout() -> dmc.Container:
    """Render the user profile / dashboard page."""
    return dmc.Container(
        fluid=True,
        children=[
            _profile_header(),
            _stat_cards(),
            # Main 3-column grid: Subscription | Account Status | Quick Actions
            dmc.SimpleGrid(
                cols={"base": 1, "sm": 3},
                mb="xl",
                children=[
                    _subscription_card(),
                    _account_status_card(),
                    _quick_actions_card(),
                ],
            ),
            # Referral + Recent Activity
            dmc.SimpleGrid(
                cols={"base": 1, "sm": 2},
                children=[
                    _referral_card(),
                    _recent_activity_card(),
                ],
            ),
        ],
    )

