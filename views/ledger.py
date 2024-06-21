from datetime import datetime
from typing import Literal, Sequence

from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import (
    Button,
    DataTable,
)
from textual.widgets.data_table import RowKey

from screens import MonthYearPopup
from screens import IODetail

from api_clients import OneOffAPI


class LedgerTable(Container):
    """Hold Table related components"""

    def __init__(self, table_data):
        super().__init__()
        self.table_content: list[list] = table_data

    def compose(self) -> ComposeResult:
        yield DataTable(id='data-table')

    def on_mount(self) -> None:
        table: DataTable = self.query_one(DataTable)
        table.zebra_stripes = True
        table.cursor_type = "row"

        if self.table_content == [[]]:
            table.add_column('Create new record to fill the table 🤭')
        else:
            table.add_columns(*self.table_content[0])
            table.add_rows(self.table_content[1:])


class Ledger(Container):
    """Main view wrapper"""
    DEFAULT_CSS = """
    #flow-section {
        layout: horizontal;
        width: 21%;
        align: left middle;
    }

    #type-section {
        layout: horizontal;
        width: 26%;
        align: left middle;
    }

    #date-section {
        layout: horizontal;
        width: 53%;
        align: right middle;
    }

    #month-button {
        color: $secondary;
    }

    #ledger-menu {
        layout: horizontal;
        height: 4;
    }

    #ledger-menu Button {
        min-width: 1;
    }

    #data-table {
        scrollbar-gutter: stable;
    }
    """
    ONE_OFF_API = OneOffAPI()
    MONTHS: list[str] = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]
    TODAY: datetime = datetime.now()
    year: int = TODAY.year
    month: int = TODAY.month
    endpoint_url: str = 'outflows/'

    def compose(self) -> ComposeResult:
        with Container(id='ledger-menu'):
            with Horizontal(id='flow-section'):
                yield Button('Outflows', id='outflows', variant='primary')
                yield Button('Inflows', id='inflows')

            with Horizontal(id='type-section'):
                yield Button('One-off', id='one-off', variant='primary')
                yield Button(' All ', id='all')
                yield Button('Recurring', id='recurring')

            with Horizontal(id='date-section'):
                yield Button('Prev Month', id='prev-month')
                yield Button(
                    f"{self.MONTHS[self.month - 1]} {self.year}",
                    id='month-button'
                )
                yield Button('Today', id='today')
                yield Button('Next Month', id='next-month')

        yield LedgerTable(table_data=self.request_table_data())

    @on(Button.Pressed, '#month-button')
    def month_button_pressed(self) -> None:
        """Handle press on month button and open months popup"""

        def update_table(date_tuple: tuple[int, int]) -> None:
            """Update table when month popup is dismissed and date has changed"""
            if (self.year, self.month) != date_tuple:
                self.year, self.month = date_tuple
                self.update_month_button_label()
                self.reload_table()

        popup: MonthYearPopup = MonthYearPopup(self.year, self.month)
        self.app.push_screen(popup, update_table)

    @on(Button.Pressed, '#outflows, #inflows')
    def flow_section_pressed(self, event: Button.Pressed) -> None:
        """
        Change the endpoint_url between 'inflows/' and 'outflows/'
        and reload ledger table
        """
        button: Button = event.button
        if button.variant == 'primary':
            return

        self.endpoint_url: Literal['outflows/', 'inflows/'] = 'inflows/' if button.id == 'inflows' else 'outflows/'
        self.update_button_variants(('outflows', 'inflows'), button)
        self.reload_table()

    @on(Button.Pressed, '#one-off, #all, #recurring')
    def type_section_pressed(self, event: Button.Pressed) -> None:
        """
        Change the type of flow to 'one-off', 'all', or 'recurring' based
        on the button pressed. TODO: Implement those types on backend
        """
        button: Button = event.button
        if button.variant == 'primary':
            return

        self.update_button_variants(('one-off', 'all', 'recurring'), button)
        self.reload_table()

    @on(Button.Pressed, '#prev-month, #next-month')
    def month_section_pressed(self, event: Button.Pressed) -> None:
        """
        Handle press on prev and next month buttons.
        Update the date displayed on the month button
        and reload the table to reflect the new date.
        """
        month_delta: int = -1 if event.button.id == 'prev-month' else 1
        self.month += month_delta
        if self.month == 0:
            self.year -= 1
            self.month = 12
        elif self.month == 13:
            self.year += 1
            self.month = 1
        self.update_month_button_label()
        self.reload_table()

    @on(Button.Pressed, '#today')
    def today_button_pressed(self) -> None:
        """
        Update the current date to today's date.
        Updates the date displayed on the month button
        and refreshes the table to reflect the new date.
        """
        if (self.year, self.month) == (self.TODAY.year, self.TODAY.month):
            return
        self.year, self.month = self.TODAY.year, self.TODAY.month
        self.update_month_button_label()
        self.reload_table()

    @on(DataTable.RowSelected)
    def open_popup_with_details(self, event: DataTable.RowSelected) -> None:
        """
        Open a popup with detailed information about a selected row in the DataTable.
        """

        def reload_table(code: str):
            """Reloads the DataTable if the given code is 'DELETE' or 'PATCH'."""
            if code != 'DELETE' and code != 'PATCH':
                return
            self.reload_table()

        row_key: RowKey = event.row_key
        table_row: list = self.query_one(DataTable).get_row(row_key)
        flow_data: dict = self.ONE_OFF_API.get_flow(self.endpoint_url, pk=table_row[1])
        self.app.push_screen(IODetail(flow_data, self.endpoint_url), reload_table)

    def request_table_data(self) -> list[tuple]:
        """
        Call Pulporo endpoint and return a 2D list representing table.
        Each row in the table is numbered sequentially starting from 1.
        If servers returns empty list return empty 2D list.
        """
        data: list[dict] = self.ONE_OFF_API.get_flow(
            endpoint=self.endpoint_url,
            param_dict={'year': self.year, 'month': self.month}
        )

        if not data:
            return [()]

        # Columns names are extracted from keys of first row (1st row of 2d array)
        formatted_table: list[tuple] = [('No', *[key.capitalize() for key in data[0]])]
        formatted_table.extend([(num, *row.values()) for num, row in enumerate(data, start=1)])
        return formatted_table

    def reload_table(self) -> None:
        """Remove and mount a new table to the ledger."""
        self.query_one(LedgerTable).remove()
        self.mount(LedgerTable(table_data=self.request_table_data()))

    def update_button_variants(self, list_of_ids: Sequence[str], bt: Button) -> None:
        """Change all buttons to default variant and the chosen button to primary."""
        for obj_id in list_of_ids:
            self.get_widget_by_id(obj_id).variant = 'default'
        bt.variant = 'primary'

    def update_month_button_label(self) -> None:
        """Updates the label of the month button."""
        new_name = f"{self.MONTHS[self.month - 1]} {self.year}"
        self.get_widget_by_id('month-button').label = new_name
