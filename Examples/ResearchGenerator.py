from GPTPipelines.Filters.IdeaPipelineFilters import IdeaGenerator, IdeaRanker
from GPTPipelines.Core.PipeFilter import Pipe
from keychain import API_KEY
from GPTPipelines.Filters.UtilFilters.WriterFilter import WriterFilter
from GPTPipelines.Core.Pipeline import Pipeline

def main():
    # Set up the IdeaGenerator object with the necessary arguments
    idea_generator_kwargs = {
        "api_key": API_KEY,
        "out_file": "out/ideas.txt",
        "num_requests": 10,
        "field_word_limit": 100,
        "json_fields": 
            "method_description, required_materials, instructions",
        "idea_seed_prompt": 
            """
            Scientific research methods for a PHD student to determine an optimal concrete mix design using only: portland cement, silica sand, perlite, sodium silicate (waterglass). Optional additives include steel whool and fiberglass strings. 
            """ 
    }
    idea_generator = IdeaGenerator(**idea_generator_kwargs)

    # Set up the IdeaRanker object with the necessary arguments
    idea_ranker_kwargs = {
        'api_key': API_KEY,
        'out_file': "out/ranked_ideas.txt",
        'ranking_prompt':
            "Provide only the top 5 ideas from the perspective of a professor providing feedback to a PHD student developing a research proposal to determine an optimal concrete mix design using only: portland cement, silica sand, perlite, sodium silicate (waterglass). Optional additives include steel wool and fiberglass strings. ",
        
        'json_fields': "Rank, method_description, required_materials, instructions"
    }
    idea_ranker = IdeaRanker(**idea_ranker_kwargs)

    # Set up the Writer object to create an outline for the article

    outliner_kwargs = {
        'api_key': API_KEY,
        'out_file': "out/article_outline.txt",
        'writing_prompt': 
            f"""
                Incorporate the top 5 ranked research methods to create a detailed outline for a research proposal for Scientific research methods for a PHD student to determine an optimal concrete mix design using only: portland cement, silica sand, perlite, sodium silicate (waterglass). Optional additives include steel wool and fiberglass strings. 
            """
    }
    outliner = WriterFilter(**outliner_kwargs)

    # Set up the pipeline to connect the objects
    pipeline = Pipeline()
    pipeline.add_pipe(Pipe(idea_generator, idea_ranker))
    pipeline.add_pipe(Pipe(idea_ranker, outliner))

    pipeline.execute()

    print("Done!")
