from textual import on
from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll, Center
from textual.events import Click
from textual.screen import ModalScreen
from textual.widgets import (
    Button,
    OptionList,
    Label
)
from textual.widgets.option_list import Option, Separator

from forms.form import OutflowsForm, InflowsForm
from api_clients.api_client import OneOffClient


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
    
    #show-forms {
        margin-top: 1;
        width: 70%;
    }
    
    #list-form-wrapper {
        margin-top: 1;
        width: 90%;
        height: 32;
        padding-bottom: 2;
    }
    
    #list-form-wrapper > OutflowsForm > * {
        margin-bottom: 1;
    }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = OneOffClient()
        self.toggle_list = False
        self.toggle_form = False
        self.current_form = None
        self.options = [
            Option('Outflow One-off', id='outflow-one-off'),
            Separator(),
            Option('Inflow One-off', id='inflow-one-off'),
        ]

    def compose(self) -> ComposeResult:
        with Container(id='new-popup-body'):
            with Center():
                yield Label("CREATE NEW", id='header-title')
            with Center():
                yield Button('Show forms', id='show-forms')
            with Center():
                with VerticalScroll(id='list-form-wrapper'):
                    pass

    def on_click(self, event: Click):
        """Close popup when clicked on the background"""
        if self.get_widget_at(event.screen_x, event.screen_y)[0] is self:
            self.dismiss(False)

    @on(Button.Pressed, '#show-forms')
    def toggle_list_display(self) -> None:
        """Toggle the visibility of the form list when the button is pressed"""
        self.toggle_list = not self.toggle_list

        if self.toggle_form:
            self.toggle_form = False
            self.query_one('#popup-form').remove()

        if self.toggle_list:
            self.query_one('#show-forms').variant = 'primary'
            forms_list = self.query_one("#list-form-wrapper")
            forms_list.mount(OptionList(*self.options, id="choose-form"))
        else:
            self.query_one('#show-forms').variant = 'default'
            self.query_one('#choose-form').remove()

    @on(Button.Pressed, '#form-cancel-button')
    def remove_form_from_dom(self) -> None:
        """Remove form from dom on cancel button click"""
        self.query_one('#popup-form').remove()
        self.query_one('#show-forms').disabled = False
        self.toggle_form = False
        self.toggle_list_display()

    @on(Button.Pressed, '#form-submit-button')
    def remove_form_from_dom(self) -> None:
        """Send request and remove form from DOM when accepted"""
        match self.current_form:
            case 'outflow-one-off':
                form = self.query_one(OutflowsForm)
                self.api.post_flow('outflows/', form.form_to_dict())
            case 'inflow-one-off':
                form = self.query_one(InflowsForm)
                self.api.post_flow('inflows/', form.form_to_dict())

        self.current_form = None

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        """Called when Option is clicked"""

        self.toggle_list = False
        self.toggle_form = True
        selected_option = event.option.id
        show_form_bt = self.query_one('#show-forms')
        show_form_bt.variant = 'default'
        show_form_bt.disabled = True
        self.query_one('#choose-form').remove()

        match selected_option:
            case 'outflow-one-off':
                self.current_form = 'outflow-one-off'
                self.query_one('#list-form-wrapper').mount(OutflowsForm(id='popup-form'))
            case 'inflow-one-off':
                self.current_form = 'inflow-one-off'
                self.query_one('#list-form-wrapper').mount(InflowsForm(id='popup-form'))

