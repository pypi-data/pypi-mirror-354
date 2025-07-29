import re
from jsonschema import validate, ValidationError
from nicegui import ui
import json
from mcp_open_client import state

def sanitize_input(input_string, max_length=None):
    """
    Sanitizes user input by removing potentially harmful characters and trimming whitespace.
    
    Args:
        input_string (str): The input string to sanitize.
        max_length (int, optional): Maximum allowed length for the input string.
    
    Returns:
        str: The sanitized input string.
    """
    cleaned = re.sub(r'<[^>]*>', '', input_string)
    cleaned = ''.join(char for char in cleaned if char.isprintable() or char in '\n\t')
    cleaned = cleaned.strip()
    
    if max_length is not None:
        cleaned = cleaned[:max_length]
    
    return cleaned

# JSON Schema for tool parameters
TOOL_PARAMETER_SCHEMA = {
    "type": "object",
    "properties": {
        "properties": {
            "type": "object",
            "patternProperties": {
                "^[a-zA-Z_][a-zA-Z0-9_]*$": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string", "enum": ["string", "number", "boolean", "array", "object"]},
                        "description": {"type": "string"},
                        "default": {},
                        "required": {"type": "boolean"}
                    },
                    "required": ["type"]
                }
            },
            "additionalProperties": False
        }
    },
    "required": ["properties"]
}

def validate_json_schema(schema):
    """
    Validates the JSON schema for tool parameters.
    
    Args:
        schema (dict): The JSON schema to validate.
    
    Returns:
        tuple: (bool, str) A tuple containing a boolean indicating if the schema is valid,
               and a string with an error message if it's not valid (or None if it is).
    """
    try:
        validate(instance=schema, schema=TOOL_PARAMETER_SCHEMA)
        return True, None
    except ValidationError as e:
        return False, f"Error de validación del esquema JSON: {e.message}"

def validate_python_code(code, silent=False):
    """
    Validates the given Python code by attempting to compile it.
    
    Args:
        code (str): The Python code to validate.
        silent (bool): If True, suppresses UI notifications.
    
    Returns:
        bool: True if the code is valid, False otherwise.
    """
    try:
        compile(code, '<string>', 'exec')
        if not silent:
            ui.notify('El código Python es válido', color='positive')
        return True
    except SyntaxError as e:
        if not silent:
            ui.notify(f'Error de sintaxis en el código Python: {str(e)}', color='negative')
        return False

def show_json_schema_help():
    """
    Displays a modal with detailed information about the JSON schema structure.
    """
    with ui.dialog() as help_dialog, ui.card():
        ui.label('Estructura del Esquema JSON').classes('text-h6')
        ui.markdown('''
        El esquema JSON debe seguir esta estructura:
        ```json
        {
          "properties": {
            "param_name": {
              "type": "string|number|boolean|array|object",
              "description": "Descripción del parámetro",
              "default": "Valor por defecto (opcional)"
            }
          }
        }
        ```
        - `param_name`: Nombre del parámetro
        - `type`: Tipo de dato (string, number, boolean, array, object)
        - `description`: Descripción del parámetro
        - `default`: Valor por defecto (opcional)
        
        Ejemplo:
        ```json
        {
          "properties": {
            "nombre": {
              "type": "string",
              "description": "Nombre del usuario"
            },
            "edad": {
              "type": "number",
              "description": "Edad del usuario",
              "default": 18
            }
          }
        }
        ```
        ''')
        ui.button('Cerrar', on_click=help_dialog.close).classes('app-button')
    help_dialog.open()

def add_tool_and_update(name, description, json_editor, python_editor, dialog, callback):
    """
    Validates input, creates a new tool, and updates the tool list.
    
    Args:
        name (str): Name of the tool.
        description (str): Description of the tool.
        json_editor (ui.codemirror): CodeMirror editor containing JSON schema for tool parameters.
        python_editor (ui.codemirror): CodeMirror editor containing Python code.
        dialog (ui.dialog): Dialog to be closed on success.
        callback (function): Function to be called after successfully adding a tool.
    """
    from mcp_open_client import state  # Import here to avoid circular imports
    
    sanitized_name = sanitize_input(name, max_length=100)
    if not sanitized_name:
        ui.notify('El nombre es obligatorio y no puede estar vacío', color='secondary')
        return
    
    sanitized_description = sanitize_input(description, max_length=500)
    
    try:
        schema = json.loads(json_editor.value)
        is_valid, error_message = validate_json_schema(schema)
        if not is_valid:
            ui.notify(error_message, color='secondary')
            return
    except json.JSONDecodeError:
        ui.notify('Error al analizar el JSON. Por favor, verifica la sintaxis.', color='secondary')
        return
    
    if not validate_python_code(python_editor.value, silent=True):
        return
    
    new_tool = {
        'id': state.generate_unique_id(),
        'name': sanitized_name,
        'description': sanitized_description,
        'parameters': schema,
        'code': python_editor.value,
        'type': 'custom',  # Add a default type for new tools
        'active': True  # Set the tool as active by default
    }
    
    try:
        state.add_tool(new_tool)
        dialog.close()
        ui.notify('Herramienta agregada exitosamente', color='primary')
        callback()
    except Exception as e:
        ui.notify(f'Error al guardar la herramienta: {str(e)}', color='negative')

def edit_tool_and_update(tool_id, name, description, json_editor, python_editor, dialog, callback, tool_type='custom', active=True):
    """
    Validates input, updates an existing tool, and refreshes the tool list.
    
    Args:
        tool_id (str): ID of the tool to be edited.
        name (str): Updated name of the tool.
        description (str): Updated description of the tool.
        json_editor (ui.codemirror): CodeMirror editor containing updated JSON schema for tool parameters.
        python_editor (ui.codemirror): CodeMirror editor containing updated Python code.
        dialog (ui.dialog): Dialog to be closed on success.
        callback (function): Function to be called after successfully editing the tool.
        tool_type (str): Type of the tool, defaults to 'custom'.
        active (bool): Whether the tool is active or not, defaults to True.
    """
    from mcp_open_client import state  # Import here to avoid circular imports
    
    existing_tool = state.get_tool(tool_id)
    if not existing_tool:
        ui.notify('Herramienta no encontrada', color='negative')
        return
    
    sanitized_name = sanitize_input(name, max_length=100)
    if not sanitized_name:
        ui.notify('El nombre es obligatorio y no puede estar vacío', color='secondary')
        return
    
    sanitized_description = sanitize_input(description, max_length=500)
    
    try:
        schema = json.loads(json_editor.value)
        is_valid, error_message = validate_json_schema(schema)
        if not is_valid:
            ui.notify(error_message, color='secondary')
            return
    except json.JSONDecodeError:
        ui.notify('Error al analizar el JSON. Por favor, verifica la sintaxis.', color='secondary')
        return
    
    if not validate_python_code(python_editor.value, silent=True):
        return
    
    updated_tool = {
        'id': tool_id,
        'name': sanitized_name,
        'description': sanitized_description,
        'parameters': schema,
        'code': python_editor.value,
        'type': tool_type,
        'active': active
    }
    
    try:
        state.update_tool(tool_id, updated_tool)
        dialog.close()
        ui.notify('Herramienta actualizada exitosamente', color='primary')
        callback()
    except Exception as e:
        ui.notify(f'Error al actualizar la herramienta: {str(e)}', color='negative')
        ui.notify('Herramienta no encontrada', color='negative')
        return
    
    sanitized_name = sanitize_input(name, max_length=100)
    if not sanitized_name:
        ui.notify('El nombre es obligatorio y no puede estar vacío', color='secondary')
        return
    
    sanitized_description = sanitize_input(description, max_length=500)
    
    try:
        schema = json.loads(json_editor.value)
        is_valid, error_message = validate_json_schema(schema)
        if not is_valid:
            ui.notify(error_message, color='secondary')
            return
    except json.JSONDecodeError:
        ui.notify('Error al analizar el JSON. Por favor, verifica la sintaxis.', color='secondary')
        return
    
    if not validate_python_code(python_editor.value, silent=True):
        return
    
    updated_tool = {
        'id': tool_id,
        'name': sanitized_name,
        'description': sanitized_description,
        'parameters': schema,
        'code': python_editor.value,
        'type': existing_tool.get('type', 'custom')  # Preserve existing type or use 'custom' as default
    }
    
    if state.update_tool(updated_tool):
        dialog.close()
        ui.notify('Herramienta actualizada exitosamente', color='primary')
        callback()
    else:
        ui.notify('Error al actualizar la herramienta', color='negative')