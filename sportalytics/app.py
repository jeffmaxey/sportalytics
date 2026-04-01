import dash_mantine_components as dmc
from dash import Dash, _dash_renderer

_dash_renderer._set_react_version("18.2.0")


def create_app() -> Dash:
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
    return app


app = create_app()
server = app.server

if __name__ == "__main__":
    app.run(debug=True)
