from typing import cast

from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.events import Click
from textual.screen import ModalScreen
from textual.widgets import Button


class MonthYearPopup(ModalScreen):
    """
    ModalScreen display month calendar
    and returns chosen year and month on dismissal
    """

    DEFAULT_CSS = """
    MonthYearPopup {
        width: auto;
        height: auto;
        align: right top;
    }
    
    #month-popup-body {
        width: 28;
        height: 14;
        offset-x: -6;
        offset-y: 2;
        content-align: center middle;
        padding: 1 2;
    }
    
    .year-bt {
        min-width: 8;
    }
    
    .year-bt:hover {
        background: $accent;
        color: $text;
        text-style: bold;
    }
    
    .month-bt {
        min-width: 6;
    }
    
    .month-bt:hover {
        background: $accent;
        color: $text;
        text-style: bold;
    }
    """
    MONTHS_DICT: dict[str, int] = {
        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
        'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
    }

    MONTHS: list[str] = [
        'Dummy_string_to_index_from_1',
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    def __init__(self, year, month) -> None:
        super().__init__()
        self.popup_year: int = year
        self.year: int = year
        self.month: int = month

    def compose(self) -> ComposeResult:
        with Container(id='month-popup-body'):
            with Horizontal(id='year-section'):
                yield Button('⬅️', id='prev-year', classes='year-bt')
                yield Button(f'{self.year}', id='this-year', classes='year-bt')
                yield Button('➡️', id='next-year', classes='year-bt')
            with Horizontal():
                yield Button('Jan', id='Jan', classes='month-bt')
                yield Button('Feb', id='Feb', classes='month-bt')
                yield Button('Mar', id='Mar', classes='month-bt')
                yield Button('Apr', id='Apr', classes='month-bt')
            with Horizontal():
                yield Button('May', id='May', classes='month-bt')
                yield Button('Jun', id='Jun', classes='month-bt')
                yield Button('Jul', id='Jul', classes='month-bt')
                yield Button('Aug', id='Aug', classes='month-bt')
            with Horizontal():
                yield Button('Sep', id='Sep', classes='month-bt')
                yield Button('Oct', id='Oct', classes='month-bt')
                yield Button('Nov', id='Nov', classes='month-bt')
                yield Button('Dec', id='Dec', classes='month-bt')

    def on_mount(self) -> None:
        """Color button on mount"""
        self.update_button_colors_if_current_year()

    def on_click(self, event: Click) -> None:
        """Remove widget from DOM when clicked on background"""
        if self.get_widget_at(event.screen_x, event.screen_y)[0] is self:
            self.dismiss((self.year, self.month))

    @on(Button.Pressed, '.month-bt')
    def month_button(self, event: Button.Pressed) -> None:
        """Return chosen date"""
        self.month = self.MONTHS_DICT[cast(str, event.button.id)]
        self.year = self.popup_year
        self.dismiss((self.year, self.month))

    @on(Button.Pressed, '#prev-year')
    def change_year_back(self) -> None:
        """Change displayed year to one before"""
        self.popup_year -= 1
        self.query_one('#this-year', Button).label = str(self.popup_year)
        self.update_button_colors_if_current_year()

    @on(Button.Pressed, '#next-year')
    def change_year_next(self) -> None:
        """Change displayed year to next"""
        self.popup_year += 1
        self.query_one('#this-year', Button).label = str(self.popup_year)
        self.update_button_colors_if_current_year()

    @on(Button.Pressed, '#this-year')
    def this_year(self, event: Button.Pressed) -> None:
        """Change displayed year to current"""
        self.popup_year = self.year
        event.button.label = str(self.popup_year)
        self.update_button_colors_if_current_year()

    def update_button_colors_if_current_year(self) -> None:
        """
        Change year and month buttons to primary
        when popup set to current year
        and to default on the other year
        """
        color = 'primary' if self.popup_year == self.year else 'default'
        self.query_one(f"#{self.MONTHS[self.month]}", Button).variant = color
        self.query_one('#this-year', Button).variant = color
