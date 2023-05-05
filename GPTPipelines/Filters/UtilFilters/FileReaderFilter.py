from GPTPipelines.Core.PipeFilter import Filter

class FileReaderFilter(Filter):
    
    def __init__(self, file_path):
        super().__init__() 
        self.prompt_content['out_file'] = file_path
        self.out_file = file_path