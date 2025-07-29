from pathlib import Path
from typing import Any, Final

import pydicom
import pydicom.datadict
import pydicom.tag
import typer
from pydicom import DataElement
from rich.style import Style
from rich.text import Text
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Input, Static, Tree

PLACEHOLDER: Final[str] = '🔍'

app = typer.Typer(add_completion=False, no_args_is_help=True)


def _sequence(data_element: pydicom.DataElement, filter_value: str, indent: int = 0) -> list[tuple[Text, DataElement]]:
    leafs = []
    for sequence_element in data_element:  # type: ignore
        if isinstance(sequence_element, pydicom.dataset.Dataset):
            for element in sequence_element:
                if element.VR == 'SQ':
                    leafs.extend(_sequence(element, filter_value=filter_value, indent=indent + 2))
                    continue
                try:
                    keyword = pydicom.datadict.get_entry(element.tag)[2]
                except KeyError:
                    keyword = None

                if keyword is not None and filter_value.casefold() not in keyword.casefold():
                    continue

                leafs.append((create_text(element, indent=indent + 2), element))
    return leafs


def create_text(data_element: pydicom.dataelem.DataElement, indent: int = 0) -> Text:
    # noinspection PyTypeChecker
    tag: pydicom.tag.BaseTag = data_element.tag
    if tag.is_private:
        keyword = 'Unknown Tag & Data'
    else:
        keyword = pydicom.datadict.get_entry(tag)[2]

    keyword_length = 60 - indent

    text = Text()
    text.append(" " * indent)
    text.append(f'{tag.element:04X}', style=Style(reverse=True))
    try:
        text.append(f' {keyword:{keyword_length}}', style=Style(color='green'))
        text.append(f'{data_element.VR}',
                    style=Style(color='red', italic=True,
                                link='https://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html'))
        text.append(': ')
        text.append(f'{data_element.repval:75s}', style=Style(color='cyan'))
    except (TypeError, AttributeError, ValueError, KeyError):
        pass

    return text


class DicomTree(Static):
    DEFAULT_CSS = """
        Vertical {
        height: auto;
    }
    
    Horizontal {
        width: 1fr;
        height: auto;
    }
    """

    BINDINGS = [
        ('d', 'detail', 'Detail'),
        ('e', 'export', 'Export'),
    ]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._dataset: pydicom.Dataset | None = None

    def compose(self) -> ComposeResult:
        with Vertical():
            with Horizontal():
                yield Input(placeholder=PLACEHOLDER, id='filter_input')
                yield Button(label='Filter', id='filter_button')
            tree: Tree = Tree(id='dicom_tree', label='Dicom')
            tree.show_root = False
            yield tree

    def set_dataset(self, dataset: pydicom.Dataset | None) -> None:
        self._dataset = dataset
        self._update_tree()

    @on(Input.Changed, '#filter_input')
    def filter_changed(self) -> None:
        value = self.query_one(Input)
        if value == PLACEHOLDER:
            return

        self._update_tree()

    def action_detail(self) -> None:
        ...

    def action_export(self) -> None:
        ...
        # # Provide export for Surface Segmentation Storage for now
        # if self._dataset.SOPClassUID != '1.2.840.10008.5.1.4.1.1.66.5':
        #     return

    def _update_tree(self) -> None:
        tree = self.query_one(Tree)
        tree.root.remove_children()

        if self._dataset is None:
            return

        filter_value: str = self.query_one(Input).value

        # noinspection PyUnresolvedReferences
        groups = {k.tag.group for k in self._dataset}
        nodes = {group: tree.root.add(Text(f'{group:04X}', 'reverse'), expand=group % 2 == 0) for group in sorted(groups)}

        for data_element in self._dataset:
            # noinspection PyTypeChecker
            tag: pydicom.tag.BaseTag = data_element.tag

            if tag.is_private:
                keyword = 'Unknown Tag & Data'
            else:
                keyword = pydicom.datadict.get_entry(tag)[2]

            if data_element.VR == 'SQ':
                leafs = _sequence(data_element, filter_value)
                if len(leafs) > 0:
                    node = nodes[tag.group]
                    node.add_leaf(create_text(data_element), data=data_element)
                    for leaf, element in leafs:
                        node.add_leaf(leaf, data=element)
                continue

            if filter_value.casefold() not in keyword.casefold():
                continue

            nodes[tag.group].add_leaf(create_text(data_element), data=data_element)

        while True:
            for key, node in nodes.items():
                if len(node.children) == 0:
                    node.remove()
                    nodes.pop(key, None)
                    break
            else:
                break


class DicomTreeApp(App):

    def __init__(self, filename: Path) -> None:
        super().__init__()
        self.filename = filename

    def compose(self) -> ComposeResult:
        yield DicomTree()

    async def on_mount(self) -> None:
        self.call_after_refresh(self.update)

    async def update(self) -> None:
        ds = pydicom.dcmread(self.filename)

        self.query_one(DicomTree).set_dataset(ds)
        self.title = f'Dicom: {self.filename}'


@app.command()
def view(filename: Path) -> None:
    DicomTreeApp(filename).run()


if __name__ == "__main__":
    app()
