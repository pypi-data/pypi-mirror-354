# Settings management functions
import json
import os
from . import core

# Paths for storing settings
HOME_DIR = os.path.expanduser("~")
CONFIG_DIR = os.path.join(HOME_DIR, ".mcp-open-client", "config")
SETTINGS_FILE = os.path.join(CONFIG_DIR, "user_settings.json")
TOOLS_FILE = os.path.join(CONFIG_DIR, "user_tools.json")
THEME_FILE = os.path.join(CONFIG_DIR, "user_theme.css")
CONVERSATIONS_DIR = os.path.join(HOME_DIR, ".mcp-open-client", "conversations")

def load_settings():
    """Load settings and user tools from the settings files"""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    os.makedirs(CONVERSATIONS_DIR, exist_ok=True)
    
    if not os.path.exists(SETTINGS_FILE):
        # If settings file doesn't exist, use default settings
        save_settings()
    else:
        try:
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                # Update the app state settings
                core.app_state['settings'].update(settings)
        except Exception as e:
            print(f"Error loading settings: {e}")
            # If there's an error, use default settings
            save_settings()
    
    # Load user tools
    load_user_tools()

def load_user_tools():
    """Load user's custom tools from the tools file"""
    if os.path.exists(TOOLS_FILE):
        try:
            with open(TOOLS_FILE, 'r', encoding='utf-8') as f:
                user_tools = json.load(f)
                # Update the app state tools
                core.app_state['tools'].extend(user_tools)
        except Exception as e:
            print(f"Error loading user tools: {e}")

def save_settings():
    """Save current settings to the settings file"""
    try:
        # Ensure directories exist
        os.makedirs(CONFIG_DIR, exist_ok=True)
        os.makedirs(CONVERSATIONS_DIR, exist_ok=True)
        
        # Save settings
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(core.app_state['settings'], f, ensure_ascii=False, indent=2)
        
        # Save tools
        save_user_tools()
        
        return True
    except Exception as e:
        print(f"Error saving settings: {e}")
        return False

def save_user_tools():
    """Save user's custom tools to the tools file"""
    try:
        with open(TOOLS_FILE, 'w', encoding='utf-8') as f:
            json.dump(core.app_state['tools'], f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving user tools: {e}")
        return False

def update_setting(key, value):
    """Update a specific setting"""
    if key in core.app_state['settings']:
        core.app_state['settings'][key] = value
        save_settings()
        return True
    return False

def get_setting(key, default=None):
    """Get a specific setting value"""
    return core.app_state['settings'].get(key, default)

def toggle_dark_mode():
    """Toggle dark mode setting"""
    core.app_state['settings']['dark_mode'] = not core.app_state['settings']['dark_mode']
    save_settings()
    return core.app_state['settings']['dark_mode']

def set_model(model):
    """Set the AI model to use"""
    core.app_state['settings']['model'] = model
    save_settings()

def set_temperature(temperature):
    """Set the temperature parameter for the AI model"""
    # Ensure temperature is a float between 0 and 1
    temperature = float(temperature)
    temperature = max(0.0, min(1.0, temperature))
    
    core.app_state['settings']['temperature'] = temperature
    save_settings()

def set_max_tokens(max_tokens):
    """Set the max tokens parameter for the AI model"""
    # Ensure max_tokens is an integer greater than 0
    max_tokens = int(max_tokens)
    max_tokens = max(1, max_tokens)
    
    core.app_state['settings']['max_tokens'] = max_tokens
    save_settings()

def set_api_key(api_key):
    """Set the API key for the AI service"""
    core.app_state['settings']['api_key'] = api_key
    save_settings()

def set_base_url(base_url):
    """Set the base URL for the AI service"""
    core.app_state['settings']['base_url'] = base_url
    save_settings()

def set_system_prompt(system_prompt):
    """Set the system prompt for the AI model"""
    core.app_state['settings']['system_prompt'] = system_prompt
    save_settings()

def toggle_debug_logging():
    """Toggle debug logging setting"""
    core.app_state['settings']['debug_logging'] = not core.app_state['settings']['debug_logging']
    save_settings()
    return core.app_state['settings']['debug_logging']