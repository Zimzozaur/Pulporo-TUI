


from typing import List, Literal


def test_static_data(endpoint: Literal['outflows', 'inflows']) -> List[dict]:
    """return some testing static data """
    # description of the dict found in the backend file "finanace/serializer.py" 

    # if returning outflow stuff :
    if endpoint == "outflows":
        
        return [{
        "title":"some title",
        "value":0.4,
        "date":"Someday",
        "prediction":"You gonna get rich!",
        "notes": "Have fun",
    }]

    else :
        return [{
            "title":"some title",
            "value":0.4,
            "date":"Someday",
            "notes": "Have fun",
        }]

