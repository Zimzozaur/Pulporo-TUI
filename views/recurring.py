from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Static, Button


class Recurring(Container):

    def compose(self) -> ComposeResult:
        yield Button("Recurring", id="start", variant="success")

