from dotenv import load_dotenv
import os
from cogniteClient.congite_interac import get_client
from agent_dev import IlaFilter
import json
# Load environment variables
from src.queryStream import query_ila

load_dotenv()

def main(user_query: str):

    # Choose authentication mode
    interactive_mode = True  # Set to False for client credentials authentication

    try:
        # Get the Cognite client
        client = get_client(interactive=interactive_mode)
        print("Cognite client initialized successfully.")

    except Exception as e:
        print("Error during Cognite client initialization or fetching data:", e)


    # Create an instance of the IlaFilter class
    ila_filter = IlaFilter()
    generated_ila_filter = ila_filter.generate_ila_filter( client, user_query)


    #save in a .txt file
    # with open('generated_f_prompt.txt', 'w') as f:
    #     f.write(ila_filter.filter_prompt)
    #save in a .json file

    with open('generated_f_prompt.json', 'w', encoding='utf-8') as f:
        json.dump(generated_ila_filter , f)

    
    #query the ILA
    return query_ila(generated_ila_filter, client)

if __name__ == "__main__":
    user_query = "What is the average ROP in the Tor formation?"
    #"find all the the wells with hugin formation"#"find all the formations that are drilled between depths of 50 and 100 meters"
    
    #'find all the the wells with hugin formation"
    
    #"find all the formations drilled in the wells with the name '15/9-F-11 A'"
    #"find all the formations that are drilled between depths of 50 and 100 meters"#'find all the the wells with hugin formation'
    result = main(user_query)  # Call the function
    print(result)  # Print the return value
