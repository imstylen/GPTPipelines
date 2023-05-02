class Filter:
    def __init__(self):
        """
        A base class for filters that can be used in a pipeline.

        Attributes:
            did_run (bool): Whether or not the filter has been run.
            input_filter (Filter, optional): The input filter to use in a pipeline. Defaults to None.
        """
        self.data_dict = dict()
        self.did_run = False
        self.input_filter = None
        self.out_file = None
        
    def run(self):
        """Run the filter."""
        self.did_run = True
        

        
class Pipe:
    def __init__(self, input_filter: Filter, output_filter: Filter):
        """
        A class representing a pipeline between two filters.

        Args:
            input_filter (Filter): The input filter for the pipeline.
            output_filter (Filter): The output filter for the pipeline.
        """
        self.input_filter = input_filter
        self.output_filter = output_filter
        self.output_filter.input_filter = input_filter


        
    def execute(self):
        """Execute the pipeline."""
        if not self.input_filter.did_run:
            self.input_filter.run()
            
        with open(self.input_filter.out_file,"r") as file:
            self.output_filter.data_dict['input_filter_out_file'] = file.read()    
            
        self.output_filter.run()
