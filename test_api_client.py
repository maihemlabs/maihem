import sys
import os
import requests
import time
import json
from tqdm import tqdm

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from typing import Tuple, List, Optional
from maihem.api import MaihemHTTPClientSync
from maihem.clients import Maihem

maihem_client = Maihem()

maihem_client._override_base_url(base_url="http://localhost:8000")
maihem_client._override_base_url_ui(base_url_ui="http://localhost:3000")


def chat_function_colin(
    conversation_id: str,
    agent_maihem_message: str,
) -> Tuple[str, List[str]]:

    url = "http://localhost:8002/chat?use_db=false"

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


# target_agent = maihem_client.create_target_agent(
#     identifier="agent-colin-prod-v2",
#     name="Agent Colin Local",
#     industry="Technology",
#     description="A helpful customer support agent",
#     role="customer_support",
#     language="en",
# )

target_agent = maihem_client.get_target_agent("agent-colin-local-v2")

target_agent.set_chat_function(chat_function=chat_function_colin)

# target_agent.add_documents(["/Users/simon/Downloads/test1.pdf"])

# test = maihem_client.create_test(
#     identifier="test-v-58",
#     name="Test V58",
#     initiating_agent="maihem",
#     conversation_turns_max=10,
#     metrics_config={
#         "qa_rag_hallucination": 1,
#     },
# )

test = maihem_client.get_test("test-v-58")

test_run = maihem_client.create_test_run(
    test_identifier="test-v-58", target_agent=target_agent, concurrent_conversations=4
)

test_run = maihem_client.get_test_run_result(test_run_id=test_run.id)

print(test_run)
