import pandas as pd
from dash import Input, Output, callback
from dash import dash_table

from app.utils import similarity_to_color


def ResultsTable(df: pd.DataFrame):
    style_conditions = [
        {
            "if": {"filter_query": f"{{Similarity}} = {sim}", "column_id": "Similarity"},
            "backgroundColor": similarity_to_color(sim),
            "color": "black",
        }
        for sim in df["Similarity"]
    ]
    return dash_table.DataTable(
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



@callback(
    Output("file-table", "style_data"),
    Output("file-table", "style_header"),
    Input("mantine-provider", "forceColorScheme"),
)
def update_table_style(theme):
    dark_mode = theme == "dark"
    bg_color = "#1E1E1E" if dark_mode else "white"
    text_color = "white" if dark_mode else "black"
    header_bg = "#292929" if dark_mode else "#f4f4f4"

    return {"backgroundColor": bg_color, "color": text_color}, {"backgroundColor": header_bg, "color": text_color}
