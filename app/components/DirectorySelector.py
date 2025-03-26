import os

import dash_mantine_components as dmc
from dash import dcc, Output, Input, callback
from dash_iconify import DashIconify


def FileSelector():
    return dmc.Stack(
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
                children=[
                    dmc.Button("Cancel", id="directory-modal-cancel-button", variant="outline", color="cyan"),
                    dmc.Button("Scan Directory", id="directory-modal-submit-button", color="cyan"),
                ], justify="flex-end", grow=True),

            dcc.Store(id="path-store", data={"path": None, "regex": None}),
        ]
    )


@callback(
    Output("path-input", "error"),
    Output("directory-modal-submit-button", "disabled"),
    Input("path-input", "value"),
    prevent_initial_call=True
)
def get_path(path):
    if path and not os.path.exists(path):
        return "Path not found", True
    else:
        return "", False


@callback(
    Output("filepaths", "data"),
    Input("directory-modal-submit-button", "n_clicks"),

    prevent_initial_call=True,
)
def handle_scan(submit_click):
    print("Clicked")
    return []
