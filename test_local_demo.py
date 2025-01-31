from datetime import datetime
import os
from typing import List, Tuple, Dict

from maihem.clients import Maihem

MAIHEM_API_KEY_LOCAL = "809bb4f5d4e3cc1a10bca0ddca8c8a9ab17c6eb16a599d82551f5743b0546b15cae0d20fb7d05d4694b0afdba24ad943"

maihem_client = Maihem(env="local", api_key=MAIHEM_API_KEY_LOCAL)
# maihem_client = Maihem(env="local", api_key=api_key_local)


def wrapper_function(
    conversation_id: str,
    maihem_agent_message: str | None,
    conversation_history: dict,
) -> Tuple[str, List[str]]:
    import requests

    """Callable function to wrap your target agent to be tested."""
    # Call demo Maihem target agent for quickstart
    url = "http://localhost:5005/generate"
    headers = {"Content-Type": "application/json"}
    data = {"query": maihem_agent_message}
    print(maihem_agent_message)
    response = requests.post(url, headers=headers, json=data)
    print(response.json()["response"])
    response.raise_for_status()  # Raises an HTTPError for bad responses (4xx, 5xx)

    return response.json()["response"], []

    # maihem_client.create_target_agent(
    #     name="target-deco",
    #     # label="label",
    #     role="Airbnb customer support agent",
    #     description="Airbnb customer support agent that can help with questions about the platform",
    # )


test_name = "test_local_rag" + str(datetime.now().strftime("%Y%m%d_%H%M%S"))

maihem_client.create_test(
    name=test_name,
    target_agent_name="target-deco",
    initiating_agent="maihem",
    # label="Test Staging #2",
    maihem_behavior_prompt="act like an angry customer",
    maihem_goal_prompt="goal prompt",
    maihem_population_prompt="population prompt",
    conversation_turns_max=1,
    metrics_config={
        "qa_cx_helpfulness": 1,
    },
)

results = maihem_client.run_test(
    name=datetime.now().strftime("%Y%m%d_%H%M%S"),
    label="test run 1 label 2",
    test_name=test_name,
    wrapper_function=wrapper_function,
    concurrent_conversations=5,
)

print(results)
