import requests
import os
import warnings
from datetime import datetime
import random


class APIKeyWarning(UserWarning):
    pass


class NoResponseData(UserWarning):
    pass


class CallAPI():
    """
    Class to generate synthetic data using the MAIHEM API
    """
    def __init__(self, local_run=False):
        self.headers = {'Content-Type': 'application/json'}
        self.local_run = local_run
        if self.local_run:
            self.URL_API = "http://localhost"
        else:
            self.URL_API = "https://maihem-api-access.azure-api.net/demo"
        self.api_key = None
        self._get_api_key()
        
    def _get_api_key(self):
        if os.getenv('MAIHEM_API_KEY') is not None:
            self.api_key = os.getenv('MAIHEM_API_KEY')
            if not self.local_run:
                self.headers['Ocp-Apim-Subscription-Key'] = self.api_key
        else:
            warnings.warn("MAIHEM_API_KEY not found in environment variables, please set manually with the set_api_key() function", 
                          APIKeyWarning)
    
    def _call_api(self, item, endpoint, error_msg="No data was returned, check incorrect input parameters"):
        try:
            response = requests.post(self.URL_API + endpoint, headers=self.headers, json=item)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        try: 
            msg_max = "Maximum number of conversation steps reached"
            if response.json()['info'] == msg_max:
                warnings.warn(msg_max, NoResponseData)
                return msg_max
            return response.json()['data']
        except:
            print(response)
            warnings.warn(error_msg, NoResponseData)

    def _check_params(self, intent_params:dict, persona_params: dict, generator_params: dict, async_call=False):
        """
        Check if parameters are valid
        """
        assert 'intent' in intent_params.keys(), "<intent> must be provided"
        assert type(intent_params['intent']) == str, "<intent> must be a string"
        assert 'context' in intent_params.keys(), "<context> must be provided"
        assert type(intent_params['context']) == str, "<context> must be a string"
        assert 'category' in intent_params.keys(), "<category> must be provided"
        assert type(intent_params['category']) == str, "<category> must be a string"

        assert type(persona_params) == dict, "persona_params must be a dictionary"
        assert type(generator_params) == dict, "generator_params must be a dictionary"

        for param in persona_params.keys():
            assert type(persona_params[param]) == str, "persona parameter must be a string"

        if async_call:
            assert 'n_calls' in generator_params.keys(), "n_calls must be provided"
            assert 'n_prompts_per_call' in generator_params.keys(), "n_prompts_per_call must be provided"
        assert type(generator_params['model_temperature']) == float, "model_temperature must be a number"
        assert 0 <= generator_params['model_temperature'] <= 2 , "model_temperature must be between 0 and 2"


class PromptGenerator(CallAPI):

    def generate_prompts(self, intent_params:dict, persona_params: dict, model_temperature: float, n_prompts: int) -> list:
        generator_params = {
            'data_to_generate': "Prompt",
            'model_temperature': model_temperature,
            'n_calls': 2,
            'n_prompts_per_call': str(int(n_prompts/2 + 1)),
        }
        return self._generate_data(intent_params, persona_params, generator_params)

    def generate_full_conversations(self, intent_params:dict, persona_params: dict, model_temperature: float, n_convs: int, conv_max_steps: int) -> list:
        generator_params = {
            'data_to_generate': "ConversationFull",
            'model_temperature': model_temperature,
            'n_calls': n_convs,
            'n_prompts_per_call': 1,
            'conv_max_steps': conv_max_steps
        }
        return self._generate_data(intent_params, persona_params, generator_params)

    def _generate_data(self, intent_params:dict, persona_params: dict, generator_params: dict) -> list:
        """
        Generate data using intent, persona and generator model parameters 
        """
        self._check_params(intent_params, persona_params, generator_params)
        item = {
            "intent": intent_params,
            "persona": persona_params,
            "generator": generator_params
        }

        data = self._call_api(item, '/prompt_generator', error_msg="No data was returned, check incorrect input parameters")
        if generator_params['data_to_generate'] == "Prompt":
            data_converted = self._convert_response_prompts(data, generator_params)
        elif generator_params['data_to_generate'] == "ConversationFull":
            data_converted = self._convert_response_convs(data, generator_params)

        return data_converted
    
    def generate_queries(self, columns: list, n_prompts: int, column_synonyms=False) -> list:
        return self._generate_queries(columns, n_prompts, query=None, column_synonyms=column_synonyms, )
    
    def variate_query(self, columns: list, n_prompts: int, query: str) -> list:
        return self._generate_queries(columns, n_prompts, query=query)
    
    def _generate_queries(self, columns: list, n_prompts: int, query: str=None, column_synonyms=False) -> list:
        """
        Generate data using intent, persona and generator model parameters 
        """
        intent = {
            "columns": str(columns),
            "column_synonyms": str(column_synonyms)
        }
        if query is not None:
            intent['query'] = query

        generator = {
            'data_to_generate': "NL_queries",
            'type': 'human',
            'model': 'azure',
            'model_temperature': 0.7,
            'n_calls': 2,
            'n_prompts_per_call': str(int(n_prompts/2 + 1)),
        }

        item = {
            "intent": intent,
            "generator": generator
        }

        data = self._call_api(item, '/prompt_generator', error_msg="No data was returned, check incorrect input parameters")
        data_converted = self._convert_response_prompts(data, generator)

        return data_converted

    def _convert_response_prompts(self, data: dict, generator_params: dict) -> list:
        """
        Convert response from API to a dictionary
        """
        l = []
        for call in data:
            call_list = call.split("\n")
            for c in call_list:
                t = c[3:].replace("\n", "")
                if t != "": 
                    l.append(t)
        return l
    
    def _convert_response_convs(self, data: dict, generator_params: dict) -> list:
        """
        Convert response from API to a dictionary
        """
        return data

            
class ConversationGenerator(CallAPI):

    def __init__(self, type_chat="human", local_run=False):
        super().__init__(local_run=local_run)
        self.id_conv = None
        self.type_chat = type_chat

    def initialize(self, intent_params:dict, persona_params: dict, model_temperature: float, conv_max_steps: int, max_n_words: int) -> None:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        random_num = random.randint(0, 1000000)
        self.id_conv = f"{timestamp}_{random_num}_{self.api_key}"
        """
        Initialize or reset conversation generator object
        """
        self.intent_params = intent_params
        self.persona_params = persona_params
        self.generator_params = {
            'data_to_generate': "InitializeConversation",
            'type': self.type_chat,
            'model_temperature': model_temperature,
            'max_conv_steps': conv_max_steps,
            "max_n_words": max_n_words,
            'n_calls': 1,
            'n_prompts_per_call': str(1),
        }
        self._check_params(self.intent_params, self.persona_params, self.generator_params)
        message = {
            "message": "", 
            "id_conv": self.id_conv
        }

        item = {
            "intent": self.intent_params,
            "persona": self.persona_params,
            "generator": self.generator_params,
            "message": message
        }

        return self._call_api(item, '/conversation_generator', error_msg="Conversation could not be initialized, check incorrect input parameters or API key")

    def chat(self, input_message: str) -> str:
        """
        Chat with the conversation generator
        """
        self.generator_params['data_to_generate'] = "ContinueConversation"
        message = {
            "message": input_message, 
            "id_conv": self.id_conv
        }
        item = {
            "generator": self.generator_params,
            "message": message}

        return self._call_api(item, '/conversation_generator', error_msg="Conversation could not be continued, check incorrect input message")
    

class Evaluator(CallAPI):

    def __init__(self, local_run=False, model="azure", temperature=0.0):
        super().__init__(local_run=local_run)
        self.model = model
        self.temperature = temperature

    def evaluate(self, conversation: str, metrics: dict, intent: dict) -> list:
        """
        Evaluate a conversation using inputted custom metrics
        """
        item = {
            'evaluator': {
                "conversation": conversation,
                "metrics": metrics,
                "model": self.model,
                "model_temperature": self.temperature
            },
            'intent': intent
        }

        scores_str = self._call_api(item, '/evaluation', error_msg="Conversation could not be evaluated, check incorrect input parameters")
        scores_list = scores_str.strip('][').split(', ')[0:-1]
        scores_list_n = [float(i) for i in scores_list]

        return scores_list_n



