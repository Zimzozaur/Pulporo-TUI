from typing import Literal

from requests import Response
from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Center, VerticalScroll
from textual.events import Click
from textual.screen import ModalScreen
from textual.widgets import Static, Button

from forms import OutflowsForm, InflowsForm, NotBlinkingInput
from api_clients import OneOffAPI
from screens import ConfirmPopup


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
    FORMS_DICT: dict = {
        'outflows/': OutflowsForm,
        'inflows/': InflowsForm,
    }

    def __init__(self, data: dict, flow_type: Literal['outflows/', 'inflows/'], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = OneOffAPI()
        self.flow_type: Literal['outflows/', 'inflows/'] = flow_type
        self.pk = data.pop('id')
        self.form = self.FORMS_DICT[flow_type]('Update', json=data)
        self.form_default_data: dict = self.form.form_to_dict()  # Holds form value from initialization

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
        background_click = self.get_widget_at(event.screen_x, event.screen_y)[0] is self
        form_not_changed = self.form_default_data == self.form.form_to_dict()
        if background_click and form_not_changed:
            self.dismiss()

    @on(Button.Pressed, '#form-cancel-button')
    def close_popup(self) -> None:
        """Close popup on cancel button click"""
        self.dismiss()

    @on(Button.Pressed, '#form-submit-button')
    def patch_io(self) -> None:
        """Send PATCH request for IO and send back `PATCH` string"""
        json: dict = self.form.form_to_dict()
        pk = f'{self.pk}/'
        response: Response = self.api.patch_flow(endpoint=self.flow_type, json=json, pk=pk)
        if response.status_code == 200:
            self.dismiss('PATCH')

    @on(Button.Pressed, '#delete-io')
    def delete_io(self) -> None:
        """
        Display Confirmation Popup to double-check does user want to remove IO
        if yes - send DELETE request, reload ledger and close popup
        else - just close the confirmation popup
        """
        def delete_io(accepted: bool) -> None:
            """Send DELETE request for IO and send back `PATCH` string"""
            if not accepted:
                return
            response: Response = self.api.delete_flow(self.flow_type, f'{self.pk}/')
            if response.status_code == 204:
                self.dismiss('DELETE')

        message = 'Do you want to remove this flow?\nYou cannot revers this action.'
        self.app.push_screen(ConfirmPopup(message=message), delete_io)

    @on(NotBlinkingInput.Changed)
    def update_validation(self) -> None:
        """Disallow user to send PATCH request when form was not changed"""
        if self.form_default_data == self.form.form_to_dict():
            self.query_one('#form-submit-button').disabled = True

