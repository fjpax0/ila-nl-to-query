import json
import sys
import os
# Add the project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#the goal here is to embed and upsert in the pinecone for the historical query and generated ILA filter
from embed.embedding_api.embeddings import CreateEmbeddings
from pinecone_client.pc import PineconeClient


DATA_PATH = 'data_to_embed/witsml_queries_samp.jsonl'

def _format_jsonl_entry(jsonl_entry):
    """
    Formats a single JSONL entry into the specified string format.

    Args:
        jsonl_entry (str): A single JSONL formatted string.

    Returns:
        str: The formatted output string.
    """
    # Parse the JSONL entry into a dictionary
    data = jsonl_entry

    # Extract constants, user_query, and generated_query
    constants = json.dumps(data.get("constants", {}))
    user_query = data.get("user_query", "")
    generated_query = json.dumps(data.get("generated_query", {}))

    # Format the output
    formatted = (
        f"Constants: {constants}\n"
        f"User query: {user_query}\n"
        f"Generated query: {generated_query}\n"
    )

    return formatted

def main():
    # Initialize Pinecone client
    pc = PineconeClient()
    emb = CreateEmbeddings()
    #load data
    # Open the JSONL file and iterate over each line
    with open(DATA_PATH, "r") as file:
        for line in file:
            # Parse the JSON content from the current line
            record = json.loads(line)
   
            
            # Access fields from the JSON object
            user_query = record.get("user_query", "No user query found")
            #ila_filter = record.get("generated_query", {})
            
            # Create embeddings
            #test if user_query is a str if not make it a string
            if not isinstance(user_query, str):
                user_query = str(user_query)

            embeddings = emb.get_embeddings([{'text': user_query}])

            assert len(embeddings) == 1, "Expected one embedding to be returned because we iterate over the jsonl file"
    
            vectors_list = [{'id':embeddings[0]['text'], "values": embeddings[0]['embedding'], 'metadata': {'ila_sample':_format_jsonl_entry(record)}}]
   
            # Upsert embeddings to Pinecone
            pc.insert(vector=vectors_list, namespace='user_query')


            # Upsert embeddings to Pinecone

    return

if __name__ == "__main__":
    main()
