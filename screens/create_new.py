from collections import namedtuple

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

from forms import OutflowsForm, InflowsForm


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
    
    #popup-title {
        text-style: bold;
        text-align: center;
        width: 100%;
    }
    
    #form-list-wrapper {
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
        OptionT = namedtuple('OptionT', 'form_class endpoint')
        self.forms_dict: dict[str, OptionT] = {
            'outflow-one-off': OptionT(OutflowsForm, 'outflows/'),
            'inflow-one-off': OptionT(InflowsForm, 'inflows/'),
        }

    def compose(self) -> ComposeResult:
        with Container(id='new-popup-body'):
            with Center():
                yield Static("CREATE NEW", id='popup-title')
            with Center():
                with VerticalScroll(id='form-list-wrapper'):
                    yield OptionList(*self.options, id="form-list")

    def on_click(self, event: Click):
        """Close popup when clicked on the background"""
        if self.get_widget_at(event.screen_x, event.screen_y)[0] is self and not self.form:
            self.dismiss()

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        """Mount selected form from OptionList to popup"""
        selected_form_id: str = event.option.id
        self.query_one('#form-list').remove()
        self.form = self.forms_dict[selected_form_id].form_class('Create', id='popup-form')
        self.form_name = selected_form_id
        self.form_default_data = self.form.form_to_dict()
        self.query_one('#form-list-wrapper').mount(self.form)

    @on(Button.Pressed, '#form-submit-button')
    def send_request(self) -> None:
        """Send request and remove form from DOM when accepted"""
        f_name = self.form_name  # shorter names for better readability
        f_dict = self.forms_dict

        form = self.query_one(f_dict[f_name].form_class)
        self.one_off_api.post_flow(f_dict[f_name].endpoint, form.form_to_dict())
        self.remove_form_from_dom()

    @on(Button.Pressed, '#form-cancel-button')
    def remove_form_from_dom(self) -> None:
        """Remove form from dom on cancel button click"""
        self.query_one('#popup-form').remove()
        option_list = OptionList(*self.options, id="form-list")
        self.query_one('#form-list-wrapper').mount(option_list)
        self.form = None

