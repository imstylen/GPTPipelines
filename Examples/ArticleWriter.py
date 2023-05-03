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
        "num_requests": 3,
        "field_word_limit": 100,
        "json_fields": 
            "title, description, required_materials, setup_instructions",
        "idea_seed_prompt": 
            """
            Birthday parties for a kid who loves science.
            """ 
    }
    idea_generator = IdeaGenerator(**idea_generator_kwargs)

    # Set up the IdeaRanker object with the necessary arguments
    idea_ranker_kwargs = {
        'api_key': API_KEY,
        'out_file': "out/ranked_ideas.txt",
        'ranking_prompt':
            "Provide only the top idea after sorting from least to most complex from the perspective of the busy parent who has to set it up.",
        'json_fields': "Rank, title, description, required_materials, setup_instructions"
    }
    idea_ranker = IdeaRanker(**idea_ranker_kwargs)

    # Set up the Writer object to create an outline for the article
    number_of_sections = 3
    outliner_kwargs = {
        'api_key': API_KEY,
        'out_file': "out/article_outline.txt",
        'writing_prompt': 
            f"""
                Create a detailed outline for a web article on the top ranked party idea. The article is for busy parents with young children. The article is divided into {number_of_sections} sections. Section {number_of_sections} is the conclusion.

                For each of the {number_of_sections} sections, follow these steps:
                - Create an appropriate section title.
                - Write a brief summary of the section.
                - Provide an outline for the section.
            """
    }
    article_outliner = WriterFilter(**outliner_kwargs)

    # Set up the pipeline to connect the objects
    pipeline = Pipeline()
    pipeline.add_pipe(Pipe(idea_generator, idea_ranker))
    pipeline.add_pipe(Pipe(idea_ranker, article_outliner))

    writers = []
    editors = []

    # Set up the Writer and Editor objects for each section of the article
    for i in range(number_of_sections):
        writer_kwargs = {
            'api_key': API_KEY,
            'out_file': f"out/article{i+1}_draft.txt",
            'writing_prompt': f"Write paragraphs of text for section {i+1} of the provided outline for a web article. this section will be combined with the others to form the full article."
        }
        article_writer = WriterFilter(**writer_kwargs)
        writers.append(article_writer)

        editor_kwargs = {
            'api_key': API_KEY,
            'out_file': f"out/article{i+1}_edited.txt",
            'writing_prompt': f"The provided text is section {i+1} of {number_of_sections} for a web article. edit the partial article to increase clarity, and use a fun tone suitable for a birthday party. Your text will be combined with the others to form the full article."
        }
        
        article_editor = WriterFilter(**editor_kwargs)
        editors.append(article_editor)

        # Set up the pipeline to connect the Writer and Editor objects to the article outline
        pipeline.add_pipe(Pipe(article_outliner, article_writer))
        pipeline.add_pipe(Pipe(article_writer, article_editor))

    # Execute the pipeline
    pipeline.execute()

    # Assemble the final article by combining the edited sections
    print("Assembling Articles...")
    full_article_text = ""
    for editor in editors:
        with open(editor.out_file, "r") as reader:
            full_article_text += "\n" + reader.read()
    with open("out/FinalArticle.txt", "w") as writer:
        writer.writelines(full_article_text)

    print("Done!")
