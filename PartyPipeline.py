from PipeFilter import *

class PartyIdeaGenerator(Filter):
    
    def generate_prompt(self) -> str:
        prompt = f"""Reply to the following prompt in less than 100 words with a new idea. Using in the following format:
        ###
        Birthday Party Idea:
        Materials Needed:
        ###

        prompt:
        ###
        Give me birthday party ideas with the materials needed.
        ###

        previous ideas:
        ###
        {self.data_dict['responses']}
        ###
        """
        return prompt
    
        
class PartyIdeaRanker(Filter):
    
    def generate_prompt(self) -> str:
        
        prompt = f"""
        Rank the following party ideas in terms of cost from most to least.
        ###
        {self.data_dict['input_file']}
        ###
        """
        return prompt
    
