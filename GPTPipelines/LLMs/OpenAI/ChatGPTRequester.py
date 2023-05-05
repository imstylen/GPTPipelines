import openai

class ChatGPTRequester:
    def __init__(self,api_key, model, temperature, max_tokens,system_message):
        openai.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.system_message = system_message

    def submit_request(self, prompt):
        # Submit request to OpenAI API and return response
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature
        )
        
        return response

