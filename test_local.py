from datetime import datetime
import os
from typing import List, Tuple, Dict

from maihem.clients import Maihem

MAIHEM_API_KEY_LOCAL = os.getenv("MAIHEM_API_KEY_LOCAL")
MAIHEM_API_KEY_STAGING = os.getenv("MAIHEM_API_KEY_STAGING")

maihem_client = Maihem(env="staging")
# maihem_client = Maihem(env="local", api_key=api_key_local)


def wrapper_function(
    conversation_id: str, maihem_agent_message: str, conversation_history: Dict
) -> Tuple[str, List[str]]:
    """Callable wrapper function to wrap your target agent to be tested."""

    # Replace with the message from your target agent
    print(maihem_agent_message)
    target_agent_message = input("Enter your message: ")

    # List of retrieved contexts for RAG evaluations, pass empty list if not needed
    contexts = ["Hi", "Context 2"]

    return target_agent_message, contexts

# maihem_client.create_target_agent(
#     name="ta_local_10dic",
#     # label="label",
#     role="role",
#     description="description",
# )

test_name = "test_staging_10dec_cx_rag"

maihem_client.create_test(
    name=test_name,
    target_agent_name="ta_staging_1",
    initiating_agent="target",
    # label="Test Staging #2",
    maihem_agent_behavior_prompt="behavior prompt",
    maihem_agent_goal_prompt="goal prompt",
    maihem_agent_population_prompt="population prompt",
    conversation_turns_max=4,
    modules=["rag"],
    # metrics_config={
    #     "qa_cx_helpfulness": 4,
    #     "qa_cx_goal_completion": 4,
    # },
    number_conversations=7,
)

results = maihem_client.run_test(
    name=datetime.now().strftime("%Y%m%d_%H%M%S"),
    label="test run 1 label 2",
    test_name=test_name,
    wrapper_function=wrapper_function,
    concurrent_conversations=5,
)

print(results)
