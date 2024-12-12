import importlib.util
import os
from typing import List, Callable

import maihem.errors as errors
from maihem.logger import get_logger

logger = get_logger()


def spread_n_into_buckets(n: int, buckets: int) -> List[int]:
    assert n >= 1, "n must be greater than or equal to 1"
    assert buckets >= 1, "buckets must be greater than or equal to 1"

    return [
        max(1, n // buckets + (1 if x < n % buckets else 0)) for x in range(buckets)
    ]


def import_wrapper_function(path: str = "wrapper_function.py") -> Callable:
    try:
        spec = importlib.util.spec_from_file_location(
            "wrapper_function", os.path.abspath(path)
        )
        wrapper_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(wrapper_module)
        wrapper_function = wrapper_module.wrapper_function

        return wrapper_function
    except Exception as e:
        errors.raise_not_found_error(
            f"Wrapper function coudl not be imported. Error: {e}"
        )


def create_project_folder(name: str) -> None:
    os.makedirs(
        name,
        exist_ok=True,
    )

    file_content = """import requests
from typing import List, Tuple

def wrapper_function(
	conversation_id: str,
	maihem_agent_message: str | None,
	conversation_history: dict,
) -> Tuple[str, List[str]]:
    \"\"\"Callable function to wrap your target agent to be tested.\"\"\"

	# Call demo Maihem target agent for quickstart
	url = "https://demo-agent.maihem.ai/chat"
	payload = {"message": maihem_agent_message if maihem_agent_message else ""}
	response = requests.request("POST", url, json=payload).json()
	return response["message"], response["contexts"]
"""

    # Write the content to a Python file
    file_name = "wrapper_function.py"

    with open(name + "/" + file_name, "w") as file:
        file.write(file_content)

    logger.info(f"Project folder created: '{name}'")
