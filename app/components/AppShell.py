import dash_mantine_components as dmc
import pandas as pd
from dash import dcc, html, dash_table, callback, Output, Input, State
from dash_iconify import DashIconify

from app.components.DirectorySelector import FileSelector
from app.components.DirectoryView import FileTree
from app.components.FilePreviews import FilePreviews
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

style_conditions = [
    {
        "if": {"filter_query": f"{{Similarity}} = {sim}", "column_id": "Similarity"},
        "backgroundColor": similarity_to_color(sim),
        "color": "black",
    }
    for sim in df["Similarity"]
]


def AppShell():
    return dmc.AppShell(
        padding=0,
        children=[
            dmc.AppShellHeader(
                dmc.Group(
                    [
                        dmc.Burger(id="burger", size="sm", hiddenFrom="sm", opened=False),
                        dmc.Title("File Similarity Comparer", c="cyan"),
                    ],
                    h="100%",
                    px="md",
                )
            ),
            dmc.AppShellNavbar(
                id="navbar",
                children=[
                    dmc.Button("Open directory", id="directory-modal-open", color="cyan", variant="light"),
                    dmc.Modal(
                        title="Choose directory",
                        id="directory-modal",
                        children=[
                            FileSelector(),
                        ],
                    ),

                    dmc.ScrollArea(
                        children=FileTree(r"C:\Users\adrian\Documents\URz\inne\file_cmp\data").render()
                    ),
                ],
                p="md",
            ),
            dmc.AppShellMain(
                dmc.Flex(
                    direction="column",
                    h="calc(100vh - 95px)",
                    children=[
                        html.Div(
                            style={"margin": "10px"},
                            children=dash_table.DataTable(
                                id="file-table",
                                data=df.to_dict("records"),
                                columns=[{"name": col, "id": col} for col in df.columns],
                                row_selectable="single",
                                style_table={"overflowX": "auto", "flexGrow": "1"},
                                page_size=10,
                                filter_action="native",
                                sort_action="native",
                                sort_mode="multi",
                                style_data_conditional=style_conditions,
                            )
                        ),

                        *FilePreviews()
                    ]
                )
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
