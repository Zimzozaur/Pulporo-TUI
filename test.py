from requests import get


print(get('localhost:8000/outflows').json())