from PipeFilter import *

class IdeaGenerator(Filter):
    
    def __init__(self, api_key: str, out_file: str,idea_seed_prompt:str, json_fields:str,field_word_limit=50, num_requests=1, model="gpt-3.5-turbo", temperature=0.7, max_tokens=500):
        super().__init__(api_key, out_file, num_requests, model, temperature, max_tokens)
        
        self.data_dict['idea_seed_prompt'] = idea_seed_prompt
        self.data_dict['json_fields'] = json_fields
        self.data_dict['field_word_limit'] = field_word_limit
    
    def generate_prompt(self) -> str:
        prompt = f"""Write a new idea following prompt delimited by triple backticks.

        prompt:
        ```
        {self.data_dict['idea_seed_prompt']}
        ```
        previous responses:
        ###
        {self.data_dict['responses']}
        ###
        
        format your response as json with the following fields:
        ###
        {self.data_dict['json_fields']}
        ###
        
        limit the length of your response in any field to {self.data_dict['field_word_limit']}
        
        """
        return prompt
    
        
class IdeaRanker(Filter):
    def __init__(self, api_key: str, out_file: str, ranking_prompt:str, json_fields:str, num_requests=1, model="gpt-3.5-turbo", temperature=0.7, max_tokens=500):
        super().__init__(api_key, out_file, num_requests, model, temperature, max_tokens)
        
        self.data_dict['ranking_prompt'] = ranking_prompt
        self.data_dict['json_fields'] = json_fields
        
        
    def generate_prompt(self) -> str:
        
        prompt = f"""
        The provided ideas is delimited by ```triple backticks``` 
        The provided prompt is delimited by <<<angle brackets>>>

        The Ideas are provided in json format with the following fields:
        *{self.input_filter.data_dict['json_fields']}*
        
        <<<Prompt:
        {self.data_dict['ranking_prompt']}
        >>>
        
        ```Ideas:
        {self.data_dict['input_filter_out_file']}
        ```
        
        Take the following steps:
        1. for each idea, provide a 1 sentence summary of the advantages and disadvantages of the idea with respect to the provided prompt.
        2. Provide your final ranking using your thoughts from step 1. Format your response to this step as json with the following fields: 
        *{self.data_dict['json_fields']}*
                
        """
        return prompt
    
