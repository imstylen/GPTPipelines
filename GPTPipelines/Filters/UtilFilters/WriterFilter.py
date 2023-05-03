from GPTPipelines.LLMs.OpenAIAssistant import OpenAIAssistant

class WriterFilter(OpenAIAssistant):
    def __init__(self, **kwargs):
        """
        A class for generating discourse based on a writing prompt, and reference material.

        Args:
            **kwargs: Additional keyword arguments to pass to the parent class.
                writing_prompt (str): The prompt to use for generating writing prompts.
        """
        super().__init__(**kwargs)
        
        self.data_dict['writing_prompt'] = kwargs.get('writing_prompt')
        
    def generate_prompt(self) -> str:
        """
        Generate a prompt for the user to follow when writing.

        Returns:
            str: The generated prompt.
        """
        
        ref_material = self.data_dict['input_filter_out_file']
        
        prompt = f"""
        The provided prompt is delimited by <<<angle brackets>>>
        The provided reference material is delimited by ```triple backticks``` 

        <<<Prompt:
        Use the provided reference material as the basis for your response.
        {self.data_dict['writing_prompt']}
        >>>
        
        ```reference material:
        {ref_material}
        ```
 
        """
        return prompt
