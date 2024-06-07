from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Static, Button

from requests import get


def json_to_list(json_file):
    result = ''
    for key, value in json_file.items():
        result += f"""{key}: [@click=open_link('{value}')]Photo[/]\n"""
    return result


class StaticWithLink(Static):
    def action_open_link(self, link: str) -> None:
        self.app.bell()
        import webbrowser
        webbrowser.open(link)


class Media(Container):
    def compose(self) -> ComposeResult:
        json_data = get('http://127.0.0.1:8000/images/').json()
        links_markup = json_to_list(json_data)
        yield StaticWithLink(links_markup)


