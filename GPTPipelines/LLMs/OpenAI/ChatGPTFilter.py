import openai
from tqdm import tqdm
import GPTPipelines
from GPTPipelines.Core.LLMInterface import LLMInterface
from tenacity import retry, wait_random_exponential, stop_after_attempt, retry_if_not_exception_type
from GPTPipelines.LLMs.OpenAI.ChatGPTRequester import ChatGPTRequester
from jinja2 import Environment, FileSystemLoader

class ChatGPTFilter(LLMInterface):
    """
    A class that represents a chatbot using OpenAI's GPT-3 API.

    Attributes:
        prompt_content (dict): A dictionary containing the content to be used in the Jinja2 template.
        prompt_template (str): The name of the Jinja2 template file to use.
        debug_prompt (bool): Whether or not to output the last generated prompt to a separate file.
        num_requests (int): The number of requests to make to the OpenAI API.
        output (str): The generated text from the OpenAI API.
        out_file (str): The name of the file to write the generated text to.
        requester (ChatGPTRequester): An instance of the ChatGPTRequester class for making requests to the OpenAI API.
    """
    
    #static template_dirs
    template_dirs = ['GPTPipelines/Templates']

    def __init__(self, **kwargs):
        """
        Initializes a new instance of the ChatGPTFilter class.

        Args:
            **kwargs: Keyword arguments to configure the chatbot.
                        api_key (str): The OpenAI API key.
                        model (str, optional): The name of the GPT-3 model to use. Defaults to 'gpt-3.5-turbo'.
                        temperature (float, optional): The sampling temperature to use when generating responses. Defaults to 0.0.
                        max_tokens (int, optional): The maximum number of tokens to generate in the response. Defaults to 2048.
                        system_message (str, optional): The message to display to the user before the first prompt. Defaults to 'You are a helpful assistant'.
                        debug_prompt (bool, optional): Whether or not to output the last generated prompt to a separate file. Defaults to False.
                        num_requests (int, optional): The number of requests to make to the OpenAI API. Defaults to 1.
        """

        super().__init__()
        
        #initialize properties
        self.prompt_content['responses'] = []
        self.prompt_template = 'Writer.prompt'
        self.debug_prompt = kwargs.get('debug_prompt', False)
        self.num_requests = kwargs.get('num_requests', 1)
        self.output = ''
        self.out_file = kwargs['out_file']
        
        #setup requester
        api_key = kwargs['api_key']
        model = kwargs.get('model', 'gpt-3.5-turbo')
        temperature = kwargs.get('temperature', 0.0)
        max_tokens = kwargs.get('max_tokens', 2048)
        system_message = kwargs.get('system_message', 'You are a helpful assistant')
        
        self.requester = ChatGPTRequester(api_key, model, temperature, max_tokens, system_message)
        
    
    def run(self):
        """
        Runs the chatbot and saves the responses to a file.
        """
        super().run()
                
        for _ in tqdm(range(self.num_requests)):
            self._submit_request()
                
        self.write_out_file()
    
    @staticmethod
    def add_template_dir(template_dir: str):
        """
        Add a new template directory to the static template_dirs list.

        Args:
            template_dir (str): The path to the new template directory.
        """
        ChatGPTFilter.template_dirs.append(template_dir)
    
    
    # let's make sure to not retry on an invalid request, because that is what we want to demonstrate
    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6), retry=retry_if_not_exception_type(openai.InvalidRequestError))    
    def _submit_request(self):
        """
        Submits a request to the OpenAI API and stores the response in `self.data_dict`.
        """
        prompt = self.generate_prompt()
        response = self.requester.submit_request(prompt)
        self.process_response(response)
        self.last_prompt = prompt   
             
    def generate_prompt(self) -> str:
        """
        Generates a prompt using Jinja2 templating.

        Returns:
            str: The generated prompt.
        """
        # Set up Jinja2 environment
        env = Environment(loader=FileSystemLoader(self.template_dirs))

        # Load template file
        prompt_template = env.get_template(self.prompt_template)

        # Render template with content dictionary
        rendered_prompt = prompt_template.render(self.prompt_content)

        return rendered_prompt

    def process_response(self, response):
        """
        Processes the response from the OpenAI API and adds it to `self.data_dict`.

        Args:
            response (dict): The response from the OpenAI API.
        """

        self.prompt_content['responses'].append(response['choices'][0]['message']['content'])
        
    def write_out_file(self):
        """
        Writes the generated text to the output file.
        """

        with open(self.out_file,"w") as writer:
            for t in self.prompt_content['responses']:
                writer.writelines(t)
                self.output += t + '\n'

        if(self.debug_prompt):
           with open(self.out_file+"P","w") as writer:
                writer.writelines(self.last_prompt)
