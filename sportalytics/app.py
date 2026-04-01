"""
Sportalytics Dash application factory.

This module creates and configures the Dash application instance,
registers the dark-mode clientside callback, and exposes ``app`` and
``server`` for WSGI deployment.

Notes
-----
``_dash_renderer._set_react_version`` **must** be called before
``dash_mantine_components`` is imported.  The import order in this file
is intentional and must not be reordered.
"""

from dash import Dash, Input, Output, _dash_renderer

_dash_renderer._set_react_version("18.2.0")

import dash_mantine_components as dmc  # noqa: E402


def create_app() -> Dash:
    """
    Create and configure the Dash application instance.

    Returns
    -------
    Dash
        A fully configured :class:`dash.Dash` application with Mantine
        theme, page routing, and dark-mode toggle wired up.

    Notes
    -----
    * ``suppress_callback_exceptions=True`` is required because page
      callbacks reference components that do not exist in the root layout.
    * The dark-mode clientside callback reads the ``theme-toggle`` switch
      state and writes ``forceColorScheme`` on the ``mantine-provider``
      component directly in the browser — no server round-trip needed.
    """
    app = Dash(
        __name__,
        use_pages=True,
        pages_folder="pages",
        suppress_callback_exceptions=True,
    )

    from sportalytics.layout import create_layout
    from sportalytics.theme import MANTINE_THEME

    app.layout = dmc.MantineProvider(
        create_layout(),
        theme=MANTINE_THEME,
        id="mantine-provider",
    )

    # Wire the header dark-mode toggle → MantineProvider.forceColorScheme
    app.clientside_callback(
        """
        function(checked) {
            return checked ? 'dark' : 'light';
        }
        """,
        Output("mantine-provider", "forceColorScheme"),
        Input("theme-toggle", "checked"),
    )

    return app


app = create_app()
server = app.server

if __name__ == "__main__":
    app.run(debug=True)
