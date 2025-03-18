import os

import dash_mantine_components as dmc
from dash import dcc, Output, Input, callback
from dash_iconify import DashIconify


def FileSelector():
    return dmc.Fieldset(
        children=[
            dmc.TextInput(
                id="path-input",
                label="Directory path",
                placeholder="Enter path",
                debounce=200
            ),

            dmc.TextInput(id="regex-input", label="Filename regex", placeholder=".txt"),

            dmc.Group(
                mt="sm",
                children=dmc.Button("Scan Directory"), justify="flex-end", grow=True),

            dcc.Store(id="path-store", data={"path": None, "regex": None}),
        ],
        legend="Input files",
    )


@callback(
    Output("path-input", "error"),
    Input("path-input", "value"),
    prevent_initial_call=True
)
def get_path(path):
    if path and not os.path.exists(path):
        return "Path not found"
    else:
        return ""
