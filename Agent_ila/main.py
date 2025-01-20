import os
import logging
from log_utils.logger_config import logger
from dotenv import load_dotenv
from cogniteClient.cognite_interac import get_client
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
        generated_ila_filter, _container_properties = ila_filter.generate_ila_filter(client, user_query)
        #logger.info(f"Generated ILA filter: {generated_ila_filter}")

        # Query ILA
        ila_result = query_ila(generated_ila_filter, client)
        logger.debug("ILA query completed successfully.")

        # Save results to JSON
        append_to_json('generated_f_prompt.json', generated_ila_filter, user_query, ila_result)
        logger.debug("Results saved to generated_f_prompt.json.")

        return ila_result, generated_ila_filter , _container_properties

    except Exception as e:
        #logger.error(f"Error in main function: {e}")
        logger.exception("Error in main function:")
        raise





if __name__ == "__main__":
    raw_user_query ="calculate the average rop for each wells 15-F-11 A and 15-F-1 C?"#"In wells 15-F-11 A and 15-F-1 C, which formations were drilled and Which drill bits were used for 8.5 and 17.5 sizes?" #"summarize the daily drillign report for the  8.5 hole Section of well  15-F-1 C"#"show me the wells that drilled in the Tor Formation."#"Take all the daily drilling report of well 15-F-11 A. Give me three events that are important on the well operation."#"summarize the 8.5 section of wells 15-F-11 A and 15-F-1 C. give the average ROP, the dr ill bit used and the rig used to drill."#"Tell me the some info on the daily drilling report of well 15-F-11 A."
    #    "summarize the daily drilling report of 8.5 section of wells 15-F-11 A "
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
        logging.info("=== START Agent ===")
        split_query = query_preprocess(raw_user_query, client)
        
        logger.debug(f"Query preprocessing completed: {split_query}")
        logger.info(f"Raw user query: {raw_user_query}")

        compile_qa = f"""This is the raw user query that has been split into multiple queries: {raw_user_query}. The split queries and answers are as follows: \n"""

        
        for single_user_query in split_query:
            logger.debug(f"Processing query: {single_user_query}")

            # Log query before processing
            logger.debug_split_query(raw_user_query, split_query)

            # Process the query through main
            ila_result,ila_filter, container_properties = main(single_user_query, client)

            # Summarize the result
            summary_result = summarizer(client).single_summary(single_user_query, ila_result, container_properties)

            # Log the query-response pair
            logger.log_query_response(single_user_query,ila_filter,  ila_result, summary_result)

            compile_qa += f"Query: {single_user_query} \nAnswer: {summary_result}\n"
        print(compile_qa)
        compile_qa = summarizer(client).combined_summary(compile_qa)
        logger.info(f"Combined summary: {compile_qa}")



    except Exception as e:
        logger.error(f"Error during query processing: {e}")
