
from pinecone import Pinecone
from dotenv import load_dotenv
import os

load_dotenv()

pc = Pinecone(api_key=os.getenv('PINECONE_API'))
index = pc.Index("ilastream")


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
        
    def insert(self, vector:list, namespace=None):
        self.index.upsert(vectors=vector, namespace=namespace)
    #      {
    #   "id": "A", 
    #   "values": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
    #   "metadata": {"genre": "comedy", "year": 2020}}
    
        
    def query(self, data:list, top_k=5, namespace=None):
        return self.index.query(vector=data, top_k=top_k, namespace=namespace)