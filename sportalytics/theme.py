"""
Mantine 8 design-system tokens for Sportalytics.

This module centralises every visual constant shared across the
application: full 10-shade colour palettes, a typography scale,
shadow definitions, and a reusable Plotly layout dictionary.

Import ``MANTINE_THEME`` into ``app.py`` and pass it to
:class:`dmc.MantineProvider`.  Import ``PLOTLY_LAYOUT_DEFAULTS`` into
any page that renders a :class:`dcc.Graph` and unpack it inside
``fig.update_layout(**PLOTLY_LAYOUT_DEFAULTS)``.

Notes
-----
All colour ramps follow Mantine's standard 10-shade convention
(index 0 = lightest, index 9 = darkest).  ``PLOTLY_LAYOUT_DEFAULTS``
uses transparent backgrounds so charts blend with both light and dark
colour schemes.
"""

# ---------------------------------------------------------------------------
# Internal colour ramps — 10 shades each (lightest → darkest)
# ---------------------------------------------------------------------------

_BLUE: list[str] = [
    "#e7f5ff", "#d0ebff", "#a5d8ff", "#74c0fc",
    "#4dabf7", "#339af0", "#228be6", "#1c7ed6",
    "#1971c2", "#1864ab",
]
_GREEN: list[str] = [
    "#ebfbee", "#d3f9d8", "#b2f2bb", "#8ce99a",
    "#69db7c", "#51cf66", "#40c057", "#37b24d",
    "#2f9e44", "#2b8a3e",
]
_RED: list[str] = [
    "#fff5f5", "#ffe3e3", "#ffc9c9", "#ffa8a8",
    "#ff8787", "#ff6b6b", "#fa5252", "#f03e3e",
    "#e03131", "#c92a2a",
]
_YELLOW: list[str] = [
    "#fff9db", "#fff3bf", "#ffec99", "#ffe066",
    "#ffd43b", "#fcc419", "#fab005", "#f59f00",
    "#f08c00", "#e67700",
]
_TEAL: list[str] = [
    "#e6fcf5", "#c3fae8", "#96f2d7", "#63e6be",
    "#38d9a9", "#20c997", "#12b886", "#0ca678",
    "#099268", "#087f5b",
]
_ORANGE: list[str] = [
    "#fff4e6", "#ffe8cc", "#ffd8a8", "#ffc078",
    "#ffa94d", "#ff922b", "#fd7e14", "#f76707",
    "#e8590c", "#d9480f",
]

# ---------------------------------------------------------------------------
# Public: Mantine theme dict
# ---------------------------------------------------------------------------

MANTINE_THEME: dict = {
    "primaryColor": "green",
    "fontFamily": (
        "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    ),
    "fontFamilyMonospace": (
        "JetBrains Mono, 'Fira Code', 'Fira Mono', 'Courier New', monospace"
    ),
    "defaultRadius": "md",
    "colors": {
        "blue": _BLUE,
        "green": _GREEN,
        "red": _RED,
        "yellow": _YELLOW,
        "teal": _TEAL,
        "orange": _ORANGE,
    },
    "headings": {
        "fontFamily": (
            "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
        ),
        "fontWeight": "700",
        "sizes": {
            "h1": {"fontSize": "2.25rem", "lineHeight": "1.20"},
            "h2": {"fontSize": "1.875rem", "lineHeight": "1.25"},
            "h3": {"fontSize": "1.5rem", "lineHeight": "1.30"},
            "h4": {"fontSize": "1.25rem", "lineHeight": "1.40"},
            "h5": {"fontSize": "1.125rem", "lineHeight": "1.45"},
        },
    },
    "shadows": {
        "card": "0 1px 3px rgba(0,0,0,.08), 0 1px 2px rgba(0,0,0,.06)",
        "elevated": "0 4px 6px rgba(0,0,0,.07), 0 2px 4px rgba(0,0,0,.06)",
        "modal": "0 20px 25px rgba(0,0,0,.15), 0 10px 10px rgba(0,0,0,.04)",
    },
}

# ---------------------------------------------------------------------------
# Public: Plotly layout defaults
# ---------------------------------------------------------------------------

#: Unpack inside ``fig.update_layout(**PLOTLY_LAYOUT_DEFAULTS)`` to keep
#: every chart visually consistent with the Mantine theme.
PLOTLY_LAYOUT_DEFAULTS: dict = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": {
        "family": (
            "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
        ),
        "size": 12,
    },
    "colorway": [
        "#228be6", "#40c057", "#fab005",
        "#fa5252", "#15aabf", "#be4bdb",
    ],
    "margin": {"t": 40, "r": 20, "b": 40, "l": 50},
    "xaxis": {
        "gridcolor": "rgba(128,128,128,0.12)",
        "linecolor": "rgba(128,128,128,0.20)",
        "showgrid": True,
    },
    "yaxis": {
        "gridcolor": "rgba(128,128,128,0.12)",
        "linecolor": "rgba(128,128,128,0.20)",
        "showgrid": True,
    },
}
