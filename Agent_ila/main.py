from dotenv import load_dotenv
import os
from cogniteClient.congite_interac import get_client
from agent_dev import IlaFilter
# Load environment variables
from src.queryStream import query_ila
from src.logs_filters import append_to_json
from src.query_preprocess import query_preprocess
load_dotenv()

def main(user_query: str, client):

    # Create an instance of the IlaFilter class
    ila_filter = IlaFilter()
    generated_ila_filter = ila_filter.generate_ila_filter( client, user_query)


    #save in a .txt file
    # with open('generated_f_prompt.txt', 'w') as f:
    #     f.write(ila_filter.filter_prompt)
    #save in a .json file
    print(generated_ila_filter)
    ila_result =query_ila(generated_ila_filter, client)

    append_to_json('generated_f_prompt.json', generated_ila_filter, user_query, ila_result)

    
    #query the ILA
    return ila_result 

if __name__ == "__main__":
    raw_user_query = "In wells 15-F-11 A and 15-F-1 C, which formations were drilled?"
    #"What is the average inclination that the Hugin formation is drilled?"
    #"which formations are drilled in well 15-F-1 C"# and 15/9-F-11 A

    # Choose authentication mode
    interactive_mode = True  # Set to False for client credentials authentication

    try:
        # Get the Cognite client
        client = get_client(interactive=interactive_mode)
        print("Cognite client initialized successfully.")

    except Exception as e:
        print("Error during Cognite client initialization or fetching data:", e)

    #"What is the average ROP in the Hidra formation?" 
    # #"find all the the wells with hugin formation"#What is the average ROP in the Hidra formation?"
    #"find all the the wells with hugin formation"#"find all the formations that are drilled between depths of 50 and 100 meters"
    
    #'find all the the wells with hugin formation"
    #"What is the average inclination that the Hugin formation is drilled?"
    #"find all the formations drilled in the wells with the name '15/9-F-11 A'"
    #"find all the formations that are drilled between depths of 50 and 100 meters"#'find all the the wells with hugin formation'
    print('hello')
    for single_user_query in query_preprocess(raw_user_query, client):
        print(single_user_query)
        result = main(single_user_query, client)  # Call the function
        print(result)  # Print the return value