from typing import Literal

from requests import Response
from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Center, VerticalScroll
from textual.events import Click
from textual.screen import ModalScreen
from textual.widgets import Static, Button

from fields.fields import NotBlinkingInput
from forms.form import OutflowsForm, InflowsForm
from api_clients.api_client import OneOffAPI
from screens.confirmation_popup import ConfirmPopup


class IODetail(ModalScreen):
    """
    Modal screen that shows all IOs detail
    and allow to delete or patch it
    """

    DEFAULT_CSS = """
    IODetail {
        align: center middle;
        width: auto;
        height: auto;
    }

    #io-detail-body {
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
    
    #detail-form-wrapper {
        margin-top: 1;
        width: 90%;
        height: 36;
        padding-bottom: 2;
    }
    
    #delete-io {
        margin-top: 1;
    }
    """

    def __init__(self, *args, data: dict, flow_type: Literal['outflows/', 'inflows/'], **kwargs):
        super().__init__(*args, **kwargs)
        self.api = OneOffAPI()
        self.flow_type: Literal['outflows/', 'inflows/'] = flow_type
        self.pk = data.pop('id')
        self.data = data

        if self.flow_type == 'outflows/':
            self.form: OutflowsForm = OutflowsForm(**self.data)
        else:
            self.form: InflowsForm = InflowsForm(**self.data)

        self.form_default_data: dict = self.form.form_to_dict()  # Holds from initialization

    def compose(self) -> ComposeResult:
        with Container(id='io-detail-body'):
            with Center():
                yield Static('UPDATE FLOW', id='header-title')
            with Center():
                with VerticalScroll(id='detail-form-wrapper'):
                    yield self.form
                    with Center():
                        yield Button('Delete', 'error', id='delete-io')

    def on_click(self, event: Click):
        """Close popup when clicked on the background"""
        if self.get_widget_at(event.screen_x, event.screen_y)[0] is self:
            self.dismiss()

    @on(Button.Pressed, '#form-cancel-button')
    def remove_form_from_dom(self) -> None:
        """Close popup on cancel button click"""
        self.dismiss()

    @on(Button.Pressed, '#form-submit-button')
    def patch_io(self) -> None:
        """
        Send PATCH request for IO if accepted is True
        and send back `PATCH` string with dismiss() method
        """
        json: dict = self.form.form_to_dict()
        pk = f'{self.pk}/'
        response: Response = self.api.patch_flow(endpoint=self.flow_type, json=json, pk=pk)
        if response.status_code == 200:
            self.dismiss('PATCH')

    @on(Button.Pressed, '#delete-io')
    def delete_button(self) -> None:
        """
        Display Confirmation Popup to double-check does user want to remove IO
        if yes - send DELETE request, reload ledger and close popup
        else - just close the confirmation popup

        """
        message = 'Do you want to remove this flow?\nYou cannot revers this action.'
        self.app.push_screen(ConfirmPopup(message=message), self.delete_io)

    def delete_io(self, accepted: bool) -> None:
        """
        Send DELETE request for IO if accepted is True
        and send back `DELETE` string with dismiss() method
        """
        if not accepted:
            return
        pk = f'{self.pk}/'
        response: Response = self.api.delete_flow(self.flow_type, pk)
        if response.status_code == 204:
            self.dismiss('DELETE')

    @on(NotBlinkingInput.Changed)
    def update_validation(self) -> None:
        """Disallow user to send PATCH request when form was not changed"""
        if self.form_default_data == self.form.form_to_dict():
            self.query_one('#form-submit-button').disabled = True

