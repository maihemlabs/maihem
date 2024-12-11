from datetime import datetime
import os
from typing import List, Tuple, Dict

from maihem.clients import Maihem

MAIHEM_API_KEY_LOCAL = os.getenv("MAIHEM_API_KEY_LOCAL")
MAIHEM_API_KEY_STAGING = os.getenv("MAIHEM_API_KEY_STAGING")
# Also add to env "MAIHEM_STAGING_URL" and "MAIHEM_STAGING_URL_UI"
# Also add to env "MAIHEM_LOCAL_URL" and "MAIHEM_LOCAL_URL_UI"

maihem_client = Maihem(env="local")
# maihem_client = Maihem(env="local", api_key=api_key_local)


def wrapper_function(
    conversation_id: str, maihem_agent_message: str, conversation_history: Dict
) -> Tuple[str, List[str]]:
    """Callable wrapper function to wrap your target agent to be tested."""

    # Replace with the message from your target agent
    target_agent_message = "Hi, how can I help you?"

    # List of retrieved contexts for RAG evaluations, pass empty list if not needed
    contexts = ["Hi", "Context 2"]

    return target_agent_message, contexts


# maihem_client.create_target_agent(
#     name="ta_local_10dic",
#     # label="label",
#     role="role",
#     description="description",
# )

test_name = "test_11dec_cx_5"
test_run_name = "testrun_x"  # + datetime.now().strftime("%Y%m%d_%H%M%S")

# maihem_client.create_test(
#     name=test_name,
#     target_agent_name="ta_staging_1",
#     initiating_agent="target",
#     # label="Test Staging #2",
#     maihem_agent_behavior_prompt="behavior prompt",
#     maihem_agent_goal_prompt="goal prompt",
#     maihem_agent_population_prompt="population prompt",
#     conversation_turns_max=4,
#     modules=["cx"],
#     # metrics_config={
#     #     "qa_cx_helpfulness": 4,
#     #     "qa_cx_goal_completion": 4,
#     # },
#     number_conversations=7,
# )

# results = maihem_client.run_test(
#     name=test_run_name,
#     # label="test run 1 label 2",
#     test_name=test_name,
#     wrapper_function=wrapper_function,
#     concurrent_conversations=5,
# )

results = maihem_client.get_test_run_result(
    test_name=test_name, test_run_name=test_run_name
)

print(results)
