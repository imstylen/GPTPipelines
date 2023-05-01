from abc import ABC, abstractmethod
from GPTPipelines.Core.PipeFilter import Filter

class LLMInterface(Filter, ABC):
    """
    Abstract base class for a generic interface to interact with Language Model APIs.
    """

    def __init__(self):
        super().__init__()
        self.data_dict = {}
    @abstractmethod
    def run(self):
        super().run()
        """
        Run the assistant and save the responses to a file.
        """
        pass
    
    @abstractmethod
    def _submit_request(self):
        """
        Submit a request to the LLM API and store the response in `self.data_dict`.
        """
        pass
    
    @abstractmethod
    def generate_prompt(self) -> str:
        """
        Generate a prompt string.

        Returns:
            str: A prompt string.
        """
        pass

    @abstractmethod
    def process_response(self, response):
        """
        Process the response from the LLM API and add it to `self.data_dict`.

        Args:
            response: The response from the LLM API.
        """
        pass
