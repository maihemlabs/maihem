import importlib.util
import os
from typing import List, Callable

import maihem.errors as errors
from maihem.logger import get_logger

logger = get_logger()


def spread_n_into_buckets(n: int, buckets: int) -> List[int]:
    if not isinstance(n, int) or not isinstance(buckets, int):
        raise TypeError("n and buckets must be integers")
    if n < 1 or buckets < 1:
        raise ValueError("n and buckets must be greater than or equal to 1")

    return [
        max(1, n // buckets + (1 if x < n % buckets else 0)) for x in range(buckets)
    ]


def import_wrapper_function(path: str = "wrapper_function.py") -> Callable:
    if not os.path.exists(path):
        errors.raise_not_found_error(f"Wrapper function file not found at: {path}")

    if not os.path.isfile(path):
        errors.raise_not_found_error(f"Path exists but is not a file: {path}")

    try:
        spec = importlib.util.spec_from_file_location(
            "wrapper_function", os.path.abspath(path)
        )
        if spec is None or spec.loader is None:
            errors.raise_not_found_error("Failed to load module specification")

        wrapper_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(wrapper_module)

        if not hasattr(wrapper_module, "wrapper_function"):
            errors.raise_not_found_error("Module does not contain 'wrapper_function'")

        wrapper_function = wrapper_module.wrapper_function
        return wrapper_function
    except Exception as e:
        errors.raise_not_found_error(
            f"Wrapper function could not be imported. Error: {e}"
        )


def create_project_folder(name: str) -> None:
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
    payload = {"message": maihem_agent_message if maihem_agent_message else " "}
    response = requests.request("POST", url, json=payload).json()
    return response["message"], response["contexts"]
"""
    if not name or not isinstance(name, str):
        raise ValueError("Project name must be a non-empty string")

    # Sanitize the folder name to prevent directory traversal
    name = os.path.basename(name)

    try:
        os.makedirs(name, exist_ok=True, mode=0o755)  # Explicit permissions

        file_path = os.path.join(name, "wrapper_function.py")

        # Check if file already exists to prevent accidental overwrites
        if os.path.exists(file_path):
            logger.warning(f"File already exists at {file_path}")
            return

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(file_content)

        logger.info(f"Project folder created: '{name}'")
    except OSError as e:
        logger.error(f"Failed to create project folder: {e}")
        raise
