import openai
from tqdm import tqdm
from PipeFilter import Filter

class OpenAIAssistant(Filter):
    def __init__(self, **kwargs):
        """
        A class that uses the OpenAI API to generate text based on a prompt.

        Args:
            api_key (str): The OpenAI API key.
            model (str, optional): The name of the OpenAI model to use. Defaults to 'gpt-3.5-turbo'.
            temperature (float, optional): Controls the "creativity" of the generated text. Higher values result in more creative responses. Defaults to 0.0.
            max_tokens (int, optional): The maximum number of tokens (words) in the generated response. Defaults to 2048.
            system_message (str, optional): The message to display as the "system" role in the chat. Defaults to 'You are a helpful assistant'.
            out_file (str): The path to the output file where the generated text will be saved.
            debug_prompt (bool, optional): Whether or not to save the last prompt used to generate text to a separate file. Defaults to True.
            num_requests (int, optional): The number of requests to make to the OpenAI API. Defaults to 1.
        """
        super().__init__()
        openai.api_key = kwargs['api_key']
        self.model = kwargs.get('model', 'gpt-3.5-turbo')
        self.temperature = kwargs.get('temperature', 0.0)
        self.max_tokens = kwargs.get('max_tokens', 2048)
        self.system_message = kwargs.get('system_message', 'You are a helpful assistant')
        self.data_dict = {'responses': []}
        self.out_file = kwargs['out_file']
        self.debug_prompt = kwargs.get('debug_prompt', True)
        self.num_requests = kwargs.get('num_requests', 1)
            

    def generate_prompt(self) -> str:
        """Return a prompt string.

        Example only, subclasses should override this method.
        """
        prompt = f"""
        Overwrite me.
        """
        return prompt
        
    def _submit_request(self):
        """Submit a request to the OpenAI API and store the response in `self.data_dict`."""
        prompt = self.generate_prompt()
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature
        )
        self.process_response(response)
        self.last_prompt = prompt

    def process_response(self, response):
        """Process the response from the OpenAI API and add it to `self.data_dict`."""
        self.data_dict['responses'].append(response['choices'][0]['message']['content'])
        
    def run(self):
        """Run the assistant and save the responses to a file."""
        super().run()
        
        if self.input_filter is not None:
            with open(self.input_filter.out_file,"r") as file:
                self.data_dict['input_filter_out_file'] = file.read()
                
        for _ in tqdm(range(self.num_requests)):
            self._submit_request()
                
        self.write_out_file()

    def write_out_file(self):
        """Write the generated text to the output file."""
        with open(self.out_file,"w") as writer:
            for t in self.data_dict['responses']:
                writer.writelines(t)

        if(self.debug_prompt):
           with open(self.out_file+"P","w") as writer:
                writer.writelines(self.last_prompt)
