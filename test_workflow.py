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


@maihem.workflow_step(
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


@maihem.workflow_step(evaluator=MaihemNER(inputs=MaihemNER.Inputs(query="text")))
async def name_entity_recognition(text: str) -> list[str]:  # Different parameter name
    return ["Paris", "France"]


@maihem.workflow_step(
    evaluator=MaihemRephrasing(inputs=MaihemRephrasing.Inputs(query="input_text"))
)
async def rephrase_query(input_text: str) -> str:  # Different parameter name
    return input_text + "?"


@maihem.workflow_step(
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


@maihem.workflow_step(
    evaluator=MaihemReranking(
        inputs=MaihemReranking.Inputs(query="query", documents="docs")
    )
)
async def reranking(
    query: str, docs: list[str]
) -> list[str]:  # Different parameter name
    random.shuffle(docs)
    return docs


@maihem.workflow_step(
    evaluator=MaihemFiltering(
        inputs=MaihemFiltering.Inputs(query="query", documents="documents")
    )
)
async def filtering(
    query: str, documents: list[str]
) -> list[str]:  # Different parameter name
    return [x for x in documents if "42" in x]


@maihem.workflow_step(
    evaluator=MaihemFinalAnswer(
        inputs=MaihemFinalAnswer.Inputs(query="question", documents="context")
    )
)
async def answer(question: str, context: list[str]) -> str:  # Different parameter names
    return "42"


@maihem.workflow(
    agent_target="target-deco",
    evaluator=MaihemQA(
        inputs=MaihemQA.Inputs(query="user_input"),
    ),
)
async def generate_message(user_input: str) -> str:
    ####### NOTE THIS
    maihem.set_attribute("external_conversation_id", "convconvconv")
    ###################
    intent = await intent_recognition(user_input=user_input)
    entities = await name_entity_recognition(text=user_input)
    rephrased_query = await rephrase_query(input_text=user_input)
    retrieval_results = await retrieval(search_query=rephrased_query)
    reranking_results = await reranking(
        query=rephrased_query, docs=retrieval_results["documents"]
    )
    filtered_results = await filtering(
        query=rephrased_query, documents=reranking_results
    )
    result = await answer(question=rephrased_query, context=filtered_results)
    return result


if __name__ == "__main__":
    #### DEBUG with json
    # import json

    # data = {
    #     "query": "What is six times nine",
    #     "maihem_ids": {
    #         "conversation_id": "c_01jjvtme0jfz6rwt3xkq6ccjfj",
    #         "conversation_message_id": "cm_01jjvtmjvdfrvr5b6zsj0e4k7y",
    #         "test_run_id": "tr_01jjvtkvg6f289gn8ttcz31xww",
    #     },
    # }
    # asyncio.run(generate_message(json.dumps(data)))  # test args
    # asyncio.run(generate_message(user_input=json.dumps(data)))  # test kwargs

    ### MONITORING
    asyncio.run(generate_message("What is six times lol"))

    #### TESTING
    setattr(generate_message, "conversation_id", "c_01jjvtme0jfz6rwt3xkq6ccjfj")
    setattr(
        generate_message, "conversation_message_id", "cm_01jjvtmjvdfrvr5b6zsj0e4k7y"
    )
    setattr(generate_message, "agent_target_id", "at_01jjvkfq37ewtrathzx1k07zvw")
    setattr(generate_message, "test_run_id", "tr_01jjvtkvg6f289gn8ttcz31xww")
    setattr(generate_message, "testing", True)
    asyncio.run(generate_message("What is six times nine"))
