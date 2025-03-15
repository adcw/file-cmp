from dash import Dash
from .layout import create_layout
from .callbacks import register_callbacks


def get():
    app = Dash(__name__)
    app.layout = create_layout()

    register_callbacks(app)

    return app
