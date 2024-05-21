from datetime import datetime

from requests import get

from textual.widget import Widget
from textual import on
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import (
    Button,
    DataTable,
)

from screens.month_year_popup import MonthYearPopup


MONTHS: list[str] = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]


class FlowSection(Container):
    """Hold Button to switch between Outflows & Inflows"""

    def compose(self) -> ComposeResult:
        yield Button('Outflows', id='outflows', variant='primary')
        yield Button('Inflows', id='inflows')


class TypeSection(Container):
    """Hold Buttons to switch between One-off, All & Recurring"""

    def compose(self) -> ComposeResult:
        yield Button('One-off', id='one-off', variant='primary')
        yield Button('All', id='all')
        yield Button('Recurring', id='recurring')


class DateSection(Container):
    """Hold Buttons and widget to switch target date"""

    def __init__(self, date_dict, *children: Widget):
        super().__init__(*children)
        self.date_dict: dict = date_dict

    def compose(self) -> ComposeResult:
        yield Button('Prev Month', id='prev-month')
        yield MonthButton(
            f"{MONTHS[self.date_dict['month'] - 1]} {self.date_dict['year']}",
            id='month-button'
        )
        yield Button('Today', id='today')
        yield Button('Next Month', id='next-month')


class MonthButton(Button):
    """
    On click display month calendar.
    Does not request on click
    """


class LedgerMenu(Container):
    """Hold all menu button containers"""
    def __init__(self, date_dict):
        super().__init__()
        self.date_dict: dict = date_dict

    def compose(self) -> ComposeResult:
        yield FlowSection()
        yield TypeSection()
        yield DateSection(date_dict=self.date_dict)


class Table(DataTable):
    """Table that renders data from server"""
    pass


class LedgerTable(Container):
    """Hold Table related components"""

    def __init__(self, table_data):
        super().__init__()
        self.table_data: list[dict] = table_data

    def compose(self) -> ComposeResult:
        yield Table()

    def on_mount(self):
        table = self.query_one(Table)
        table.zebra_stripes = True
        table_data: list[dict] = self.table_data
        if table_data:
            table.add_columns(*table_data[0])
            table.add_rows(table_data[1:])
            table.cursor_type = "row"
        else:
            table.add_column('Create new records to fill the table 🤭')


class Ledger(Container):
    """Main view wrapper"""
    ENDPOINT_URL: str = 'outflows'
    PULPORO_API_URL: str = "TEST"
    TODAY = datetime.now()
    params: dict = {
        'year': TODAY.year,
        'month': TODAY.month,
    }

    def compose(self) -> ComposeResult:
        yield LedgerMenu(date_dict=self.params)
        yield LedgerTable(table_data=self.request_table_data())

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Send request and swap table on click"""
        button: Button = event.button
        if button.variant == 'primary' or button.id == 'month-button':
            return

        flow_section: set = {'outflows', 'inflows'}
        type_section: set = {'one-off', 'all', 'recurring'}
        month_section: set = {'prev-month', 'next-month'}

        if button.id in flow_section:
            self.ENDPOINT_URL: str = 'inflows' if button.id == 'inflows' else 'outflows'
            self.all_to_default_one_to_primary(flow_section, button)

        elif button.id in type_section:
            self.all_to_default_one_to_primary(type_section, button)

        elif button.id in month_section:
            # Change month before request
            month_operation: int = -1 if button.id == 'prev-month' else 1
            self.params['month'] += month_operation
            if self.params['month'] == 0:
                self.params['year'] -= 1
                self.params['month'] = 12
            elif self.params['month'] == 13:
                self.params['year'] += 1
                self.params['month'] = 1
            self.change_date_on_month_button()

        elif button.id == 'today':
            if self.params['year'] == self.TODAY.year and self.params['month'] == self.TODAY.month:
                return
            self.params['year'] = self.TODAY.year
            self.params['month'] = self.TODAY.month
            self.change_date_on_month_button()

        self.query_one(LedgerTable).remove()
        self.mount(LedgerTable(table_data=self.request_table_data()))

    def all_to_default_one_to_primary(self, iterable, bt: Button) -> None:
        """Change all buttons to default variant and chosen to primary"""
        for obj_id in iterable:
            self.get_widget_by_id(obj_id).variant = 'default'
        bt.variant = 'primary'

    def change_date_on_month_button(self):
        new_name = f"{MONTHS[self.params['month'] - 1]} {self.params['year']}"
        self.get_widget_by_id('month-button').label = new_name

    @on(Button.Pressed, '#month-button')
    def month_button_pressed(self):
        """Open months popup"""
        def swap_table_to_new_update_month_button(boolean):
            if boolean:
                self.query_one(LedgerTable).remove()
                self.mount(LedgerTable(table_data=self.request_table_data()))
                self.change_date_on_month_button()

        self.app.push_screen(
            MonthYearPopup(self.params),
            swap_table_to_new_update_month_button
        )

    def request_table_data(self) -> list[tuple]:
        """Call Pulporo endpoint and return list of tuples"""
        endpoint: str = self.PULPORO_API_URL + self.ENDPOINT_URL
        response = get(endpoint, params=self.params)
        list_of_dicts: list[dict] = response.json()

        # Escape if there is no data
        if not list_of_dicts:
            return []

        table_data: list[tuple] = [tuple(key.capitalize() for key in ['No', *list_of_dicts[0]])]
        table_data.extend((num, *d.values()) for num, d in enumerate(list_of_dicts, start=1))
        return table_data
