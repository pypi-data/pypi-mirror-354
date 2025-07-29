# Core state management
# Contains the basic state variables and structures

# API instance (will be initialized in main.py)
api = None

# State of the application
app_state = {
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
content_container = None
chat_container = None
chat_input = None

def get_app_state():
    """
    Returns the current application state.
    """
    return app_state

# Make sure the function is available for import
__all__ = ['get_app_state', 'app_state']