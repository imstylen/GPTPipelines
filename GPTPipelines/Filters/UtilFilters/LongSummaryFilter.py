from GPTPipelines.LLMs.OpenAIAssistant import OpenAIAssistant
from GPTPipelines.Util.Text.SplitText import split_text_by_tokens


class LongSummaryFilter(OpenAIAssistant):
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
        
        prompt = f"""
        The provided prompt is delimited by <<<angle brackets>>>
        The provided reference material is delimited by ```triple backticks``` 

        <<<Prompt:
        Use the provided reference material as the basis for your response.
        {self.data_dict['writing_prompt']}
        >>>
        
        ```reference material:
        {self.text_chunks[self.chunk_counter]}
        ```
 
        """
        self.chunk_counter+=1
        return prompt

    def run(self):
        # Split the text into chunks of 2048 tokens each.
        token_count = 2048
        self.text_chunks = split_text_by_tokens(self.data_dict['input_filter_out_file'], token_count)
        # Set a counter to increment after each submission.
        self.chunk_counter = 0
        
        self.num_requests = len(self.text_chunks)
        
        super().run()