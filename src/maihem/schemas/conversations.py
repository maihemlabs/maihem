from typing import NamedTuple, Optional
from maihem.api_client.maihem_client.models.conversation_nested import (
    ConversationNested,
)


class ConversationTurnCreateResponse(NamedTuple):
    conversation: ConversationNested
    pending_target_message_id: Optional[str] = None
    turn_id: Optional[str] = None
