from typing import Union

from textual.widgets import Checkbox

from forms import NotBlinkingInput, NotBlinkingTextArea, InflowsForm, OutflowsForm

# Represent 1D JSON
JsonDict = dict[str, Union[str, float, int, bool, None]]

# Represent field from every form
FormField = Union[NotBlinkingInput, Checkbox, NotBlinkingTextArea]

# Represent every form
FormType = Union[InflowsForm, OutflowsForm]
