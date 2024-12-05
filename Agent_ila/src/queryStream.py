
from typing import Dict, Any
def query_ila(gen_query, client) -> Dict[str, Any]:
    """generates a query for the database

    Args:
        gen_query (dict): _description_
        client (_type_): _description_

    Returns:
        Dict[str, Any]: _description_
    """

    #print(gen_query['filter'])
    request = {
    "createdTime": {
        "gt": 1705341600000  # Replace with your desired start time (epoch timestamp in milliseconds)
    },
    "filter": gen_query["filter"],
    "aggregates": gen_query["aggregates"],
}

    result = client.post(
    url="/api/v1/projects/welldelivery-demo/streams/logs3/records/aggregate",
    json=request,
    headers={"cdf-version": "alpha"},
)
    


    return result.json()