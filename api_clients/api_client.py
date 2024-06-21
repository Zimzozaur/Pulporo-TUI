import os

from typing import Literal, Optional

from requests import (
    get, post, patch, delete,
    Response
)

JsonDict = dict[str, str | float | int | bool | None]


class BasePulporoAPI:
    def __init__(self) -> None:
        self._url = os.getenv("PULPORO_API_URL", "http://localhost:8000/")


class OneOffAPI(BasePulporoAPI):
    """Client for the OneOffs Operations."""

    def get_flow(
        self,
        endpoint: Literal['outflows/', 'inflows/'],
        param_dict: dict[str, int] | None = None,
        pk: int | None = None
    ) -> list[JsonDict] | JsonDict:
        """
        Retrieve data from the specified endpoint.

        Args:
            endpoint (Literal['outflows/', 'inflows/']): The endpoint to retrieve data from.
            param_dict (dict, optional): Dictionary of query parameters to include in the request. Defaults to None.
            pk (int, optional): Primary key to retrieve a specific record. Defaults to None.

        Returns:
            list[dict] | dict: The response data from the endpoint, either a list of dicts or a single dict.
        """
        endpoint_url: str = self._url + endpoint
        if pk:
            endpoint_url += f'{pk}/'

        response: Response = get(endpoint_url, params=param_dict)
        list_of_dicts: list[JsonDict] | JsonDict = response.json()
        return list_of_dicts

    def post_flow(
        self,
        endpoint: Literal['outflows/', 'inflows/'],
        json: JsonDict
    ) -> Response:
        """
        Send a POST request to the specified endpoint.

        Args:
            endpoint (Literal['outflows/', 'inflows/']): The endpoint to send the POST request to.
            json (dict): The JSON payload to include in the POST request.

        Returns:
            Response: The response from the endpoint.
        """
        endpoint_url: str = self._url + endpoint
        response: Response = post(endpoint_url, json=json)
        return response

    def patch_flow(
        self,
        endpoint: Literal['outflows/', 'inflows/'],
        json: JsonDict,
        pk: str
    ) -> Response:
        """
        Send a PATCH request to the specified endpoint.

        Args:
            endpoint (Literal['outflows/', 'inflows/']): The endpoint to send the PATCH request to.
            json (dict): The JSON payload to include in the PATCH request.
            pk (str): The primary key to identify the specific record to update.

        Returns:
            Response: The response from the endpoint.
        """
        endpoint_url: str = self._url + endpoint + pk
        response: Response = patch(endpoint_url, json=json)
        return response

    def delete_flow(
        self,
        endpoint: Literal['outflows/', 'inflows/'],
        pk: str
    ) -> Response:
        """
        Send a DELETE request to the specified endpoint.

        Args:
            endpoint (Literal['outflows/', 'inflows/']): The endpoint to send the DELETE request to.
            pk (str): The primary key to identify the specific record to delete.

        Returns:
            Response: The response from the endpoint.
        """
        final_endpoint: str = self._url + endpoint + pk
        response: Response = delete(final_endpoint)
        return response
