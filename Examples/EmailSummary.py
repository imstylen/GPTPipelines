import os

from GPTPipelines.Core.PipeFilter import Pipe
from GPTPipelines.Core.Pipeline import Pipeline
from GPTPipelines.Filters.UtilFilters.MemoryTextFilter import MemoryTextFilter
from keychain import API_KEY

from GPTPipelines.Filters.UtilFilters.WriterFilter import WriterFilter

import json
import pandas as pd


import csv

def main():
    
    df = pd.read_csv('out/emails.csv')
    data = df.to_dict('records')

    
    prompt = """
For each email in the email chain, take the followings steps.

-From: Write only the name of who sent the message.
-To: Write only the name of who the message is addressing.
-Original: Write the original message without editing it in any way.
-Summary: Write a summary the extracted message from the previous step.

separate each email with a line.

For the conversation as a whole provide:
-Write an outline of important details.
-Write a list of outstanding action items.

 The email chain is wrapped by triple backticks. 
``` 
    """

    for i, email_data in enumerate(data):

        email_data['body'] = email_data['body']
        
        print(f"File: {i+1} of {len(data)}")
                
        email_string = json.dumps(email_data,indent=4)
        email_string = email_string.replace("\\n","\n")
        
        current_file_filter = MemoryTextFilter(
            "out/CurrentFile.txt", email_string)

        code_summarizer_kwargs = {
            'api_key': API_KEY,
            'out_file': f"out/Email{i}.txt",
            'writing_prompt':prompt,
            'debug_prompt':True
        }

        code_summarizer = WriterFilter(**code_summarizer_kwargs)

        pipe = Pipe(current_file_filter,code_summarizer)
        pipe.execute()

    print("Done!")
