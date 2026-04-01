"""
Betting Calculators page for Sportalytics.

Provides three interactive tools in a tabbed layout:

* **Arbitrage** — checks two American odds for an arb opportunity and
  computes optimal stake splits.
* **Expected Value** — estimates EV given win probability and stake.
* **Odds Converter** — converts between American, decimal, fractional,
  and implied-probability formats.

All calculator logic lives in :mod:`sportalytics.services.calculators`.
"""

import dash
import dash_mantine_components as dmc
from dash import Input, Output, State, callback, html
from dash_iconify import DashIconify

from sportalytics.components import page_header, section_title, styled_table
from sportalytics.services.calculators import (
    calculate_arbitrage,
    calculate_ev,
    convert_odds,
)

dash.register_page(__name__, path="/calculators", title="Calculators", name="Calculators")

# ---------------------------------------------------------------------------
# Panel builders
# ---------------------------------------------------------------------------


def arb_panel() -> dmc.Stack:
    """
    Build the Arbitrage Calculator input panel.

    Returns
    -------
    dmc.Stack
        A vertical stack containing two odds inputs, a total stake
        input, a calculate button, and a result placeholder ``html.Div``.
    """
    return dmc.Stack(
        gap="md",
        children=[
            section_title("Arbitrage Calculator", order=4, mt="xs"),
            dmc.Text(
                "Enter American odds for both sides to check for an arbitrage opportunity.",
                size="sm",
                c="dimmed",
            ),
            dmc.Group(
                gap="sm",
                wrap="wrap",
                children=[
                    dmc.NumberInput(
                        id="arb-odds1",
                        label="Side 1 Odds (American)",
                        placeholder="-110",
                        value=-110,
                        w=200,
                    ),
                    dmc.NumberInput(
                        id="arb-odds2",
                        label="Side 2 Odds (American)",
                        placeholder="-110",
                        value=-110,
                        w=200,
                    ),
                    dmc.NumberInput(
                        id="arb-stake",
                        label="Total Stake ($)",
                        placeholder="100",
                        value=100,
                        min=1,
                        w=200,
                    ),
                ],
            ),
            dmc.Button("Calculate", id="arb-calc-btn", color="blue", radius="md"),
            html.Div(id="arb-result"),
        ],
    )


def ev_panel() -> dmc.Stack:
    """
    Build the Expected Value Calculator input panel.

    Returns
    -------
    dmc.Stack
        A vertical stack containing odds, win-probability, and stake
        inputs, a calculate button, and a result placeholder ``html.Div``.
    """
    return dmc.Stack(
        gap="md",
        children=[
            section_title("Expected Value Calculator", order=4, mt="xs"),
            dmc.Text(
                "Calculate the expected value of a bet given your estimated win probability.",
                size="sm",
                c="dimmed",
            ),
            dmc.Group(
                gap="sm",
                wrap="wrap",
                children=[
                    dmc.NumberInput(
                        id="ev-odds",
                        label="Odds (American)",
                        placeholder="-110",
                        value=-110,
                        w=200,
                    ),
                    dmc.NumberInput(
                        id="ev-prob",
                        label="Win Probability (%)",
                        placeholder="55",
                        value=55,
                        min=1,
                        max=99,
                        w=200,
                    ),
                    dmc.NumberInput(
                        id="ev-stake",
                        label="Stake ($)",
                        placeholder="100",
                        value=100,
                        min=1,
                        w=200,
                    ),
                ],
            ),
            dmc.Button("Calculate", id="ev-calc-btn", color="blue", radius="md"),
            html.Div(id="ev-result"),
        ],
    )


def converter_panel() -> dmc.Stack:
    """
    Build the Odds Converter input panel.

    Returns
    -------
    dmc.Stack
        A vertical stack containing a numeric odds input, a source-format
        selector, a convert button, and a result placeholder ``html.Div``.
    """
    return dmc.Stack(
        gap="md",
        children=[
            section_title("Odds Converter", order=4, mt="xs"),
            dmc.Text(
                "Convert odds between American, Decimal, and Implied Probability formats.",
                size="sm",
                c="dimmed",
            ),
            dmc.Group(
                gap="sm",
                align="flex-end",
                wrap="wrap",
                children=[
                    dmc.NumberInput(
                        id="conv-value",
                        label="Odds Value",
                        placeholder="-110",
                        value=-110,
                        w=200,
                    ),
                    dmc.Select(
                        id="conv-format",
                        label="From Format",
                        data=[
                            {"value": "american", "label": "American"},
                            {"value": "decimal",  "label": "Decimal"},
                            {"value": "implied",  "label": "Implied Probability (%)"},
                        ],
                        value="american",
                        w=220,
                    ),
                    dmc.Button("Convert", id="conv-calc-btn", color="blue", radius="md"),
                ],
            ),
            html.Div(id="conv-result"),
        ],
    )


# ---------------------------------------------------------------------------
# Page layout
# ---------------------------------------------------------------------------


def layout() -> dmc.Container:
    """
    Render the Betting Calculators page layout.

    Returns
    -------
    dmc.Container
        A fluid container with a page header and a :class:`dmc.Tabs`
        component containing three panels: Arbitrage, Expected Value,
        and Odds Converter.
    """
    return dmc.Container(
        fluid=True,
        children=[
            page_header(
                "Betting Calculators",
                subtitle="Arbitrage detection, expected value, and odds conversion tools",
            ),
            dmc.Tabs(
                value="arb",
                children=[
                    dmc.TabsList(
                        children=[
                            dmc.TabsTab("Arbitrage",       value="arb"),
                            dmc.TabsTab("Expected Value",  value="ev"),
                            dmc.TabsTab("Odds Converter",  value="converter"),
                        ]
                    ),
                    dmc.TabsPanel(arb_panel(),       value="arb",       pt="md"),
                    dmc.TabsPanel(ev_panel(),        value="ev",        pt="md"),
                    dmc.TabsPanel(converter_panel(), value="converter", pt="md"),
                ],
            ),
        ],
    )


# ---------------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------------


@callback(
    Output("arb-result", "children"),
    Input("arb-calc-btn", "n_clicks"),
    State("arb-odds1", "value"),
    State("arb-odds2", "value"),
    State("arb-stake", "value"),
    prevent_initial_call=True,
)
def calculate_arb(
    n_clicks: int,
    odds1: float | None,
    odds2: float | None,
    stake: float | None,
):
    """
    Compute arbitrage opportunity and render the result.

    Parameters
    ----------
    n_clicks : int
        Number of times the Calculate button has been clicked.
    odds1 : float or None
        American odds for side 1.
    odds2 : float or None
        American odds for side 2.
    stake : float or None
        Total stake in USD.

    Returns
    -------
    dmc.Alert
        A green alert if an arb exists, red if not, or an error message
        if inputs are invalid.
    """
    if odds1 is None or odds2 is None:
        return dmc.Alert("Please enter valid odds for both sides.", color="red")
    try:
        result = calculate_arbitrage(float(odds1), float(odds2))
        arb_text = (
            f"{result['arb_pct']:.2f}%"
            if result["has_arb"]
            else f"{abs(result['arb_pct']):.2f}% over"
        )
        color = "teal" if result["has_arb"] else "red"
        return dmc.Alert(
            dmc.Stack(
                gap="xs",
                children=[
                    dmc.Group(
                        gap="xs",
                        children=[
                            DashIconify(
                                icon="mdi:check-circle-outline" if result["has_arb"] else "mdi:close-circle-outline",
                                width=16,
                                color="#12b886" if result["has_arb"] else "#fa5252",
                            ),
                            dmc.Text("Arbitrage Opportunity!" if result["has_arb"] else "No Arbitrage", fw=700),
                        ],
                    ),
                    dmc.Text(f"Total Implied Probability: {result['total_implied']:.2f}%"),
                    dmc.Text(f"Arb Margin: {arb_text}"),
                    dmc.Text(f"Side 1 Implied: {result['prob1']:.2f}%"),
                    dmc.Text(f"Side 2 Implied: {result['prob2']:.2f}%"),
                ],
            ),
            color=color,
        )
    except Exception as exc:
        return dmc.Alert(f"Error: {exc}", color="red")


@callback(
    Output("ev-result", "children"),
    Input("ev-calc-btn", "n_clicks"),
    State("ev-odds", "value"),
    State("ev-prob", "value"),
    State("ev-stake", "value"),
    prevent_initial_call=True,
)
def calculate_ev_callback(
    n_clicks: int,
    odds: float | None,
    prob_pct: float | None,
    stake: float | None,
):
    """
    Compute expected value and render the result.

    Parameters
    ----------
    n_clicks : int
        Number of times the Calculate button has been clicked.
    odds : float or None
        American odds.
    prob_pct : float or None
        Estimated win probability as a percentage (e.g. ``55`` for 55 %).
    stake : float or None
        Bet stake in USD.

    Returns
    -------
    dmc.Alert
        A teal alert for positive EV, red for negative EV, or an error
        message if inputs are invalid.
    """
    if odds is None or prob_pct is None or stake is None:
        return dmc.Alert("Please fill all fields.", color="red")
    try:
        win_prob = float(prob_pct) / 100
        result = calculate_ev(float(odds), win_prob, float(stake))
        color = "teal" if result["ev"] >= 0 else "red"
        return dmc.Alert(
            dmc.Stack(
                gap="xs",
                children=[
                    dmc.Text(f"Expected Value: ${result['ev']:.2f}", fw=700),
                    dmc.Text(f"Potential Payout: ${result['payout']:.2f}"),
                    dmc.Text(f"ROI: {result['roi_pct']:.2f}%"),
                    dmc.Group(
                        gap="xs",
                        children=[
                            DashIconify(
                                icon="mdi:check-circle-outline" if result["ev"] >= 0 else "mdi:close-circle-outline",
                                width=16,
                                color="#12b886" if result["ev"] >= 0 else "#fa5252",
                            ),
                            dmc.Text("Positive EV bet!" if result["ev"] >= 0 else "Negative EV bet", fw=600),
                        ],
                    ),
                ],
            ),
            color=color,
        )
    except Exception as exc:
        return dmc.Alert(f"Error: {exc}", color="red")


@callback(
    Output("conv-result", "children"),
    Input("conv-calc-btn", "n_clicks"),
    State("conv-value", "value"),
    State("conv-format", "value"),
    prevent_initial_call=True,
)
def convert_odds_callback(
    n_clicks: int,
    value: float | None,
    fmt: str | None,
):
    """
    Convert odds from the selected format and render all equivalent values.

    Parameters
    ----------
    n_clicks : int
        Number of times the Convert button has been clicked.
    value : float or None
        Odds value in the source format.
    fmt : str or None
        Source format: ``'american'``, ``'decimal'``, or ``'implied'``.

    Returns
    -------
    dmc.Card or dmc.Alert
        A bordered card containing a :func:`styled_table` with the
        converted odds in all formats, or a red error alert on failure.
    """
    if value is None:
        return dmc.Alert("Please enter a value.", color="red")
    try:
        result = convert_odds(float(value), fmt)
        american_val = result["american"]
        american_str = (
            f"{int(american_val):+d}"
            if american_val == round(american_val)
            else f"{american_val:+.2f}"
        )
        return dmc.Card(
            withBorder=True,
            radius="md",
            p="lg",
            shadow="sm",
            mt="sm",
            children=[
                section_title("Converted Odds", order=5, mt="xs", mb="sm"),
                styled_table(
                    head=["Format", "Value"],
                    body=[
                        ["American",           american_str],
                        ["Decimal",            f"{result['decimal']:.4f}"],
                        ["Fractional",         result["fractional"]],
                        ["Implied Probability",f"{result['implied']:.2f}%"],
                    ],
                ),
            ],
        )
    except Exception as exc:
        return dmc.Alert(f"Error: {exc}", color="red")
