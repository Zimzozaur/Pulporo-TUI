from datetime import datetime

from settings import PULPORO_URL

from requests import get

from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual.widgets import (
    Button,
    DataTable,
)

ENDPOINT_URL = 'outflows'
TODAY = datetime.now()

PARAMS = {
    'year': TODAY.year,
    'month': TODAY.month,
}
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def request_table_data() -> list[tuple]:
    """Call Pulporo endpoint and return list of tuples"""
    endpoint = PULPORO_URL + ENDPOINT_URL
    response = get(endpoint, params=PARAMS)
    list_of_dicts: list[dict] = response.json()

    # Escape if there is no data
    if not list_of_dicts:
        return []

    table_data = [tuple(key.capitalize() for key in ['No', *list_of_dicts[0]])]
    table_data.extend((num, *d.values()) for num, d in enumerate(list_of_dicts, start=1))
    return table_data


class MonthsPopup(ModalScreen):
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Button('⬅️')
            yield Button('TEXT')
            yield Button('➡️')

        with Container():
            with Horizontal():
                yield Button('Jan', id='jan')
                yield Button('Feb', id='feb')
                yield Button('Mar', id='mar')
                yield Button('Apr', id='apr')
            with Horizontal():
                yield Button('May', id='may')
                yield Button('Jun', id='jun')
                yield Button('Jul', id='jul')
                yield Button('Aug', id='aug')
            with Horizontal():
                yield Button('Sep', id='sep')
                yield Button('Oct', id='oct')
                yield Button('Nov', id='nov')
                yield Button('Dec', id='dec')


class MonthButton(Button):
    pass


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
    """Hold Buttons and widget to switch targe date"""
    def compose(self) -> ComposeResult:
        yield Button('Prev Month', id='prev-month')
        yield MonthButton(f"{MONTHS[PARAMS['month'] - 1]} {PARAMS['year']}", id='month-button')
        yield Button('Today', id='today')
        yield Button('Next Month', id='next-month')


class LedgerMenu(Container):
    """Hold all menu button containers"""
    def compose(self) -> ComposeResult:
        yield FlowSection()
        yield TypeSection()
        yield DateSection()


class Table(DataTable):
    """Table that renders data from server"""
    pass


class TablePagination(Container):
    """Menu to query data ranges"""
    pass


class LedgerTable(Container):
    """Hold Table related components"""

    def __init__(self, *args, **kwargs):
        self.table_data = kwargs.pop('table_data')
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        yield Table()
        yield TablePagination()

    def on_mount(self):
        table = self.query_one(Table)
        table.zebra_stripes = True
        table_data = self.table_data
        if table_data:
            table.add_columns(*table_data[0])
            table.add_rows(table_data[1:])
            table.cursor_type = "row"
        else:
            table.add_column('Create new records to fill the table 🤭')


class Ledger(Container):
    """Main view wrapper"""
    def compose(self) -> ComposeResult:
        yield LedgerMenu()
        yield LedgerTable(table_data=request_table_data())

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Send request and swap table on click"""
        global ENDPOINT_URL, PARAMS

        button: Button = event.button
        if button.variant == 'primary':
            return

        flow_section = {'outflows', 'inflows'}
        type_section = {'one-off', 'all', 'recurring'}
        month_section = {'prev-month', 'next-month'}

        if button.id in flow_section:
            ENDPOINT_URL = 'inflows' if button.id == 'inflows' else 'outflows'
            self.all_to_default_one_to_primary(flow_section, button)

        elif button.id in type_section:
            self.all_to_default_one_to_primary(type_section, button)

        elif button.id in month_section:
            # Change month before request
            month_operation = -1 if button.id == 'prev-month' else 1
            PARAMS['month'] += month_operation
            if PARAMS['month'] == 0:
                PARAMS['year'] -= 1
                PARAMS['month'] = 12
            elif PARAMS['month'] == 13:
                PARAMS['year'] += 1
                PARAMS['month'] = 1
            self.change_date_on_month_button()

        elif button.id == 'today':
            if PARAMS['year'] == TODAY.year and PARAMS['month'] == TODAY.month:
                return
            PARAMS['year'] = TODAY.year
            PARAMS['month'] = TODAY.month
            self.change_date_on_month_button()

        self.query_one(LedgerTable).remove()
        self.mount(LedgerTable(table_data=request_table_data()))

    def all_to_default_one_to_primary(self, iterable, bt: Button) -> None:
        """Change all buttons to default variant and chosen to primary"""
        for obj_id in iterable:
            self.get_widget_by_id(obj_id).variant = 'default'
        bt.variant = 'primary'

    def change_date_on_month_button(self):
        new_name = f"{MONTHS[PARAMS['month'] - 1]} {PARAMS['year']}"
        self.get_widget_by_id('month-button').label = new_name


