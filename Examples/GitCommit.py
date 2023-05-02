from GPTPipelines.Core.PipeFilter import Pipe
from keychain import API_KEY
from GPTPipelines.Filters.Util.WriterFilter import WriterFilter
from GPTPipelines.Core.Pipeline import Pipeline
from GPTPipelines.Filters.Util.JsonConcatFilesFilter import JsonConcatFilesFilter
from GPTPipelines.Filters.Util.FileReaderFilter import FileReaderFilter


def main():

    actor_kwargs = {
        'api_key': API_KEY,
        'out_file': "out/proposal0.txt",
        'writing_prompt': 
            f"""
                Take the following steps to use the provided git diff to write a commit message. :
                Step 1. Write a thorough list of the of the changes shown in the diff in outline format.
                Step 2. Write a detailed summary of these changes based on your outline.
                Step 3. Write a full commit message in the following format:
                
                Step 3 format:
                ###
                Commit title:
                Commit description:
                ###
            """
    }
    
    file_reader_filter = FileReaderFilter(f"out/diff.txt")  
    
    actor_kwargs['out_file'] = f"out/commit.txt"
    actor_filter = WriterFilter(**actor_kwargs)
    
    pipeline = Pipeline()
    pipeline.add_pipe(Pipe(file_reader_filter,actor_filter))
    pipeline.execute()
    
    num_meetings = 3
    
    print("Done!")
