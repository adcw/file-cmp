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
    return html.Div([
        html.Div(
            style={"display": "flex", "height": "100vh"},
            children=[
                html.Div(
                    style={"width": "400px", "minWidth":"300px", "borderRight": "1px solid #ddd"},
                    children=[
                        html.H4("Details"),
                        html.Div(id="output-div", style={"marginTop": "10px"})
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
                                style_table={'overflowX': 'auto', "flexGrow": "1"},
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
                                "height": "500px",
                                "marginTop": "auto",
                                "width": "100%",
                                "display": "flex",
                                "flexDirection": "row",
                                "borderTop": "1px solid #ddd",
                            },
                            children=[
                                dcc.Textarea(
                                    id="file1-content",
                                    value="Sample text",
                                    style={"width": "100%", "height": "100%", "margin": "10px", "marginRight": "5px", "padding": "5px", "resize": "none", "border": "1px solid #ddd"},
                                    readOnly=True
                                ),
                                dcc.Textarea(
                                    id="file2-content",
                                    value="Sample text",
                                    style={"width": "100%", "height": "100%", "margin": "10px", "marginLeft": "5px","padding": "5px", "resize": "none", "border": "1px solid #ddd"},
                                    readOnly=True
                                )
                            ]
                        ),
                    ]
                ),
            ],
        )
    ])
