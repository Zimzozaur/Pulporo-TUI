from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Static, Button


class Dashboard(Container):

    def compose(self) -> ComposeResult:
        yield Button("Dashboard", id="start", variant="success")


