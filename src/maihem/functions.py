import os
import pandas as pd
import requests
from typing import List


class APIKeyWarning(UserWarning):
    pass


class NoResponseData(UserWarning):
    pass


class ExceptionAPI(Exception):
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
            self.URL_API = "https://maihem-api-access.azure-api.net/service"
        self.api_key = None
        self._get_api_key()
        
    def _get_api_key(self):
        if os.getenv('MAIHEM_API_KEY') is not None:
            self.api_key = os.getenv('MAIHEM_API_KEY')
            self.headers['Authorization'] = "Bearer " + self.api_key
        else:
            raise ExceptionAPI("""MAIHEM_API_KEY not found in environment variables, please pass it with this code: 'os.environ['MAIHEM_API_KEY'] = "<your_maihem_api_key>"'""")
    
    def _call_api(self, payload, endpoint):
        try:
            response = requests.post(self.URL_API + endpoint, headers=self.headers, json=payload)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        
        if response.status_code == 401:
            raise ExceptionAPI("Invalid or missing API key")
        
        try:
            json_response = response.json()
        except ValueError: # If no response received, try one more time
            try:
                response = requests.post(self.URL_API + endpoint, headers=self.headers, json=payload)
            except requests.exceptions.HTTPError as err:
                raise SystemExit(err)
            try:
                json_response = response.json()
            except ValueError:
                raise NoResponseData("No response was received")

        if "info" in json_response:
            print(json_response['info'])    
            return json_response
        else:
            raise ExceptionAPI(json_response['detail'])


def create_test(
        test_name: str,
        chatbot_role: str,
        industry: str,
        n: int,
        topic: str = None,
        intents: List[str] = None,
        behavior_instructions: List[str] = None,
        language:  str = None,
        demographics: dict = None,
        writing_styles: List[str] = None
    ) -> None:
    """
    Create a test with a set of AI personas

    No return value

    Parameters
    ----------
    test_name : str
        Name of the test to be created, e.g. "testA"
    chatbot_role : str
        Role of the chatbot, must match one of the supported chatbot use cases. See the list of available roles in the documentation https://docs.maihem.ai/usecases
    industry : str
        Industry of the chatbot (e.g., finance, retail, healthcare, etc.)
    n : int
        Number of AI personas to create
    topic : str, optional
        Topic that the AI personas will focus on during the test, if not provided, a set of random topics will be selected
    intents : List[str], optional
        List of intents (goals) for the AI personas to sample from, if not provided, a set of random intents will be selected
    behavior_instructions : List[str], optional
        List of behavior instructions to sample from to guide the behavior of AI personas, if not provided, a set of random instructions will be selected
    language : str, optional
        Language of the chatbot, default is English
    demographics : dict, optional
        Dictionary with the demographics of the AI personas,
            example = {
                "regions": ["US", "UK", "CA"],
                "age_range": [18, 65],
                "female_ratio": 0.5,
                "non-binary_ratio": 0.1,
                "openness_range": [0.0, 1.0],
                "conscientiousness_range": [0.0, 1.0],
                "extraversion_range": [0.0, 1.0],
                "agreeableness_range": [0.0, 1.0],
                "neuroticism_range": [0.0, 1.0]
            },
    writing_styles : List[str], optional
        List of writing styles to sample from to guide the writing style of AI personas, if not provided, a set of random writing styles will be selected

    Returns
    -------
    None

    """    
    print("Creating test and AI personas... It might take a few minutes")

    # Create API object
    api = CallAPI()

    payload = {
        "test_name": test_name,
        "chatbot_role": chatbot_role,
        "industry": industry,
        "n": n,
        "topic": topic,
        "intents": intents,
        "behavior_instructions": behavior_instructions,
        "language": language,
        "demographics": demographics,
        "writing_styles": writing_styles
    }
    response = api._call_api(payload, "/create_test_simulated")
    print(response['response']) 
    

def chat_with_persona(test_name: str, test_run_name: str, persona_id: int, message: str=None, num_turns_max=None) -> str:
    """
    Chat in a conversation with a single AI persona

    Returns the message from the AI persona

    Parameters
    ----------
    test_name : str
        Name of the test to be created, e.g. "testA"
    test_run_name : str
        Name of the test run, e.g. "testA_run1"
    persona_id : int
        ID of the AI persona to chat with, must be between 0 and n-1, where n is the number of AI personas created in the test
    message : str
        The chatbot message to send to the AI persona
    num_turns_max : int, optional
        Maximum number of turns to end the conversation 

    Returns
    -------
    str
    """
    # Create API object
    api = CallAPI()

    payload = {
        "test_name": test_name,
        "test_run_name": test_run_name,
        "persona_id": persona_id,
        "message": message,
        "num_turns_max": num_turns_max
    }

    response = api._call_api(payload, "/chat_with_persona")
    print(response['response'])
    return response['response']


def log_conversations(test_name: str, chatbot_role: str, conversations: List[dict]):
    """
    Log a list of historical conversations for evaluation

    No return value

    Parameters
    ----------
    test_name : str
        Name of the test to be evaluated, e.g. "testA"
    chatbot_role : str
        Role of the chatbot, must match one of the supported chatbot use cases. See the list of available roles in the documentation https://docs.maihem.ai/usecases
    conversations : List[dict]
        List of conversations to log. Each conversation should be a dictionary with the following format:
        {
            "turn_1": {
                "chatbot": "<chatbot_message_1>",
                "persona": "<persona_message_1>"
            },
            "turn_2": {
                "chatbot": "<chatbot_message_2>",
                "persona": "<persona_message_2>"
            },
            ...
        }

    Returns
    -------
    None
    """
    def check_conversations(conversations: List[dict]):
        """Check if conversations are valid"""
        for conv in conversations:
            assert type(conv) == dict, "Conversations must be a list of dictionaries"
            for turn in conv:
                assert turn[:5] == "turn_", "Conversation turns must start with 'turn_'"
                assert type(conv[turn]) == dict, "Conversation turns must be dictionaries"
                assert "chatbot" in conv[turn], "Chatbot key not found in conversation"
                assert "persona" in conv[turn], "Persona key not found in conversation"
                assert type(conv[turn]["chatbot"]) == str, "Chatbot message must be a string"
                assert type(conv[turn]["persona"]) == str, "Persona message must be a string"

    check_conversations(conversations)

    # Create API object
    api = CallAPI()

    payload = {
        "test_name": test_name,
        "chatbot_role": chatbot_role,
        "conversations": conversations
    }

    response = api._call_api(payload, "/log_conversations")
    print(response['response'])


def evaluate(test_name: str, test_run_name: str, metrics_chatbot: dict, metrics_persona: dict, eval_type: str = None) -> pd.DataFrame:
    """
    Evaluate a test run with a set of custom metrics

    Returns a DataFrame with the evaluation scores for the defined metrics

    Parameters
    ----------
    test_name : str
        Name of the test to be evaluated, e.g. "testA"
    test_run_name : str
        Name of the test run to be evaluated, e.g. "testA_run1"
    metrics_chatbot : dict
        Dictionary with the custom metrics to evaluate the chatbot's messages (e.g. helpfulness). The keys are the metric names and the values are the descriptions of the metrics
    metrics_persona : dict
        Dictionary with the custom metrics to evaluate the persona's messages (e.g. their sentiment). The keys are the metric names and the values are the descriptions of the metrics
    eval_type : str, optional
        Type of evaluation to perform, must be one of "scores" or "flagged"

    Returns
    -------
    DataFrame
    """
    print(f"Evaluating test run '{test_run_name}' of test '{test_name}'...")

    def check_metrics(metrics_chatbot: dict, metrics_persona: dict):
        """Check if metrics are valid"""
        assert len(metrics_chatbot) > 0, "At least a metric should be defined for the chatbot"
        assert len(metrics_persona) > 0, "At least a metric should be defined for the persona"

        for metric in metrics_chatbot:
            assert type(metric) == str, "Metric name must be a string in metrics_chatbot"
            assert type(metrics_chatbot[metric]) == str, "Metric description must be a string in metrics_chatbot"

        for metric in metrics_persona:
            assert type(metric) == str, "Metric name must be a string in metrics_persona"
            assert type(metrics_persona[metric]) == str, "Metric description must be a string in metrics_persona"

    check_metrics(metrics_chatbot, metrics_persona)

    # Create API object
    api = CallAPI()

    payload = {
        "test_name": test_name,
        "test_run_name": test_run_name,
        "metrics_chatbot": metrics_chatbot,
        "metrics_persona": metrics_persona,
        "eval_type": eval_type
    }

    response = api._call_api(payload, "/eval_metrics")
    return pd.DataFrame.from_dict(response['eval'])


def survey(test_name: str,  survey_type: str, questions: List[dict], test_run_name: str = None) -> pd.DataFrame:
    """
    Survey AI personas to collect feedback

    Returns a DataFrame with the survey results

    Parameters
    ----------
    test_name : str
        Name of the test with the AI personas to survey, e.g. "testA"
    type : str
        Type of survey to perform, must be one of "pre-survey" or "post-survey"
    questions : List[dict]
        List of survey questions to ask the AI personas in the following format
            questions = [
                {
                    "question": "Did you like the interaction with the chatbot?",
                    "possible_values": ["Strong Yes", "Strong No", "Neutral", "Some things were good, some things were bad"]
                },
                {
                    "question": "What could be better in a conversation?",
                    "possible_values": []  # If no possible values are provided, the AI persona can answer freely
                },
            ]

    test_run_name : str, optional
        Name of the test run to survey AI persona after having a conversation with them, e.g. "testA_run1"

    Returns
    -------
    DataFrame
    """
    print(f"Surveying AI personas in test '{test_name}'...")

    # Create API object
    api = CallAPI()

    payload = {
        "test_name": test_name,
        "test_run_name": test_run_name,
        "type": survey_type,
        "questions": questions
    }

    response = api._call_api(payload, "/survey")
    return pd.DataFrame.from_dict(response['eval'])


def ideal_conversation(test_name: str, test_run_name: str) -> pd.DataFrame:
    """
    Generate labeled conversations with the ideal responses from the chatbot that the AI persona would prefer

    Returns a DataFrame with the labeled ideal conversations

    Parameters
    ----------
    test_name : str
        Name of the test, e.g. "testA"
    test_run_name : str
        Name of the test run, e.g. "testA_run1"

    Returns
    -------
    DataFrame
    """
    print(f"Generating ideal conversations for test '{test_name}'...")

    # Create API object
    api = CallAPI()

    payload = {
        "test_name": test_name,
        "test_run_name": test_run_name,
    }

    response = api._call_api(payload, "/ideal_conversation")
    return pd.DataFrame.from_dict(response['eval'])
