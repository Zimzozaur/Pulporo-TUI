from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Button


class Liabilities(Container):

    def compose(self) -> ComposeResult:
        yield Button("Liabilities", id="q", variant="success")
        yield Button("Liabilities", id="w", variant="success")
        yield Button("Liabilities", id="e", variant="success")
        yield Button("Liabilities", id="r", variant="success")
        yield Container(
            Button("Liabilities", id="q", variant="warning"),
             Button("Liabilities", id="w", variant="warning"),
             Button("Liabilities", id="e", variant="warning"),
             Button("Liabilities", id="r", variant="warning")
        )
        yield Container(
            Button("Liabilities", id="q", variant="error"),
            Button("Liabilities", id="w", variant="error"),
            Button("Liabilities", id="e", variant="error"),
            Button("Liabilities", id="r", variant="error")
        )
        yield Container(
            Button("Liabilities", id="q", variant="warning"),
            Button("Liabilities", id="w", variant="warning"),
            Button("Liabilities", id="e", variant="warning"),
            Button("Liabilities", id="r", variant="warning")
        )
        yield Container(
            Button("Liabilities", id="q", variant="error"),
            Button("Liabilities", id="w", variant="error"),
            Button("Liabilities", id="e", variant="error"),
            Button("Liabilities", id="r", variant="error")
        )
        yield Container(
            Button("Liabilities", id="q", variant="warning"),
            Button("Liabilities", id="w", variant="warning"),
            Button("Liabilities", id="e", variant="warning"),
            Button("Liabilities", id="r", variant="warning")
        )
        yield Container(
            Button("Liabilities", id="q", variant="error"),
            Button("Liabilities", id="w", variant="error"),
            Button("Liabilities", id="e", variant="error"),
            Button("Liabilities", id="r", variant="error")
        )
        yield Button("Liabilities", id="t", variant="success")
        yield Button("Liabilities", id="y", variant="success")
        yield Button("Liabilities", id="u", variant="success")
        yield Button("Liabilities", id="i", variant="success")