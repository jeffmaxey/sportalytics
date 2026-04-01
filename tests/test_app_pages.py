from __future__ import annotations

import dash
from dash.development.base_component import Component

from sportalytics.app import create_app
import sportalytics.pages.home as home_page
import sportalytics.pages.help as help_page


EXPECTED_ROUTES = {
    "/",
    "/free-pick",
    "/predictions",
    "/player-props",
    "/model-tracker",
    "/odds-insight",
    "/marketplace",
    "/live-totals",
    "/calculators",
    "/profile",
    "/settings",
    "/help",
}


def _walk(component: Component | None):
    """Yield a component tree depth-first for simple structural assertions."""
    if component is None:
        return
    yield component

    children = getattr(component, "children", None)
    if children is None:
        return

    if isinstance(children, (list, tuple)):
        for child in children:
            if isinstance(child, Component):
                yield from _walk(child)
    elif isinstance(children, Component):
        yield from _walk(children)


def test_create_app_smoke():
    app = create_app()
    assert isinstance(app, dash.Dash)
    assert app.layout is not None


def test_page_registry_contains_expected_routes():
    create_app()
    routes = {page["path"] for page in dash.page_registry.values()}
    assert EXPECTED_ROUTES.issubset(routes)


def test_layout_contains_theme_toggle_and_provider_callback():
    app = create_app()

    component_ids = {
        getattr(component, "id")
        for component in _walk(app.layout)
        if getattr(component, "id", None)
    }

    assert "mantine-provider" in component_ids
    assert "theme-toggle" in component_ids
    assert "mantine-provider.forceColorScheme" in app.callback_map


def test_home_layout_renders_without_component_prop_errors():
    page_layout = home_page.layout()
    assert isinstance(page_layout, Component)


def test_help_layout_renders_without_component_prop_errors():
    create_app()
    page_layout = help_page.layout()
    assert isinstance(page_layout, Component)
