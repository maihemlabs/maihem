import time
from datetime import datetime
from typing import Optional, Tuple, List, Callable


from src.maihem import Maihem, MaihemAsync
from src.maihem.agents import AgentTarget  # , AgentTargetAsync, AgentMaihem


m = MaihemAsync()


# Create a target agent to be tested (Sync)
# Create chat callable function (sync)
def chat_function(
    conversation_id: str,
    agent_maihem_message: str,
    agent_maihem_end_code: Optional[str] = None,
    contexts: Optional[List[str]] = None,
) -> Tuple[str, bool]:
    """
    Callable chat function to wrap your target agent to be tested.

    params:
    - conversation_id: can take a unique conversation ID to keep track of different conversations. If entire test is serialized in same conversation, the same conversation ID will be passed.
    - agent_maihem_msg: last message from maihem agent
    - agent_maihem_end_code: end code from maihem agent
    - contexts: list of contexts from RAG

    return:
    - str - response message from target agent
    - str - end conversation flag from target agent
    """

    if agent_maihem_end_code is None:  # If no end code is provided from maihem agent
        agent_target_message = (
            f"({datetime.now()}) Your target agent message when no end code is provided"
        )
        end = "<END_CODE>"  # True if the conversation should end, False if it should continue
    else:  # If end code is provided from maihem agent
        agent_target = (
            f"({datetime.now()}) Your target agent message when end code is provided"
        )
        end = "<END_CODE>"  # True if the conversation should end, False if it should continue

    return agent_target, end


# Create chat callable function (async)
async def async_chat_function(
    conversation_id: str, agent_maihem_msg: str, agent_maihem_end_code: Optional[str]
) -> Tuple[str, bool]:
    """
    Callable function to wrap your target agent to be tested.

    params:
    - conversation_id: can take a unique conversation ID to keep track of different conversations. If entire test is serialized in same conversation, the same conversation ID will be passed.
    - agent_maihem_msg: last message from maihem agent
    - agent_maihem_end_code: end code from maihem agent

    return:
    - str - response message from target agent
    - bool - end conversation flag
    """

    time.sleep(5)  # delay to test async

    if agent_maihem_end_code is None:  # If no end code is provided from maihem agent
        response_message = (
            f"({datetime.now()}) Your target agent message when no end code is provided"
        )
        end = False  # True if the conversation should end, False if it should continue
    else:  # If end code is provided from maihem agent
        response_message = (
            f"({datetime.now()}) Your target agent message when end code is provided"
        )
        end = True  # True if the conversation should end, False if it should continue

    return response_message, end


# Create an agent target
agent_target = m.create_target_agent(
    identifier="unique_identifier",  # Unique identifier for the agent
    role="Customer support chatbot",
    company="Airbnb",
    industry="Hospitality",
    description="A chatbot that answers questions about Airbnb services and policies",
    workflow={},  # Optional, to describe the workflow of the target agent
    rag_params={},  # Optional for testing RAG
)

# OR get an existing agent target
agent_target = m.get_target_agent(identifier="unique_identifier")

# Set chat function to the agent target
agent_target.set_chat_function(chat_function)


metrics_config = {  # Check the metrics available in the documentation
    "qa_cx_goal_completion": 5,
    "qa_cx_helpfulness": 10,
    "qa_rag_hallucination": 5,
    "qa_rag_answer_relevance": 5,
    "sec_pii": 10,
    "sec_pii_address": 8,
    "sec_brand_competitor_recommendation": 10,
    "sec_toxicity_profanity": 12,
}

# Create test, which can be run multiple times with different agents
response_test: Test = m.create_test(
    test_identifier="unique_test_identifier",  # Unique ID for the test
    initiating_agent="maihem",  # 'maihem' or 'target'
    agent_maihem_behavior_prompt="Clarify cancelation policies",  # Prompt to guide behavior of maihem agents in test
    conversation_turns_max=5,  # Maximum number of turns per conversation
    metrics_config=metrics_config,  # Configuration of metrics to evaluate the agents
)

# Run test with selected target agent
test_run: TestRun = m.run_test(
    identifier="unique_test_run_identifier",  # Unique ID for the test run
    test_identifier="unique_test_identifier",  # Test ID from created test
    agent_target=agent_target,  # AgentTarget to be tested with callable function
    dynamic_mode="dynamic",  # True if maihem agents respond with the same message, False if they can adapt and respond dynamically to the target agent
    concurrent_conversations=5,  # Number of concurrent conversations
)

# Get test run results
test_run_results: TestRunResults = (
    m.get_test_run_results(  # AgentTarget to be tested with callable function
        test_run_identifier="test_run_identifier",  # ID from test run
    )
)


##################################################################

# Simulate specific users with Maihem agents

# agent_maihem = AgentMaihem(
#     id="unique_id",                   # Unique ID for the maihem agent
#     workflow={},                      # Optional, to describe the workflow of the target agent to test
#     behavior_prompt="Clarify cancelation policies", # Prompt to guide behavior of maihem agents in test
#     metrics=metrics,                  # Metrics to evaluate the agent
# )

# agent_maihem.chat(
#     id_conversation="unique_id_conversation", # Unique ID for the conversation, to start a new one or to continue an existing one
#     target_agent_msg="<msg/None>",    # Message from the target agent
#     end=True,                         # True if the conversation should end, False if it should continue
# )
