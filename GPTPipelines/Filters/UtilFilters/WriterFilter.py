from GPTPipelines.LLMs.OpenAI.ChatGPTFilter import ChatGPTFilter

class WriterFilter(ChatGPTFilter):
    def __init__(self, **kwargs):
        """
        A class for generating discourse based on a writing prompt, and reference material.

        Args:
            **kwargs: Additional keyword arguments to pass to the parent class.
                writing_prompt (str): The prompt to use for generating writing prompts.
        """
        super().__init__(**kwargs)

        self.prompt_content['writing_prompt'] = kwargs.get('writing_prompt')
        self.prompt_template = "Writer.prompt"
        
        
