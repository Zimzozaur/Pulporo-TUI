from typing import Type

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import (
    Button,
    Footer,
    Header,
)

from screens import CreateNewPopup

from views import (
    Dashboard,
    Investment,
    Ledger,
    Liabilities,
    Media,
    Recurring,
    Reminders
)


class LeftNavMenu(Container):
    """Menu used to switch between basic views"""
    MENU_BUTTONS: dict = {
        'DashboardBt': (Dashboard, 'Dashboard'),
        'LedgerBt': (Ledger, 'Ledger'),
        'RecurringBt': (Recurring, 'Recurring'),
        'InvestmentBt': (Investment, 'Investment'),
        'LiabilitiesBt': (Liabilities, 'Liabilities'),
        'RemindersBt': (Reminders, 'Reminders'),
        'MediaBt': (Media, 'Media'),
    }
    clicked = 'LedgerBt'

    def compose(self) -> ComposeResult:
        """Compose menu of MENU_BUTTONS"""
        for bt_id, (view_class, view_name) in self.MENU_BUTTONS.items():
            yield Button(view_name, id=bt_id)

    def on_mount(self) -> None:
        """
        Mark Ledger as primary to indicate opened view
        Ledger is default on app start
        """
        ledgerBt = self.query_one('#LedgerBt')
        ledgerBt.variant = 'primary'

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Change view of the main-app container"""
        button_id: str = event.button.id
        if button_id == self.clicked:
            return
        self.get_child_by_id(button_id, Button).variant = 'primary'
        self.get_child_by_id(self.clicked, Button).variant = 'default'
        self.clicked = button_id
        self.swap_view(*self.MENU_BUTTONS[button_id])

    def swap_view(self, view_class: Type[Container], view_name: str) -> None:
        """Swap view inside MainApp"""
        main_app_wrapper = self.app.query_one('#main-app')
        for child in main_app_wrapper.children:
            child.remove()
        main_app_wrapper.mount(view_class(id=view_name))


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
    
    .-hidden-margin {
        margin: 0 !important;
    }
    
    .-hidden {
        display: none;
    }
    """

    TITLE = 'Pulporo 🐙'
    BINDINGS = [
        ('ctrl+d', 'toggle_dark', 'Dark Mode'),
        ('ctrl+n', 'create_new', 'Create New'),
        ('ctrl+o', 'toggle_left_panel', 'Full Screen')
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        with Container(id='body'):
            yield LeftNavMenu(id='left-menu')
            with Container(id='main-app'):
                yield Ledger(id='Ledger')
        yield Footer()

    def action_create_new(self) -> None:
        """
        Display a popup screen for creating new database entries.

        This method triggers the display of the 'CreateNewPopup' screen,
        which allows users to input details for new entries to be added
        to the database.
        """
        def reload_if_required(boolean: bool):
            if boolean and isinstance(self.query_one('#main-app').children[0], Ledger):
                self.query_one(Ledger).reload_table()
        self.push_screen(CreateNewPopup('CreateNewPopup'), reload_if_required)

    def action_toggle_left_panel(self) -> None:
        """
        Toggle the visibility of the left panel and adjust margins for full-screen mode.

        This method toggles the left panel by toggling the '-hidden' class
        on the element with the 'LeftNavMenu'. It also adjusts the margins of
        elements with IDs 'body' and 'main-app' by toggling the '-hidden-margin'
        """
        self.query_one('#body').toggle_class('-hidden-margin')
        self.query_one('#left-menu').toggle_class('-hidden')
        self.query_one('#main-app').toggle_class('-hidden-margin')


if __name__ == '__main__':
    app = AppBody()
    app.run()

