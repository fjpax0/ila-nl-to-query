import sys
import os
# Add the project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cogniteClient.congite_interac import get_client
import os
from typing import Dict, List

class CreateEmbeddings:
    def __init__(self, client=None, model:str = 'azure/text-embedding-3-large'):
        if client is None:
            self.client = get_client(interactive=True, cdf_version="alpha")
            self.model = model
            
        else:
            self.client = client

    def get_embeddings(self, input_text:List[Dict])->List[Dict]:
        """get embeddings for a given text

        Args:
            input_text (str): text to be embedded
            model (str): model to be used for embedding

        Returns:
            List[Dict]: list of dictionaries containing the text and embeddings. Dict's keys are 'text' and 'embedding' . 
        """
        url = f"/api/v1/projects/{self.client.config.project}/ai/embeddings"
   
        body = {
            "items": input_text, 
            "model": self.model
        }
      
        response = self.client.post(url, json=body).json()

        return response["items"]

if __name__ == "__main__":
    emb = CreateEmbeddings()
    text =[{"text": "Hellofefwefewf"},{'text': 'Worldfeqfwefwefwefwe'}]#
