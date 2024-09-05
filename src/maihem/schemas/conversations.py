from typing import NamedTuple
from maihem.api_client.maihem_client.models.conversation_nested import (
    ConversationNested,
)


class ConversationTurnCreateResponse(NamedTuple):
    turn_id: str
    conversation: ConversationNested
