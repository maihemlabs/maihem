import importlib.util
import os
from typing import List, Callable

from maihem.logger import get_logger

logger = get_logger()


def spread_n_into_buckets(n: int, buckets: int) -> List[int]:
    assert n >= 1, "n must be greater than or equal to 1"
    assert buckets >= 1, "buckets must be greater than or equal to 1"

    return [
        max(1, n // buckets + (1 if x < n % buckets else 0)) for x in range(buckets)
    ]


def import_wrapper_function(path: str = "wrapper_function.py") -> Callable:
    spec = importlib.util.spec_from_file_location(
        "wrapper_function", os.path.abspath(path)
    )
    wrapper_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(wrapper_module)
    wrapper_function = wrapper_module.wrapper_function

    return wrapper_function


def create_project_folder(name: str) -> None:
    os.makedirs(
        name,
        exist_ok=True,
    )

    file_content = """import requests

def wrapper_function(
    conversation_id: str, maihem_agent_message: str, conversation_history
):
    \"\"\"Callable function to wrap your target agent to be tested.\"\"\"

    # Call demo Maihem target agent for quickstart
    url = "http://api.maihem.ai/demo"
    payload = {"conversation_id": conversation_id, "message": maihem_agent_message}
    target_agent_message = requests.request("POST", url, data=payload).json()["message"]

    # (Optional) List of contexts for RAG evaluations, pass empty list if not needed
    contexts = []

    return target_agent_message, contexts
"""

    # Write the content to a Python file
    file_name = "wrapper_function.py"

    with open(name + "/" + file_name, "w") as file:
        file.write(file_content)

    logger.info(f"Project folder created: '{name}'")
