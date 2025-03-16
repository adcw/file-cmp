import os

from dash.dependencies import Input, Output, State
import pandas as pd


def register_callbacks(app):
    @app.callback(
        Output("file1-content", "value"),
        Output("file2-content", "value"),

        Input("file-table", "selected_rows"),
        Input("file-table", "data"),

        prevent_initial_call=True
    )
    def open_file(selected_rows, table_data):
        if selected_rows and len(selected_rows) > 0:
            selected_index = selected_rows[0]
            df = pd.DataFrame(table_data)

            file1_path = df.iloc[selected_index]["First File"]
            file2_path = df.iloc[selected_index]["Second File"]

            try:
                with open(file1_path, "r", encoding="UTF-8") as file1, open(file2_path, "r", encoding="UTF-8") as file2:
                    file1_content = file1.read()
                    file2_content = file2.read()
                return file1_content, file2_content
            except Exception as e:
                return f"Error: {str(e)}", f"Error: {str(e)}"

        return "", ""

    @app.callback(
        Output("modal-container", "style"),
        Output("path-output", "style"),
        Input("analyze-button", "n_clicks"),
        State("path-input", "value"),
        prevent_initial_call=True
    )
    def check_path(n_clicks: int, path: str):
        if os.path.isdir(path):
            return {
                    "position": "fixed",
                    "display": "flex",
                    "top": "0",
                    "left": "0",
                    "width": "100vw",
                    "height": "100vh",
                    "backgroundColor": "rgba(0, 0, 0, 0.5)",
                    "alignItems": "center",
                    "justifyContent": "center",
                }, {"display": "none"}
        return {"display": "none"}, {"paddingLeft": "5px", "paddingBottom": "15px", "color": "#a84632"}

    @app.callback(
        Output("modal-container", "style", allow_duplicate=True),
        Input("close-modal", "n_clicks"),
        prevent_initial_call="initial_duplicate"
    )
    def close_modal(n_clicks: int):
        return {"display": "none"}
