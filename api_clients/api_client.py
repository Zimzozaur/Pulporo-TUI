import os

from typing import Literal

from requests import (
    get, post,
    Response
)


class BasePulporoClient:
    def __init__(self):
        self.url = os.getenv("PULPORO_API_URL", "http://localhost:8000/")
        self.headers = {}


class OneOffClient(BasePulporoClient):
    """Client for the OneOffs Operations """
    def get_flow(self, endpoint: Literal['outflows', 'inflows'], param_dict):
        endpoint_url: str = self.url + endpoint
        response: Response = get(endpoint_url, params=param_dict, headers=self.headers)
        list_of_dicts: list[dict] = response.json()
        return list_of_dicts

    def post_flow(self, endpoint: Literal['outflows/', 'inflows/'], json: dict) -> Response:
        endpoint_url: str = self.url + endpoint
        response: Response = post(endpoint_url, json=json)
        return response

