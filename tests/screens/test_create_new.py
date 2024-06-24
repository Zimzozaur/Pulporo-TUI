import pytest

from textual.containers import Container, Center, VerticalScroll
from textual.widgets import Static, OptionList
from textual.app import App

from screens import CreateNewPopup


@pytest.fixture
def create_new():
    return CreateNewPopup()


async def test_pushing_create_new(create_new):
    app = App()
    async with app.run_test():
        await app.push_screen(create_new)
        assert len(app.screen_stack) == 2


async def test_create_new_structure(create_new):
    app = App()
    async with app.run_test():
        await app.push_screen(create_new)
        assert create_new.query_one('#new-popup-body', Container)

        children = create_new.query_one('#new-popup-body', Container).children
        for child in children:
            assert isinstance(child, Center)

        assert str(create_new.query_one('#popup-title', Static).renderable) == "CREATE NEW"
        assert create_new.query_one('#form-list-wrapper', VerticalScroll)
        assert create_new.query_one('#form-list', OptionList)


async def test_click_on_background_dismiss(create_new):
    app = App()
    async with app.run_test(size=(132, 33)) as pilot:
        assert len(app.screen_stack) == 1

        await app.push_screen(create_new)
        assert len(app.screen_stack) == 2

        await pilot.click(offset=(1, 1))
        assert len(app.screen_stack) == 1


