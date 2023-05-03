import openai
from tqdm import tqdm
from GPTPipelines.Core.LLMInterface import LLMInterface
from tenacity import retry, wait_random_exponential, stop_after_attempt, retry_if_not_exception_type

class OpenAIAssistant(LLMInterface):
    def __init__(self, **kwargs):

        super().__init__()
        openai.api_key = kwargs['api_key']
        self.model = kwargs.get('model', 'gpt-3.5-turbo')
        self.temperature = kwargs.get('temperature', 0.0)
        self.max_tokens = kwargs.get('max_tokens', 2048)
        self.system_message = kwargs.get('system_message', 'You are a helpful assistant')
        self.data_dict['responses'] = []
        self.out_file = kwargs['out_file']
        self.debug_prompt = kwargs.get('debug_prompt', False)
        self.num_requests = kwargs.get('num_requests', 1)
        self.output = ''
            
    def run(self):
        """Run the assistant and save the responses to a file."""
        super().run()
                
        for _ in tqdm(range(self.num_requests)):
            self._submit_request()
                
        self.write_out_file()
        
    # let's make sure to not retry on an invalid request, because that is what we want to demonstrate
    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6), retry=retry_if_not_exception_type(openai.InvalidRequestError))    
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
             
    def generate_prompt(self) -> str:
        """Return a prompt string.

        Example only, subclasses should override this method.
        """
        prompt = f"""
        Overwrite me.
        """
        return prompt
        
    def process_response(self, response):
        """Process the response from the OpenAI API and add it to `self.data_dict`."""
        self.data_dict['responses'].append(response['choices'][0]['message']['content'])
        
    def write_out_file(self):
        """Write the generated text to the output file."""
        
        with open(self.out_file,"w") as writer:
            for t in self.data_dict['responses']:
                writer.writelines(t)
                self.output += t + '\n'

        if(self.debug_prompt):
           with open(self.out_file+"P","w") as writer:
                writer.writelines(self.last_prompt)
