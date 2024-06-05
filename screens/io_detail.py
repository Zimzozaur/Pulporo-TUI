from collections import namedtuple

from textual.app import ComposeResult
from textual.containers import Container
from textual.events import Click
from textual.screen import ModalScreen
from textual.widgets import Static

from forms.form import OutflowsForm, InflowsForm
from api_clients.api_client import OneOffClient

RowDataOutflow = namedtuple('RowDataOutflow', 'no id title value date '
                                              'prediction notes creation_date last_modification')

RowDataInflows = namedtuple('RowDataInflows', 'no id title value date '
                                              'notes creation_date last_modification')


class IODetail(ModalScreen):
    DEFAULT_CSS = """
    IODetail {
        align: center middle;
        width: auto;
        height: auto;
    }

    #io-detail-body {
        padding: 1 3;
        min-width: 70;
        min-height: 40;
        padding-top: 1;
        width: 70;
        height: 40;
        background: $surface-lighten-1;
    }
    """

    def __init__(self, *args, data: list, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = OneOffClient()
        if len(data) == 9:
            self.data: RowDataOutflow = RowDataOutflow(*data)
        elif len(data) == 8:
            self.data: RowDataInflows = RowDataInflows(*data)
        else:
            raise TypeError('Wrong length of list')

    def compose(self) -> ComposeResult:
        if isinstance(self.data, RowDataOutflow):
            form = OutflowsForm()
            form.fields['prediction'].value = self.data.prediction
        else:
            form = InflowsForm()

        form.fields['title'].value = self.data.title
        form.fields['value'].value = self.data.value
        form.fields['date'].value = self.data.date
        form.fields['notes'].text = self.data.notes

        with Container(id='io-detail-body'):
            yield form
            yield Static()
            yield Static(f'Creation Date: {self.data.creation_date}')
            yield Static(f'Last Modification: {self.data.last_modification}')

    def on_click(self, event: Click):
        """Close popup when clicked on the background"""
        if self.get_widget_at(event.screen_x, event.screen_y)[0] is self:
            self.dismiss(False)
