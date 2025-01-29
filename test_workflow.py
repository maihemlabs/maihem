import maihem
from maihem.evaluators import (
    MaihemIntent,
    MaihemNER,
    MaihemRephrasing,
    MaihemRetrieval,
    MaihemReranking,
    MaihemFiltering,
    MaihemFinalAnswer,
    MaihemQA,
)
import asyncio
import random


@maihem.observe(
    evaluator=MaihemIntent(
        inputs=MaihemIntent.Inputs(query="user_input"),
        output_fn=lambda x: x["intent"],  # Extract intent from the returned dict
    )
)
async def intent_recognition(
    user_input: str,  # Different parameter name than the standard "query"
) -> dict:
    # Return richer data
    return {
        "intent": "Internal Knowledge",
        "confidence": 0.95,
        "alternatives": ["FAQ", "General Query"],
    }


@maihem.observe(evaluator=MaihemNER(inputs=MaihemNER.Inputs(query="text")))
async def name_entity_recognition(text: str) -> list[str]:  # Different parameter name
    return ["Paris", "France"]


@maihem.observe(
    evaluator=MaihemRephrasing(inputs=MaihemRephrasing.Inputs(query="input_text"))
)
async def rephrase_query(input_text: str) -> str:  # Different parameter name
    return input_text + "?"


@maihem.observe(
    evaluator=MaihemRetrieval(
        inputs=MaihemRetrieval.Inputs(query="search_query"),
        output_fn=lambda x: x["documents"],  # Extract just the documents
    )
)
async def retrieval(search_query: str) -> dict:  # Different parameter names
    # Return richer data
    return {
        "documents": [
            "The Eiffel Tower is in Paris, France",
            "Guglieo Marconi was born in Bologna, Italy",
            "Tesla was founded in 2003 in Palo Alto, California",
            "42",
            "In 1942 then most common car was the Ford Model T",
        ],
        "scores": [0.95, 0.85, 0.75, 0.65, 0.55],
        "metadata": [
            {"source": "wiki", "date": "2024"},
            {"source": "web", "date": "2023"},
            {"source": "news", "date": "2024"},
            {"source": "book", "date": "2022"},
            {"source": "archive", "date": "2021"},
        ],
    }


@maihem.observe(
    evaluator=MaihemReranking(inputs=MaihemReranking.Inputs(documents="docs"))
)
async def reranking(docs: list[str]) -> list[str]:  # Different parameter name
    random.shuffle(docs)
    return docs


@maihem.observe(
    evaluator=MaihemFiltering(inputs=MaihemFiltering.Inputs(documents="documents"))
)
async def filtering(documents: list[str]) -> list[str]:  # Different parameter name
    return [x for x in documents if "42" in x]


@maihem.observe(
    evaluator=MaihemFinalAnswer(
        inputs=MaihemFinalAnswer.Inputs(query="question", documents="context")
    )
)
async def answer(question: str, context: list[str]) -> str:  # Different parameter names
    return "42"


@maihem.observe(
    workflow_name="workflow_v1",
    evaluator=MaihemQA(
        inputs=MaihemQA.Inputs(query="user_input"),
    ),
)
async def generate_message(query: str) -> str:
    ####### NOTE THIS
    maihem.set_attribute("external_conversation_id", "convconvconv")
    ###################

    intent = await intent_recognition(user_input=query)
    entities = await name_entity_recognition(text=query)
    rephrased_query = await rephrase_query(input_text=query)
    retrieval_results = await retrieval(search_query=rephrased_query)
    reranking_results = await reranking(docs=retrieval_results["documents"])
    filtered_results = await filtering(documents=reranking_results)
    result = await answer(question=rephrased_query, context=filtered_results)
    return result


if __name__ == "__main__":
    #### MONITORING
    asyncio.run(generate_message("What is six times lol"))

    #### TESTING
    setattr(generate_message, "conversation_id", "c_01jjm9yr56fe0vckf989vecn1a")
    setattr(
        generate_message, "conversation_message_id", "cm_01jjm9yyehe6rsxvtz1nz509f9"
    )
    setattr(generate_message, "agent_target_id", "at_01j9q95r56eng9daxt85nyfhca")
    setattr(generate_message, "test_run_id", "tr_01jjm9yr3tfmrtxmxx0dfdbfcr")
    setattr(generate_message, "testing", True)
    asyncio.run(generate_message("What is six times nine"))
