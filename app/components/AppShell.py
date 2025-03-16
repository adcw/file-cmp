import dash_mantine_components as dmc
import pandas as pd
from dash import dcc, html, dash_table

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

def app_shell():
    return dmc.AppShell(
        padding=0,
        children=[
            dmc.AppShellHeader(
                dmc.Group(
                    [
                        dmc.Burger(id="burger", size="sm", hiddenFrom="sm", opened=False),
                        dmc.Title("File Similarity Comparer", c="blue"),
                    ],
                    h="100%",
                    px="md",
                )
            ),
            dmc.AppShellNavbar(
                id="navbar",
                children=[
                    dmc.Fieldset(
                        children=[
                            dmc.TextInput(label="Directory path", placeholder="Enter path"),
                            dmc.TextInput(label="Filename regex", placeholder=".txt"),
                            dmc.Group(
                                mt="sm",
                                children=[dmc.Button("Scan Directory")], justify="flex-end", grow=True),
                        ],
                        legend="Input files",
                    )
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
                        dmc.Group(
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
