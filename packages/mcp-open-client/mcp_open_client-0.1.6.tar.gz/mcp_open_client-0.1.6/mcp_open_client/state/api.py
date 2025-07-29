# API initialization and interaction functions
import os
import json
import requests
from . import core
from . import settings

def initialize_api():
    """Initialize the API client with current settings"""
    # Here we would typically initialize an API client
    from mcp_open_client.api import ChatAPI
    
    try:
        # Get settings with detailed logging
        base_url = settings.get_setting('base_url')
        model = settings.get_setting('model')
        api_key = settings.get_setting('api_key')
        
        print(f"Initializing API with: base_url={base_url}, model={model}")
        
        # Create the API client
        core.api = ChatAPI(
            base_url=base_url,
            model=model,
            api_key=api_key
        )
        
        print("API initialized successfully")
        return core.api
    except Exception as e:
        print(f"ERROR initializing API: {type(e).__name__}: {e}")
        
        # Create a minimal API client that will show errors to the user
        # instead of crashing the application
        from nicegui import ui
        
        try:
            # Still create the API object to prevent NoneType errors
            from mcp_open_client.api import ChatAPI
            core.api = ChatAPI(
                base_url=settings.get_setting('base_url', 'http://localhost:8000'),
                model=settings.get_setting('model', 'claude-3-7-sonnet'),
                api_key=settings.get_setting('api_key', 'dummy-key')
            )
            
            # Show error notification to the user
            try:
                ui.notify(f"Error initializing API: {str(e)}", type='negative')
            except:
                # If UI isn't ready yet, just log the error
                pass
                
            return core.api
        except Exception as inner_e:
            print(f"CRITICAL ERROR creating fallback API: {type(inner_e).__name__}: {inner_e}")
            # Return None to indicate initialization failed completely
            return None

def reinitialize_api():
    """Reinitializes the API client with current settings"""
    from mcp_open_client.api import ChatAPI
    
    # Helper function to sanitize function names for API compatibility
    def sanitize_function_name(name):
        """Sanitizes function names to match the pattern ^[a-zA-Z0-9_-]+$"""
        # Replace spaces with underscores and remove any other invalid characters
        return ''.join(c if c.isalnum() or c in '_-' else '_' for c in name.replace(' ', '_'))
    
    try:
        core.api = ChatAPI(
            base_url=settings.get_setting('base_url'),
            model=settings.get_setting('model'),
            api_key=settings.get_setting('api_key')
        )
        from nicegui import ui
        ui.notify("API reinicializada con la nueva configuración")
        return True
    except Exception as e:
        from nicegui import ui
        ui.notify(f"Error al reinicializar API: {str(e)}", type='negative')
        return False

async def send_message(messages, stream=True):
    """Send a message to the API and get a response"""
    # Make sure API is initialized
    if core.api is None:
        print("API is None in send_message, trying to initialize it")
        core.api = initialize_api()
        if core.api is None:
            from nicegui import ui
            ui.notify("API not available. Please check your settings.", type='negative')
            return False, "API not available. Please check your settings.", False
    
    # Prepare the request payload
    payload = {
        'model': settings.get_setting('model'),
        'messages': messages,
        'temperature': settings.get_setting('temperature'),
        'max_tokens': settings.get_setting('max_tokens'),
        'stream': stream
    }
    
    # Add system prompt if available
    system_prompt = settings.get_setting('system_prompt')
    if system_prompt:
        # Insert system message at the beginning
        if messages and messages[0].get('role') != 'system':
            messages.insert(0, {
                'role': 'system',
                'content': system_prompt
            })
    
    # Debug logging
    if settings.get_setting('debug_logging'):
        print(f"API Request: {json.dumps(payload, indent=2)}")
    
    try:
        # Use the async API client instead of requests
        response = await core.api.send_message(
            messages=messages,
            model=settings.get_setting('model'),
            temperature=settings.get_setting('temperature'),
            max_tokens=settings.get_setting('max_tokens')
        )
        
        # Debug logging
        if settings.get_setting('debug_logging'):
            print(f"API Response received successfully")
        
        return response
    
    except Exception as e:
        print(f"API Error: {type(e).__name__}: {e}")
        from nicegui import ui
        ui.notify(f"Error sending message: {str(e)}", type='negative')
        
        # Return a tuple with error information to prevent further errors
        return False, f"Error: {str(e)}", False

def test_api_connection():
    """Test the connection to the API"""
    if core.api is None:
        initialize_api()
    
    try:
        # Make a simple request to test the connection
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {settings.get_setting('api_key')}"
        }
        
        response = requests.get(
            f"{settings.get_setting('base_url')}/models",
            headers=headers
        )
        
        if response.status_code == 200:
            return True, "Connection successful"
        else:
            return False, f"Connection failed: {response.status_code} - {response.text}"
    
    except Exception as e:
        return False, f"Connection error: {e}"

async def get_available_models():
    """Fetches available models from the API"""
    # Create a dictionary with only the current model
    current_model = settings.get_setting('model')
    current_model_dict = {current_model: f'Current: {current_model}'}
    
    # If API is not initialized, return only the current model
    if core.api is None:
        return False, current_model_dict
    
    try:
        success, models_list = await core.api.get_available_models()
        if success and models_list:
            # Convert list to dictionary format
            models_dict = {model: model for model in models_list}
            
            # Always ensure current model is in the dictionary
            if current_model not in models_dict:
                models_dict[current_model] = f'Current: {current_model}'
                
            return True, models_dict
        return False, current_model_dict
    except Exception as e:
        from nicegui import ui
        ui.notify(f"Error al obtener modelos: {str(e)}", type='negative')
        return False, current_model_dict