# Custom tools management functions
import json
import os
import importlib.util
import sys
import uuid
from . import core
from .settings import CONFIG_DIR, TOOLS_FILE

# Path for storing custom tools
TOOLS_DIRECTORY = "tools"

def initialize_tools():
    """Initialize tools directory and load existing tools"""
    # Create tools directory if it doesn't exist
    if not os.path.exists(TOOLS_DIRECTORY):
        os.makedirs(TOOLS_DIRECTORY)
    
    # Load existing tools
    load_tools()
    
    # Load user's custom tools
    load_user_tools()

def load_tools():
    """Load all tools from the tools directory"""
    core.app_state['tools'] = []
    
    if not os.path.exists(TOOLS_DIRECTORY):
        return
    
    # Look for Python files in the tools directory
    for filename in os.listdir(TOOLS_DIRECTORY):
        if filename.endswith('.py'):
            tool_path = os.path.join(TOOLS_DIRECTORY, filename)
            tool_name = filename[:-3]  # Remove .py extension
            
            try:
                # Load the tool module
                spec = importlib.util.spec_from_file_location(tool_name, tool_path)
                tool_module = importlib.util.module_from_spec(spec)
                sys.modules[tool_name] = tool_module
                spec.loader.exec_module(tool_module)
                
                # Check if the module has the required attributes
                if hasattr(tool_module, 'tool_name') and hasattr(tool_module, 'execute'):
                    tool = {
                        'name': tool_module.tool_name,
                        'description': getattr(tool_module, 'tool_description', ''),
                        'module': tool_module,
                        'file': filename
                    }
                    core.app_state['tools'].append(tool)
            except Exception as e:
                print(f"Error loading tool {tool_name}: {e}")

def load_user_tools():
    """Load user's custom tools from the user_tools.json file"""
    if not os.path.exists(TOOLS_FILE):
        return
    
    try:
        with open(TOOLS_FILE, 'r', encoding='utf-8') as f:
            user_tools = json.load(f)
        
        for tool in user_tools:
            if 'name' in tool and 'description' in tool:
                core.app_state['tools'].append(tool)
    except Exception as e:
        print(f"Error loading user tools: {e}")

def get_tool_by_name(name):
    """Get a tool by its name"""
    for tool in core.app_state['tools']:
        if tool['name'] == name:
            return tool
    return None

def execute_tool(tool_name, args):
    """Execute a tool by its name with the given arguments"""
    tool = get_tool_by_name(tool_name)
    if tool is None:
        return {
            'success': False,
            'error': f"Tool '{tool_name}' not found"
        }
    
    try:
        # Call the tool's execute function
        result = tool['module'].execute(args)
        return {
            'success': True,
            'result': result
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def create_tool(name, description, code):
    """Create a new tool with the given name, description, and code"""
    # Sanitize the filename
    filename = name.lower().replace(' ', '_') + '.py'
    file_path = os.path.join(TOOLS_DIRECTORY, filename)
    
    # Check if a tool with this name already exists
    if get_tool_by_name(name) is not None:
        return {
            'success': False,
            'error': f"A tool with the name '{name}' already exists"
        }
    
    # Create the tool file
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        # Add the tool to user_tools.json
        new_tool = {
            'name': name,
            'description': description,
            'file': filename
        }
        save_user_tool(new_tool)
        
        # Reload the tools
        load_tools()
        load_user_tools()
        
        return {
            'success': True,
            'message': f"Tool '{name}' created successfully"
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def delete_tool(name):
    """Delete a tool by its name"""
    tool = get_tool_by_name(name)
    if tool is None:
        return {
            'success': False,
            'error': f"Tool '{name}' not found"
        }
    
    try:
        # Delete the tool file
        file_path = os.path.join(TOOLS_DIRECTORY, tool['file'])
        os.remove(file_path)
        
        # Remove the tool from the list and user_tools.json
        core.app_state['tools'] = [t for t in core.app_state['tools'] if t['name'] != name]
        remove_user_tool(name)
        
        return {
            'success': True,
            'message': f"Tool '{name}' deleted successfully"
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def update_tool(name, description, code):
    """Update an existing tool with new code"""
    tool = get_tool_by_name(name)
    if tool is None:
        return {
            'success': False,
            'error': f"Tool '{name}' not found"
        }
    
    try:
        # Update the tool file
        file_path = os.path.join(TOOLS_DIRECTORY, tool['file'])
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        # Update the tool in user_tools.json
        updated_tool = {
            'name': name,
            'description': description,
            'file': tool['file']
        }
        save_user_tool(updated_tool)
        
        # Reload the tools
        load_tools()
        load_user_tools()
        
        return {
            'success': True,
            'message': f"Tool '{name}' updated successfully"
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def save_user_tool(tool):
    """Save or update a user tool in user_tools.json"""
    try:
        # Ensure the CONFIG_DIR exists
        os.makedirs(CONFIG_DIR, exist_ok=True)
        
        user_tools = []
        if os.path.exists(TOOLS_FILE):
            with open(TOOLS_FILE, 'r', encoding='utf-8') as f:
                user_tools = json.load(f)
        
        # Update existing tool or add new one
        updated = False
        for i, t in enumerate(user_tools):
            if t['name'] == tool['name']:
                user_tools[i] = tool
                updated = True
                break
        if not updated:
            user_tools.append(tool)
        
        with open(TOOLS_FILE, 'w', encoding='utf-8') as f:
            json.dump(user_tools, f, indent=2)
        
        print(f"Tool '{tool['name']}' saved successfully to {TOOLS_FILE}")
    except Exception as e:
        print(f"Error saving user tool: {e}")
        raise  # Re-raise the exception to be caught by the calling function

def remove_user_tool(name):
    """Remove a user tool from user_tools.json"""
    try:
        if os.path.exists(TOOLS_FILE):
            with open(TOOLS_FILE, 'r', encoding='utf-8') as f:
                user_tools = json.load(f)
            
            user_tools = [t for t in user_tools if t['name'] != name]
            
            with open(TOOLS_FILE, 'w', encoding='utf-8') as f:
                json.dump(user_tools, f, indent=2)
    except Exception as e:
        print(f"Error removing user tool: {e}")

def get_tools_for_api():
    """Get a list of tools in the format required by the API"""
    api_tools = []
    
    for tool in core.app_state['tools']:
        api_tool = {
            'type': 'function',
            'function': {
                'name': tool['name'],
                'description': tool['description']
            }
        }
        
        # Add parameters if the tool module has them
        if hasattr(tool['module'], 'parameters'):
            api_tool['function']['parameters'] = tool['module'].parameters
        
        api_tools.append(api_tool)
    
    return api_tools

def sanitize_function_name(name):
    """
    Sanitize a function name to make it compatible with API requirements.
    Removes special characters and spaces, ensuring the name follows proper naming conventions.
    """
    # Replace spaces and special characters with underscores
    sanitized = ''.join(c if c.isalnum() else '_' for c in name)
    
    # Ensure the name starts with a letter or underscore
    if sanitized and not (sanitized[0].isalpha() or sanitized[0] == '_'):
        sanitized = 'f_' + sanitized
    
    # Ensure the name is not empty
    if not sanitized:
        sanitized = 'function_' + str(uuid.uuid4())[:8]
    
    return sanitized