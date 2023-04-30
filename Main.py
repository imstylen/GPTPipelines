from PartyPipeline import PartyIdeaGenerator,PartyIdeaRanker
from PipeFilter import Pipe

from keychain import API_KEY



idea_generator = PartyIdeaGenerator(API_KEY,"out/out1.txt",3)
idea_ranker = PartyIdeaRanker(API_KEY,"out/out2.txt")

pipe1 = Pipe(idea_generator,idea_ranker)
