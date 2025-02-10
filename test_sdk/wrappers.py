from test_dummy_workflow import generate_message, reranking


async def wrapper_generate_message(
    conversation_id: str, user_input: str, conversation_history: dict
) -> str:
    return await generate_message(user_input)


async def wrapper_reranking(query: str, docs: list[str]) -> str:
    return reranking(query=query, docs=docs)
