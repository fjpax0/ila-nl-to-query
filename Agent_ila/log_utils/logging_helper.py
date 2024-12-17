# log_utils/logging_helper.py

import logging
import logging.config
import os
import random
import string
from typing import List

class NoPineconeFilter(logging.Filter):
    """
    Custom logging filter to exclude logs from 'pinecone' and 'pinecone_plugins' loggers.
    """
    def filter(self, record):
        excluded_loggers = ['pinecone', 'pinecone_plugins']
        return not any(record.name.startswith(excl) for excl in excluded_loggers)

class Logger:
    _instance = None  # Singleton instance

    def __new__(cls, log_dir="logs", log_file="query_response_log.log", level=logging.INFO):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)

            # Initialize logger configuration
            cls._instance.log_dir = log_dir
            cls._instance.log_file = os.path.join(cls._instance.log_dir, log_file)

            # Ensure the log directory exists
            if not os.path.exists(cls._instance.log_dir):
                os.makedirs(cls._instance.log_dir)

            # Define logging configuration using dictConfig for advanced setup
            logging_config = {
                'version': 1,
                'disable_existing_loggers': False,
                'filters': {
                    'no_pinecone': {
                        '()': 'log_utils.logging_helper.NoPineconeFilter',  # Corrected path
                    },
                },
                'formatters': {
                    'standard': {
                        'format': '%(asctime)s - %(levelname)s - %(message)s',
                    },
                },
                'handlers': {
                    'file': {
                        'level': level,
                        'class': 'logging.FileHandler',
                        'filename': cls._instance.log_file,
                        'formatter': 'standard',
                        'filters': ['no_pinecone'],
                    },
                    'console': {
                        'level': level,
                        'class': 'logging.StreamHandler',
                        'formatter': 'standard',
                        'filters': ['no_pinecone'],
                    },
                },
                'root': {  # Root logger configuration
                    'handlers': ['file', 'console'],
                    'level': level,
                },
                'loggers': {
                    'pinecone': {  # Suppress logs from 'pinecone'
                        'handlers': [],
                        'level': 'WARNING',
                        'propagate': False,
                    },
                    'pinecone_plugins': {  # Suppress logs from 'pinecone_plugins'
                        'handlers': [],
                        'level': 'WARNING',
                        'propagate': False,
                    },
                }
            }

            # Apply the logging configuration
            logging.config.dictConfig(logging_config)

            # Explicitly set levels for sub-loggers if necessary
            logging.getLogger('pinecone').setLevel(logging.WARNING)
            logging.getLogger('pinecone_plugins').setLevel(logging.WARNING)
            logging.getLogger('pinecone_plugins.inference').setLevel(logging.WARNING)

        return cls._instance

    # Function to generate a short identifier
    def generate_short_id(self, length=8):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def log_query_response(self, single_user_query: str, ila_filter: dict, ila_result: dict, summarized_response: str):
        logging.info("=== START QUERY ===")
        logging.info("Query: %s", single_user_query)
        logging.info("ILA query: %s", ila_filter)
        logging.info("ILA Raw result: %s", ila_result)
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
