from GPTPipelines.Core.PipeFilter import Filter

class MemoryTextFilter(Filter):
    
    def __init__(self, out_file, text):
        super().__init__() 
        self.prompt_content['out_file'] = out_file
        self.out_file = out_file
        self.text = text
        
    def run(self):
        super().run()

        with open(self.out_file, "w") as writer:
            writer.write(self.text)