from typing import List, Dict

import json
class IlaFilter:
    """
    Creates an ILA stream filter.

    Attributes:
        properties_path (str, optional): _description_. Defaults to 'containersProperties.txt'.
        filter_struct (str, optional): _description_. Defaults to 'filter_structure.txt'.
        filter_args (str, optional): _description_. Defaults to 'filterArguments.txt'.
        filter_sample (str, optional): _description_. Defaults to 'filter_sample.txt'.
        filter_prompt (str): llm prompt used for generating the filter
    """

    def __init__(self, 
                 container_properties :str = 'prompts/container_props.txt', 
                # filter_struct: str = 'filter_texts/filterStruc.txt' , 
                 args_filter: str = 'prompts/args_filter.txt',
                 args_aggregate: str = 'prompts/args_aggregation.txt',
                examples: str = 'prompts/examples.txt',
                 header: str = 'prompts/header.txt') -> None:
    

        #load the .txt files
        self.container_properties = open(container_properties, 'r', encoding='utf-8').read()
        #self.filter_struct = open(filter_struct, 'r').read()
        self.filter_args = open(args_filter, 'r', encoding='utf-8').read()
        self.filter_aggregate = open(args_aggregate, 'r', encoding='utf-8').read()
        self.filter_sample = open(examples, 'r', encoding='utf-8').read()
        self.header = open(header, 'r', encoding='utf-8').read()
        self.filter_prompt = None



    def _create_prompt(self, user_query: str)->None:
        """_description_

        Returns:
            str: _description_
        """

       # filter_prompt = header + '\n' 
        compiled_texts = self.container_properties + '\n' + self.filter_args + '\n' + self.filter_aggregate + '\n' + self.filter_sample
        
       # self.filter_struct + '\n' + self.filter_args + '\n' + self.filter_sample + '\n' + self.container_properties


        body = {
        "messages": [
            {
                "role": "system",
                "content": (
                    self.header
                ),
            },
            {"role": "system", "content":  compiled_texts},
            {"role": "user", "content":  user_query},
        ],
       # "functions": functions,
      #  "functionCall": {"name": "get_the_fact_and_joke"},
        "temperature": 0,
        "model": "gpt-4o-mini",
    }


        self.filter_prompt = body

        #save in a text file
        #with open('filter_prompt.txt', 'w') as file:
        #    file.write(self.filter_prompt)
        #print(self.filter_prompt)

       
       

    def generate_ila_filter(self, client, user_query: str)->Dict:

        """creates an ILA filter based on the user query

        Args:
            user_query (str): raw user query to be used to create the filter

        Returns:
            Dict: filter to be appended to the ILA stream payload request
        """

        #create the prompt
        self._create_prompt(user_query)

        #establish connection to the AI server
        proxy_path = f"/api/v1/projects/{client.config.project}/ai/chat/completions"


        response = client.post(url=proxy_path, json=self.filter_prompt).json()

        response_items = response["choices"][0]
        
        

        return json.loads(response_items["message"]['content'])