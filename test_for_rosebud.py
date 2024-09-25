import time
import requests
from typing import Tuple, List, Dict

from maihem.clients import Maihem

###################################### Parameters to change ######################################

# Your API key
api_key = "8a8e277166cc21d26c71fb104e16d30a7cc22bbded7ee130236119b8dd1e736e684c6421eb2d0aab466ebe90f66cc707"

# Unique identifier for the target agent
target_agent_name = "agent_rosebud_5"

# Unique identifier for the test
test_identifier = "test_123_5"

# Prompt to guide behavior of maihem agents in test
maihem_agent_behavior_prompt = "Write daily journals about your day, that are emotionally complex and are at least 300 words long."

# Maximum number of turns per conversation
conversation_turns_max = 5

# Metrics to be evaluated and how many conversations to generate for each metric
# Check the metrics available in the documentation
metrics_config = {
    "qa_cx_goal_completion": 2,
    "qa_cx_helpfulness": 2,
    "qa_cx_retention": 2,
    "qa_cx_nps": 2,
}

###################################### End Parameters to change ######################################


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

    payload = {"type": "generic", "messages": messages}

    for retry in range(3):
        try:
            response = requests.post(url, headers=headers, json=payload)
            response_json = response.json()
            break
        except Exception as e:
            time.sleep(2)
            if retry == 2:
                raise Exception(f"Error in API call after 3 retries: {e}")

    return response_json["response"]


def chat_function(
    conversation_id: str, agent_maihem_message: str
) -> Tuple[str, List[str]]:
    """
    Callable chat function to wrap your target agent to be tested.

    params:
    - conversation_id: can take a unique conversation ID to keep track of different conversations. If entire test is serialized in same conversation, the same conversation ID will be passed.
    - agent_maihem_msg: last message from maihem agent

    return:
    - str - response message from target agent
    - contexts: list of contexts for RAG assessment
    """
    # if conversation_id not in memory:
    #     memory[conversation_id] = []

    # # Append to memory the message from the maihem agent
    # memory[conversation_id].append({"content": agent_maihem_message, "role": "user"})

    # # Get response from the target agent
    # agent_target_message = api_call_rosebud(memory[conversation_id])
    # memory[conversation_id].append(
    #     {"content": agent_target_message, "role": "assistant"}
    # )

    # # Convert messages to contexts for RAG assessment
    # context = "Conversation history:\n"
    # for m in memory[conversation_id]:
    #     context += f"{m['role']}: {m['content']}\n"
    # contexts = [context]
    
    agent_target_message = "asdasd"
    contexts = []
    time.sleep(10)

    return agent_target_message, contexts


if __name__ == "__main__":

    # Create Maihem client
    m = Maihem(api_key=api_key)

    # Get target agent if it exists, if not create it
    try:
        target_agent = m.get_target_agent(identifier=target_agent_name)
    except Exception as e:
        target_agent = m.create_target_agent(
            identifier=target_agent_name,  # Unique identifier for the agent
            role="Mental health assistant",
            industry="Mental health",
            description="A chatbot that combines journaling, habit-building, and emotional support",
        )

    # Set chat function to the agent target
    target_agent.set_chat_function(chat_function)

    # Create test, which can be run multiple times with different agents
    response_test = m.create_test(
        identifier=test_identifier,  # Unique ID for the test
        initiating_agent="maihem",  # 'maihem' or 'target'
        maihem_agent_behavior_prompt=maihem_agent_behavior_prompt,
        conversation_turns_max=conversation_turns_max,  # Maximum number of turns per conversation
        metrics_config=metrics_config,  # Configuration of metrics to evaluate the agents
    )

    # Run test with selected target agent
    test_run = m.create_test_run(
        test_identifier=test_identifier,  # ID from test
        target_agent=target_agent,  # AgentTarget to be tested with callable function
        concurrent_conversations=5,  # Number of concurrent conversations
    )

    # Get test run results
    test_run_results = (
        m.get_test_run_result(  # AgentTarget to be tested with callable function
            test_run_id=test_run.id,  # ID from test run
        )
    )
    print(test_run_results)

    # Get test run conversations
    test_run_conversations = m.get_test_run_conversations(
        test_run_id=test_run.id
    )  # ID from test run
    print(test_run_conversations)
