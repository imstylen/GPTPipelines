class Pipeline:
    def __init__(self):
        self.pipes = []

    def add_pipe(self, pipe):
        self.pipes.append(pipe)

    def execute(self):
        for pipe in self.pipes:
            pipe.execute()