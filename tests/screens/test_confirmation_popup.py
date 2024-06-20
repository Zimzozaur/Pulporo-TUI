import pytest
from textual.containers import Container, Horizontal
from textual.widgets import Static, Button

from screens import ConfirmPopup
from main import AppBody


@pytest.fixture
def confirm_popup():
    return ConfirmPopup(message="Are you sure?")


@pytest.mark.asyncio
async def test_pushing_create_new(confirm_popup):
    app = AppBody()
    async with app.run_test():
        await app.push_screen(confirm_popup)
        assert len(app.screen_stack) == 2


@pytest.mark.asyncio
async def test_confirm_popup_structure(confirm_popup):
    app = AppBody()
    async with app.run_test():
        await app.push_screen(confirm_popup)

        assert confirm_popup.query_one('#confirm-popup-body', Container)
        assert str(confirm_popup.query_one('#confirm-popup-message', Static).renderable) == "Are you sure?"
        assert confirm_popup.query_one('#confirm-popup-buttons', Horizontal)

        assert str(confirm_popup.query_one("#no-button", Button).label) == "No"
        assert confirm_popup.query_one("#no-button", Button).variant == 'error'
        assert str(confirm_popup.query_one("#yes-button", Button).label) == "Yes"
        assert confirm_popup.query_one("#yes-button", Button).variant == 'success'


@pytest.mark.asyncio
async def test_reject_method(confirm_popup):
    app = AppBody()
    async with app.run_test() as pilot:
        def check_callback(boolean: bool):
            assert boolean is False

        await app.push_screen(confirm_popup, check_callback)
        await pilot.click('#no-button')


@pytest.mark.asyncio
async def test_confirm_method(confirm_popup):
    app = AppBody()
    async with app.run_test() as pilot:
        def check_callback(boolean: bool):
            assert boolean is True

        await app.push_screen(confirm_popup, check_callback)
        await pilot.click('#yes-button')

