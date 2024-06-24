import pytest

from textual.widgets import Button

from main import AppBody
from screens import CreateNewPopup
from views import Ledger, Media


################################################
#              Testing Bindings                #
################################################

async def test_toggle_left_panel(mocker):
    app = AppBody()
    mocker.patch.object(Ledger, 'request_table_data', return_value=[[]])

    async with app.run_test() as pilot:
        body = app.query_one('#body')
        left = app.query_one('#left-menu')
        main = app.query_one('#main-app')

        assert not body.has_class('-hidden-margin')
        assert not left.has_class('-hidden')
        assert not main.has_class('-hidden-margin')

        await pilot.press('ctrl+o')

        assert body.has_class('-hidden-margin')
        assert left.has_class('-hidden')
        assert main.has_class('-hidden-margin')


async def test_create_new(mocker):
    app = AppBody()
    mocker.patch.object(Ledger, 'request_table_data', return_value=[[]])

    async with app.run_test() as pilot:
        assert len(app.screen_stack) == 1
        await pilot.press('ctrl+n')
        assert len(app.screen_stack) == 2
        screen = app.screen_stack[1]
        assert isinstance(screen, CreateNewPopup)


################################################
#            Testing LeftNavMenu               #
################################################


async def test_on_mount(mocker):
    app = AppBody()
    mocker.patch.object(Ledger, 'request_table_data', return_value=[[]])

    async with app.run_test(size=(132, 33)):
        assert app.query_one('#LedgerBt', Button).variant == 'primary'


view_buttons = (
    ('DashboardBt', 'Dashboard'),
    ('LedgerBt', 'Ledger'),
    ('RecurringBt', 'Recurring'),
    ('InvestmentBt', 'Investment'),
    ('LiabilitiesBt', 'Liabilities'),
    ('RemindersBt', 'Reminders'),
    ('MediaBt', 'Media')
)


@pytest.mark.parametrize('left_menu_button, el_class', view_buttons)
async def test_open_view_and_check_button(left_menu_button, el_class, mocker):
    app = AppBody()
    mocker.patch.object(Ledger, 'request_table_data', return_value=[[]])

    def compose_mock():
        yield Button(label="Mock Button")

    mocker.patch.object(Media, 'compose', side_effect=compose_mock)

    async with app.run_test(size=(132, 33)) as pilot:
        await pilot.click(f'#{left_menu_button}')
        assert app.query_one(f'#{el_class}')
        assert app.query_one(f'#{left_menu_button}', Button).variant == 'primary'
