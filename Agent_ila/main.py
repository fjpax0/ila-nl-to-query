import os
import logging
from log_utils.logger_config import logger
from dotenv import load_dotenv
from cogniteClient.congite_interac import get_client
from src.agent_dev import IlaFilter
# Load environment variables
from src.queryStream import query_ila
from src.logs_filters import append_to_json
from src.query_preprocess import query_preprocess
from src.summarizer import summarizer

# Load environment variables
load_dotenv()

 # Ensure INFO level logs are visible

def main(user_query: str, client):
    try:

        # Create an instance of IlaFilter
        logger.debug("Initializing IlaFilter...")
        ila_filter = IlaFilter()
        generated_ila_filter = ila_filter.generate_ila_filter(client, user_query)
        logger.debug(f"Generated ILA filter: {generated_ila_filter}")

        # Query ILA
        ila_result = query_ila(generated_ila_filter, client)
        logger.debug("ILA query completed successfully.")

        # Save results to JSON
        append_to_json('generated_f_prompt.json', generated_ila_filter, user_query, ila_result)
        logger.debug("Results saved to generated_f_prompt.json.")

        return ila_result

    except Exception as e:
        logger.error(f"Error in main function: {e}")
        raise

# if __name__ == "__main__":
#     raw_user_query =
    #"what is the average axial and lateral vibration for well 15-F-11 A" 
    #"Whaw well had the highest average axial vibration and lateral vibration in the Tor formation."
    #"Which rig performed the best the Hod formation based on the ROP."#"In wells 15-F-11 A and 15-F-1 C, which formations were drilled?" #"Which drill bits were used for 8.5 and 17.5 sizes?"
    #"What is the average inclination that the Hugin formation is drilled?"
    #"which formations are drilled in well 15-F-1 C"# and 15/9-F-11 A

if __name__ == "__main__":
    raw_user_query ="which rig performed on hole sections 8.5 bit size"#"What is the average ROP in the Tor formation?"# "what is the average axial and lateral vibration for well 15-F-11 A" # Input the query string here

    # Choose authentication mode
    interactive_mode = True  # Set to False for client credentials authentication

    try:
        # Initialize Cognite client
        client = get_client(interactive=interactive_mode)
        logger.info("Cognite client initialized successfully.")
    except Exception as e:
        logger.error(f"Error during Cognite client initialization: {e}")
        exit(1)

    try:
        # Preprocess the query
        query_id = logger.generate_short_id()
        logger.info(f"Query ID: {query_id}")
        split_query = query_preprocess(raw_user_query, client)
        
        logger.info(f"Query preprocessing completed. Split queries: {split_query}")

        for single_user_query in split_query:
            logger.debug(f"Processing query: {single_user_query}")

            # Log query before processing
            logger.debug_split_query(raw_user_query, split_query)

            # Process the query through main
            ila_result = main(single_user_query, client)

            # Summarize the result
            summary_result = summarizer(client).single_summary(single_user_query, ila_result)
          

            # Log the query-response pair
            logger.log_query_response(single_user_query, ila_result, summary_result)

    except Exception as e:
        logger.error(f"Error during query processing: {e}")
