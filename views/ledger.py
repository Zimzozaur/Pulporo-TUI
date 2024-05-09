from datetime import datetime

from settings import PULPORO_URL

from requests import get

from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import (
    Button,
    DataTable,
)


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
        yield Button('Custom Widget')
        yield Button('Today')
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
        table.add_columns(*table_data[0])
        table.add_rows(table_data[1:])
        table.cursor_type = "row"


class Ledger(Container):
    """Main view wrapper"""
    TODAY = datetime.now()
    params = {
        'year': TODAY.year,
        'month': TODAY.month,
    }
    ENDPOINT_URL = 'outflows'

    def compose(self) -> ComposeResult:
        yield LedgerMenu()
        yield LedgerTable(table_data=self.request_to_table())

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Send request and swap table on click"""
        button: Button = event.button
        if button.variant == 'primary':
            return
        self.query_one(LedgerTable).remove()

        flow_section = {'outflows', 'inflows'}
        type_section = {'one-off', 'all', 'recurring'}
        month_section = {'prev-month', 'next-month'}

        if button.id in flow_section:
            self.ENDPOINT_URL = 'inflows' if button.id == 'inflows' else 'outflows'
            self.all_to_default_one_to_primary(flow_section, button)

        elif button.id in type_section:
            self.all_to_default_one_to_primary(type_section, button)

        elif button.id in month_section:
            # Change month before request
            month_operation = -1 if button.id == 'prev-month' else 1
            self.params['month'] += month_operation
            if self.params['month'] == 0:
                self.params['year'] -= 1
                self.params['month'] = 12
            elif self.params['month'] == 13:
                self.params['year'] += 1
                self.params['month'] = 1

        self.mount(LedgerTable(table_data=self.request_to_table()))

    def all_to_default_one_to_primary(self, iterable, bt: Button):
        """Change all buttons to default variant and chosen to primary"""
        for obj_id in iterable:
            self.get_widget_by_id(obj_id).variant = 'default'
        bt.variant = 'primary'

    def request_to_table(self) -> list[tuple]:
        """Call Pulporo endpoint and return list of tuples"""
        endpoint = PULPORO_URL + self.ENDPOINT_URL
        response = get(endpoint, params=self.params)
        list_of_dicts: list[dict] = response.json()

        table_data = [tuple(key.capitalize() for key in ['No', *list_of_dicts[0]])]
        table_data.extend((num, *d.values()) for num, d in enumerate(list_of_dicts, start=1))
        return table_data
