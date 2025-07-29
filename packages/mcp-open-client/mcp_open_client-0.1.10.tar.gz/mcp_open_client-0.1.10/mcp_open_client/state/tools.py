# Custom tools management functions
import json
import os
import importlib.util
import sys
from typing import Dict, Any, Optional, List, TypedDict, Union
import uuid

class Tool(TypedDict):
    name: str
    description: str
    module: Any
    file: str
from . import core
from .settings import CONFIG_DIR, TOOLS_FILE

# Path for storing custom tools
TOOLS_DIRECTORY = "tools"

def initialize_tools() -> None:
    """Initialize tools directory and load existing tools"""
    # Create tools directory if it doesn't exist
    if not os.path.exists(TOOLS_DIRECTORY):
        os.makedirs(TOOLS_DIRECTORY)
    
    # Load existing tools
    load_tools()
    
    # Load user's custom tools
    load_user_tools()

def load_tools() -> None:
    """Load all tools from the tools directory"""
    core.app_state['tools'] = []
    
    # First load default tools
    from mcp_open_client.default_tools import get_default_tools
    default_tools = get_default_tools()
    
    for tool in default_tools:
        # Normalize default tool structure
        normalized_tool: Dict[str, Any] = {
            'id': tool.get('id'),
            'name': tool.get('name'),
            'original_name': tool.get('name'),  # Preserve original name
            'sanitized_name': sanitize_function_name(tool.get('name', '')),
            'description': tool.get('description', ''),
            'type': tool.get('type', 'function'),
            'parameters': tool.get('parameters'),
            'code': tool.get('code'),
            'active': tool.get('active', True),
            'source': 'default'
        }
        core.app_state['tools'].append(normalized_tool)
    
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
                if spec is not None and spec.loader is not None:
                    tool_module = importlib.util.module_from_spec(spec)
                    sys.modules[tool_name] = tool_module
                    spec.loader.exec_module(tool_module)
                else:
                    print(f"Error loading tool {tool_name}: Invalid module specification")
                    continue
                
                # Check if the module has the required attributes
                if hasattr(tool_module, 'tool_name') and hasattr(tool_module, 'execute'):
                    tool: Dict[str, Any] = {
                        'name': tool_module.tool_name,
                        'original_name': tool_module.tool_name,
                        'sanitized_name': sanitize_function_name(tool_module.tool_name),
                        'description': getattr(tool_module, 'tool_description', ''),
                        'module': tool_module,
                        'file': filename,
                        'source': 'custom'
                    }
                    core.app_state['tools'].append(tool)
            except Exception as e:
                print(f"Error loading tool {tool_name}: {e}")

def load_user_tools() -> None:
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

def get_tool_by_name(name: str) -> Optional[Dict[str, Any]]:
    """Get a tool by its name"""
    tools: List[Dict[str, Any]] = core.app_state.get('tools', [])
    return next((tool for tool in tools if tool['name'] == name), None)

def execute_tool(tool_name: str, args: Dict[str, Any]) -> Dict[str, Union[bool, str, Dict[str, Any]]]:
    """Execute a tool by its name with the given arguments"""
    tool = get_tool_by_name(tool_name)
    if tool is None:
        # Try to find by sanitized name, original name, or id
        tools = core.app_state.get('tools', [])
        for t in tools:
            if (t.get('sanitized_name') == tool_name or
                t.get('original_name') == tool_name or
                t.get('id') == tool_name or
                sanitize_function_name(t.get('name', '')) == tool_name):
                tool = t
                break
        
        if tool is None:
            # Log available tools for debugging
            available_tools = [t.get('id', t.get('name', 'unknown')) for t in tools]
            print(f"Tool '{tool_name}' not found. Available tools: {available_tools}")
            return {
                'success': False,
                'error': f"Tool '{tool_name}' not found. Available tools: {available_tools}"
            }
    
    try:
        # Handle different tool types
        if 'module' in tool and hasattr(tool['module'], 'execute'):
            # Custom tool with module
            result = tool['module'].execute(args)
        elif 'code' in tool:
            # Default tool with embedded code - execute dynamically
            exec_globals = {
                'params': args,
                'ui': None,  # Will be imported if needed
                'uuid': None,  # Will be imported if needed
            }
            
            # Import commonly needed modules
            try:
                from nicegui import ui
                import uuid
                exec_globals['ui'] = ui
                exec_globals['uuid'] = uuid
            except ImportError:
                pass
            
            # Execute the tool code
            try:
                exec(tool['code'], exec_globals)
                if 'execute_tool' in exec_globals and callable(exec_globals['execute_tool']):
                    result = exec_globals['execute_tool'](args)
                else:
                    result = {"success": False, "error": "No callable execute_tool function found in code"}
            except Exception as exec_error:
                result = {"success": False, "error": f"Error executing tool code: {str(exec_error)}"}
        else:
            return {
                'success': False,
                'error': f"Tool '{tool_name}' has no executable code or module"
            }
            
        # Ensure result is properly formatted
        if not isinstance(result, dict):
            result = {"success": True, "result": result}
            
        return {
            'success': True,
            'result': result
        }
    except Exception as e:
        print(f"Error executing tool '{tool_name}': {str(e)}")
        return {
            'success': False,
            'error': f"Error executing tool: {str(e)}"
        }

def create_tool(name: str, description: str, code: str) -> Dict[str, Union[bool, str, Dict[str, Any]]]:
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
        new_tool: Dict[str, Any] = {
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

def delete_tool(name: str) -> Dict[str, Union[bool, str, Dict[str, Any]]]:
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


def update_tool(name: str, description: str, code: str) -> Dict[str, Union[bool, str, Dict[str, Any]]]:
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
        updated_tool: Dict[str, Any] = {
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

def save_user_tool(tool: Dict[str, Any]) -> None:
    """Save or update a user tool in user_tools.json"""
    try:
        # Ensure the CONFIG_DIR exists
        os.makedirs(CONFIG_DIR, exist_ok=True)
        
        user_tools: List[Dict[str, Any]] = []
        if os.path.exists(TOOLS_FILE):
            with open(TOOLS_FILE, 'r', encoding='utf-8') as f:
                user_tools = json.load(f)
        
        # Update existing tool or add new one
        for i, t in enumerate(user_tools):
            if t['name'] == tool['name']:
                user_tools[i] = tool
                break
        else:
            user_tools.append(tool)
        
        with open(TOOLS_FILE, 'w', encoding='utf-8') as f:
            json.dump(user_tools, f, indent=2)
        
        print(f"Tool '{tool['name']}' saved successfully to {TOOLS_FILE}")
    except Exception as e:
        print(f"Error saving user tool: {e}")
        raise  # Re-raise the exception to be caught by the calling function

def remove_user_tool(name: str) -> None:
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

def get_tools_for_api() -> List[Dict[str, Any]]:
    """Get a list of tools for API consumption"""
    api_tools: List[Dict[str, Any]] = []
    for tool in core.app_state['tools']:
        api_tool: Dict[str, Any] = {
            'type': 'function',
            'function': {
                'name': sanitize_function_name(tool['name']),
                'description': tool['description'],
                'parameters': getattr(tool['module'], 'parameters', {}),
            }
        }
        api_tools.append(api_tool)
    return api_tools

def sanitize_function_name(name: str) -> str:
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


def generate_unique_id() -> str:
    """Generate a unique ID for tools.
    
    Returns:
        str: A unique identifier string
    """
    return str(uuid.uuid4())


def delete_tool_by_id(tool_id: str) -> bool:
    """Delete a tool from user tools by ID.
    
    Args:
        tool_id: The ID of the tool to delete
        
    Returns:
        bool: True if tool was deleted successfully, False otherwise
    """
    try:
        # Load user tools from JSON file
        user_tools = []
        if os.path.exists(TOOLS_FILE):
            with open(TOOLS_FILE, 'r', encoding='utf-8') as f:
                user_tools = json.load(f)
        
        # Find and remove the tool with the given ID
        original_count = len(user_tools)
        user_tools = [tool for tool in user_tools if tool.get('id') != tool_id]
        
        # Check if a tool was actually removed
        if len(user_tools) == original_count:
            print(f"Tool with ID {tool_id} not found")
            return False
        
        # Save the updated tools list back to JSON file
        with open(TOOLS_FILE, 'w', encoding='utf-8') as f:
            json.dump(user_tools, f, indent=2)
        
        print(f"Tool {tool_id} deleted successfully")
        return True
        
    except Exception as e:
        print(f"Error deleting tool {tool_id}: {e}")
        return False


# Create a wrapper function that matches the original delete_tool signature
def delete_tool_wrapper(tool_id: str) -> bool:
    """Wrapper for delete_tool_by_id to maintain UI compatibility."""
    return delete_tool_by_id(tool_id)