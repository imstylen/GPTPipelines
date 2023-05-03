from GPTPipelines.Core.PipeFilter import Pipe
from keychain import API_KEY
from GPTPipelines.Filters.UtilFilters.WriterFilter import WriterFilter
from GPTPipelines.Core.Pipeline import Pipeline
from GPTPipelines.Filters.UtilFilters.JsonConcatFilesFilter import JsonConcatFilesFilter
from GPTPipelines.Filters.UtilFilters.FileReaderFilter import FileReaderFilter


def main():

    critic_kwargs = {
        'api_key': API_KEY,
        'out_file': "out/0feedback.txt",
        'writing_prompt': 
            f"""
                You are an esteemed professor in the field of material science. You mentor a PHD student who is preparing a research proposal to determine an optimal concrete mix design using only: portland cement, silica sand, perlite, sodium silicate (waterglass). Optional additives include steel wool and fiberglass strings. Most importantly, the mix is intended to be used in a refractory setting with very high temperatures.
                
                To compare current progress of the proposal, you are given the following json formated fields: CurrentProposal, Previous Proposal.
                
                To provide feedback complete the following steps.
                
                1. summarize the changes between the current and previous proposals.
                2. discuss how each of these changes either improved or worsened the proposal.
                3. Write whether the changes made as a whole were, positive, negative, or neutral.
                4. Provide brief feedback on how to improve the proposal for the next iteration.
                
                The student understands that your feedback is intended to help improve the final proposal and appreciates your critiques.

            """
    }

    actor_kwargs = {
        'api_key': API_KEY,
        'out_file': "out/proposal0.txt",
        'temperature':0.75,
        'writing_prompt': 
            f"""
                You are a PHD student who is preparing a research proposal to determine an optimal concrete mix design using only: portland cement, silica sand, perlite, sodium silicate (waterglass). Optional additives include steel wool and fiberglass strings. Most importantly, the mix is intended to be used in a refractory setting with very high temperatures.
                
                Your professor has provided you feedback on your current iteration of the proposal. Use the feedback to rewrite and improve your proposal in no more that 500 words. Only include the rewritten proposal in your response.
            """
    }

    num_meetings = 3
    
    for i in range(1,num_meetings):
        file_reader_filter = FileReaderFilter(f"out/{i-1}proposal.txt")  
        
        actor_kwargs['out_file'] = f"out/{i}proposal.txt"
        actor_filter = WriterFilter(**actor_kwargs)

        concat_filter = JsonConcatFilesFilter(
                                                f"out/{i}progress.txt",
                                                ("CurrentProposal",f"out/{i}proposal.txt"),
                                                ("PreviousProposal: ",f"out/{i-1}proposal.txt")
                                            )
        
        critic_kwargs['out_file'] = f"out/{i}feedback.txt"
        critic_filter = WriterFilter(**critic_kwargs)
        
        pipeline = Pipeline()
        pipeline.add_pipe(Pipe(file_reader_filter,actor_filter))
        pipeline.add_pipe(Pipe(actor_filter,concat_filter))
        pipeline.add_pipe(Pipe(concat_filter,critic_filter))
        pipeline.execute()

    print("Done!")
