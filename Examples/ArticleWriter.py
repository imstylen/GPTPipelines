from GPTPipelines.Pipelines.IdeaPipeline import IdeaGenerator,IdeaRanker
from GPTPipelines.Core.PipeFilter import Pipe
from keychain import API_KEY
from GPTPipelines.Util.Util import Writer

#   filter           pipe        filter
# (generator)===>===>===>===>===(ranker)
# 
# generation prompt -> out1.txt -> next prompt -> out2.txt

def main():
    ###########################
    # Plan the Article
    ###########################
    kwargs = {
        "api_key": API_KEY,
        "out_file": "out/ideas.txt",
        "idea_seed_prompt": """
            Birthday parties for a kid who loves science.
        """,
        "json_fields": "title, description, required_materials, setup_instructions",
        "num_requests": 3,
        "field_word_limit": 100
    }

    idea_generator = IdeaGenerator(**kwargs)
        
    kwargs = {
        'api_key': API_KEY,
        'out_file': "out/ranked_ideas.txt",
        'ranking_prompt': "Provide only the top idea after sorting from least to most complex from the perspective of the busy parent who has to set it up.",
        'json_fields': "Rank, title, description, required_materials, setup_instructions"
    }

    idea_ranker = IdeaRanker(**kwargs)

    kwargs = {
        'api_key': API_KEY,
        'out_file': "out/article_outline.txt",
        'writing_prompt': "write a detailed outline divided into exactly 3 sections for an web article intended for busy parents of young children on the rank 1 party idea."
    }

    article_outliner = Writer(**kwargs)

    
    pipeline = []
    pipeline.append(Pipe(idea_generator, idea_ranker))
    pipeline.append(Pipe(idea_ranker, article_outliner))
    
    ###########################
    # Write the Article
    ###########################
    writers = []
    editors = []
    for i in range (1,4):
        kwargs = {
            'api_key': API_KEY,
            'out_file': f"out/article{i}_draft.txt",
            'writing_prompt': f"write the full text for only section {i} of the web article. Use no more than 1000 words. The article is based on the provided outline.This section will be combined with the others to form the full article."
        }

        article_writer = Writer(**kwargs)

        writers.append(article_writer)
        
        kwargs = {
            'api_key': API_KEY,
            'out_file': f"out/article{i}_edited.txt",
            'writing_prompt': f"edit the article section to maximize the reader's comprehension, and use a fun tone suitable for a birthday party. This section will be combined with the others to form the full article."
        }

        article_editor = Writer(**kwargs)

        editors.append(article_editor)
        
        pipeline.append(Pipe(article_outliner, article_writer))
        pipeline.append(Pipe(article_writer, article_editor))
    
    for i,pipe in enumerate(pipeline):
        print(f"Step {i} of {len(pipeline)}:")
        pipe.execute()
        
    print("Assembling Articles...")
    
    full_article_text = ""
    for editor in editors:
        with open(editor.out_file, "r") as reader:
            full_article_text+= "\n" + reader.read()
            
        with open("FinalArticle.txt","w") as writer:
            writer.writelines(full_article_text)
                
    print("Done!")
        
