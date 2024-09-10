import sys
import os
import requests
import json

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from typing import Tuple, List, Optional
from maihem.api import MaihemHTTPClientSync
from maihem.clients import MaihemSync

maihem_client = MaihemSync(
    "aa1cd4fb59e0638a0280e8e523a8a29674f77fd2e17b67ce0df61762929c44a597ff8cb651b8433bdcf0e316370acceb"
)


def chat_function_colin(
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


# target_agent = maihem_client.create_target_agent(
#     identifier="agent-colin-local",
#     name="Agent Colin Local",
#     industry="Technology",
#     description="A helpful customer support agent",
#     role="customer_support",
# )

target_agent = maihem_client.get_target_agent("agent-colin-local")

target_agent.set_chat_function(chat_function=chat_function_colin)

test = maihem_client.create_test(
    identifier="test-v-4",
    name="Test V4",
    initiating_agent="maihem",
    conversation_turns_max=7,
    maihem_agent_behavior_prompt="Example prompt",
    metrics_config={"qa_rag_answer_relevance": 2, "qa_rag_hallucination": 2},
)

test_run = maihem_client.run_test(
    test_identifier="test-v-4", target_agent=target_agent, concurrent_conversations=4
)

# print(conv)
