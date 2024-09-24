import sys
import os
import requests
import json
from typing import Tuple, List

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from maihem.clients import Maihem

maihem_client = Maihem()

try:
    target_agent = maihem_client.create_target_agent(
        identifier="mh-bot-v4",
        role="Mental health assistant",
        industry="Medical",
        description="A chatbot that combines journaling, habit-building, and emotional support",
    )
except Exception as e:
    print(e)
    target_agent = maihem_client.get_target_agent(identifier="mh-bot-v4")

print(target_agent)


def chat_function(
    conversation_id: str,
    agent_maihem_message: str,
) -> Tuple[str, List[str]]:

    url = "http://localhost:8002/chat"

    payload = json.dumps(
        {
            "conversation_id": conversation_id,
            "message": agent_maihem_message,
        }
    )
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url, headers=headers, data=payload)

    response_dict = response.json()

    return response_dict["message"], response_dict["contexts"]


target_agent.set_chat_function(chat_function)

target_agent.add_documents(["test_data/test.pdf", "test_data/test1.pdf"])

metrics_config = {
    "qa_cx_helpfulness": 5,
    "qa_cx_goal_completion": 5,
}

test = maihem_client.create_test(
    identifier="mh-test-0",
    metrics_config=metrics_config,
)

test_run = maihem_client.create_test_run(
    test_identifier="mh-test-0",
    target_agent=target_agent,
    concurrent_conversations=5,
)
