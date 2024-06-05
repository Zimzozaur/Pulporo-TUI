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

from screens.month_year_popup import MonthYearPopup
from screens.io_detail import IODetail

from utils.date_time import format_date_string

from api_clients.api_client import OneOffClient


class LedgerTable(Container):
    """Hold Table related components"""

    def __init__(self, table_data):
        super().__init__()
        self.table_data: list[dict] = table_data

    def compose(self) -> ComposeResult:
        yield DataTable(id='data-table')

    def on_mount(self) -> None:
        table: DataTable = self.query_one(DataTable)
        table.zebra_stripes = True
        table_data: list[dict] = self.table_data
        if table_data == [[]]:
            table.add_column('Create new records to fill the table 🤭')
        else:
            table.add_columns(*table_data[0])
            table.add_rows(table_data[1:])
            table.cursor_type = "row"


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
    
    
    Table {
        height: 1fr;
        width: 1fr;
    }
    """

    MONTHS: list[str] = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]
    TODAY: datetime = datetime.now()
    date: dict = {
        'year': TODAY.year,
        'month': TODAY.month,
    }
    endpoint_url: str = 'outflows/'

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.one_off_api = OneOffClient()

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
                    f"{self.MONTHS[self.date['month'] - 1]} {self.date['year']}",
                    id='month-button'
                )
                yield Button('Today', id='today')
                yield Button('Next Month', id='next-month')

        yield LedgerTable(table_data=self.request_table_data())

    @on(Button.Pressed, '#month-button')
    def month_button_pressed(self) -> None:
        """Handle press on month button and open months popup"""
        def swap_table_to_new_update_month_button(date_changed: bool) -> None:
            """When month popup is dismissed and date has been changed - date_changed is True"""
            if date_changed:
                self.remove_and_mount_new_table()
                self.change_date_on_month_button()

        popup: MonthYearPopup = MonthYearPopup(self.date)
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
        self.remove_and_mount_new_table()

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
        self.remove_and_mount_new_table()

    @on(Button.Pressed, '#prev-month, #next-month')
    def month_section_pressed(self, event: Button.Pressed) -> None:
        """
        Handle press on prev and next month buttons.

        Update the current month and year based on the button pressed
        ('prev-month' or 'next-month'). It then updates the date displayed on the month
        button and refreshes the table to reflect the new date.

        Args:
            event (Button.Pressed): The button press event.
        """
        button: Button = event.button
        month_operation: int = -1 if button.id == 'prev-month' else 1
        self.date['month'] += month_operation
        if self.date['month'] == 0:
            self.date['year'] -= 1
            self.date['month'] = 12
        elif self.date['month'] == 13:
            self.date['year'] += 1
            self.date['month'] = 1
        self.change_date_on_month_button()
        self.remove_and_mount_new_table()

    @on(Button.Pressed, '#today')
    def today_button_pressed(self) -> None:
        """
        Handle press on today button.

        Update the current date to today's date. It then updates the date
        displayed on the month button and refreshes the table to reflect the new date.
        """
        if self.date['year'] == self.TODAY.year and self.date['month'] == self.TODAY.month:
            return
        self.date['year'] = self.TODAY.year
        self.date['month'] = self.TODAY.month
        self.change_date_on_month_button()
        self.remove_and_mount_new_table()

    @on(DataTable.RowSelected)
    def open_popup_with_details(self, event: DataTable.RowSelected) -> None:
        """
        Open a popup with I/O details.

        Handle the event when a row in the DataTable is selected. It retrieves
        the details of the selected row and opens a popup displaying the I/O details.

        Args:
            event (DataTable.RowSelected): The row selection event.
        """
        key: RowKey = event.row_key
        table: DataTable = self.query_one(DataTable)
        row: list = table.get_row(key)
        self.app.push_screen(IODetail(data=row))

    def request_table_data(self) -> list[list]:
        """
        Call Pulporo endpoint and return a list to render table.

        Make a request to the Pulporo API endpoint to retrieve data for
        the table. It formats the data into a list of lists suitable for display in
        the DataTable. Each row includes a formatted date string for the last two columns.

        Returns:
            list[list]: A list of lists representing the table data.
        """
        list_of_dicts = self.one_off_api.get_flow(
            endpoint=self.endpoint_url,
            param_dict=self.date
        )

        # Escape if there is no data
        if not list_of_dicts:
            return [[]]

        column_labels: tuple = ('No', *list_of_dicts[0])
        table_data: list[list] = [[key.capitalize() for key in column_labels]]

        table: list[list] = [[num, *d.values()] for num, d in enumerate(list_of_dicts, start=1)]
        for row in table:
            row[-1] = format_date_string(row[-1])
            row[-2] = format_date_string(row[-2])

        table_data.extend(table)
        return table_data

    def remove_and_mount_new_table(self) -> None:
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

    def change_date_on_month_button(self) -> None:
        """
        Change the date displayed on the month button.

        This method updates the label of the month button to reflect the current month
        and year based on `self.date`.
        """
        new_name = f"{self.MONTHS[self.date['month'] - 1]} {self.date['year']}"
        self.get_widget_by_id('month-button').label = new_name


if __name__ == '__main__':
    from main import AppBody
    app = AppBody()
    ledger = Ledger()
    ledger.request_table_data()

