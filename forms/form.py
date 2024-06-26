from datetime import datetime
from typing import Literal, TYPE_CHECKING

from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Checkbox, Button, Static

from .custom_validators import (
    TitleMax50Validator,
    DateValidator,
    ValueValidator
)
from .fields import NotBlinkingTextArea, NotBlinkingInput
from utils import format_date_string

if TYPE_CHECKING:
    from utils.data_types import JsonDict, FormField


class BaseFormWidget(Static):
    """
    A base class for form widgets providing common functionality and layout.

    Attributes:
        DEFAULT_CSS (str): Default CSS for the widget.
        FIELD_TYPES (dict): Mapping of field types to their respective classes and arguments.
        FORM_FIELDS (dict): Fields to be included in the form.
        REQUIRED_FIELDS (list): List of required fields.
    """
    DEFAULT_CSS = """  
    Static {
        width: 1fr;
    }

    NotBlinkingInput, NotBlinkingTextArea, Checkbox {
        margin-bottom: 1;
    }    

    NotBlinkingTextArea {
        min-height: 6;
        height: 6;
    }

    #form-action-buttons {
        height: auto;
        width: 1fr;
        margin-top: 1;
        padding: 0 1;
    }
    """
    FIELD_TYPES: dict[str, tuple] = {
        'title_field': (
            NotBlinkingInput, {
                'placeholder': 'Title',
                'validators': [TitleMax50Validator()],
                'restrict': r'^.{0,50}$'
            }
        ),
        'value_field': (
            NotBlinkingInput, {
                'placeholder': 'Value',
                'validators': [ValueValidator()],
                'restrict': r'^(0|[1-9]\d{0,14})(\.\d{0,2})?$',
            }
        ),
        'date_field': (
            NotBlinkingInput, {
                'placeholder': 'Date YYYY-MM-DD',
                'type': 'text',
                'value': datetime.today().strftime('%Y-%m-%d'),
                'restrict': r'^\d{0,4}-?\d{0,2}-?\d{0,2}$',
                'validators': [DateValidator()],
            }
        ),
        'checkbox_field': (
            Checkbox, {
                'label': 'Prediction',
                'value': True,
            }
        ),
        'notes_field': (
            NotBlinkingTextArea, {}
        ),
    }

    FORM_FIELDS: tuple[tuple[str, str], ...]
    REQUIRED_FIELDS: tuple[str, ...]

    def __init__(
        self,
        submit_button_name: Literal['Create', 'Update'],
        json: dict | None = None,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.submit_button_name: str = submit_button_name
        self.fields: dict[str, FormField] = {}
        self.required_fields: dict[str, bool] = {}
        self.json = json

        if self.json:
            self.creation_date = self.json.pop('creation_date', None)
            self.last_modification = self.json.pop('last_modification', None)

        self.create_fields()
        self.create_required_fields()

    def create_fields(self) -> None:
        """Create and populate the fields based on FORM_FIELDS."""
        for field_name, field_type in self.FORM_FIELDS:
            field_class, arguments = self.FIELD_TYPES[field_type]
            field: FormField = field_class(**arguments)
            field.id = field_name
            self.fields[field_name] = field
            if self.json:
                if not isinstance(field, NotBlinkingTextArea):
                    field.value = self.json.get(field_name, '')
                else:
                    field.text = self.json.get(field_name, '')

    def create_required_fields(self):
        """Create the list of required fields."""
        for field_name in self.REQUIRED_FIELDS:
            self.required_fields[field_name] = False

    def form_to_dict(self) -> 'JsonDict':
        """Return a dictionary representation of the form."""
        form_data: JsonDict = {}
        for field_name, field in self.fields.items():
            field_value = field.text if isinstance(field, NotBlinkingTextArea) else field.value
            form_data[field_name] = field_value

        return form_data

    def compose(self) -> ComposeResult:
        for field in self.fields.values():
            yield field

        if self.json is not None:
            yield Static()
            yield Static(f'Creation Date: {format_date_string(self.creation_date)}')
            yield Static(f'Last Modification: {format_date_string(self.last_modification)}')
        with Horizontal(id='form-action-buttons'):
            yield Button('Cancel', variant='warning', id='form-cancel-button')
            yield Static()
            yield Button(f'{self.submit_button_name}', variant='success', id='form-submit-button', disabled=True)

    @on(NotBlinkingInput.Changed)
    def update_required_fields(self, event: NotBlinkingInput.Changed) -> None:
        """Update the state of required fields based on input changes."""
        if event.input.id not in self.REQUIRED_FIELDS:
            return

        if event.validation_result is not None and event.validation_result.is_valid:
            self.required_fields[event.input.id] = True
        else:
            self.required_fields[event.input.id] = False

        is_form_changed = self.json == self.form_to_dict()
        submit_button = self.query_one('#form-submit-button')

        submit_button.disabled = not self.is_form_valid() or is_form_changed

    def is_form_valid(self):
        """Check if the form is valid based on the required fields."""
        return all(self.required_fields.values())
