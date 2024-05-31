import os

from typing import Dict

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import (
    Button,
    Footer,
    Header,
)

from screens.create_new import CreateNewPopup

from views.dashboard import Dashboard
from views.ledger import Ledger
from views.recurring import Recurring
from views.investment import Investment
from views.liabilities import Liabilities
from views.reminders import Reminders
from views.media import Media


class Body(Container):
    """Wraps main application"""
    pass


class LeftNavMenu(Container):
    """Menu used to switch between basic views"""
    clicked = 'LedgerBt'

    def compose(self) -> ComposeResult:
        yield Button("Dashboard", id='DashboardBt')
        yield Button("Ledger", id='LedgerBt', variant="primary")
        yield Button("Recurring", id='RecurringBt')
        yield Button("Investment", id='InvestmentBt')
        yield Button("Liabilities", id='LiabilitiesBt')
        yield Button("Reminders", id='RemindersBt')
        yield Button("Media", id='MediaBt')

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button = event.button.id
        if button == self.clicked:
            return

        self.get_child_by_id(button).variant = 'primary'
        self.get_child_by_id(self.clicked).variant = 'default'

        self.clicked = button

        match button:
            case 'DashboardBt':
                self.add_and_remove_from_dom(Dashboard)
            case 'LedgerBt':
                self.add_and_remove_from_dom(Ledger)
            case 'RecurringBt':
                self.add_and_remove_from_dom(Recurring)
            case 'InvestmentBt':
                self.add_and_remove_from_dom(Investment)
            case 'LiabilitiesBt':
                self.add_and_remove_from_dom(Liabilities)
            case 'RemindersBt':
                self.add_and_remove_from_dom(Reminders)
            case 'MediaBt':
                self.add_and_remove_from_dom(Media)

    def add_and_remove_from_dom(self, cls):
        """Remove Swaps view inside MainApp"""
        main_app_wrapper = self.parent.parent.query('#MainApp').last()
        for child in main_app_wrapper.children:
            child.remove()
        main_app_wrapper.mount(cls())


class MainApp(Container):
    """Wrapper that holds views inside"""
    pass


def load_globals() -> Dict[str, str]:
    return {
        "PULPORO_API_URL": os.getenv("PULPORO_API_URL", "http://localhost:8000/")
    }


class AppConfig(App):
    """Subclass of App with config attribute"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = load_globals()


class AppBody(AppConfig):
    """Container for the whole app"""

    TITLE = 'Pulporo 🐙'
    CSS_PATH = 'main.tcss'
    BINDINGS = [
        ('ctrl+d', 'toggle_dark', 'Dark Mode'),
        ('ctrl+n', 'create_new', 'Create New'),
    ]

    def compose(self) -> ComposeResult:
        # create the ledger widget with the URL in the config
        ledger = Ledger(id='ledger')
        ledger.PULPORO_API_URL = self.config["PULPORO_API_URL"]
        with Container():
            yield Header(show_clock=False)
            with Body():
                yield LeftNavMenu()
                with MainApp(id='MainApp'):
                    yield ledger
        yield Footer()

    def action_create_new(self):
        self.push_screen(CreateNewPopup('CreateNewPopup'))


if __name__ == '__main__':
    app = AppBody()
    app.run()

