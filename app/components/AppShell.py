import dash_mantine_components as dmc
import pandas as pd
from dash import dcc, html, dash_table, callback, Output, Input, State, clientside_callback
from dash_iconify import DashIconify

from app.components.DirectorySelector import FileSelector
from app.components.DirectoryView import FileTree
from app.components.FilePreviews import FilePreviews
from app.components.ReultsTable import ResultsTable
from app.utils import similarity_to_color

df = pd.DataFrame({
    "First File": [
        r"C:\Users\adrian\Documents\URz\inne\file_cmp\test_dir\a.txt",
        r"C:\Users\adrian\Documents\URz\inne\file_cmp\test_dir\b.txt",
        r"C:\Users\adrian\Documents\URz\inne\file_cmp\test_dir\b.txt",
        r"C:\Users\adrian\Documents\URz\inne\file_cmp\test_dir\c.txt",
    ],
    "Second File": [
        r"C:\Users\adrian\Documents\URz\inne\file_cmp\test_dir\c.txt",
        r"C:\Users\adrian\Documents\URz\inne\file_cmp\test_dir\d.txt",
        r"C:\Users\adrian\Documents\URz\inne\file_cmp\test_dir\a.txt",
        r"C:\Users\adrian\Documents\URz\inne\file_cmp\test_dir\d.txt",
    ],
    "Similarity": [0.1, 0.3, 0.5, 0.9],
}).sort_values("Similarity", ascending=False)

theme_toggle = dmc.Switch(
    offLabel=DashIconify(icon="radix-icons:sun", width=15, color=dmc.DEFAULT_THEME["colors"]["yellow"][8]),
    onLabel=DashIconify(icon="radix-icons:moon", width=15, color=dmc.DEFAULT_THEME["colors"]["yellow"][6]),
    id="color-scheme-switch",
    persistence=True,
    color="grey",
)


def AppShell():
    return dmc.AppShell(
        padding=0,
        children=[
            dmc.AppShellHeader(
                dmc.Group(
                    [
                        dmc.Burger(id="burger", size="sm", hiddenFrom="sm", opened=False),
                        dmc.Title("File Similarity Comparer", c="cyan"),
                        theme_toggle
                    ],
                    h="100%",
                    px="md",
                )
            ),
            dmc.AppShellNavbar(
                id="navbar",
                children=[
                    dmc.Box(
                        dmc.Button("Open directory", id="directory-modal-open", color="cyan", variant="light",
                                   size="sm", w="100%"),
                        w="100%",
                    ),
                    dmc.Modal(
                        title="Choose directory",
                        id="directory-modal",
                        children=[
                            FileSelector(),
                        ],
                    ),

                    FileTree(r"C:\Users\adrian\Documents\URz\inne\file_cmp\data").render()
                ],
                p="md",
            ),
            dmc.AppShellMain(
                [
                    dcc.Store(id="filepaths", data=[]),
                    dmc.Flex(
                        direction="column",
                        h="calc(100vh - 95px)",
                        children=[
                            html.Div(
                                style={"margin": "10px"},
                                children=ResultsTable(df)
                            ),

                            *FilePreviews()
                        ]
                    )
                ]
            ),
        ],
        header={"height": 60},
        navbar={
            "width": 300,
            "breakpoint": "sm",
            "collapsed": {"mobile": True},
        },
        id="appshell",
    )


clientside_callback(
    """
    (switchOn) => {
       document.documentElement.setAttribute('data-mantine-color-scheme', switchOn ? 'dark' : 'light');
       return window.dash_clientside.no_update
    }
    """,
    Output("color-scheme-switch", "id"),
    Input("color-scheme-switch", "checked"),
)


@callback(
    Output("directory-modal", "opened"),
    Input("directory-modal-open", "n_clicks"),
    Input("directory-modal-submit-button", "n_clicks"),
    Input("directory-modal-cancel-button", "n_clicks"),
    State("directory-modal", "opened"),
    prevent_initial_call=True,
)
def handle_modal(open_click, submit_click, cancel_click, opened):
    return not opened


