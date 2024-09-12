import sys
import os
from typing import List, Tuple
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from maihem.clients import Maihem


def chat_function(
    conversation_id: str,
    agent_maihem_message: str,
) -> Tuple[str, List[str]]:

    message = "Target agent message"
    contexts = []

    return message, contexts


if __name__ == "__main__":

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    # timestamp = "20240911172717"

    # api_key = "10c972323b5a56914452fe58980b1502a64014af0bee0978f3202d7ce81a0b4cf4a3601d97d1344fac00e65a1d9371ab"
    api_key = "8a8e277166cc21d26c71fb104e16d30a7cc22bbded7ee130236119b8dd1e736e684c6421eb2d0aab466ebe90f66cc707"

    maihem_client = Maihem(api_key=api_key)

    print(maihem_client)

    target_agent = maihem_client.create_target_agent(
        identifier="mh-bot-v1_" + timestamp,
        role="Mental health assistant",
        industry="Medical",
        description="A chatbot that combines journaling, habit-building, and emotional support",
    )

    target_agent.set_chat_function(chat_function)

    print(target_agent)

    metrics_config = {
        "qa_cx_goal_completion": 1,
    }

    test = maihem_client.create_test(
        identifier="mh-test-v1_" + timestamp,
        metrics_config=metrics_config,
    )

    print(test)

    test_run = maihem_client.create_test_run(
        test_identifier="mh-test-v1_" + timestamp,
        target_agent=target_agent,
        concurrent_conversations=5,
    )

    print(test_run)

    convs = maihem_client.get_test_run_results_with_conversations(
        test_run_id=test_run.id
    )

    print(convs)

    d = convs.to_dict()

    print(d)
