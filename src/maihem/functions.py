import os
import pandas as pd
import requests
import warnings
import sys
import threading
import time
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
    
    def _call_api(self, payload, endpoint, error_msg="No data was returned, check incorrect input parameters"):
        try:
            response = requests.post(self.URL_API + endpoint, headers=self.headers, json=payload)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        
        if response.status_code == 401:
            raise ExceptionAPI("Invalid or missing API key")

        if "info" in response.json():
            print(response.json()['info'])
            return response.json()
        else:
            raise ExceptionAPI(response.json()['detail'])


def create_test(test_name: str, chatbot_role: str, industry: str, n: int, topic: str=None, language: str=None):
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
    language : str, optional
        Language of the chatbot, default is English

    Returns
    -------
    None

    """
    print("Creating test and AI personas...")
    # Create API object
    api = CallAPI()

    payload = {
        "test_name": test_name,
        "chatbot_role": chatbot_role,
        "industry": industry,
        "n": n,
        "topic": topic,
        "language": language
    }
    response = api._call_api(payload, "/create_test_simulated")
    print(response['response']) 
    

def chat_with_persona(test_name: str, test_run_name: str, persona_id: int, message: str) -> str:
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
        "message": message
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


def evaluate(test_name: str, test_run_name: str, metrics_chatbot: dict, metrics_persona: dict) -> pd.DataFrame:
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
        "metrics_persona": metrics_persona
    }

    response = api._call_api(payload, "/eval_test_run")
    return pd.DataFrame.from_dict(response['eval'])