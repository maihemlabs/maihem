from typing import Optional, Callable, Any
import inspect
from functools import wraps, lru_cache


workflow_registry = {}


def workflow():

    def decorator(func: Callable) -> Callable:

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:

            return func(*args, **kwargs)

        return wrapper

    return decorator


def workflow():
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Get function name
            func_name = func.__name__
            print(f"Executing workflow for function: {func_name}")

            # Get arguments
            bound_args = inspect.signature(func).bind(*args, **kwargs)
            bound_args.apply_defaults()
            print(f"Arguments: {bound_args.arguments}")

            # Call the actual function
            result = func(*args, **kwargs)

            # Return the result
            return result

        workflow_registry[func.__name__] = func
        print(f"Function {func.__name__} saved to registry")

        return wrapper

    return decorator


@workflow()
def sum(x: int, y: int) -> int:
    return x + y


# Function is registered but not called in the decorator
print(f"Registered functions: {list(workflow_registry.keys())}")

print(sum(5, 4))

# Function is registered but not called in the decorator
print(f"Registered functions: {list(workflow_registry.keys())}")

# Call the function manually using the registry
r = workflow_registry["sum"](**{"x": 1, "y": 2})
print(r)

raise
