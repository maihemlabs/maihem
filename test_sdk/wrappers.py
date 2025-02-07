from test_dummy_workflow import generate_message


async def wrapper_generate_message(
    conversation_id: str, user_input: str, conversation_history: dict
) -> str:
    return await generate_message(user_input)
