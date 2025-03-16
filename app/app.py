import dash_mantine_components as dmc
from dash import Dash, _dash_renderer

from app.components.AppShell import app_shell

_dash_renderer._set_react_version("18.2.0")


def get():
    app = Dash(external_stylesheets=dmc.styles.ALL)

    app.layout = dmc.MantineProvider(
        app_shell()
    )

    return app
