import pandas as pd
from dash import html, dash_table, dcc
from .utils import similarity_to_color

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


def create_layout():
    return html.Div(
        style={"display": "flex", "height": "100vh"},
        children=[

            html.Div(
                style={
                    "width": "350px",
                    "minWidth": "300px",
                    "borderRight": "1px solid #ddd",
                    "padding": "15px",
                    "backgroundColor": "#f8f9fa",
                    "display": "flex",
                    "flexDirection": "column",
                },
                children=[
                    html.Label("Choose file:", style={"fontWeight": "bold", "marginBottom": "4px", "paddingLeft": "5px"}),
                    dcc.Input(id="path-input", type="text", placeholder="Enter path...",
                              style={"padding": "8px", "borderRadius": "15px", "border": "1px solid #ddd"}),
                    html.Label("Error - path not found", id="path-output", style={"paddingLeft": "5px", "paddingBottom": "15px", "color": "#a84632"}),

                    html.Label("Regex:", style={"fontWeight": "bold", "marginBottom": "4px", "paddingLeft": "5px"}),
                    dcc.Input(id="regex-input", type="text", placeholder="Enter regex...",
                              style={ "padding": "8px", "marginBottom": "15px", "borderRadius": "15px", "border": "1px solid #ddd"}),

                    html.Button("Analyze", id="analyze-button", style={"width": "100%", "padding": "8px", "borderRadius": "15px", "border": "1px solid #ddd",}),
                ],
            ),

            html.Div(
                style={"flexGrow": "1", "display": "flex", "flexDirection": "column"},
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

                    html.Div(
                        id="editor-space",
                        style={
                            "height": "50%",
                            "width": "100%",
                            "display": "flex",
                            "flexDirection": "row",
                            "borderTop": "1px solid #ddd",
                            "backgroundColor": "#ffffff",
                            "marginTop": "auto",
                        },
                        children=[
                            dcc.Textarea(
                                id="file1-content",
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
                                id="file2-content",
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
                            )
                        ]
                    ),
                ]
            ),
        ],
    )
