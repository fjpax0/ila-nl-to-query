
from pinecone import Pinecone
from dotenv import load_dotenv
import os
load_dotenv()
import logging
pc = Pinecone(api_key=os.getenv('PINECONE_API'))
index = pc.Index("ilastream")
import logging
from log_utils.logging_helper import Logger
logger = Logger(level=logging.DEBUG)
class PineconeClient:
    """_summary_
    """
    def __init__(self):
        self.api_key = os.getenv('PINECONE_API')
        self.index = os.getenv('PINECONE_INDEX')

        if self.api_key:
            self.pc = Pinecone(api_key=self.api_key)
            self.index = self.pc.Index(self.index)
        
        else:
            raise ValueError("Pinecone API key not found")
    
    def _format_sample_query(self, pc_raw_result)->str:
        """this files receives the raw output of the pinecone, takes the metadta 'ila_sample', and creates a string of with 'example number' adn the metadata, then \n for the next example.

        Args:
            pc_raw_result (_type_): _description_

            Sample output:
                {'matches': [{'id': 'B',
                            'metadata': {'genre': 'documentary'},
                            'score': 0.0800000429,
                            'values': []}],
                'namespace': 'example-namespace'}

        Returns:
            str: _description_
        """

        # Extract the metadata from the raw Pinecone result
        metadata_list = [result['metadata']['ila_sample'] for result in pc_raw_result['matches']]

        #iterate over the metadata_list and add the example number
        formatted_samples = ""
        for i, metadata in enumerate(metadata_list):
            formatted_samples += f"Example {i+1}:\n{metadata}\n"

        return formatted_samples
    

    def insert(self, vector:list, namespace=None):
        self.index.upsert(vectors=vector, namespace=namespace)
    #      {
    #   "id": "A", 
    #   "values": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
    #   "metadata": {"genre": "comedy", "year": 2020}}
    
        
    def query(self, data:list, top_k=5, namespace='user_query', format_output=True):
        if format_output:
            #output is a string
            logger.debug(f"Raw Pinecone output received: {self.index.query(vector=data, top_k=top_k, namespace=namespace, include_metadata=True)}")
            return self._format_sample_query(self.index.query(vector=data, top_k=top_k, namespace=namespace, include_metadata=True))
        
        return self.index.query(vector=data, top_k=top_k, namespace=namespace)