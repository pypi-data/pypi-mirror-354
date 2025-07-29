# State module initialization

from typing import Any, Dict, Optional, Callable, Union

from . import core
from . import conversations
from . import settings
from . import api
from . import tools

# Import and export the necessary functions
from .core import get_app_state, add_tool, update_tool, AppState
from .tools import sanitize_function_name, execute_tool, delete_tool, delete_tool_wrapper, generate_unique_id
from .conversations import (
    get_current_conversation,
    add_message_to_conversation,
    add_message,
    save_conversations_to_storage,
    select_conversation,
    delete_conversation
)
from typing import Dict, Any, Callable
from .settings import save_settings

# Add type annotations
sanitize_function_name: Callable[[str], str]
execute_tool: Callable[[str, Dict[str, Any]], Dict[str, Union[bool, str, Dict[str, Any]]]]
get_current_conversation: Callable[[], Optional[Dict[str, Any]]]
add_message_to_conversation: Callable[[str, Dict[str, Any]], None]
add_message: Callable[[Dict[str, Any]], None]
save_settings: Callable[[], bool]

def initialize_state():
    """Initialize all state components"""
    settings.load_settings()
    conversations.initialize_conversations()
    tools.initialize_tools()
    api.initialize_api()
    core.app_state['initialized'] = True
    return core.app_state

# Export the functions
__all__ = ['get_app_state', 'sanitize_function_name', 'execute_tool', 'delete_tool', 'delete_tool_wrapper', 'generate_unique_id', 'get_current_conversation', 'add_message_to_conversation', 'add_message', 'save_conversations_to_storage', 'select_conversation', 'delete_conversation', 'initialize_state', 'save_settings', 'add_tool', 'update_tool', 'AppState']