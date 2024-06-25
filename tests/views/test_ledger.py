from datetime import datetime
import pytest

from textual.containers import Container, Center, VerticalScroll, Horizontal
from textual.widgets import Static, OptionList, DataTable, Button
from textual.widgets.data_table import ColumnKey
from textual.app import App

from screens import MonthYearPopup, IODetail
from views.ledger import LedgerTable, Ledger
from main import AppBody


MONTHS: list[str] = [
    "Dummy_month_to_start_form_index_1",
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]


async def test_empty_ledger_table():
    app = App()
    async with app.run_test():
        await app.mount(LedgerTable([[]]))
        data_table = app.query_one(DataTable)
        assert data_table.row_count == 0

        column_keys = list(data_table.columns.keys())
        label = 'Create new record to fill the table 🤭'
        assert str(data_table.columns[column_keys[0]].label) == label


async def test_populated_ledger_table():
    app = App()
    async with app.run_test():
        await app.mount(LedgerTable([[1, 2], [3, 4]]))
        data_table = app.query_one(DataTable)
        column_keys = list(data_table.columns.keys())
        assert str(data_table.columns[column_keys[0]].label) == '1'
        assert str(data_table.columns[column_keys[1]].label) == '2'

        table_row = data_table.get_row_at(0)
        assert table_row[0] == 3
        assert table_row[1] == 4


async def test_ledger_structure():
    app = App()
    async with app.run_test():
        await app.mount(Ledger())
        assert len(app.query(Horizontal)) == 3
        today = datetime.now()
        buttons = [
            ('Outflows', 'outflows'),
            ('Inflows', 'inflows'),
            ('One-off', 'one-off'),
            ('All', 'all'),
            ('Recurring', 'recurring'),
            ('Prev Month', 'prev-month'),
            (f'{MONTHS[today.month]} {today.year}', 'month-button'),
            ('Today', 'today'),
            ('Next Month', 'next-month')
        ]

        for bt_name, bt_id in buttons:
            button = app.query_one(f'#{bt_id}', Button)
            assert str(button.label).strip() == bt_name


# TODO: Test button presses

