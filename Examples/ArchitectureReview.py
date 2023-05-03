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
Respond in the following steps.
1. For each file: in less that 100 words, summarize the main architectural aspects of the file including: inheritance, dependencies, patterns, etc.
2. Summarize the structure of the architecture of the code base as a whole.
3. Provide feedback on the architecture with respect to solid principles.
4. Provide a thorough list of specific recommendations with examples to optimize the architecture of this code base.

The format of the provided reports is shown below surrounded by <<<tripple angle brackets>>>. Each section begins with two hyphens "--".

<<<
-- The relative location of this file. 

-- The list of the files that this file depends on.

-- The json format delimited by ###tripple pound symbols### create a list of the classes declared in this file.

### start class json format
Example step response:
[
    {
    class: "Dog",
    parent_class:"Animal",
    other_dependencies: [House, Family]
    class_methods: ["bark()"],
    parent_method_overrides: [eat(food), poop(), sleep(time)],
    properties: ["family (Family), house (House), breed (string), age (int)]
    description: "A 'Dog' animal that belongs to a house, with a family"
    }, ...
]
### end class json format

-- The json format delimited by ```tripple backticks``` to list the stand-alone functions declared in this file. Stand-alone functions do not belong to a class.

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
        'out_file': f"out/ArchitectureReview.txt",
        'writing_prompt':prompt
    }

    code_summarizer = WriterFilter(**code_summarizer_kwargs)

    pipe = Pipe(current_file_filter,code_summarizer)
    pipe.execute()

    print("Done!")
