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
import time
from maihem import Maihem, MaihemClient


@maihem.workflow_step(
    name="intent_recognition_custom_name",
    evaluator=MaihemIntent(
        inputs=MaihemIntent.Inputs(query="user_input"),
        output_fn=lambda x: x["intent"],  # Extract intent from the returned dict
    ),
)
async def intent_recognition_function(
    user_input: str,  # Different parameter name than the standard "query"
) -> dict:
    # Return richer data
    return {
        "intent": "Internal Knowledge",
        "confidence": 0.95,
        "alternatives": ["FAQ", "General Query"],
    }


@maihem.workflow_step(evaluator=MaihemNER(inputs=MaihemNER.Inputs(query="text")))
async def name_entity_recognition_function(
    text: str,
) -> list[str]:  # Different parameter name
    return ["Paris", "France"]


@maihem.workflow_step(
    evaluator=MaihemRephrasing(inputs=MaihemRephrasing.Inputs(query="input_text"))
)
async def rephrase_query_function(input_text: str) -> str:  # Different parameter name
    return input_text + "?"


@maihem.workflow_step(
    evaluator=MaihemRetrieval(
        inputs=MaihemRetrieval.Inputs(query="search_query"),
        output_fn=lambda x: x["documents"],  # Extract just the documents
    )
)
async def retrieval_function(search_query: str) -> dict:  # Different parameter names
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
async def reranking_function(
    query: str, docs: list[str], other_param: str = "default"
) -> list[str]:  # Different parameter name
    random.shuffle(docs)
    return docs


@maihem.workflow_step(
    evaluator=MaihemFiltering(
        inputs=MaihemFiltering.Inputs(query="query", documents="documents")
    )
)
async def filtering_function(
    query: str, documents: list[str]
) -> list[str]:  # Different parameter name
    return [x for x in documents if "42" in x]


@maihem.workflow_step(
    evaluator=MaihemFinalAnswer(
        inputs=MaihemFinalAnswer.Inputs(query="question", documents="context")
    )
)
async def answer_function(
    question: str, context: list[str]
) -> str:  # Different parameter names
    return "42"


@maihem.workflow_step(
    target_agent_name="target-deco-names",
    name="generate_message",
    evaluator=MaihemQA(
        inputs=MaihemQA.Inputs(query="user_input"),
    ),
)
async def generate_message(user_input: str) -> str:
    ####### NOTE THIS
    maihem.set_attribute("external_conversation_id", "convconvconv")
    ###################
    intent = await intent_recognition_function(user_input=user_input)
    entities = await name_entity_recognition_function(text=user_input)
    rephrased_query = await rephrase_query_function(input_text=user_input)
    retrieval_results = await retrieval_function(search_query=rephrased_query)
    reranking_results = await reranking_function(
        query=rephrased_query, docs=retrieval_results["documents"]
    )
    filtered_results = await filtering_function(
        query=rephrased_query, documents=reranking_results
    )
    result = await answer_function(question=rephrased_query, context=filtered_results)
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
    Maihem(
        api_key="",
        target_agent_name="target-deco",
        env="DEVELOPMENT",
        revision="test",
        base_url="http://localhost:8000",
    )
    asyncio.run(generate_message("What is six times lol"))
    # asyncio.run(intent_recognition("What is six times lol"))
    #### TESTING
    # setattr(generate_message, "conversation_id", "c_01jjvtme0jfz6rwt3xkq6ccjfj")
    # setattr(
    #     generate_message, "conversation_message_id", "cm_01jjvtmjvdfrvr5b6zsj0e4k7y"
    # )
    # setattr(generate_message, "agent_target_id", "at_01jjvkfq37ewtrathzx1k07zvw")
    # setattr(generate_message, "test_run_id", "tr_01jjvtkvg6f289gn8ttcz31xww")
    # setattr(generate_message, "testing", True)
    # asyncio.run(generate_message("What is six times nine"))
