from typing import Dict, Any, TypedDict

class Conversation(TypedDict):
    id: str
    name: str
    messages: list[Dict[str, Any]]

class AppState(TypedDict):
    conversations: Dict[str, Conversation]
    current_conversation_id: str | None
    settings: Dict[str, Any]

# Add more custom types as needed