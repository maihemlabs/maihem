import sys
import os
import requests
import json

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from typing import Tuple, List, Optional
from maihem.api import MaihemHTTPClientSync
from maihem.clients import MaihemSync


m = MaihemHTTPClientSync(
    "https://intent-premium-mammal.ngrok-free.app/",
    "10c972323b5a56914452fe58980b1502a64014af0bee0978f3202d7ce81a0b4cf4a3601d97d1344fac00e65a1d9371ab",
)

maihem_client = MaihemSync(
    "10c972323b5a56914452fe58980b1502a64014af0bee0978f3202d7ce81a0b4cf4a3601d97d1344fac00e65a1d9371ab"
)

print(m.whoami())


def chat_function_colin(
    conversation_id: str,
    agent_maihem_message: str,
) -> Tuple[str, bool, List[str]]:

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
#    identifier="agent-v-6",
#    name="Agent V6",
#    industry="Technology",
#    description="A helpful customer support agent",
#    role="customer_support",
# )

target_agent = maihem_client.get_target_agent("agent-v-6")

target_agent.set_chat_function(chat_function=chat_function_colin)

# test = maihem_client.create_test(
#     identifier="test-v-17",
#     name="Test V17",
#     target_agent=target_agent,
#     initiating_agent="maihem",
#     maihem_agent_behavior_prompt="Example prompt",
#     conversation_turns_max=10,
#     metrics_config={"qa_cx_helpfulness": 2},
# )

test = maihem_client.get_test("test-v-17")

# test_run = maihem_client.run_test(
#     test=test, target_agent=target_agent, concurrent_conversations=1
# )

# print(test_run)

# turn = maihem_client._create_conversation_turn(
#     test_run_id="tr_01j71a5nb8fb890wkgpsat46k1",
#     conversation_id="c_01j71a5ncceb3axknxbqy57kdq",
#     message=None,
# )
# print(turn)

# turn_id, conversation = maihem_client._create_conversation_turn(
#     test_run_id="tr_01j71mccpzetdr81qh9r5fdf42",
#     conversation_id="c_01j71mcwgfe1ntnf40f99q3w0s",
#     target_agent_message="",
#     contexts=["here is some demo context"],
# )

# maihem_message = maihem_client._get_conversation_message_from_conversation(
#     turn_id=turn_id, agent_type="maihem", conversation=conversation
# )

# message, contexts = target_agent._send_message(
#     "c_01j71mcwgfe1ntnf40f99q3w0s", maihem_message.content
# )

# print(message)

# conv = maihem_client._run_conversation(
#     test_run_id="tr_01j71mccpzetdr81qh9r5fdf42",
#     conversation_id="c_01j71mcwgbek7v4t2psp0hahnv",
#     test=test,
#     target_agent=target_agent,
# )

test_run = maihem_client.run_test(
    test=test, target_agent=target_agent, concurrent_conversations=1
)
print(test_run)

# print(conv)
