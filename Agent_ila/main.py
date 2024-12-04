from dotenv import load_dotenv
import os
from cogniteClient.congite_interac import get_client
from agent_dev import IlaFilter
import json
# Load environment variables
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
    print(generated_ila_filter)
    with open('generated_f_prompt.json', 'w') as f:
        json.dump(generated_ila_filter , f)

if __name__ == "__main__":
    user_query = "find all the the wells with hugin formation"#"find all the formations that are drilled between depths of 50 and 100 meters"
    
    #'find all the the wells with hugin formation"
    
    #"find all the formations drilled in the wells with the name '15/9-F-11 A'"
    #"find all the formations that are drilled between depths of 50 and 100 meters"#'find all the the wells with hugin formation'
    main(user_query)