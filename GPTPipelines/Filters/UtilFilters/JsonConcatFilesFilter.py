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
                data[key] = reader.read()
        
        # Replace escaped newline characters with actual new lines
        data_str = json.dumps(data, indent=4, separators=(", ", ": "), ensure_ascii=False)
        data_str = data_str.replace('\\n', '\n')        
        
        with open(self.out_file, "w") as writer:
            writer.write(data_str)

    
        