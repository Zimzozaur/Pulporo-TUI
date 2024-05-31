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
                self.add_and_remove_from_dom(Dashboard, 'dashboard')
            case 'LedgerBt':
                self.add_and_remove_from_dom(Ledger, 'ledger')
            case 'RecurringBt':
                self.add_and_remove_from_dom(Recurring, 'recurring')
            case 'InvestmentBt':
                self.add_and_remove_from_dom(Investment, 'investment')
            case 'LiabilitiesBt':
                self.add_and_remove_from_dom(Liabilities, 'liabilities')
            case 'RemindersBt':
                self.add_and_remove_from_dom(Reminders, 'reminders')
            case 'MediaBt':
                self.add_and_remove_from_dom(Media, 'media')

    def add_and_remove_from_dom(self, cls, element_id):
        """Remove Swaps view inside MainApp"""
        main_app_wrapper = self.app.query_one('#main-app')
        for child in main_app_wrapper.children:
            child.remove()
        main_app_wrapper.mount(cls(id=element_id))


def load_globals() -> Dict[str, str]:
    return {
        "PULPORO_API_URL": os.getenv("PULPORO_API_URL", "http://localhost:8000/")
    }


class AppBody(App):
    """Container for the whole app"""
    DEFAULT_CSS = """
    #body {
        margin: 1 2;
        height: 100%;
        width: 100%;
        background: $surface;
    }
    
    #left-menu {
        width: 16;
        dock: left;
        background: $surface-lighten-1;
        padding: 0 1 1 1;
    }
    
    #left-menu Button {
        margin-top: 1;
        content-align: center middle;
    }
    
    #left-menu Button:hover {
        background: $accent;
        color: $text;
        text-style: bold;
    }
    
    #main-app {
        margin: 0 0 0 2;
        background: $surface-lighten-1;
        padding: 1;
    }
    """

    TITLE = 'Pulporo 🐙'
    BINDINGS = [
        ('ctrl+d', 'toggle_dark', 'Dark Mode'),
        ('ctrl+n', 'create_new', 'Create New'),
    ]
    config = load_globals()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        with Container(id='body'):
            yield LeftNavMenu(id='left-menu')
            with Container(id='main-app'):
                yield Ledger(id='ledger')
        yield Footer()

    def action_create_new(self):
        self.push_screen(CreateNewPopup('CreateNewPopup'))


if __name__ == '__main__':
    app = AppBody()
    app.run()

