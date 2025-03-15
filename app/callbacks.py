from dash.dependencies import Input, Output
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
