# Custom tools management functions
import json
import os
import importlib.util
import sys
import uuid
from . import core

# Path for storing custom tools
TOOLS_DIRECTORY = "tools"

def initialize_tools():
    """Initialize tools directory and load existing tools"""
    # Create tools directory if it doesn't exist
    if not os.path.exists(TOOLS_DIRECTORY):
        os.makedirs(TOOLS_DIRECTORY)
    
    # Load existing tools
    load_tools()

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
        
        # Reload the tools
        load_tools()
        
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
        
        # Remove the tool from the list
        core.app_state['tools'] = [t for t in core.app_state['tools'] if t['name'] != name]
        
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
        
        # Reload the tools
        load_tools()
        
        return {
            'success': True,
            'message': f"Tool '{name}' updated successfully"
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

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