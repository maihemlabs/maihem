from test_dummy_workflow import generate_message


def wrapper_generate_message(
    conversation_id: str, user_input: str, conversation_history: dict
) -> str:
    return generate_message(user_input)
