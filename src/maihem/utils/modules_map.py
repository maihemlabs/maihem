from typing import List, Dict, Any

import maihem.shared.lib.errors as errors
from maihem.utils.utils import spread_n_into_buckets
from maihem.shared.lib.logger import get_logger


def map_module_list_to_metrics(
    modules: List[str], number_conversations: int
) -> Dict[str, Dict[str, Any]]:
    """Map modules to metrics."""
    logger = get_logger()
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
            errors.raise_not_found_error(
                logger=logger,
                entity_type="module",
                entity_key=module,
                comment="Please check the supported modules in https://docs.maihem.ai/reference/metric-collection",
            )

    return metrics_config
