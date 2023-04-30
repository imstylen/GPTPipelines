from OpenAIAssistant import OpenAIAssistant

class Filter(OpenAIAssistant):
    def __init__(self, api_key: str, out_file: str, num_requests = 1, model="gpt-3.5-turbo", temperature=0.0, max_tokens=2048):
        super().__init__(api_key, out_file, model, temperature, max_tokens)
        self.did_run = False
        self.num_requests = num_requests
        self.input_filter = None
        
    def run(self):
        if self.input_filter is not None:
            with open(self.input_filter.out_file,"r") as file:
                self.data_dict['input_filter_out_file'] = file.readlines()
                
        self.execute(self.num_requests)
        self.did_run = True
        
class Pipe:
    def __init__(self, input_filter: Filter, output_filter: Filter):
        self.input_filter = input_filter
        
        self.output_filter = output_filter
        self.output_filter.input_filter = input_filter
        
        
    def execute(self):
        if not self.input_filter.did_run:
            self.input_filter.run()
            
        self.output_filter.run()
