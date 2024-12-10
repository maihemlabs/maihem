import os
from typing import List, Tuple

from maihem.clients import Maihem

MAIHEM_API_KEY_LOCAL = os.getenv("MAIHEM_API_KEY_LOCAL")
MAIHEM_API_KEY_STAGING = os.getenv("MAIHEM_API_KEY_STAGING")

maihem_client = Maihem(env="local", api_key=MAIHEM_API_KEY_LOCAL)
# maihem_client = Maihem(env="local", api_key=api_key_local)


def wrapper_function(
    conversation_id: str, maihem_agent_message: str
) -> Tuple[str, List[str]]:
    """Callable wrapper function to wrap your target agent to be tested."""

    # Replace with the message from your target agent
    print(maihem_agent_message)
    target_agent_message = input("Enter your message: ")

    # List of retrieved contexts for RAG evaluations, pass empty list if not needed
    contexts = []

    return target_agent_message, contexts


try:
    maihem_client.create_target_agent(
        name="ta_local_3",
        # label="label",
        role="role",
        description="description",
    )
except Exception as e:
    pass

try:
    maihem_client.create_test(
        name="test_local_10",
        target_agent_name="ta_local_3",
        initiating_agent="maihem",
        maihem_agent_behavior_prompt="behavior prompt",
        maihem_agent_goal_prompt="goal prompt",
        maihem_agent_population_prompt="population prompt",
        conversation_turns_max=3,
        metrics_config={
            "qa_rag_answer_relevance": 1,
        },
        documents_path="documents",
    )
except Exception as e:
    pass

results = maihem_client.run_test(
    name="test_run_local_11",
    label="test run 1 label 2",
    test_name="test_local_10",
    wrapper_function=wrapper_function,
    concurrent_conversations=3,
)

print(results)
