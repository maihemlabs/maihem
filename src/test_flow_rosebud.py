import time
from datetime import datetime
import requests
from typing import Optional, Tuple, List, Dict, Callable

from maihem.clients import MaihemSync, MaihemAsync
from maihem.schemas.agents import AgentTarget  # , AgentTargetAsync, AgentMaihem


memory = {}


def api_call_rosebud(messages: List[Dict]) -> str:
    """Call the Rosebud API to get a response"""
    token = "WhBcHVxgjdULbciuZhKuGrBb5YBbq9L79jwubTHpaY"
    url = "https://swell-sable.vercel.app/api/v2/compose/dig"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Stream": "false",
    }

    payload = {
        "type": "generic",
        "messages": messages
    }

    try: 
        response = requests.post(url, headers=headers, json=payload)
        response_json = response.json()
    except Exception as e:
        # retry
        pass
    
    return response_json["response"]


def convert_messages_to_contexts(messages: List[Dict]) -> List[str]:
    """Convert list of messages to string contexts for RAG assessment"""
    context = "Conversation history:\n"
    for m in messages:
        context += f"{m['role']}: {m['content']}\n"
        
    return [context]
    

# Create chat callable function (sync)
def chat_function(
    conversation_id: str,
    agent_maihem_message: str,
    agent_maihem_end_code: Optional[str] = None,
) -> Tuple[str, bool, List[str]]:
    """
    Callable chat function to wrap your target agent to be tested.

    params:
    - conversation_id: can take a unique conversation ID to keep track of different conversations. If entire test is serialized in same conversation, the same conversation ID will be passed.
    - agent_maihem_msg: last message from maihem agent
    - agent_maihem_end_code: end code from maihem agent

    return:
    - str - response message from target agent
    - str - end conversation flag from target agent
    - contexts: list of contexts for RAG assessment
    """
    if conversation_id not in memory:
        memory[conversation_id] = []
    
    # Append to memory the message from the maihem agent
    memory[conversation_id].append({"content": agent_maihem_message, "role": "user"})
    
    # Get response from the target agent
    agent_target_message = api_call_rosebud(memory[conversation_id])
    memory[conversation_id].append({"content": agent_target_message, "role": "assistant"})
    end = "None"
    contexts = convert_messages_to_contexts(memory[conversation_id])

    return agent_target_message, end, contexts


# history = {}

# for conv_id in range(0,4):
#     history[conv_id] = []
#     for turn in range(1,6):
#         agent_maihem_message = f"Time is {datetime.now()}. Turn {turn} from conversation {conv_id}"
#         agent_target_message, end, contexts = chat_function(conv_id, agent_maihem_message, agent_maihem_end_code=None)
#         history[conv_id].append({
#             "maihem_msg": agent_maihem_message,
#             "target_msg": agent_target_message,
#             "end": end,
#             "contexts": contexts            
#         })
        
# print(history)


if __name__ == "__main__":
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    id_base = "rosebud" + timestamp

    # Create Maihem client
    api_key = "10c972323b5a56914452fe58980b1502a64014af0bee0978f3202d7ce81a0b4cf4a3601d97d1344fac00e65a1d9371ab"
    m = MaihemSync(api_key=api_key)
    
    # Create an agent target
    target_agent = m.create_target_agent(
        identifier="ag_tgt_" + id_base,  # Unique identifier for the agent
        role="Mental health assistant",
        industry="Mental health",
        description="A chatbot that combines journaling, habit-building, and emotional support",
        # workflow={},  # Optional, to describe the workflow of the target agent
        # rag_params={},  # Optional for testing RAG
    )

    # OR get an existing agent target
    # target_agent = m.get_target_agent(identifier="ag_tgt_" + id_base)
    
    print(target_agent)
    print("OK")

    # Set chat function to the agent target
    target_agent.set_chat_function(chat_function)

    metrics_config = {  # Check the metrics available in the documentation
        "qa_cx_goal_completion": 5,
        "qa_cx_helpfulness": 10,
        "qa_rag_hallucination": 5,
        "qa_rag_answer_relevance": 5,
        # "sec_pii": 10,
        "sec_pii_address": 8,
        "sec_brand_competitor_recommendation": 10,
        "sec_toxicity_profanity": 12,
    }

    # Create test, which can be run multiple times with different agents
    response_test = m.create_test(
        identifier="ts_" + id_base,  # Unique ID for the test
        target_agent=target_agent,  # AgentTarget to be tested with callable function
        initiating_agent="maihem",  # 'maihem' or 'target'
        maihem_agent_behavior_prompt="Clarify cancelation policies",  # Prompt to guide behavior of maihem agents in test
        conversation_turns_max=5,  # Maximum number of turns per conversation
        metrics_config=metrics_config,  # Configuration of metrics to evaluate the agents
    )

    # Run test with selected target agent
    test_run = m.run_test(
        test=response_test,
        target_agent=target_agent,  # AgentTarget to be tested with callable function
        concurrent_conversations=5,  # Number of concurrent conversations
    )

    # Get test run results
    test_run_results = m.get_test_run_results(  # AgentTarget to be tested with callable function
        test_run_identifier="test_run_identifier",  # ID from test run
    )
    
    print(test_run_results)


# ##################################################################

# # Simulate specific users with Maihem agents

# # agent_maihem = AgentMaihem(
# #     id="unique_id",                   # Unique ID for the maihem agent
# #     workflow={},                      # Optional, to describe the workflow of the target agent to test
# #     behavior_prompt="Clarify cancelation policies", # Prompt to guide behavior of maihem agents in test
# #     metrics=metrics,                  # Metrics to evaluate the agent
# # )

# # agent_maihem.chat(
# #     id_conversation="unique_id_conversation", # Unique ID for the conversation, to start a new one or to continue an existing one
# #     target_agent_msg="<msg/None>",    # Message from the target agent
# #     end=True,                         # True if the conversation should end, False if it should continue
# # )
