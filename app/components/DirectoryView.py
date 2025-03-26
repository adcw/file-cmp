import os

import dash_mantine_components as dmc
from dash_iconify import DashIconify


class FileTree:
    def __init__(self, root_path: str):
        """
        Tworzy komponent drzewa katalogów na podstawie podanej ścieżki.

        :param root_path: Ścieżka do katalogu głównego.
        """
        self.root_path = root_path

    def render(self) -> dmc.ScrollArea:
        """Generuje strukturę drzewa jako komponent Dash Mantine Accordion."""
        return dmc.ScrollArea(
            mih="100%",
            children=[
                dmc.Stack(
                    pt="sm",
                    gap="xs",
                    children=[
                        dmc.Text(f"File contents of\n{self.root_path}:", size="xs"),
                        dmc.Accordion(
                            children=self._build_tree(self.root_path),
                            multiple=True,
                            chevronPosition="right",
                            variant="filled",
                            styles={
                                "label": {
                                    "padding": "4px",
                                },
                                "content": {
                                    "padding": "4px",
                                    "paddingLeft": "12px",
                                    "paddingRight": "0px",
                                },
                            },
                        ),
                    ]
                )
            ]
        )

    def _build_tree(self, path: str, level: int = 1):
        """Rekurencyjnie buduje strukturę katalogową."""
        if not os.path.exists(path):
            return []

        items = []
        if os.path.isdir(path):
            folder_name = os.path.basename(path)
            children = [item for x in os.listdir(path) for item in self._build_tree(os.path.join(path, x), level + 1)]

            items.append(
                dmc.AccordionItem(
                    [
                        self._make_folder_label(folder_name, is_empty=len(children) == 0),
                        dmc.AccordionPanel(dmc.Accordion(
                            styles={
                                "label": {
                                    "padding": "4px",
                                },
                                "content": {
                                    "padding": "4px",
                                    "paddingLeft": "12px",
                                    "paddingRight": "0px",
                                }
                            },
                            multiple=True,
                            variant="filled",
                            children=children,
                        )) if children else None
                    ],
                    value=folder_name,
                )
            )
        else:
            items.append(self._make_file_item(os.path.basename(path)))

        return items

    def _make_file_item(self, file_name: str, level: int = 1) -> dmc.AccordionItem:
        """Zwraca komponent pliku jako pojedynczy element Accordion."""
        return dmc.AccordionItem(
            [
                dmc.Group(
                    gap="xs",
                    ml=level * 16,
                    children=
                    [
                        DashIconify(icon="akar-icons:file", width=12),
                        dmc.Text(file_name, size="xs")
                    ],

                )

            ],
            value=file_name,
            p=4,
        )

    def _make_folder_label(self, folder_name: str, is_empty: bool = False) -> dmc.AccordionControl:
        """Zwraca kontrolkę folderu z ikoną."""

        return dmc.AccordionControl(
            dmc.Group(
                [
                    DashIconify(icon="akar-icons:folder", width=12),
                    dmc.Text(folder_name, size="xs")
                ],
                gap="xs"
            ),
        )
