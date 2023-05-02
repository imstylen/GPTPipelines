import json
from GPTPipelines.Core.PipeFilter import Filter

class JsonConcatFilesFilter(Filter):
    
    def __init__(self, out_file, *args):
        super().__init__() 
        self.data_dict['out_file'] = out_file
        self.out_file = out_file
        
        self.key_data_pairs = args
        
    def run(self):
        super().run()
        
        data = {}
        
        for key, file in self.key_data_pairs:
            with open(file, "r") as reader:
                data[key] = reader.read().replace("\n"," ")
                
        with open(self.out_file, "w") as writer:
            writer.write(json.dumps(data,indent=4,separators=(", ", ": ")))

    
        