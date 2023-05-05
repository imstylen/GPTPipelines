from GPTPipelines.LLMs.OpenAI.ChatGPTFilter import ChatGPTFilter
from GPTPipelines.Util.Text.SplitText import split_text_by_tokens


class LongSummaryFilter(ChatGPTFilter):
    def __init__(self, **kwargs):
        """
        A class for generating discourse based on a writing prompt, and reference material.

        Args:
            **kwargs: Additional keyword arguments to pass to the parent class.
                writing_prompt (str): The prompt to use for generating writing prompts.
        """
        super().__init__(**kwargs)
        
        self.prompt_content['writing_prompt'] = kwargs.get('writing_prompt')
        self.prompt_template = "LongSummary.prompt"

    def generate_prompt(self) -> str:
        prompt = super().generate_prompt()
        self.prompt_content['chunk_counter']+=1
        return prompt

    def run(self):
        # Split the text into chunks of 2048 tokens each.
        token_count = 2048
        self.prompt_content["text_chunks"] = split_text_by_tokens(self.prompt_content['input_filter_out_file'], token_count)
        # Set a counter to increment after each submission.
        self.prompt_content["chunk_counter"] = 0
        
        self.num_requests = len(self.prompt_content['text_chunks'])
        
        super().run()