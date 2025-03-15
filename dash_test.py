import colorsys
import webbrowser
import dash
import pandas as pd
from dash import html, dash_table, dcc
from dash.dependencies import Input, Output

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

def similarity_to_color(value: float) -> str:
    r, g, b = colorsys.hsv_to_rgb((1 - value) * 0.4, 0.53, 0.79)
    return f"rgb({int(r * 255)}, {int(g * 255)}, {int(b * 255)})"

style_conditions = [
    {
        "if": {"filter_query": f"{{Similarity}} = {sim}", "column_id": "Similarity"},
        "backgroundColor": similarity_to_color(sim),
        "color": "black",
    }
    for sim in df["Similarity"]
]

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div(
        style={"display": "flex", "height": "100vh"},
        children=[
            html.Div(
                style={"width": "400px", "borderRight": "1px solid #ddd"},
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

@app.callback(
    Output("output-div", "children"),
    Output("file1-content", "value"),
    Output("file2-content", "value"),
    Input("file-table", "selected_rows"),
    prevent_initial_call=True
)
def open_file(selected_rows):
    if selected_rows is not None and len(selected_rows) > 0:
        file1_path = df.iloc[selected_rows[0]]["First File"]
        file2_path = df.iloc[selected_rows[0]]["Second File"]
        try:
            with open(file1_path, "r", encoding="UTF-8") as file1, open(file2_path, "r", encoding="UTF-8") as file2:
                file1_content = file1.read()
                file2_content = file2.read()
            return f"Opened: {file1_path} and {file2_path}", file1_content, file2_content
        except Exception as e:
            return f"Error opening files: {file1_path} and {file2_path}", f"Error: {str(e)}", f"Error: {str(e)}"
    return "No file selected", "", ""

if __name__ == "__main__":
    app.run_server(debug=True)
