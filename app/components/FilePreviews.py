
import dash_mantine_components as dmc
from dash import dcc


def FilePreviews():
    return dmc.Group(
        p="sm",
        grow=True,

        style={"borderTop": "1px solid #ddd", "marginTop": "auto"},
        h="700px",
        mah="50%",
        children=[
            dcc.Textarea(
                value="Sample text",
                style={
                    "width": "50%",
                    "height": "100%",
                    "padding": "10px",
                    "resize": "none",
                    "border": "1px solid #ddd",
                    "backgroundColor": "#f8f9fa",
                    "fontFamily": "monospace"
                },
                readOnly=True
            ),

            dcc.Textarea(
                value="Sample text",
                style={
                    "width": "50%",
                    "height": "100%",
                    "padding": "10px",
                    "resize": "none",
                    "border": "1px solid #ddd",
                    "backgroundColor": "#f8f9fa",
                    "fontFamily": "monospace"
                },
                readOnly=True
            ),
        ]
    ),
