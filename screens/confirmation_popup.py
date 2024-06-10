from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Center
from textual.screen import ModalScreen
from textual.widgets import Static, Button


class ConfirmPopup(ModalScreen):
    """ModalScreen to ask user for confirmation of certain action"""

    DEFAULT_CSS = """
        ConfirmPopup {
            align: center middle;
            width: auto;
            height: auto;
        }

        #confirm-popup-body {
            width: auto;
            height: auto;
            padding: 1 2;
            background: $panel;
        }
        
        #confirm-popup-message {
            text-style: bold;
        }
        
        #confirm-popup-buttons {
            width: auto;
            height: auto;
            margin-top: 1;
            
            & > #confirm-button {
                margin-left: 10;
            }
        }
        """

    def __init__(self, *args, message, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = message

    def compose(self) -> ComposeResult:
        with Container(id='confirm-popup-body'):
            yield Static(self.message, id='confirm-popup-message')
            with Horizontal(id='confirm-popup-buttons'):
                yield Button('Reject', variant='error', id='reject-button')
                yield Button('Confirm', variant='success', id='confirm-button')

    @on(Button.Pressed, '#reject-button')
    def reject(self):
        """Return False to callback"""
        self.dismiss(False)

    @on(Button.Pressed, '#confirm-button')
    def confirm(self):
        """Return True to callback"""
        self.dismiss(True)
