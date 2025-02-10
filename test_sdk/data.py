data_e2e = [
    {
        "input_payload": {
            # "conversation_id": "123",
            "text": "I want to book a stay in London",
        },
        "conversation_history": [],
        "output_payload_expected": {
            "text": "OK",
        },
    },
    {
        "input_payload": {
            # "conversation_id": "456",
            "text": "I want to book a stay in San Francisco",
        },
        "conversation_history": [],
        "output_payload_expected": {
            "text": "OK",
        },
    },
]

data_reranking = [
    {
        "input_payload": {
            "query": "I want to book a stay in London",
            "documents": [
                "E",
                "C",
                "B",
                "D",
                "A",
            ],
        },
        "conversation_history": [],
        "output_payload_expected": {
            "documents": [
                "A",
                "B",
                "C",
                "D",
                "E",
            ],
        },
    },
    {
        "input_payload": {
            "query": "Re-rank the following documents: 3,4,5,2,1",
            "documents": [
                "3",
                "4",
                "5",
                "2",
                "1",
            ],
        },
        "conversation_history": [],
        "output_payload_expected": {
            "documents": [
                "1",
                "2",
                "3",
                "4",
                "5",
            ],
        },
    },
]
