from typing import Any, Callable, Optional

function_registry = {}


def register_function(function: Callable, function_name: Optional[str] = None) -> None:
    function_name_dict = function_name or function.__name__
    function_registry[function_name_dict] = function


def call_function(function_name: str, *args, **kwargs) -> Any:
    return function_registry[function_name](*args, **kwargs)


def get_function(function_name: str) -> Callable:
    return function_registry[function_name]
