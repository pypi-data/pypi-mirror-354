# State module initialization

from . import core
from . import conversations
from . import settings
from . import api
from . import tools
from . import navigation

# Import and export the necessary functions
from .core import get_app_state, generate_unique_id, add_tool, update_tool
from .tools import sanitize_function_name, execute_tool
from .conversations import get_current_conversation, add_message_to_conversation, save_conversations_to_storage
from .settings import save_settings

def initialize_state():
    """Initialize all state components"""
    settings.load_settings()
    conversations.initialize_conversations()
    tools.initialize_tools()
    api.initialize_api()
    core.app_state['initialized'] = True
    return core.app_state

# Export the functions
__all__ = ['get_app_state', 'sanitize_function_name', 'execute_tool', 'get_current_conversation', 'add_message_to_conversation', 'save_conversations_to_storage', 'initialize_state', 'save_settings', 'add_tool', 'update_tool']