from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Input, Checkbox, TextArea, Button, Static


class OutflowsForm(Static):
    DEFAULT_CSS = """
    #form-textarea {
        height: 6;
    }
    
    #form-action-buttons {
        height: auto;
        margin-top: 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Input(id='form-title', placeholder='Title')
        yield Input(id='form-value', placeholder='Value')
        yield Input(id='form-date', placeholder='Date DD-MM-YYYY')
        yield Checkbox('Prediction', True, id='form-prediction')
        yield TextArea(id='form-textarea', show_line_numbers=True)
        with Horizontal(id='form-action-buttons'):
            yield Button('Cancel', variant='error', id='form-cancel-button')
            yield Button('Submit', variant='success', id='form-submit-button')
