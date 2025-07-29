import uuid
from typing import Optional, TypedDict, List, Dict, Any

class Settings(TypedDict):
    temperature: float
    max_tokens: int
    model: str
    base_url: str
    api_key: str
    dark_mode: bool
    system_prompt: str
    debug_logging: bool

class AppState(TypedDict):
    initialized: bool
    current_page: str
    messages: List[Dict[str, Any]]
    conversations: List[Dict[str, Any]]
    current_conversation_id: Optional[str]
    settings: Settings
    tools: List[Dict[str, Any]]
    page_renderers: Dict[str, Any]
from nicegui import ui

# Core state management
# Contains the basic state variables and structures

# API instance (will be initialized in main.py)
api = None

def generate_unique_id():
    """
    Generates a unique ID using UUID4.
    """
    return str(uuid.uuid4())

# State of the application
app_state: AppState = {
    'initialized': False,
    'current_page': 'chat',
    'messages': [],
    'conversations': [],
    'current_conversation_id': None,
    'settings': {
        'temperature': 0.7,
        'max_tokens': 2000,
        'model': 'claude-3-7-sonnet',
        'base_url': 'http://192.168.58.101:8123/v1',
        'api_key': 'not-needed',
        'dark_mode': False,
        'system_prompt': 'You are a helpful AI assistant.',
        'debug_logging': False
    },
    'tools': [],  # List to store custom tools
    'page_renderers': {}
}

# UI references (will be set in main.py)
content_container: Optional[ui.column] = None
chat_container: Optional[ui.column] = None
conversations_container: Optional[ui.column] = None
chat_input: Optional[ui.input] = None
messages_container: Optional[ui.column] = None
loading_spinner: Optional[ui.spinner] = None
send_button: Optional[ui.button] = None

def get_app_state() -> AppState:
    """
    Returns the current application state.
    """
    return app_state

# Make sure the functions are available for import
from .settings import save_user_tools

def add_tool(new_tool: Dict[str, Any]) -> bool:
    """
    Adds a new tool to the app_state['tools'] list and saves it to the file.
    
    Args:
        new_tool (dict): The new tool to be added.
    
    Returns:
        bool: True if the tool was added and saved successfully, False otherwise.
    """
    if new_tool and 'id' in new_tool:
        app_state['tools'].append(new_tool)
        if save_user_tools():
            print(f"Tool '{new_tool['name']}' added and saved successfully.")
            return True
        else:
            print(f"Error: Tool '{new_tool['name']}' was added to app_state but couldn't be saved to file.")
    return False

def update_tool(tool_id: str, is_active: Optional[bool] = None, **kwargs: Any) -> bool:
    """
    Updates an existing tool in the app_state['tools'] list and saves the changes.
    
    Args:
        tool_id (str): The ID of the tool to update.
        is_active (bool, optional): The new active state of the tool.
        **kwargs: Additional key-value pairs to update in the tool.
    
    Returns:
        bool: True if the tool was updated and saved successfully, False otherwise.
    """
    for index, tool in enumerate(app_state['tools']):
        if tool['id'] == tool_id:
            if is_active is not None:
                app_state['tools'][index]['active'] = is_active
            for key, value in kwargs.items():
                app_state['tools'][index][key] = value
            if save_user_tools():
                print(f"Tool '{tool['name']}' updated and saved successfully.")
                return True
            else:
                print(f"Error: Tool '{tool['name']}' was updated in app_state but couldn't be saved to file.")
    return False

__all__ = ['get_app_state', 'app_state', 'generate_unique_id', 'add_tool', 'update_tool', 'AppState']