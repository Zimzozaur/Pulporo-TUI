import json
from datetime import datetime

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
        self.fields = {
            'title': NotBlinkingInput(
                id='form-title', placeholder='Title',
                validators=[TitleMax50Validator()]
            ),

            'value': NotBlinkingInput(
                id='form-value', placeholder='Value',
                type='number',
                restrict=r'^(0|[1-9]\d{0,14})(\.\d{0,2})?$',
            ),
            'date': NotBlinkingInput(
                id='form-date', placeholder='Date DD-MM-YYYY',
                type='text', value=datetime.today().strftime('%-d-%-m-%Y'),
                restrict=r'^\d{0,2}-?\d{0,2}-?\d{0,4}$',
                validators=[DateValidator()],
            ),
            'prediction': Checkbox('Prediction', True, id='form-prediction'),
            'notes': NotBlinkingTextArea(id='form-textarea', show_line_numbers=True),
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
            yield Button('Submit', variant='success', id='form-submit-button')

    def form_valid(self):
        """Return is form valid """
        for field in self.fields.values():
            if not isinstance(self.fields, NotBlinkingTextArea) or not field.is_valid:
                return False
        return True

    def form_to_json(self):
        """Return JSON representation of a form"""
        form_data = {
            'title': self.fields['title'].value,
            'value': self.fields['value'].value,
            'date': self.fields['date'].value,
            'prediction': self.fields['prediction'].value,
            'notes': self.fields['notes'].text,
        }
        return json.dumps(form_data)

