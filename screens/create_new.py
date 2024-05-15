from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.events import Click
from textual.screen import ModalScreen
from textual.widgets import (
    Button,
    Static
)


class CreateNewPopup(ModalScreen):

    def compose(self) -> ComposeResult:
        with Container(id='new-popup-body'):
            with Horizontal():
                yield Static("CREATE NEW", id='new-popup-title')
                yield Button('X', variant='error')
