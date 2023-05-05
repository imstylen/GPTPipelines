import os

from GPTPipelines.Core.PipeFilter import Pipe
from GPTPipelines.Core.Pipeline import Pipeline
from GPTPipelines.Filters.UtilFilters.MemoryTextFilter import MemoryTextFilter
from GPTPipelines.Filters.UtilFilters.JsonConcatFilesFilter import JsonConcatFilesFilter
from keychain import API_KEY

from GPTPipelines.Filters.UtilFilters.WriterFilter import WriterFilter

from Examples.Util.AllFilesText import get_all_file_paths,read_files


def main():
    
    json_concat_filter = JsonConcatFilesFilter("out/current_implementation.txt",
                                               ("feedback","C:\Dev\GPT\out\ArchitectureReviewExample.txt"),
                                               ("current_implementation","C:\Dev\GPT\GPTPipelines\Filters\IdeaPipelineFilters.py"))
    
    prompt = """
    
Respond in the following steps. The provided steps are surrounded by <<<tripple angle brackets>>>. Each step begins with two hyphens "--".

<<<
-- write a list of the architectural difference between what the feedback is suggesting, and the current implementation.
-- Write a list of actions that must take place to update our code to reflect the essence of the feedback.
-- Add TODO comments to the code from the current_implementation that when implemented will reflect the actions from the previous step.
>>>


The lead architect has provided you feedback on the implementation of one of the classes in the codebase. Without delving too deeply into the codebase, he has provided you with some vague skeleton classes as examples that capture the essence of his recommendation. They do not match exactly your code base.

Reference material has been provided to you in the following format
{
    feedback: "...",
    current_implementation: "..."
}


    """

    code_summarizer_kwargs = {
        'api_key': API_KEY,
        'out_file': f"out/Report/CodeReviewImplementation.txt",
        'writing_prompt':prompt,
        'debug_prompt':True
    }

    code_summarizer = WriterFilter(**code_summarizer_kwargs)

    pipe = Pipe(json_concat_filter ,code_summarizer)
    pipe.execute()

    print("Done!")
