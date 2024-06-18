from textual.reactive import reactive
from textual.widgets import Input, TextArea


class NotBlinkingInput(Input):
    """Input filed but without blinking"""
    cursor_blink = reactive(False, init=False)


class NotBlinkingTextArea(TextArea):
    """TextArea field but without blinking"""
    cursor_blink = reactive(False, init=False)
