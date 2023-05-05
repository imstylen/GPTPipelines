from GPTPipelines.LLMs.OpenAI.ChatGPTFilter import ChatGPTFilter

class IdeaGenerator(ChatGPTFilter):
    
    def __init__(self, **kwargs):
        """
        A class for generating ideas using OpenAI's GPT-3 API.

        Args:
            **kwargs: Additional keyword arguments to pass to the parent class.
                idea_seed_prompt (str): The prompt to use for generating ideas. Defaults to "Ideas that help me realize I didnt provide a prompt."
                json_fields (str): The fields to include in the JSON response. Defaults to "None".
                field_word_limit (int): The maximum number of words allowed in each field of the JSON response. Defaults to 100.
        """
        super().__init__(**kwargs)
        
        self.prompt_content['idea_seed_prompt'] = kwargs.get("idea_seed_prompt", "Ideas that help me realize I didnt provide a prompt.")
        self.prompt_content['json_fields'] = kwargs.get("json_fields","None")
        self.prompt_content['field_word_limit'] = kwargs.get("field_word_limit",100)
    
    def generate_prompt(self) -> str:
        """
        Generate a prompt for the user to follow when generating an idea.

        Returns:
            str: The generated prompt.
        """
        previous = '\n'.join(self.prompt_content['responses'])
        prompt = f"""Write a new idea following prompt delimited by triple backticks.

        prompt:
        ```
        {self.prompt_content['idea_seed_prompt']}
        ```
        previous responses:
        ###
        {previous}
        ###
        
        format your response as json with the following fields:
        ###
        {self.prompt_content['json_fields']}
        ###
        
        limit the length of your response in any field to {self.prompt_content['field_word_limit']}
        
        """
        return prompt
    
    
class IdeaRanker(ChatGPTFilter):
    def __init__(self, **kwargs):
        """
        A class for ranking ideas generated using OpenAI's GPT-3 API.

        Args:
            **kwargs: Additional keyword arguments to pass to the parent class.
                ranking_prompt (str): The prompt to use for ranking ideas. Defaults to "None".
                json_fields (str): The fields to include in the JSON response. Defaults to "None".
        """
        super().__init__(**kwargs)
        self.prompt_content['ranking_prompt'] = kwargs.get("ranking_prompt","None")
        self.prompt_content['json_fields'] = kwargs.get("json_fields","None")
        
        
    def generate_prompt(self) -> str:
        """
        Generate a prompt for the user to follow when ranking ideas.

        Returns:
            str: The generated prompt.
        """
        
        prompt = f"""
        The provided ideas is delimited by ```triple backticks``` 
        The provided prompt is delimited by <<<angle brackets>>>

        The Ideas are provided in json format with the following fields:
        *{self.input_filter.data_dict['json_fields']}*
        
        <<<Prompt:
        {self.prompt_content['ranking_prompt']}
        >>>
        
        ```Ideas:
        {self.prompt_content['input_filter_out_file']}
        ```
        
        Take the following steps:
        1. for each idea, provide a 1 sentence summary of the advantages and disadvantages of the idea with respect to the provided prompt.
        
        2. Provide your final ranking using your thoughts from step 1. Format your response to this step as json with the following fields: *{self.prompt_content['json_fields']}*
        Example Response for step 2:
        Step 2:
        Json - 
        {{
          
          field1: ...,
          field2: ...  
    
        }}
                
        """
        return prompt
