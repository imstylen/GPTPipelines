from GPTPipelines.Filters.IdeaPipelineFilters import IdeaGenerator, IdeaRanker
from GPTPipelines.Core.PipeFilter import Pipe
from keychain import API_KEY
from GPTPipelines.Filters.UtilFilters.WriterFilter import WriterFilter
from GPTPipelines.Filters.UtilFilters.MemoryTextFilter import MemoryTextFilter

from GPTPipelines.Core.Pipeline import Pipeline

def main():

    mem_text_filter = MemoryTextFilter("out/MemText.txt","This is a test.")

    outliner_kwargs = {
        'api_key': API_KEY,
        'out_file': "out/article_outline.txt",
        'writing_prompt': 
            """
                Translate this to spanish.
            """,
        'debug_prompt':True
    }
    
    outliner = WriterFilter(**outliner_kwargs)

    # Set up the pipeline to connect the objects
    pipeline = Pipeline()
    pipeline.add_pipe(Pipe(mem_text_filter, outliner))
    pipeline.execute()

    print("Done!")
