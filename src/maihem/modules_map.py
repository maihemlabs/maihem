from typing import List, Dict, Any

import maihem.errors as errors
from maihem.utils.utils import spread_n_into_buckets


def map_module_list_to_metrics(
    modules: List[str], number_conversations: int
) -> Dict[str, Dict[str, Any]]:
    """Map modules to metrics."""
    metrics_config = {}
    for module in modules:
        if module == "cx":
            if 0 < number_conversations <= 4:
                metrics_config["qa_cx_goal_completion"] = number_conversations
            else:
                convs_list = spread_n_into_buckets(number_conversations, 4)
                metrics_config["qa_cx_goal_completion"] = convs_list[0]
                metrics_config["qa_cx_helpfulness"] = convs_list[1]
                metrics_config["qa_cx_retention"] = convs_list[2]
                metrics_config["qa_cx_nps"] = convs_list[3]
        elif module == "rag":
            convs_list = spread_n_into_buckets(number_conversations, 3)
            metrics_config["qa_rag_hallucination"] = convs_list[0]
            metrics_config["qa_rag_answer_relevance"] = convs_list[1]
            metrics_config["qa_rag_context_relevance"] = convs_list[2]
        else:
            raise errors.raise_not_found_error(
                f"Module '{module}' is not supported. Please check the supported modules in https://docs.maihem.ai/reference/metric-collection."
            )

    return metrics_config
