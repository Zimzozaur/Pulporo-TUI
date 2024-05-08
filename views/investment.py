from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Static, Button


class Investment(Container):

    def compose(self) -> ComposeResult:
        yield Button("Investment", id="start", variant="success")


