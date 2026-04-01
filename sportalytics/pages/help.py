"""
Help Center page for Sportalytics.

FAQ accordion, topic browsing, contact support channels, and quick
navigation links — mirroring the WiseSportsAI Help Center layout.
"""

import dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify

dash.register_page(__name__, path="/help", title="Help Center", name="Help")

# ---------------------------------------------------------------------------
# Content data
# ---------------------------------------------------------------------------

POPULAR_FAQS = [
    {
        "q": "What is the Free Pick of the Day?",
        "a": (
            "The Free Pick of the Day is a single AI-generated prediction published every morning. "
            "It includes the matchup, our recommended selection, a confidence score, and the model's "
            "rationale. It resets at midnight ET. No account required to view it."
        ),
    },
    {
        "q": "Why is my prediction locked?",
        "a": (
            "Full AI prediction access (50+ daily picks, player props, and deep analytics) requires "
            "a Pro subscription. Free accounts receive one pick per day. Upgrade to Pro to unlock "
            "everything."
        ),
    },
    {
        "q": "How accurate are the predictions?",
        "a": (
            "Our models currently track a 53.6% win rate across all sports with +1.67 units per pick "
            "on a flat-betting basis. Accuracy varies by sport and confidence tier — Tier A picks "
            "historically perform best. Check the Model Tracker page for full transparency."
        ),
    },
    {
        "q": "How do I upgrade to Pro?",
        "a": (
            "Click the 'Upgrade' button in the sidebar or visit the Profile page. "
            "Pro is $29/month and includes 50+ daily AI picks, player props, live totals, "
            "and priority support. Cancel anytime."
        ),
    },
]

TOPICS = [
    {"icon": "mdi:rocket-outline", "title": "Getting Started",    "desc": "Learn the basics",              "count": 4, "color": "green"},
    {"icon": "mdi:lightning-bolt", "title": "Features & Tools",   "desc": "Understand our predictions",    "count": 4, "color": "blue"},
    {"icon": "mdi:credit-card-outline", "title": "Billing & Plans",    "desc": "Payments & subscriptions",      "count": 4, "color": "orange"},
    {"icon": "mdi:shield-lock-outline", "title": "Account & Security", "desc": "Settings & privacy",            "count": 4, "color": "red"},
]

QUICK_LINKS = [
    {"icon": "mdi:gift-outline", "label": "Free Pick",    "href": "/free-pick"},
    {"icon": "mdi:robot-outline", "label": "Predictions",  "href": "/predictions"},
    {"icon": "mdi:chart-areaspline", "label": "Insights",     "href": "/odds-insight"},
    {"icon": "mdi:calculator-variant-outline", "label": "Tools",        "href": "/calculators"},
    {"icon": "mdi:storefront-outline", "label": "Marketplace",  "href": "/marketplace"},
    {"icon": "mdi:account-outline", "label": "Profile",      "href": "/profile"},
]


# ---------------------------------------------------------------------------
# Section builders
# ---------------------------------------------------------------------------


def _page_header() -> dmc.Group:
    return dmc.Group(
        mb="xl",
        justify="space-between",
        wrap="wrap",
        gap="md",
        children=[
            dmc.Group(
                gap="md",
                children=[
                    dmc.Avatar(DashIconify(icon="mdi:help-circle-outline", width=20), size="lg", radius="md", color="green"),
                    dmc.Stack(
                        gap=2,
                        children=[
                            dmc.Title("Help Center", order=2),
                            dmc.Text("Find answers & get support", size="sm", c="dimmed"),
                        ],
                    ),
                ],
            ),
            dmc.Group(
                gap="sm",
                children=[
                    dmc.Badge([DashIconify(icon="mdi:file-document-outline", width=14), " 16+ Articles"], color="blue", variant="light", size="lg", radius="md"),
                    dmc.Badge([DashIconify(icon="mdi:tools", width=14), " 6 Free Tools"], color="teal", variant="light", size="lg", radius="md"),
                    dmc.Badge([DashIconify(icon="mdi:chat-outline", width=14), " 24/7 Support"], color="green", variant="filled", size="lg", radius="md"),
                ],
            ),
        ],
    )


def _search_section() -> dmc.TextInput:
    return dmc.TextInput(
        placeholder="Search help articles...",
        size="lg",
        radius="md",
        mb="xl",
        leftSection=DashIconify(icon="mdi:magnify", width=16),
        style={"maxWidth": 600},
    )


def _popular_section() -> dmc.Stack:
    return dmc.Stack(
        gap="md",
        mb="xl",
        children=[
            dmc.Group(
                gap="sm",
                children=[
                    dmc.Badge([DashIconify(icon="mdi:fire", width=14), " Popular 4"], color="orange", variant="light", size="md"),
                    dmc.Text("Most frequently asked", size="sm", c="dimmed"),
                ],
            ),
            dmc.Accordion(
                multiple=True,
                children=[
                    dmc.AccordionItem(
                        value=f"faq-{i}",
                        children=[
                            dmc.AccordionControl(
                                faq["q"],
                                style={"fontWeight": 500},
                            ),
                            dmc.AccordionPanel(
                                dmc.Text(faq["a"], size="sm", c="dimmed"),
                            ),
                        ],
                    )
                    for i, faq in enumerate(POPULAR_FAQS)
                ],
            ),
        ],
    )


def _topics_section() -> dmc.Stack:
    return dmc.Stack(
        gap="md",
        mb="xl",
        children=[
            dmc.Group(
                gap="sm",
                children=[
                    dmc.Badge([DashIconify(icon="mdi:book-open-page-variant-outline", width=14), " Browse Topics 4"], color="blue", variant="light", size="md"),
                ],
            ),
            dmc.SimpleGrid(
                cols={"base": 1, "sm": 2, "lg": 4},
                children=[
                    dmc.Card(
                        withBorder=True,
                        radius="md",
                        p="lg",
                        style={"cursor": "pointer"},
                        children=dmc.Group(
                            justify="space-between",
                            children=[
                                dmc.Group(
                                    gap="md",
                                    children=[
                                        dmc.Avatar(
                                            DashIconify(icon=t["icon"], width=18),
                                            size="md",
                                            radius="md",
                                            color=t["color"],
                                        ),
                                        dmc.Stack(
                                            gap=0,
                                            children=[
                                                dmc.Text(t["title"], fw=600, size="sm"),
                                                dmc.Text(t["desc"], size="xs", c="dimmed"),
                                            ],
                                        ),
                                    ],
                                ),
                                dmc.Group(
                                    gap="xs",
                                    children=[
                                        dmc.Badge(str(t["count"]), color="gray", variant="light", size="sm"),
                                        DashIconify(icon="mdi:chevron-right", width=18, color="#868e96"),
                                    ],
                                ),
                            ],
                        ),
                    )
                    for t in TOPICS
                ],
            ),
        ],
    )


def _contact_section() -> dmc.Stack:
    return dmc.Stack(
        gap="md",
        mb="xl",
        children=[
            dmc.Group(
                gap="sm",
                children=[
                    dmc.Badge([DashIconify(icon="mdi:chat-outline", width=14), " Contact Support"], color="green", variant="light", size="md"),
                    dmc.Text("Get help from our team", size="sm", c="dimmed"),
                ],
            ),
            dmc.SimpleGrid(
                cols={"base": 1, "sm": 2},
                children=[
                    # Discord
                    dmc.Card(
                        withBorder=True,
                        radius="md",
                        p="lg",
                        style={"borderLeft": "3px solid #5865F2"},
                        children=dmc.Group(
                            justify="space-between",
                            children=[
                                dmc.Group(
                                    gap="md",
                                    children=[
                                        dmc.Avatar(DashIconify(icon="mdi:chat-outline", width=16), size="md", radius="md", color="blue"),
                                        dmc.Stack(
                                            gap=2,
                                            children=[
                                                dmc.Group(
                                                    gap="sm",
                                                    children=[
                                                        dmc.Text("Discord Community", fw=600),
                                                        dmc.Badge("Fastest", color="green", variant="filled", size="xs"),
                                                    ],
                                                ),
                                                dmc.Text("Instant help from community & team", size="xs", c="dimmed"),
                                            ],
                                        ),
                                    ],
                                ),
                                dmc.Button("Join ↗", size="sm", color="blue", variant="light", radius="md"),
                            ],
                        ),
                    ),
                    # Email
                    dmc.Card(
                        withBorder=True,
                        radius="md",
                        p="lg",
                        style={"borderLeft": "3px solid #51cf66"},
                        children=dmc.Group(
                            justify="space-between",
                            children=[
                                dmc.Group(
                                    gap="md",
                                    children=[
                                        dmc.Avatar(DashIconify(icon="mdi:email-outline", width=16), size="md", radius="md", color="green"),
                                        dmc.Stack(
                                            gap=2,
                                            children=[
                                                dmc.Text("Email Support", fw=600),
                                                dmc.Text("We respond within 24 hours", size="xs", c="dimmed"),
                                            ],
                                        ),
                                    ],
                                ),
                                dmc.Button("Send ↗", size="sm", color="green", variant="light", radius="md"),
                            ],
                        ),
                    ),
                ],
            ),
        ],
    )


def _quick_links_section() -> dmc.Stack:
    return dmc.Stack(
        gap="md",
        children=[
            dmc.Group(
                gap="sm",
                children=[
                    dmc.Badge([DashIconify(icon="mdi:link-variant", width=14), " Quick Links"], color="gray", variant="light", size="md"),
                ],
            ),
            dmc.SimpleGrid(
                cols={"base": 2, "sm": 3, "lg": 6},
                children=[
                    dmc.Anchor(
                        href=link["href"],
                        style={"textDecoration": "none"},
                        children=dmc.Card(
                            withBorder=True,
                            radius="md",
                            p="lg",
                            style={"textAlign": "center"},
                            children=dmc.Stack(
                                align="center",
                                gap="xs",
                                children=[
                                    DashIconify(icon=link["icon"], width=28),
                                    dmc.Text(link["label"], size="sm", fw=500),
                                ],
                            ),
                        ),
                    )
                    for link in QUICK_LINKS
                ],
            ),
        ],
    )


# ---------------------------------------------------------------------------
# Page layout
# ---------------------------------------------------------------------------


def layout() -> dmc.Container:
    """Render the Help Center page."""
    return dmc.Container(
        fluid=True,
        children=[
            _page_header(),
            _search_section(),
            _popular_section(),
            _topics_section(),
            _contact_section(),
            _quick_links_section(),
            # Footer
            dmc.Group(
                justify="space-between",
                mt="xl",
                pt="lg",
                children=[
                    dmc.Group(gap="sm", children=[
                        DashIconify(icon="mdi:lightning-bolt", width=14, color="#868e96"),
                        dmc.Text("Sportalytics", size="sm", c="dimmed"),
                        dmc.Text("Available 24/7", size="sm", c="dimmed"),
                    ]),
                    dmc.Text("16+ articles", size="sm", c="dimmed"),
                ],
            ),
        ],
    )

