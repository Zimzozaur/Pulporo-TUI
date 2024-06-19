from textual import on
from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll, Center
from textual.events import Click
from textual.screen import ModalScreen
from textual.widgets import (
    Button,
    OptionList,
    Static
)
from textual.widgets.option_list import Option, Separator

from api_clients import OneOffAPI

from forms import OutflowsForm, InflowsForm, NotBlinkingInput
from . import ConfirmPopup


class CreateNewPopup(ModalScreen):
    DEFAULT_CSS = """
    CreateNewPopup {
        align: center middle;
        width: auto;
        height: auto;
    }
    
    #new-popup-body {
        padding: 1 0;
        min-width: 70;
        min-height: 40;
        padding-top: 1;
        width: 70;
        height: 40;
        background: $surface-lighten-1;
    }
    
    #header-title {
        text-style: bold;
        text-align: center;
        width: 100%;
    }
    
    #list-form-wrapper {
        margin-top: 1;
        width: 90%;
        height: 32;
        padding-bottom: 2;
    }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.one_off_api = OneOffAPI()
        self.form = None
        self.form_name: str = ''
        self.form_default_data = None
        self.options = [
            Option('Outflow One-off', id='outflow-one-off'),
            Separator(),
            Option('Inflow One-off', id='inflow-one-off'),
        ]

    def compose(self) -> ComposeResult:
        with Container(id='new-popup-body'):
            with Center():
                yield Static("CREATE NEW", id='header-title')
            with Center():
                with VerticalScroll(id='list-form-wrapper'):
                    yield OptionList(*self.options, id="choose-form")

    def on_click(self, event: Click):
        """Close popup when clicked on the background"""
        def dismiss_on_true(dismiss: bool):
            if dismiss:
                self.dismiss()

        clicked_outside_form = self.get_widget_at(event.screen_x, event.screen_y)[0] is self

        if clicked_outside_form and not self.form:
            # Form was not chosen
            self.dismiss()
        elif clicked_outside_form and not self.is_form_changed():
            # Form was not changed
            self.dismiss()
        elif clicked_outside_form and self.is_form_changed():
            message = 'Do you want to close form?'
            self.app.push_screen(ConfirmPopup(message=message), dismiss_on_true)

    @on(Button.Pressed, '#form-cancel-button')
    def remove_form_from_dom(self) -> None:
        """Remove form from dom on cancel button click"""
        self.query_one('#popup-form').remove()
        option_list = OptionList(*self.options, id="choose-form")
        self.query_one('#list-form-wrapper').mount(option_list)
        self.form = None

    @on(Button.Pressed, '#form-submit-button')
    def send_request(self) -> None:
        """Send request and remove form from DOM when accepted"""
        match self.form_name:
            case 'outflow-one-off':
                form = self.query_one(OutflowsForm)
                self.one_off_api.post_flow('outflows/', form.form_to_dict())
            case 'inflow-one-off':
                form = self.query_one(InflowsForm)
                self.one_off_api.post_flow('inflows/', form.form_to_dict())

        self.remove_form_from_dom()

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        """Called when Option is clicked"""
        selected_option = event.option.id
        self.query_one('#choose-form').remove()

        match selected_option:
            case 'outflow-one-off':
                self.form = OutflowsForm(id='popup-form')
            case 'inflow-one-off':
                self.form = InflowsForm(id='popup-form')

        self.form_name = selected_option
        self.form_default_data = self.form.form_to_dict()
        self.query_one('#list-form-wrapper').mount(self.form)

    @on(NotBlinkingInput.Changed)
    def is_form_changed(self) -> bool:
        if self.form_default_data == self.form.form_to_dict():
            return False
        return True

