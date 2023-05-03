import os

from GPTPipelines.Core.PipeFilter import Pipe
from GPTPipelines.Core.Pipeline import Pipeline
from GPTPipelines.Filters.UtilFilters.MemoryTextFilter import MemoryTextFilter
from keychain import API_KEY

from GPTPipelines.Filters.UtilFilters.WriterFilter import WriterFilter

from Examples.Util.AllFilesText import get_all_file_paths,read_files


def main():
    
    report_files = get_all_file_paths("out/Report")
    contents = read_files(report_files)
    content = '\n'.join(contents)
   
    
    prompt = """
The lead architect has provided you with feedback surrounded by +++triple plus signs+++ based on the provided reports from the current code base. 

Complete the following steps:
1. Based on the reports from the existing code base, explain why the architect has given this feedback.
2. Summarize the changes that need to be made to incorporate this feedback into the code base.
3. Write skeleton classes for the newly created, and modified classes after the feedback has been incorporated.

+++ Feedback: Refactor the OpenAIAssistant class to follow the Single Responsibility Principle by separating the responsibilities of submitting requests, processing responses, and writing output to a file into separate classes.+++

The format of the reports used to create the feedback is shown below surrounded by <<<triple angle brackets>>>. Each section begins with two hyphens "--".

<<<
-- The relative location of this file. 

-- The list of the files that this file depends on.

-- The json format delimited by ###triple pound symbols### create a list of the classes declared in this file.

### start class json format
Example step response:
[
    {
    class: "Dog",
    parent:"Animal",
    dependencies: [Animal, Building.House, Family]
    methods: ["bark()", "eat(food)", "poop()", "sleep(time)"],
    properties: ["family (Family), house (House), breed (string), age (int)]
    description: "A 'Dog' animal that belongs to a house, with a family"
    }, ...

]
### end class json format

-- The json format delimited by ```triple backticks``` to list the stand-alone functions declared in this file. Stand-alone functions do not belong to a class.

``` start function json format
Example step response:
[
    {
    function: "say_hello",
    input:"name (string)",
    output:"hello_txt (string)"
    description:"inserts name into the string: 'hello {name}'. "
    }, ...

]
``` end json function format

>>>

"""


    current_file_filter = MemoryTextFilter(
        "out/CurrentFile.txt", content)

    code_summarizer_kwargs = {
        'api_key': API_KEY,
        'out_file': f"out/ArchitectureReviewExample.txt",
        'writing_prompt':prompt
    }

    code_summarizer = WriterFilter(**code_summarizer_kwargs)

    pipe = Pipe(current_file_filter,code_summarizer)
    pipe.execute()

    print("Done!")
