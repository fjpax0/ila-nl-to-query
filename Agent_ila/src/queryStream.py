
from typing import Dict, Any
def query_ila(gen_query, client) -> Dict[str, Any]:
    """generates a query for the database

    Args:
        gen_query (dict): _description_
        client (_type_): _description_

    Returns:
        Dict[str, Any]: _description_
    """
    
   
    # Check if 'filter' and 'aggregates' are in gen_query as keys
    if 'filter' in gen_query and 'aggregates' in gen_query:
        request = {
            "createdTime": {
                "gt": 1705341600000  # Replace with your desired start time (epoch timestamp in milliseconds)
            },
            "filter": gen_query["filter"],
            "aggregates": gen_query["aggregates"],
        }
        result = client.post(
            url="/api/v1/projects/welldelivery-demo/streams/logs5/records/aggregate",
            json=request,
            headers={"cdf-version": "alpha"},
        )

    # If only 'aggregates' is present in gen_query
    elif 'aggregates' in gen_query:
        request = {
            "createdTime": {
                "gt": 1705341600000  # Replace with your desired start time (epoch timestamp in milliseconds)
            },
            "aggregates": gen_query["aggregates"],
        }
        result = client.post(
            url="/api/v1/projects/welldelivery-demo/streams/logs5/records/aggregate",
            json=request,
            headers={"cdf-version": "alpha"},
        )

    # If only 'filter' is present in gen_query
    elif 'filter' in gen_query:
        request = {
            "createdTime": {
                "gt": 1705341600000  # Replace with your desired start time (epoch timestamp in milliseconds)
            },
            "filter": gen_query["filter"],
        }
        result = client.post(
            url="/api/v1/projects/welldelivery-demo/streams/logs5/records/filter",
            json=request,
            headers={"cdf-version": "alpha"},
        )

    # Handle the case where neither 'filter' nor 'aggregates' is in gen_query
    else:
        raise ValueError("gen_query must contain at least 'filter' or 'aggregates'")



    return result.json()