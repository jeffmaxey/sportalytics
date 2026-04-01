import dash
import dash_mantine_components as dmc

from sportalytics.services.odds_insight import SPORTSBOOKS, get_odds_comparison

dash.register_page(__name__, path="/odds-insight", title="Odds Insight", name="Odds Insight")


def odds_table(game: dict) -> dmc.Card:
    books = list(game["lines"].keys())
    home_vals = [game["lines"][b]["home"] for b in books]
    away_vals = [game["lines"][b]["away"] for b in books]
    best_home_val = max(home_vals)
    best_away_val = max(away_vals)
    rows = []
    for book in books:
        h = game["lines"][book]["home"]
        a = game["lines"][book]["away"]
        rows.append([
            book,
            dmc.Text(str(h), c="green" if h == best_home_val else None),
            dmc.Text(str(a), c="green" if a == best_away_val else None),
        ])
    return dmc.Card(
        withBorder=True,
        radius="md",
        mb="lg",
        children=[
            dmc.Group(
                justify="space-between",
                mb="sm",
                children=[
                    dmc.Text(game["matchup"], fw=700),
                    dmc.Badge(game["market"].upper(), variant="light"),
                ],
            ),
            dmc.Table(
                data={
                    "head": ["Sportsbook", "Home", "Away"],
                    "body": rows,
                }
            ),
        ],
    )


def layout():
    games = get_odds_comparison()
    return dmc.Container(
        fluid=True,
        children=[
            dmc.Title("Odds Insight", order=2, mb="md"),
            dmc.Text(f"Comparing {len(SPORTSBOOKS)} sportsbooks in real-time", c="dimmed", mb="lg"),
            *[odds_table(g) for g in games],
        ],
    )
