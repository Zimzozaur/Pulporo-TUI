from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.events import Click
from textual.screen import ModalScreen
from textual.widgets import Button


class MonthYearPopup(ModalScreen):
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

    MONTHS_DICT = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
    }

    MONTHS = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    def __init__(self, date_dict) -> None:
        super().__init__()
        self.date_dict: dict = date_dict
        self.popup_year: int = self.date_dict['year']

    def compose(self) -> ComposeResult:
        with Container(id='month-popup-body'):
            with Horizontal(id='year-section'):
                yield Button('⬅️', id='prev-year', classes='year-bt')
                yield Button(f'{self.date_dict['year']}', id='popup-year', classes='year-bt')
                yield Button('➡️', id='next-year', classes='year-bt')
            with Horizontal():
                yield Button('Jan', id='jan', classes='month-bt')
                yield Button('Feb', id='feb', classes='month-bt')
                yield Button('Mar', id='mar', classes='month-bt')
                yield Button('Apr', id='apr', classes='month-bt')
            with Horizontal():
                yield Button('May', id='may', classes='month-bt')
                yield Button('Jun', id='jun', classes='month-bt')
                yield Button('Jul', id='jul', classes='month-bt')
                yield Button('Aug', id='aug', classes='month-bt')
            with Horizontal():
                yield Button('Sep', id='sep', classes='month-bt')
                yield Button('Oct', id='oct', classes='month-bt')
                yield Button('Nov', id='nov', classes='month-bt')
                yield Button('Dec', id='dec', classes='month-bt')

    def on_mount(self):
        """Color button on mount"""
        self.color_button_if_this_year()

    @on(Button.Pressed, '.month-bt')
    def month_button(self, event: Button.Pressed):
        """Change query parameters of Ledger"""
        self.date_dict['month']: int = self.MONTHS_DICT[event.button.id]
        self.date_dict['year']: int = self.popup_year
        self.dismiss(True)

    @on(Button.Pressed, '#prev-year')
    def change_year_back(self):
        """Change Display year to one before"""
        self.popup_year -= 1
        self.query_one('#popup-year').label = str(self.popup_year)
        self.color_button_if_this_year()

    @on(Button.Pressed, '#next-year')
    def change_year_next(self):
        """Change Display year to next one"""
        self.popup_year += 1
        self.query_one('#popup-year').label = str(self.popup_year)
        self.color_button_if_this_year()

    @on(Button.Pressed, '#popup-year')
    def this_year(self, event: Button.Pressed):
        self.popup_year = self.date_dict['year']
        event.button.label = str(self.popup_year)
        self.color_button_if_this_year()

    def on_click(self, event: Click):
        """Remove widget from DOM when clicked on background"""
        if self.get_widget_at(event.screen_x, event.screen_y)[0] is self:
            self.dismiss(False)

    def color_button_if_this_year(self):
        """
        Change year and month buttons to primary
        when popup set to this year
        and to default on other year
        """
        def change_color(color):
            month_abbreviations = self.MONTHS[self.date_dict['month'] - 1].lower()
            self.query_one(f"#{month_abbreviations}").variant = color
            self.query_one('#popup-year').variant = color

        if self.popup_year == self.date_dict['year']:
            change_color('primary')
        else:
            change_color('default')
