
from typing import Literal
from requests import get

from tests.data import test_static_data


class PulporoPyClient():
    """Client for the API """


    def __init__(self,url):
        self.url = url
        self.headers={}
    
    def get_flow(self,endpoint: Literal['outflows', 'inflows'],param_dict):
        return self.call_endpoint(self.url + endpoint,param_dict)
    
    def call_endpoint(self,endpoint_url,params_dict):
        response = get(endpoint_url, params=params_dict,headers=self.headers)
        list_of_dicts: list[dict] = response.json()
        return list_of_dicts
    


class PulporoPyStaticClient():
    """Dummy client with static data for the API """
    def __init__(self,url):
        pass
    def get_flow(self,endpoint: Literal['outflows', 'inflows'],param_dict):
        return test_static_data(endpoint)