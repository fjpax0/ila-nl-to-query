import logging
import os
import random
import string
from typing import List
class Logger:
    def __init__(self, log_dir="logs", log_file="query_response_log.log", level=logging.DEBUG):
        self.log_dir = log_dir
        self.log_file = os.path.join(log_dir, log_file)

        # Ensure the log directory exists
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # Configure the logging system
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
    # Function to generate a short identifier
    def generate_short_id(self, length=8):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    
    def log_query_response(self, single_user_query: str, ila_result:dict, summarized_response: str):
        logging.info("=== START QUERY ===")
        logging.info("Single Query: %s", single_user_query)
        logging.info("ILA result: %s",ila_result)
        logging.info("Response: %s", summarized_response)
        logging.info("=== END QUERY ===")

    def info(self, message):
        logging.info(message)
    
    def debug_split_query(self, raw_user_query: str, split_query: List[str]):
        logging.debug("Raw Query: %s", raw_user_query)
        logging.debug("Split Query: %s", split_query)


    def debug(self, message):
        logging.debug(message)

    def warning(self, message):
        logging.warning(message)

    def error(self, message):
        logging.error(message)
