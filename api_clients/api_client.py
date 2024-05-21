from typing import Literal

from requests import get, Response

from tests.data import test_static_data


class BasePulporoClient:
    def __init__(self, url):
        self.url = url
        self.headers = {}


class OneOffClient(BasePulporoClient):
    """Client for the OneOffs Operations """
    def get_flow(self, endpoint: Literal['outflows', 'inflows'], param_dict):
        endpoint_url: str = self.url + endpoint
        response: Response = get(endpoint_url, params=param_dict, headers=self.headers)
        list_of_dicts: list[dict] = response.json()
        return list_of_dicts

    def post_flow(self, endpoint: Literal['outflows', 'inflows'], param_dict):
        pass


