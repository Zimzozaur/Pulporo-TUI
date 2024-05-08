from datetime import datetime

from requests import request

from textual.app import ComposeResult, App
from textual.containers import Container
from textual.widgets import (
    Button,
    DataTable,
)

TODAY = datetime.now()

PARAMS = {
    'year': TODAY.year,
    'month': TODAY.month,
}


def request_(method: str, url: str) -> list[tuple]:
    """Call Pulporo endpoint and return list of tuples"""
    endpoint = 'http://localhost:8000/' + url
    response = request(method, endpoint, params=PARAMS)
    list_of_dicts: list[dict] = response.json()

    table_data = [tuple(key.capitalize() for key in list_of_dicts[0])]
    table_data.extend(tuple(d.values()) for d in list_of_dicts)
    return table_data


class FlowSection(Container):
    """Hold Button to switch between Outflows & Inflows"""
    def compose(self) -> ComposeResult:
        yield Button('Outflows', id='outflows', variant='primary')
        yield Button('Inflows', id='inflows')


class TypeSection(Container):
    """Hold Buttons to switch between One-off, All & Recurring"""
    def compose(self) -> ComposeResult:
        yield Button('One-off', variant='primary')
        yield Button('All')
        yield Button('Recurring')


class DateSection(Container):
    """Hold Buttons and widget to switch targe date"""
    def compose(self) -> ComposeResult:
        yield Button('Prev Month')
        yield Button('Custom Widget')
        yield Button('Today')
        yield Button('Next Month')


class LedgerMenu(Container):
    """Hold all menu button containers"""
    def compose(self) -> ComposeResult:
        yield FlowSection()
        yield TypeSection()
        yield DateSection()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        pass

class Table(DataTable):
    """Table that renders data from server"""
    pass


class TablePagination(Container):
    """Menu to query data ranges"""
    pass


class LedgerTable(Container):
    """Hold Table related components"""
    def compose(self) -> ComposeResult:
        yield Table()
        yield TablePagination()

    def on_mount(self):
        table = self.query_one(Table)
        table.zebra_stripes = True
        table_data = request_('get', 'outflows')
        table.add_columns(*table_data[0])
        table.add_rows(table_data[1:])
        table.cursor_type = "row"


class Ledger(Container):
    """Main view wrapper"""
    def compose(self) -> ComposeResult:
        yield LedgerMenu()
        yield LedgerTable()

