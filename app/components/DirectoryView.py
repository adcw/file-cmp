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

    def render(self) -> dmc.Accordion:
        """Generuje strukturę drzewa jako komponent Dash Mantine Accordion."""
        return dmc.Accordion(
            children=self._build_tree(self.root_path),
            multiple=True,
            chevronPosition="right",
            variant="filled",
            p=0,
        )

    def _build_tree(self, path: str):
        """Rekurencyjnie buduje strukturę katalogową."""
        if not os.path.exists(path):
            return []

        items = []
        if os.path.isdir(path):
            folder_name = os.path.basename(path)
            children = [item for x in os.listdir(path) for item in self._build_tree(os.path.join(path, x))]

            items.append(
                dmc.AccordionItem(
                    [
                        self._make_folder_label(folder_name),
                        dmc.AccordionPanel(dmc.Accordion(children=children, multiple=True, variant="filled", p=0)) if children else None
                    ],
                    value=folder_name,
                    p=0,
                )
            )
        else:
            items.append(self._make_file_item(os.path.basename(path)))

        return items

    def _make_file_item(self, file_name: str) -> dmc.AccordionItem:
        """Zwraca komponent pliku jako pojedynczy element Accordion."""
        return dmc.AccordionItem(
            [
                dmc.Group(
                    [
                        DashIconify(icon="akar-icons:file"),
                        dmc.Text(file_name, size="xs")
                    ],
                    gap="xs"
                )

            ],
            value=file_name,
            p=0,
        )

    def _make_folder_label(self, folder_name: str) -> dmc.AccordionControl:
        """Zwraca kontrolkę folderu z ikoną."""
        return dmc.AccordionControl(
            dmc.Group(
                [
                    DashIconify(icon="akar-icons:folder"),
                    dmc.Text(folder_name, size="xs")
                ],
                gap="xs"
            ),
            p=0,
        )
