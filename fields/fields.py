from textual.reactive import reactive
from textual.widgets import Input, TextArea


class NotBlinkingInput(Input):
    """Input filed but without blinking"""
    cursor_blink = reactive(False, init=False)


class NotBlinkingTextArea(TextArea):
    """TextArea field but without blinking"""
    cursor_blink = reactive(False, init=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._value = self.text

    @property
    def value(self) -> str:
        """
        Get the value of the text area.

        Returns:
            str: The current text in the text area.
        """
        return self._value

    @value.setter
    def value(self) -> None:
        """
        Set the value of the text area.

        Args:
            new_value (str): The new text to set in the text area.
        """
        self._value = self.text