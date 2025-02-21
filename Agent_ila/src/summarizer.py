from typing import List, Dict
import json

class summarizer:

    def __init__(self, client) -> None:
        self.singe_summary_header = "You are an AI assistant that could summarize a dictionary results from a database query to answer a user query. You will be given with the container properties which you will use as a reference for the units and description of the query and answer variables you will be provided. You will be provided with the result in dictionary format and a string of the user query. You are expected to generate a summary of the result that answers the user query. You need to be honest, complete, and concise in your summary. The summary should be maximum two sentences and easily readble by a user. The 'counts' in the result please do not include the summary. If it asks for each item, the sumamry should be provided for each well. Think thoroughly and step by step." 
        self.combined_summary_header = ""
        self.client = client
        self.request_body = None

    def _create_prompt(self, query:str, answer: dict, container_properties:str) -> str:
        """
        _description_

        Args:
            query (str): _description_
            text (str): _description_

        Returns:
            str: _description_
        """

        self.request_body = {
        "messages": [
            {
                "role": "system",
                "content": (
                    self.singe_summary_header
                ),
            },
            {"role": "user", "content":  f"TThis is the container properties: {container_properties}"},
            {"role": "user", "content":  f"TThis is the raw user query: {query}"},
            {"role": "user", "content": f"This is the raw answer from the database: {answer}" },
        ],
       # "functions": functions,
      #  "functionCall": {"name": "get_the_fact_and_joke"},
        "temperature": 0,
        "model": "gpt-4o-mini",
    }


        return self.request_body
    
    def _call_llm(self, prompt:str) -> str:
        #establish connection to the AI server
        proxy_path = f"/api/v1/projects/{self.client.config.project}/ai/chat/completions"


        response = self.client.post(url=proxy_path, json= prompt).json()

        response_items = response["choices"][0]
        
       

        return response_items["message"]['content']
    
        

    def single_summary(self, query:str, text: str, container_properties:str) -> str:

        summary = self._call_llm(self._create_prompt(query, text, container_properties))
        return summary

    
    def combined_summary(self, queries_answers:str) -> str:


        prompt = {
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a AI assistant that compiles the individual answers to a single answer, that addresses the raw user query. Ensure that the answer is complete, concise, and easily readable by a user. Think thoroughly and step by step."
                ),
            },
            {"role": "user", "content":  f"{queries_answers}" },
        ],
       # "functions": functions,
      #  "functionCall": {"name": "get_the_fact_and_joke"},
        "temperature": 0,
        "model": "gpt-4o-mini",
    }
        summary = self._call_llm(prompt)

        return summary
        

    
        

