from typing import Callable, Optional

function_registry = {}


def register_function(function: Callable, function_name: Optional[str] = None) -> None:
    function_name_dict = function.__name__ if not function_name else function_name
    function_registry[function_name_dict] = function


def call_function(function_name: str, *args, **kwargs) -> Callable:
    return function_registry[function_name](*args, **kwargs)
