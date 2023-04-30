from PipeFilter import *       

class Writer(Filter):
    def __init__(self, api_key: str, out_file: str, writing_prompt:str, num_requests=1, model="gpt-3.5-turbo", temperature=0.7, max_tokens=500):
        super().__init__(api_key, out_file, num_requests, model, temperature, max_tokens)
        
        self.data_dict['writing_prompt'] = writing_prompt

    def generate_prompt(self) -> str:
        
        prompt = f"""
        The provided prompt is delimited by <<<angle brackets>>>
        The provided reference material is delimited by ```triple backticks``` 

        <<<Prompt:
        Use the provided reference material as the basis for your response.
        {self.data_dict['writing_prompt']}
        >>>
        
        ```reference material:
        {self.data_dict['input_filter_out_file']}
        ```
 
        """
        return prompt
    
