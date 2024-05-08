from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Static, Button


class Reminders(Container):

    def compose(self) -> ComposeResult:
        yield Button("Reminders", id="start", variant="success")

