from datetime import datetime
from typing import Literal

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
        self.table_data: list[list] = table_data

    def compose(self) -> ComposeResult:
        yield DataTable(id='data-table')

    def on_mount(self) -> None:
        table: DataTable = self.query_one(DataTable)
        table.zebra_stripes = True
        table.cursor_type = "row"

        if self.table_data == [[]]:
            table.add_column('Create new records to fill the table 🤭')
        else:
            table.add_columns(*self.table_data[0])
            table.add_rows(self.table_data[1:])


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

        def swap_table_to_new_update_month_button(date_tuple) -> None:
            """When month popup is dismissed and date has been changed - date_changed is True"""
            if self.year != date_tuple[0] or self.month != date_tuple[1]:
                self.year, self.month = date_tuple[0], date_tuple[1]
                self.reload_table()
                self.update_month_button_label()

        popup: MonthYearPopup = MonthYearPopup(year=self.year, month=self.month)
        self.app.push_screen(popup, swap_table_to_new_update_month_button)

    @on(Button.Pressed, '#outflows, #inflows')
    def flow_section_pressed(self, event: Button.Pressed) -> None:
        """
        Handle press on flow section button.

        Change the type of flow between 'inflows' and 'outflows' based on
        the button pressed. It updates the endpoint URL accordingly and swaps the table
        to reflect the new flow type.

        Args:
            event (Button.Pressed): The button press event.
        """
        button: Button = event.button
        if button.variant == 'primary':
            return
        self.endpoint_url: Literal['outflows/', 'inflows/'] = 'inflows/' if button.id == 'inflows' else 'outflows/'
        section = 'outflows', 'inflows'
        self.all_to_default_one_to_primary(section, button)
        self.reload_table()

    @on(Button.Pressed, '#one-off, #all, #recurring')
    def type_section_pressed(self, event: Button.Pressed) -> None:
        """
        Handle press on type section button.

        Change the type of flow to 'one-off', 'all', or 'recurring' based
        on the button pressed. TODO: Implement type type on backend

        Args:
            event (Button.Pressed): The button press event.
        """
        button: Button = event.button
        if button.variant == 'primary':
            return
        section = 'one-off', 'all', 'recurring'
        self.all_to_default_one_to_primary(section, button)
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
        if self.year == self.TODAY.year and self.month == self.TODAY.month:
            return
        self.year = self.TODAY.year
        self.month = self.TODAY.month
        self.update_month_button_label()
        self.reload_table()

    @on(DataTable.RowSelected)
    def open_popup_with_details(self, event: DataTable.RowSelected) -> None:
        """
        Open a popup with detailed information about a selected row in the DataTable.
        Provide a callback function to reload the table if a 'DELETE' or 'PATCH' action was performed.
        """

        def reload_table(code: str):
            """Reloads the DataTable if the given code is 'DELETE' or 'PATCH'."""
            if code != 'DELETE' and code != 'PATCH':
                return
            self.reload_table()

        key: RowKey = event.row_key
        table: DataTable = self.query_one(DataTable)
        row: list = table.get_row(key)

        flow_type: Literal['outflows/', 'inflows/'] = 'inflows/'
        if self.query_one('#outflows', Button).variant == 'primary':
            flow_type = 'outflows/'

        flow_data: dict = self.ONE_OFF_API.get_flow(endpoint=flow_type, pk=row[1])
        self.app.push_screen(IODetail(data=flow_data, flow_type=flow_type), reload_table)

    def request_table_data(self) -> list[list]:
        """
        Call Pulporo endpoint and return a 2D list representing table.
        Each row in the table is numbered sequentially starting from 1.
        If servers returns empty list return empty 2D list.
        """
        data = self.ONE_OFF_API.get_flow(
            endpoint=self.endpoint_url,
            param_dict={'year': self.year, 'month': self.month}
        )

        if not data:
            return [[]]

        headers: tuple = ('No', *data[0])
        formatted_table: list[list] = [[key.capitalize() for key in headers]]
        formatted_table.extend([[num, *row.values()] for num, row in enumerate(data, start=1)])
        return formatted_table

    def reload_table(self) -> None:
        """
        Remove and mount a new table to the ledger.

        This method removes the existing `LedgerTable` from the UI and mounts a new
        `LedgerTable` with updated data retrieved from `request_table_data()`.
        """
        self.query_one(LedgerTable).remove()
        self.mount(LedgerTable(table_data=self.request_table_data()))

    def all_to_default_one_to_primary(self, iterable, bt: Button) -> None:
        """
        Change all buttons to default variant and the chosen button to primary.

        This method sets the variant of all buttons in the given iterable to 'default'
        and sets the variant of the specified button to 'primary'.

        Args:
            iterable: An iterable of button IDs.
            bt (Button): The button to set as primary.
        """
        for obj_id in iterable:
            self.get_widget_by_id(obj_id).variant = 'default'
        bt.variant = 'primary'

    def update_month_button_label(self) -> None:
        """Updates the label of the month button."""
        new_name = f"{self.MONTHS[self.month - 1]} {self.year}"
        self.get_widget_by_id('month-button').label = new_name
