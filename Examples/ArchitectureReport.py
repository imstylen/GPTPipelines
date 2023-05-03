import os

from GPTPipelines.Core.PipeFilter import Pipe
from GPTPipelines.Core.Pipeline import Pipeline
from GPTPipelines.Filters.UtilFilters.MemoryTextFilter import MemoryTextFilter
from keychain import API_KEY

from GPTPipelines.Filters.UtilFilters.WriterFilter import WriterFilter

from Examples.Util.AllFilesText import get_all_file_paths,read_files


def main():
    
    
    prompt = """
Respond in the following steps. The provided steps are surrounded by <<<tripple angle brackets>>>. Each step begins with two hyphens "--".

<<<
-- write the relative location of this file. 

-- create a list of the files that this file depends on.

-- Use the json format delimited by ###tripple pound symbols### create a list of the classes declared in this file.

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

-- Use the json format delimited by ```tripple backticks``` to list the stand-alone functions declared in this file. Stand-alone functions do not belong to a class.

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

Respond in the following format:
===
-- <step 1 response>
-- <step 2 response>
-- ...
===

    """

    file_paths = get_all_file_paths('GPTPipelines')
    file_contents = read_files(file_paths,['.pyc'])

    for i, file_content in enumerate(file_contents):

        print(f"File: {i+1} of {len(file_contents)}")
        
        current_file_filter = MemoryTextFilter(
            "out/CurrentFile.txt", file_content)

        code_summarizer_kwargs = {
            'api_key': API_KEY,
            'out_file': f"out/Report/File{i}.txt",
            'writing_prompt':prompt
        }

        code_summarizer = WriterFilter(**code_summarizer_kwargs)

        pipe = Pipe(current_file_filter,code_summarizer)
        pipe.execute()

    print("Done!")
