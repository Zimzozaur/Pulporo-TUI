from datetime import datetime

import pytest
from textual.containers import Container, Horizontal
from textual.widgets import Button

from screens import MonthYearPopup
from main import AppBody


MONTH_IDS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


@pytest.fixture
def popup():
    date = datetime.now()
    return MonthYearPopup(date.year, date.month)


async def test_pushing_popup_popup(popup):
    app = AppBody()
    async with app.run_test():
        await app.push_screen(popup)
        assert len(app.screen_stack) == 2


async def test_popup_popup_structure(popup):
    app = AppBody()
    async with app.run_test(size=(132, 33)):
        await app.push_screen(popup)
        assert popup.query_one('#month-popup-body', Container)
        assert len(popup.query(Horizontal)) == 4

        # Check if ids are correct
        year_buttons = ['prev-year', 'this-year', 'next-year']
        for year_button in year_buttons:
            button = popup.query_one(f"#{year_button}", Button)
            assert button.id == year_button, f"Button ID should be {year_button}"
            assert 'year-bt' in button.classes, f"Button {year_button} should have class 'year-bt'"

        for month_id in MONTH_IDS:
            button = popup.query_one(f"#{month_id}", Button)
            assert button.id == month_id, f"Button ID should be {month_id}"
            assert 'month-bt' in button.classes, f"Button {month_id} should have class 'month-bt'"

        # Check if the popup year button displays the correct year
        popup_year_button = popup.query_one("#this-year", Button)
        assert str(popup_year_button.label) == f'{datetime.now().year}'


async def test_coloring_on_mount(popup):
    app = AppBody()
    async with app.run_test(size=(132, 33)):
        await app.push_screen(popup)
        assert popup.query_one('#this-year', Button).variant == 'primary'
        month_id = MONTH_IDS[datetime.now().month - 1]
        assert popup.query_one(f'#{month_id}', Button).variant == 'primary'


async def test_month_button_returns_correct_date(popup):
    app = AppBody()
    date = datetime.now()
    async with app.run_test(size=(132, 33)) as pilot:
        def check_date(date_tuple: tuple):
            assert (date.year, date.month) == date_tuple

        await app.push_screen(popup, check_date)
        await pilot.click(f'#{MONTH_IDS[date.month - 1]}')


async def test_change_year_back(popup):
    app = AppBody()
    date = datetime.now()
    async with app.run_test(size=(132, 33)) as pilot:
        def check_date(date_tuple: tuple):
            assert date.year - 1 == date_tuple[0]
        await app.push_screen(popup, check_date)
        await pilot.click('#prev-year')
        await pilot.click(f'#{MONTH_IDS[date.month]}')


async def test_change_year_next(popup):
    app = AppBody()
    date = datetime.now()
    async with app.run_test(size=(132, 33)) as pilot:
        def check_date(date_tuple: tuple):
            assert date.year + 1 == date_tuple[0]
        await app.push_screen(popup, check_date)
        await pilot.click('#next-year')
        await pilot.click(f'#{MONTH_IDS[date.month]}')


async def test_change_this_year(popup):
    app = AppBody()
    date = datetime.now()
    async with app.run_test(size=(132, 33)) as pilot:
        def check_date(date_tuple: tuple):
            assert date.year == date_tuple[0]
        await app.push_screen(popup, check_date)
        await pilot.click('#next-year')
        await pilot.click('#this-year')
        await pilot.click(f'#{MONTH_IDS[date.month]}')