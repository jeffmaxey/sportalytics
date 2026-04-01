import dash
import dash_mantine_components as dmc
from dash import Input, Output, State, callback, html

from sportalytics.services.calculators import (
    calculate_arbitrage,
    calculate_ev,
    convert_odds,
)

dash.register_page(__name__, path="/calculators", title="Calculators", name="Calculators")


def arb_panel():
    return dmc.Stack(
        gap="md",
        children=[
            dmc.Title("Arbitrage Calculator", order=4),
            dmc.Text(
                "Enter American odds for both sides of a bet to check for arbitrage.",
                size="sm",
                c="dimmed",
            ),
            dmc.Group(
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
                ]
            ),
            dmc.Button("Calculate", id="arb-calc-btn", color="blue"),
            html.Div(id="arb-result"),
        ],
    )


def ev_panel():
    return dmc.Stack(
        gap="md",
        children=[
            dmc.Title("Expected Value Calculator", order=4),
            dmc.Text(
                "Calculate the expected value of a bet given your estimated win probability.",
                size="sm",
                c="dimmed",
            ),
            dmc.Group(
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
                ]
            ),
            dmc.Button("Calculate", id="ev-calc-btn", color="blue"),
            html.Div(id="ev-result"),
        ],
    )


def converter_panel():
    return dmc.Stack(
        gap="md",
        children=[
            dmc.Title("Odds Converter", order=4),
            dmc.Text(
                "Convert odds between American, Decimal, and Implied Probability formats.",
                size="sm",
                c="dimmed",
            ),
            dmc.Group(
                align="flex-end",
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
                            {"value": "decimal", "label": "Decimal"},
                            {"value": "implied", "label": "Implied Probability (%)"},
                        ],
                        value="american",
                        w=220,
                    ),
                    dmc.Button("Convert", id="conv-calc-btn", color="blue"),
                ],
            ),
            html.Div(id="conv-result"),
        ],
    )


def layout():
    return dmc.Container(
        fluid=True,
        children=[
            dmc.Title("Betting Calculators", order=2, mb="md"),
            dmc.Tabs(
                value="arb",
                children=[
                    dmc.TabsList(
                        children=[
                            dmc.TabsTab("Arbitrage", value="arb"),
                            dmc.TabsTab("Expected Value", value="ev"),
                            dmc.TabsTab("Odds Converter", value="converter"),
                        ]
                    ),
                    dmc.TabsPanel(arb_panel(), value="arb", pt="md"),
                    dmc.TabsPanel(ev_panel(), value="ev", pt="md"),
                    dmc.TabsPanel(converter_panel(), value="converter", pt="md"),
                ],
            ),
        ],
    )


@callback(
    Output("arb-result", "children"),
    Input("arb-calc-btn", "n_clicks"),
    State("arb-odds1", "value"),
    State("arb-odds2", "value"),
    State("arb-stake", "value"),
    prevent_initial_call=True,
)
def calculate_arb(n_clicks, odds1, odds2, stake):
    if odds1 is None or odds2 is None:
        return dmc.Alert("Please enter valid odds.", color="red")
    try:
        result = calculate_arbitrage(float(odds1), float(odds2))
        arb_text = (
            f"{result['arb_pct']:.2f}%"
            if result["has_arb"]
            else f"{abs(result['arb_pct']):.2f}% over"
        )
        color = "green" if result["has_arb"] else "red"
        return dmc.Alert(
            dmc.Stack(
                gap="xs",
                children=[
                    dmc.Text(
                        "✅ Arbitrage Opportunity!" if result["has_arb"] else "❌ No Arbitrage",
                        fw=700,
                    ),
                    dmc.Text(f"Total Implied Probability: {result['total_implied']:.2f}%"),
                    dmc.Text(f"Arb Margin: {arb_text}"),
                    dmc.Text(f"Side 1 Implied: {result['prob1']:.2f}%"),
                    dmc.Text(f"Side 2 Implied: {result['prob2']:.2f}%"),
                ],
            ),
            color=color,
        )
    except Exception as e:
        return dmc.Alert(f"Error: {e}", color="red")


@callback(
    Output("ev-result", "children"),
    Input("ev-calc-btn", "n_clicks"),
    State("ev-odds", "value"),
    State("ev-prob", "value"),
    State("ev-stake", "value"),
    prevent_initial_call=True,
)
def calculate_ev_callback(n_clicks, odds, prob_pct, stake):
    if odds is None or prob_pct is None or stake is None:
        return dmc.Alert("Please fill all fields.", color="red")
    try:
        win_prob = float(prob_pct) / 100
        result = calculate_ev(float(odds), win_prob, float(stake))
        color = "green" if result["ev"] >= 0 else "red"
        return dmc.Alert(
            dmc.Stack(
                gap="xs",
                children=[
                    dmc.Text(f"Expected Value: ${result['ev']:.2f}", fw=700),
                    dmc.Text(f"Potential Payout: ${result['payout']:.2f}"),
                    dmc.Text(f"ROI: {result['roi_pct']:.2f}%"),
                    dmc.Text(
                        "✅ Positive EV bet!" if result["ev"] >= 0 else "❌ Negative EV bet",
                        fw=600,
                    ),
                ],
            ),
            color=color,
        )
    except Exception as e:
        return dmc.Alert(f"Error: {e}", color="red")


@callback(
    Output("conv-result", "children"),
    Input("conv-calc-btn", "n_clicks"),
    State("conv-value", "value"),
    State("conv-format", "value"),
    prevent_initial_call=True,
)
def convert_odds_callback(n_clicks, value, fmt):
    if value is None:
        return dmc.Alert("Please enter a value.", color="red")
    try:
        result = convert_odds(float(value), fmt)
        american_val = result["american"]
        if american_val == round(american_val):
            american_str = f"{int(american_val):+d}"
        else:
            american_str = f"{american_val:+.2f}"
        return dmc.Card(
            withBorder=True,
            radius="md",
            mt="sm",
            children=[
                dmc.Title("Converted Odds", order=5, mb="sm"),
                dmc.Table(
                    data={
                        "head": ["Format", "Value"],
                        "body": [
                            ["American", american_str],
                            ["Decimal", f"{result['decimal']:.4f}"],
                            ["Fractional", result["fractional"]],
                            ["Implied Probability", f"{result['implied']:.2f}%"],
                        ],
                    }
                ),
            ],
        )
    except Exception as e:
        return dmc.Alert(f"Error: {e}", color="red")
