import openai
from tqdm import tqdm


class OpenAIAssistant:
    def __init__(self, api_key: str,out_file: str, model = "gpt-3.5-turbo", temperature=0.7, max_tokens=500):
        openai.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.data_dict = {'responses': []}
        self.out_file = out_file

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
                {"role": "system", "content": "You are a helpful assistant to a software engineer"},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature
        )
        self.process_response(response)

    def process_response(self, response):
        self.data_dict['responses'].append(response['choices'][0]['message']['content'])
        
    def _run(self, num_requests):
        """Run the assistant and save the responses to a file."""
        for i in tqdm(range(num_requests)):
            self._submit_request()

        with open(self.out_file,"w") as writer:
            for i,t in enumerate(self.data_dict['responses']):
                writer.write(f"###\n")
                writer.write(f"Response: {i}\n")
                writer.writelines(t)
                writer.write(f"###\n\n")
