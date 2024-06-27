"""Forms provides a comprehensive set of forms for various tasks within the application."""


# Local imports.
from .fields import NotBlinkingInput, NotBlinkingTextArea
from .forms import InflowsForm, OutflowsForm


# Public symbols.
__all__ = [
    'NotBlinkingInput', 'NotBlinkingTextArea',
    'OutflowsForm', 'InflowsForm',
]
