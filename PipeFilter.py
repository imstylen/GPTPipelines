from OpenAIAssistant import OpenAIAssistant

class Filter(OpenAIAssistant):
    def __init__(self, api_key: str, out_file: str, num_requests = 1, model="gpt-3.5-turbo", temperature=0.7, max_tokens=500):
        super().__init__(api_key, out_file, model, temperature, max_tokens)
        self.did_process = False
        self.num_requests = num_requests
        
    def process(self, input_file = None):
        if input_file is not None:
            with open(input_file,"r") as file:
                self.data_dict['input_file'] = file.readlines()
                
        self._run(self.num_requests)
        
class Pipe:
    def __init__(self, input_filter: Filter, output_filter: Filter):
        self.input_filter = input_filter
        self.output_filter = output_filter
        self.process()
        
    def process(self):
        if not self.input_filter.did_process:
            self.input_filter.process()
            
        self.output_filter.process(self.input_filter.out_file)
