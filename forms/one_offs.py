from datetime import datetime

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Input, Checkbox, TextArea, Button, Static


from .custom_validators import (
    TitleMax50Validator,
    DateValidator
)
from fields.input import NotBlinkingInput, NotBlinkingTextArea


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

    def compose(self) -> ComposeResult:
        yield NotBlinkingInput(
            id='form-title', placeholder='Title',
            validators=[TitleMax50Validator()]
        )
        yield NotBlinkingInput(
            id='form-value', placeholder='Value',
            type='number',
            restrict=r'^(0|[1-9]\d{0,14})(\.\d{0,2})?$',
        )
        yield NotBlinkingInput(
            id='form-date', placeholder='Date DD-MM-YYYY',
            type='text', value=datetime.today().strftime('%-d-%-m-%Y'),
            restrict=r'^\d{0,2}-?\d{0,2}-?\d{0,4}$',
            validators=[DateValidator()],
        )
        yield Checkbox('Prediction', True, id='form-prediction')
        yield NotBlinkingTextArea(id='form-textarea', show_line_numbers=True)
        with Horizontal(id='form-action-buttons'):
            yield Button('Cancel', variant='error', id='form-cancel-button')
            yield Static()
            yield Button('Submit', variant='success', id='form-submit-button')
