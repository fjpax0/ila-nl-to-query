from typing import List, Dict


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

    def __init__(self, properties_path :str = 'filter_texts/containerProperties.txt', 
                 filter_struct: str = 'filter_texts/filterStruc.txt' , 
                 filter_args: str = 'filter_texts/filterArgs.txt',
                 filter_sample: str = 'filter_texts/filterSample.txt' ):
    

        #load the .txt files
        self.container_properties = open(properties_path, 'r', encoding='utf-8').read()
        self.filter_struct = open(filter_struct, 'r', encoding='utf-8').read()
        self.filter_args = open(filter_args, 'r', encoding='utf-8').read()
        self.filter_sample = open(filter_sample, 'r', encoding='utf-8').read()
        self.filter_prompt = ""



    def _create_prompt(self, user_query: str)->None:
        """_description_

        Returns:
            str: _description_
        """

        header = """You are an assistant to create a filter for our own database. Essentially you will be provided with the following: \n
        1. The structure of the filter \n
        2. The arguments that the filter can take \n
        3. A sample filter \n
        4. The properties of the container \n
        5. The user query \n
        6. The value of ILA_SPACE = "test_ILA"
        7. The values of ILA_CONTAINER_ID = "test_logs_container"

        Your task is to create a filter based on the user query. The final output should be only the dictionary format of the filter. \n
        """

       # filter_prompt = header + '\n' 
        compiled_texts = "these are the possible filter arguments: \n" + self.filter_args + '\n' + "this is the structure of the filter: \n" + self.filter_struct + '\n' + "this is a sample filter structure: \n" + self.filter_sample + '\n' + "these are the properties of the container: \n" + self.container_properties + '\n' + "User query: \n" + user_query
        
       # self.filter_struct + '\n' + self.filter_args + '\n' + self.filter_sample + '\n' + self.container_properties


        body = {
        "messages": [
            {
                "role": "system",
                "content": (
                    header
                ),
            },
            {"role": "user", "content": f"This is the data: {compiled_texts}"},
        ],
       # "functions": functions,
      #  "functionCall": {"name": "get_the_fact_and_joke"},
        "temperature": 0,
        "model": "gpt-4o-mini",
    }


        self.filter_prompt = body

    

       
       

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
        
        

        return response_items["message"]['content']