from OpenAIAssistant import OpenAIAssistant

class SimpleChat(OpenAIAssistant):
    
    def __init__(self, api_key: str, out_file: str, prompt:str, model="gpt-3.5-turbo", temperature=0.7, max_tokens=500):
        super().__init__(api_key, out_file, model, temperature, max_tokens)
        self.prompt=prompt
    
    def generate_prompt(self) -> str:
        return self.prompt