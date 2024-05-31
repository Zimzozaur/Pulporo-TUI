from datetime import datetime

from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Checkbox, Button, Static

from .custom_validators import (
    TitleMax50Validator,
    DateValidator
)
from fields.fields import NotBlinkingInput, NotBlinkingTextArea


class OutflowsForm(Static):
    DEFAULT_CSS = """
    #form-textarea {
        height: 6;
    }
    
    #form-action-buttons {
        height: auto;
        width: 1fr;
        margin-top: 1;
    }
    
    Static {
        width: 1fr;
    }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields: dict[str, NotBlinkingInput | Checkbox | NotBlinkingTextArea] = {
            'title': NotBlinkingInput(
                id='form-title', placeholder='Title',
                validators=[TitleMax50Validator()],
            ),
            'value': NotBlinkingInput(
                id='form-value', placeholder='Value',
                type='number',
                restrict=r'^(0|[1-9]\d{0,14})(\.\d{0,2})?$',
            ),
            'date': NotBlinkingInput(
                id='form-date', placeholder='Date YYYY-MM-DD',
                type='text', value=datetime.today().strftime('%Y-%m-%d'),
                restrict=r'^\d{0,4}-?\d{0,2}-?\d{0,2}$',
                validators=[DateValidator()],
            ),
            'prediction': Checkbox('Prediction', True, id='form-prediction'),
            'notes': NotBlinkingTextArea(id='form-textarea', show_line_numbers=True),
        }
        self.valid_fields: dict[str, bool] = {
            'form-title': False,
            'form-value': False,
            'form-date': False,
        }

    def compose(self) -> ComposeResult:
        yield self.fields['title']
        yield self.fields['value']
        yield self.fields['date']
        yield self.fields['prediction']
        yield self.fields['notes']
        with Horizontal(id='form-action-buttons'):
            yield Button('Cancel', variant='error', id='form-cancel-button')
            yield Static()
            yield Button('Submit', variant='success', id='form-submit-button', disabled=True)

    @on(NotBlinkingInput.Changed)
    def update_validation(self, event: NotBlinkingInput.Changed) -> None:
        if event.validation_result.is_valid:
            self.valid_fields[event.input.id] = True
        else:
            self.valid_fields[event.input.id] = False

        self.query_one('#form-submit-button').disabled = not self.is_form_valid()

    def is_form_valid(self):
        """Return is form valid """
        if all(self.valid_fields.values()):
            return True
        return False

    def form_to_dict(self) -> dict:
        """Return JSON representation of a form"""
        form_data = {
            'title': self.fields['title'].value,
            'value': self.fields['value'].value,
            'date': self.fields['date'].value,
            'prediction': self.fields['prediction'].value,
            'notes': self.fields['notes'].text,
        }

        return form_data

