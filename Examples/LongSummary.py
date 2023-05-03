from GPTPipelines.Core.PipeFilter import Pipe
from keychain import API_KEY
from GPTPipelines.Filters.UtilFilters.LongSummaryFilter import LongSummaryFilter
from GPTPipelines.Filters.UtilFilters.FileReaderFilter import FileReaderFilter
from GPTPipelines.Core.Pipeline import Pipeline


def main():
    
    

    summarizer_kwargs = {
        'api_key': API_KEY,
        'out_file': "out/summary.txt",
        'writing_prompt': 
            f"""
                Write a detailed summary of the key points.
            """
    }
    
    file_reader_filter = FileReaderFilter("out/wiki.txt")
    long_summary_filter = LongSummaryFilter(**summarizer_kwargs)
    
    pipe1 = Pipe(file_reader_filter,long_summary_filter)
    
    summarizer_kwargs['out_file'] = "out/summary2.txt"
    long_summary_filter2 = LongSummaryFilter(**summarizer_kwargs)
    
    pipe2 = Pipe(long_summary_filter,long_summary_filter2)

    pipeline = Pipeline()
    pipeline.add_pipe(pipe1)
    pipeline.add_pipe(pipe2)
    
    pipeline.execute()

    print("Done!")
