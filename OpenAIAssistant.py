import openai
from tqdm import tqdm


class OpenAIAssistant:
    def __init__(self, api_key: str,out_file: str, model = "gpt-3.5-turbo", temperature=0.0, max_tokens=2048,system_message:str = "You are a helpful assistant", debug_prompt=True):
        openai.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.system_message = system_message
        self.data_dict = {'responses': []}
        self.out_file = out_file
        self.debug_prompt = debug_prompt
        

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
        self.data_dict['responses'].append(response['choices'][0]['message']['content'])
        
    def execute(self, num_requests):
        """Run the assistant and save the responses to a file."""
        for i in tqdm(range(num_requests)):
            self._submit_request()

        self.write_out_file()

    def write_out_file(self):

        with open(self.out_file,"w") as writer:
            for t in self.data_dict['responses']:
                writer.writelines(t)

        if(self.debug_prompt):
           with open(self.out_file+"P","w") as writer:
                writer.writelines(self.last_prompt)
    
