"""
Reusable UI primitives for Sportalytics.

All visual building-blocks — colour helpers, badges, page scaffolding,
stat grids, metric rows, and domain-specific cards — are defined here
so every page renders with the same design language without duplicating
component trees.

Notes
-----
* Colour props are **never** passed as ``None``.  When a colour
  parameter is falsy the prop is omitted entirely via ``**kwargs``
  spreading, which avoids the Mantine colour-parse error:
  ``"Expected color to be a string, instead got object"``.
* All card components apply ``withBorder=True``, ``radius="md"``,
  ``p="lg"``, and ``shadow="sm"`` for visual consistency.
* Import :data:`PLOTLY_LAYOUT_DEFAULTS` from :mod:`sportalytics.theme`
  in any page that renders a :class:`dcc.Graph`.
"""

from __future__ import annotations

import dash_mantine_components as dmc
from dash_iconify import DashIconify

# ---------------------------------------------------------------------------
# Internal colour lookup tables
# ---------------------------------------------------------------------------

_GRADE_COLORS: dict[str, str] = {
    "A": "green",
    "B": "yellow",
    "C": "orange",
    "D": "red",
}

_RESULT_COLORS: dict[str, str] = {
    "W": "teal",
    "L": "red",
    "P": "yellow",
}

_REC_COLORS: dict[str, str] = {
    "Over": "teal",
    "Under": "red",
}

# ---------------------------------------------------------------------------
# Colour helpers
# ---------------------------------------------------------------------------


def grade_color(grade: str) -> str:
    """
    Return the Mantine colour name for a confidence/grade tier.

    Parameters
    ----------
    grade : str
        Letter grade: ``'A'``, ``'B'``, ``'C'``, or ``'D'``.

    Returns
    -------
    str
        A Mantine named colour string.  Falls back to ``'blue'`` for
        unrecognised grades.

    Examples
    --------
    >>> grade_color("A")
    'green'
    >>> grade_color("D")
    'red'
    >>> grade_color("Z")
    'blue'
    """
    return _GRADE_COLORS.get(grade, "blue")


def result_color(result: str) -> str:
    """
    Return the Mantine colour name for a win/loss result code.

    Parameters
    ----------
    result : str
        Result code: ``'W'`` (win), ``'L'`` (loss), or ``'P'`` (push).

    Returns
    -------
    str
        A Mantine named colour string.  Falls back to ``'gray'`` for
        unrecognised codes.

    Examples
    --------
    >>> result_color("W")
    'teal'
    >>> result_color("L")
    'red'
    """
    return _RESULT_COLORS.get(result, "gray")


def recommendation_color(rec: str) -> str:
    """
    Return the Mantine colour name for a betting recommendation.

    Parameters
    ----------
    rec : str
        Recommendation string, typically ``'Over'`` or ``'Under'``.

    Returns
    -------
    str
        A Mantine named colour string.  Falls back to ``'blue'`` for
        unrecognised values.

    Examples
    --------
    >>> recommendation_color("Over")
    'teal'
    >>> recommendation_color("Under")
    'red'
    """
    return _REC_COLORS.get(rec, "blue")


# ---------------------------------------------------------------------------
# Badge helpers
# ---------------------------------------------------------------------------


def sport_badge(sport: str, **kwargs) -> dmc.Badge:
    """
    Create a standard sport identifier badge.

    Parameters
    ----------
    sport : str
        Sport abbreviation, e.g. ``'NBA'``, ``'NFL'``, ``'UFC'``.
    **kwargs
        Additional keyword arguments forwarded to :class:`dmc.Badge`.

    Returns
    -------
    dmc.Badge
        A blue, light-variant badge displaying the sport abbreviation.

    Examples
    --------
    >>> sport_badge("NBA")
    """
    return dmc.Badge(sport, color="blue", variant="light", radius="sm", **kwargs)


def grade_badge(grade: str, **kwargs) -> dmc.Badge:
    """
    Create a filled, colour-coded grade/confidence badge.

    Parameters
    ----------
    grade : str
        Letter grade: ``'A'``, ``'B'``, ``'C'``, or ``'D'``.
    **kwargs
        Additional keyword arguments forwarded to :class:`dmc.Badge`.

    Returns
    -------
    dmc.Badge
        A filled badge labelled ``'Grade <grade>'`` coloured by tier.

    Examples
    --------
    >>> grade_badge("A")  # green filled badge
    """
    return dmc.Badge(
        f"Grade {grade}",
        color=grade_color(grade),
        variant="filled",
        radius="sm",
        **kwargs,
    )


def tier_badge(tier: str, **kwargs) -> dmc.Badge:
    """
    Create a filled, colour-coded confidence tier badge.

    Parameters
    ----------
    tier : str
        Confidence tier: ``'A'``, ``'B'``, or ``'C'``.
    **kwargs
        Additional keyword arguments forwarded to :class:`dmc.Badge`.

    Returns
    -------
    dmc.Badge
        A filled badge labelled ``'Tier <tier>'`` coloured by tier.

    Examples
    --------
    >>> tier_badge("B")  # yellow filled badge
    """
    return dmc.Badge(
        f"Tier {tier}",
        color=grade_color(tier),
        variant="filled",
        radius="sm",
        **kwargs,
    )


def result_badge(result: str, **kwargs) -> dmc.Badge:
    """
    Create a colour-coded win/loss result badge.

    Parameters
    ----------
    result : str
        Result code: ``'W'``, ``'L'``, or ``'P'``.
    **kwargs
        Additional keyword arguments forwarded to :class:`dmc.Badge`.

    Returns
    -------
    dmc.Badge
        A filled badge coloured by outcome.

    Examples
    --------
    >>> result_badge("W")  # teal filled badge
    >>> result_badge("L")  # red filled badge
    """
    return dmc.Badge(
        result,
        color=result_color(result),
        variant="filled",
        radius="sm",
        **kwargs,
    )


def live_badge(**kwargs) -> dmc.Badge:
    """
    Create a ``● LIVE`` indicator badge.

    Parameters
    ----------
    **kwargs
        Additional keyword arguments forwarded to :class:`dmc.Badge`.

    Returns
    -------
    dmc.Badge
        A red, filled badge labelled ``'● LIVE'``.

    Examples
    --------
    >>> live_badge()
    """
    return dmc.Badge(
        [DashIconify(icon="mdi:circle", width=8), " LIVE"],
        color="red",
        variant="filled",
        radius="sm",
        **kwargs,
    )


# ---------------------------------------------------------------------------
# Layout scaffolding
# ---------------------------------------------------------------------------


def page_header(
    title: str,
    subtitle: str | None = None,
    right_content=None,
) -> dmc.Group:
    """
    Create a standard full-width page header.

    Parameters
    ----------
    title : str
        Primary page heading text.
    subtitle : str, optional
        Dimmed secondary line rendered below the title.
    right_content : dash component, optional
        Component rendered flush-right (e.g. filter controls or buttons).

    Returns
    -------
    dmc.Group
        A horizontally-justified :class:`dmc.Group` with the title stack
        on the left and *right_content* on the right.

    Examples
    --------
    >>> header = page_header(
    ...     "AI Predictions",
    ...     subtitle="Today's ML-graded picks",
    ... )
    """
    title_children: list = [dmc.Title(title, order=2)]
    if subtitle:
        title_children.append(dmc.Text(subtitle, c="dimmed", size="sm", mt=2))

    children = [dmc.Stack(gap=4, children=title_children)]
    if right_content is not None:
        children.append(right_content)

    return dmc.Group(
        justify="space-between",
        align="flex-start",
        mb="lg",
        children=children,
    )


def section_title(
    text: str,
    order: int = 3,
    mt: str = "lg",
    mb: str = "md",
) -> dmc.Title:
    """
    Create a consistently-spaced section sub-heading.

    Parameters
    ----------
    text : str
        Heading text.
    order : int, optional
        HTML heading level (1–6).  Default is ``3``.
    mt : str, optional
        Top-margin Mantine size token.  Default is ``'lg'``.
    mb : str, optional
        Bottom-margin Mantine size token.  Default is ``'md'``.

    Returns
    -------
    dmc.Title
        A :class:`dmc.Title` with consistent surrounding spacing.

    Examples
    --------
    >>> section_title("Performance by Sport")
    """
    return dmc.Title(text, order=order, mt=mt, mb=mb)


# ---------------------------------------------------------------------------
# Stat components
# ---------------------------------------------------------------------------


def stat_card(
    label: str,
    value: str,
    color: str | None = None,
    delta: float | None = None,
    icon: str | None = None,
) -> dmc.Card:
    """
    Create a single KPI stat card.

    Parameters
    ----------
    label : str
        Short descriptor displayed above the value, e.g. ``'Win Rate'``.
    value : str
        Primary metric value as a pre-formatted string.
    color : str, optional
        Mantine named colour applied to the value text.  When ``None``
        the Mantine default (theme foreground) is used.
    delta : float, optional
        Percentage-change figure shown below the value.  Positive values
        render in green, negative in red.
    icon : str, optional
        Unicode emoji or character shown in the top-right corner.

    Returns
    -------
    dmc.Card
        A bordered :class:`dmc.Card` containing the label, value, and
        optional delta / icon elements.

    Examples
    --------
    >>> stat_card("Win Rate", "56.4%", color="green", delta=2.1)
    >>> stat_card("ROI", "4.2%", color="teal", icon="mdi:chart-line")
    """
    value_props = {"c": color} if color else {}

    children: list = [
        dmc.Group(
            justify="space-between",
            mb=4,
            children=[
                dmc.Text(label, size="sm", c="dimmed", fw=500),
                *([dmc.Text(icon, size="md")] if icon else []),
            ],
        ),
        dmc.Text(value, size="xl", fw=700, **value_props),
    ]

    if delta is not None:
        sign = "+" if delta >= 0 else ""
        delta_color = "green" if delta >= 0 else "red"
        children.append(
            dmc.Text(f"{sign}{delta:.1f}%", size="xs", c=delta_color, mt=2)
        )

    return dmc.Card(withBorder=True, radius="md", p="lg", shadow="sm", children=children)


def stat_grid(
    stats: list[dict],
    cols: dict | None = None,
) -> dmc.SimpleGrid:
    """
    Create a responsive grid of :func:`stat_card` components.

    Parameters
    ----------
    stats : list of dict
        Each dict may contain the keys:

        * ``'label'`` *(str, required)* — metric name.
        * ``'value'`` *(str, required)* — pre-formatted metric value.
        * ``'color'`` *(str, optional)* — Mantine colour for the value.
        * ``'delta'`` *(float, optional)* — percentage change.
        * ``'icon'`` *(str, optional)* — emoji / icon character.

    cols : dict, optional
        Responsive column-count mapping accepted by
        :class:`dmc.SimpleGrid`.  Default is ``{'base': 1, 'sm': 4}``.

    Returns
    -------
    dmc.SimpleGrid
        A responsive grid populated with :class:`dmc.Card` stat tiles.

    Examples
    --------
    >>> stat_grid([
    ...     {"label": "Win Rate", "value": "56.4%", "color": "green"},
    ...     {"label": "ROI",      "value": "4.2%",  "color": "teal"},
    ... ])
    """
    if cols is None:
        cols = {"base": 1, "sm": 4}

    return dmc.SimpleGrid(
        cols=cols,
        mb="lg",
        children=[
            stat_card(
                label=s["label"],
                value=s["value"],
                color=s.get("color"),
                delta=s.get("delta"),
                icon=s.get("icon"),
            )
            for s in stats
        ],
    )


# ---------------------------------------------------------------------------
# Metric row
# ---------------------------------------------------------------------------


def metric_row(items: list[dict]) -> dmc.Group:
    """
    Create a horizontal row of label-above-value metric cells.

    Parameters
    ----------
    items : list of dict
        Each dict should contain:

        * ``'label'`` *(str)* — dimmed caption shown above the value.
        * ``'value'`` *(str)* — metric value text.
        * ``'color'`` *(str, optional)* — Mantine colour for the value.

    Returns
    -------
    dmc.Group
        A wrapping :class:`dmc.Group` of two-line stacked cells.

    Examples
    --------
    >>> metric_row([
    ...     {"label": "Prop",  "value": "Points"},
    ...     {"label": "Line",  "value": "25.5"},
    ...     {"label": "Pick",  "value": "Over", "color": "blue"},
    ... ])
    """
    cells = []
    for item in items:
        value_props = {"c": item["color"]} if item.get("color") else {}
        cells.append(
            dmc.Stack(
                gap=2,
                children=[
                    dmc.Text(item["label"], size="xs", c="dimmed"),
                    dmc.Text(str(item["value"]), fw=500, **value_props),
                ],
            )
        )
    return dmc.Group(children=cells, gap="xl", wrap="wrap")


# ---------------------------------------------------------------------------
# Domain cards
# ---------------------------------------------------------------------------


def pick_card(pick: dict) -> dmc.Card:
    """
    Create an AI prediction pick card for the predictions grid.

    Parameters
    ----------
    pick : dict
        Pick data dict with the following keys:

        * ``'sport'`` *(str)* — sport abbreviation.
        * ``'matchup'`` *(str)* — home vs. away team string.
        * ``'selection'`` *(str)* — selected side or total.
        * ``'pick_type'`` *(str)* — ``'spread'``, ``'moneyline'``, etc.
        * ``'line'`` *(float)* — current line value.
        * ``'confidence'`` *(str)* — tier letter: ``'A'``, ``'B'``, ``'C'``.
        * ``'rationale'`` *(str)* — model explanation text.
        * ``'model_version'`` *(str)* — model identifier string.

    Returns
    -------
    dmc.Card
        A bordered card with sport/tier badges, matchup, pick details,
        and rationale.

    Notes
    -----
    The confidence tier is rendered via :func:`tier_badge` which maps
    ``'A'`` → green, ``'B'`` → yellow, ``'C'`` → orange.
    """
    return dmc.Card(
        withBorder=True,
        radius="md",
        p="lg",
        shadow="sm",
        mb="sm",
        children=[
            dmc.Group(
                justify="space-between",
                mb="sm",
                children=[
                    dmc.Group(
                        gap="xs",
                        children=[
                            sport_badge(pick["sport"]),
                            tier_badge(pick["confidence"]),
                        ],
                    ),
                    dmc.Text(pick["model_version"], size="xs", c="dimmed"),
                ],
            ),
            dmc.Text(pick["matchup"], fw=600, size="md", mb=4),
            dmc.Text(
                f"Pick: {pick['selection']}  •  {pick['pick_type'].title()}",
                size="sm",
                mb=2,
            ),
            dmc.Text(f"Line: {pick['line']}", size="sm", c="dimmed", mb="sm"),
            dmc.Divider(mb="sm"),
            dmc.Text(pick["rationale"], size="sm", c="dimmed"),
        ],
    )


def prop_card(prop: dict) -> dmc.Card:
    """
    Create a player prop recommendation card.

    Parameters
    ----------
    prop : dict
        Player prop data dict with the following keys:

        * ``'player_name'`` *(str)* — full player name.
        * ``'team'`` *(str)* — team abbreviation.
        * ``'game'`` *(str)* — matchup string.
        * ``'prop_type'`` *(str)* — stat category, e.g. ``'passing_yards'``.
        * ``'line'`` *(float)* — prop line value.
        * ``'recommendation'`` *(str)* — ``'Over'`` or ``'Under'``.
        * ``'grade'`` *(str)* — quality grade letter.
        * ``'hit_rate_last_10'`` *(float)* — fraction in ``[0, 1]``.

    Returns
    -------
    dmc.Card
        A bordered card with player identity, grade badge, and a
        :func:`metric_row` summarising the key prop statistics.
    """
    return dmc.Card(
        withBorder=True,
        radius="md",
        p="lg",
        shadow="sm",
        mb="sm",
        children=[
            dmc.Group(
                justify="space-between",
                mb=4,
                children=[
                    dmc.Text(prop["player_name"], fw=700, size="md"),
                    grade_badge(prop["grade"]),
                ],
            ),
            dmc.Text(
                f"{prop['team']}  •  {prop['game']}",
                size="sm",
                c="dimmed",
                mb="sm",
            ),
            dmc.Divider(mb="sm"),
            metric_row([
                {"label": "Prop",         "value": prop["prop_type"].replace("_", " ").title()},
                {"label": "Line",         "value": str(prop["line"])},
                {"label": "Pick",         "value": prop["recommendation"], "color": "blue"},
                {"label": "Hit Rate L10", "value": f"{prop['hit_rate_last_10']:.0%}"},
            ]),
        ],
    )


def expert_card(expert: dict) -> dmc.Card:
    """
    Create an expert capper marketplace card.

    Parameters
    ----------
    expert : dict
        Expert data dict with the following keys:

        * ``'display_name'`` *(str)* — public display name.
        * ``'verified'`` *(bool)* — whether the expert is verified.
        * ``'bio'`` *(str)* — short biography.
        * ``'win_rate'`` *(float)* — fraction in ``[0, 1]``.
        * ``'roi'`` *(float)* — return on investment percentage.
        * ``'total_picks'`` *(int)* — total historical picks.
        * ``'monthly_price'`` *(float)* — subscription price in USD.
        * ``'last_5'`` *(list of str)* — list of recent result codes.
        * ``'sports'`` *(list of str)* — covered sport abbreviations.

    Returns
    -------
    dmc.Card
        A bordered card with expert identity, stats, last-5 result
        badges, and sport badges.
    """
    name_children: list = [dmc.Text(expert["display_name"], fw=700, size="md")]
    if expert.get("verified"):
        name_children.append(
            dmc.Badge(
                [DashIconify(icon="mdi:check-circle-outline", width=12), " Verified"],
                color="blue",
                variant="light",
                radius="sm",
                size="sm",
            )
        )

    return dmc.Card(
        withBorder=True,
        radius="md",
        p="lg",
        shadow="sm",
        mb="sm",
        children=[
            dmc.Group(
                justify="space-between",
                mb=4,
                children=[
                    dmc.Group(gap="xs", children=name_children),
                    dmc.Text(f"${expert['monthly_price']:.2f}/mo", fw=700, c="blue"),
                ],
            ),
            dmc.Text(expert["bio"], size="sm", c="dimmed", mt=4, mb="sm"),
            dmc.Divider(mb="sm"),
            metric_row([
                {"label": "Win Rate",    "value": f"{expert['win_rate']:.1%}"},
                {"label": "ROI",         "value": f"{expert['roi']}%", "color": "teal"},
                {"label": "Total Picks", "value": str(expert["total_picks"])},
            ]),
            dmc.Group(
                mt="sm",
                gap=4,
                children=[
                    dmc.Stack(
                        gap=2,
                        children=[
                            dmc.Text("Last 5", size="xs", c="dimmed"),
                            dmc.Group(
                                gap=4,
                                children=[result_badge(r, size="sm") for r in expert["last_5"]],
                            ),
                        ],
                    ),
                ],
            ),
            dmc.Group(
                mt="sm",
                gap="xs",
                children=[sport_badge(s, size="sm") for s in expert["sports"]],
            ),
        ],
    )


def live_game_card(game: dict) -> dmc.Card:
    """
    Create a live game pace-tracking card.

    Parameters
    ----------
    game : dict
        Live game data dict with the following keys:

        * ``'sport'`` *(str)* — sport abbreviation.
        * ``'matchup'`` *(str)* — home vs. away team string.
        * ``'period'`` *(str)* — current period / quarter / half label.
        * ``'time_remaining'`` *(str)* — time remaining in current period.
        * ``'home_score'`` *(int)* — home team score.
        * ``'away_score'`` *(int)* — away team score.
        * ``'current_total'`` *(int)* — combined points scored so far.
        * ``'opening_total'`` *(float)* — opening-line total.
        * ``'current_line'`` *(float)* — current live-line total.
        * ``'projected_total'`` *(float)* — model-projected final total.
        * ``'pace_factor'`` *(float)* — pace multiplier vs. opening.
        * ``'recommendation'`` *(str)* — ``'Over'`` or ``'Under'``.

    Returns
    -------
    dmc.Card
        A bordered card with live indicator, score, pace progress bar,
        and recommendation badge.
    """
    rec_color = recommendation_color(game["recommendation"])
    pace_pct = (
        min((game["current_total"] / game["opening_total"]) * 100, 100)
        if game["opening_total"]
        else 50
    )

    return dmc.Card(
        withBorder=True,
        radius="md",
        p="lg",
        shadow="sm",
        mb="sm",
        children=[
            dmc.Group(
                justify="space-between",
                mb="xs",
                children=[
                    dmc.Group(
                        gap="xs",
                        children=[sport_badge(game["sport"]), live_badge()],
                    ),
                    dmc.Text(
                        f"{game['period']}  •  {game['time_remaining']}",
                        size="sm",
                        c="dimmed",
                    ),
                ],
            ),
            dmc.Text(game["matchup"], fw=700, size="md", mb="xs"),
            metric_row([
                {"label": "Score",     "value": f"{game['home_score']}-{game['away_score']}"},
                {"label": "Current",   "value": f"{game['current_total']} pts"},
                {"label": "Projected", "value": str(game["projected_total"])},
            ]),
            dmc.Group(
                mt="sm",
                mb="xs",
                gap="xs",
                children=[
                    dmc.Text("Line:", size="sm"),
                    dmc.Text(str(game["current_line"]), fw=600, size="sm"),
                    dmc.Badge(
                        game["recommendation"],
                        color=rec_color,
                        variant="filled",
                        radius="sm",
                    ),
                ],
            ),
            dmc.Progress(value=pace_pct, color="blue", size="sm", radius="sm", mb=4),
            dmc.Text(f"Pace Factor: {game['pace_factor']:.2f}×", size="xs", c="dimmed"),
        ],
    )


def odds_table_card(game: dict) -> dmc.Card:
    """
    Create an odds comparison card with colour-highlighted best lines.

    Parameters
    ----------
    game : dict
        Odds data dict with the following keys:

        * ``'matchup'`` *(str)* — home vs. away team string.
        * ``'market'`` *(str)* — market type, e.g. ``'moneyline'``.
        * ``'lines'`` *(dict)* — mapping of sportsbook name →
          ``{'home': float, 'away': float}``.

    Returns
    -------
    dmc.Card
        A bordered card with a :class:`dmc.Table` that highlights the
        best available line for each side in teal.

    Notes
    -----
    "Best" home line is the maximum value; "best" away line is also the
    maximum value (most positive / least negative American odds).
    """
    books = list(game["lines"].keys())
    home_vals = [game["lines"][b]["home"] for b in books]
    away_vals = [game["lines"][b]["away"] for b in books]
    best_home = max(home_vals)
    best_away = max(away_vals)

    rows = [
        dmc.TableTr([
            dmc.TableTd(book),
            dmc.TableTd(
                dmc.Text(str(h), fw=600, **{"c": "teal"} if h == best_home else {})
            ),
            dmc.TableTd(
                dmc.Text(str(a), fw=600, **{"c": "teal"} if a == best_away else {})
            ),
        ])
        for book, h, a in zip(books, home_vals, away_vals)
    ]

    return dmc.Card(
        withBorder=True,
        radius="md",
        p="lg",
        shadow="sm",
        mb="lg",
        children=[
            dmc.Group(
                justify="space-between",
                mb="sm",
                children=[
                    dmc.Text(game["matchup"], fw=700, size="md"),
                    dmc.Badge(
                        game["market"].upper(),
                        color="blue",
                        variant="light",
                        radius="sm",
                    ),
                ],
            ),
            dmc.Table(
                striped=True,
                highlightOnHover=True,
                withTableBorder=True,
                children=[
                    dmc.TableThead(
                        dmc.TableTr([
                            dmc.TableTh("Sportsbook"),
                            dmc.TableTh("Home"),
                            dmc.TableTh("Away"),
                        ])
                    ),
                    dmc.TableTbody(rows),
                ],
            ),
        ],
    )


def featured_pick_card(pick: dict) -> dmc.Card:
    """
    Create a large featured free-pick card with ML confidence bar.

    Parameters
    ----------
    pick : dict
        Free-pick data dict with the following keys:

        * ``'sport'`` *(str)* — sport abbreviation.
        * ``'matchup'`` *(str)* — home vs. away team string.
        * ``'pick'`` *(str)* — selected side or total with line.
        * ``'pick_type'`` *(str)* — ``'spread'``, ``'moneyline'``, etc.
        * ``'grade'`` *(str)* — overall pick quality grade.
        * ``'ml_score'`` *(float)* — ML confidence in ``[0, 1]``.
        * ``'rationale'`` *(str)* — model rationale text.

    Returns
    -------
    dmc.Card
        A prominent card with sport/grade badges, matchup heading,
        pick details, a :class:`dmc.Progress` confidence bar, and a
        rationale :class:`dmc.Alert`.
    """
    return dmc.Card(
        withBorder=True,
        radius="md",
        p="xl",
        shadow="elevated",
        mb="xl",
        children=[
            dmc.Group(
                justify="space-between",
                mb="md",
                children=[
                    sport_badge(pick["sport"], size="lg"),
                    grade_badge(pick["grade"], size="lg"),
                ],
            ),
            dmc.Title(pick["matchup"], order=3, mb="xs"),
            dmc.Group(
                mb="md",
                gap="xs",
                children=[
                    dmc.Text("Pick:", fw=600),
                    dmc.Text(pick["pick"], size="xl", fw=700, c="blue"),
                    dmc.Text(f"({pick['pick_type']})", c="dimmed"),
                ],
            ),
            dmc.Progress(
                value=pick["ml_score"] * 100,
                color="green",
                size="lg",
                radius="sm",
                mb=4,
            ),
            dmc.Text(
                f"ML Confidence Score: {pick['ml_score']:.0%}",
                size="sm",
                c="dimmed",
                mb="md",
            ),
            dmc.Alert(pick["rationale"], color="blue", variant="light"),
        ],
    )


# ---------------------------------------------------------------------------
# Table helpers
# ---------------------------------------------------------------------------


def history_table(
    history: list[dict],
    columns: list[str],
    keys: list[str],
    result_key: str = "result",
) -> dmc.Table:
    """
    Create a striped history table with automatic result-badge rendering.

    Parameters
    ----------
    history : list of dict
        Row data; each dict must contain all keys listed in ``keys``.
    columns : list of str
        Column header labels in display order.
    keys : list of str
        Dict keys to extract per row, aligned with ``columns``.
    result_key : str, optional
        The key whose cell value should be rendered as a
        :func:`result_badge` instead of plain text.
        Default is ``'result'``.

    Returns
    -------
    dmc.Table
        A striped, hoverable :class:`dmc.Table` with a ``<thead>`` header
        row and a ``<tbody>`` populated from *history*.

    Examples
    --------
    >>> tbl = history_table(
    ...     history=[{"date": "2024-01-01", "pick": "Chiefs ML", "result": "W"}],
    ...     columns=["Date", "Pick", "Result"],
    ...     keys=["date", "pick", "result"],
    ... )
    """
    head = dmc.TableThead(dmc.TableTr([dmc.TableTh(col) for col in columns]))

    body_rows = []
    for row in history:
        cells = []
        for key in keys:
            val = row.get(key, "")
            if key == result_key:
                cells.append(dmc.TableTd(result_badge(str(val))))
            else:
                cells.append(dmc.TableTd(str(val)))
        body_rows.append(dmc.TableTr(cells))

    return dmc.Table(
        striped=True,
        highlightOnHover=True,
        withTableBorder=True,
        children=[head, dmc.TableTbody(body_rows)],
    )


def styled_table(head: list[str], body: list[list]) -> dmc.Table:
    """
    Create a simple styled table from plain Python lists.

    Parameters
    ----------
    head : list of str
        Column header labels.
    body : list of list
        Row data as nested lists of strings or numbers.  Each cell is
        cast to ``str`` before rendering.

    Returns
    -------
    dmc.Table
        A striped, hoverable :class:`dmc.Table` built from the provided
        lists.

    Examples
    --------
    >>> styled_table(
    ...     head=["Sport", "Record", "ROI"],
    ...     body=[["NBA", "45-32", "6.1%"], ["NFL", "28-22", "4.8%"]],
    ... )
    """
    return dmc.Table(
        striped=True,
        highlightOnHover=True,
        withTableBorder=True,
        children=[
            dmc.TableThead(dmc.TableTr([dmc.TableTh(col) for col in head])),
            dmc.TableTbody([
                dmc.TableTr([dmc.TableTd(str(cell)) for cell in row])
                for row in body
            ]),
        ],
    )

