import ast

def query_preprocess(raw_query: str, client) -> list:
    """
    Preprocess a raw user query to determine if it requires single or multiple database queries.
    
    Args:
        raw_query (str): The user's raw query.
        client: The client object to interact with the AI server.

    Returns:
        list: A list of queries derived from the raw user query.
    """
    # System instructions for the AI model
    header = (
        "You are an AI assistant that preprocesses a user query before generating a database-specific query. "
        "Your task is to evaluate if the user query requires several queries to be executed in the database or if it can be executed in a single query. "
        "The expected output should be a list indicating whether it is a single query or multiple queries."
        "If the query would require a recurssive filter or aggreagte, this is considered as one."
    )
    
    # Examples for context
    examples = (
        "Here are the examples for raw user queries and the expected output:\n"
        "Example 1: Raw user query: What is the average ROP in the Tor formation?\n"
        "{'Query': ['What is the average ROP in the Tor formation?']}\n\n"
        "Example 2: Raw user query: Show me all the formations drilled in wells 1/2-1 and 1/2-2.\n"
        "{'Query': ['Show me the formations drilled in wells 1/2-1 and 1/2-2.']}\n\n"
        "Example 3: Raw user query: Show me the formations drilled in each well 1/2-1 and 1/2-2.\n"
        "{'Query': ['Show me the formations drilled in well 1/2-1.', 'Show me the formations drilled in well 1/2-2.']}\n"
        "Example 4: Raw user query: Calculate the average of the average rops for all wells that drilled Tor formation and choose the well that drilled the fastest.\n"
        "{'Query': ['Calculate the average of the average rops for all wells that drilled Tor formation and choose the well that drilled the fastest.']}\n"
    )
    
    # Body for the AI request
    body = {
        "messages": [
            {"role": "system", "content": header},
            {"role": "user", "content": examples},
            {"role": "user", "content": raw_query},
        ],
        "temperature": 0,
        "model": "gpt-4o-mini",
    }
    
    # API path for the AI server
    proxy_path = f"/api/v1/projects/{client.config.project}/ai/chat/completions"
    
    # Send the request to the AI server
    response = client.post(url=proxy_path, json=body).json()
    
    # Extract and parse the AI's response
    response_items = response["choices"][0]["message"]['content']
    converted_dict = ast.literal_eval(response_items)
    
    # Return the list of queries
    return converted_dict.get("Query", [])

# Example usage
# preprocess_query("What is the average ROP in the Tor formation?", client)
