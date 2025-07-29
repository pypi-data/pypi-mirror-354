from nicegui import ui, events
from mcp_open_client import state
import json
from .utils import sanitize_input, validate_json_schema, validate_python_code, show_json_schema_help, add_tool_and_update, edit_tool_and_update
from .preview import toggle_preview, generate_preview, update_preview

# Configuración global de las notificaciones
ui.colors(primary='#34D399', secondary='#F87171')  # Verde para éxito, rojo para error

def open_add_tool_dialog(callback):
    """
    Opens a dialog for adding a new tool.
    
    Args:
        callback (function): Function to be called after successfully adding a tool.
    """
    with ui.dialog() as dialog, ui.card().classes('w-full max-w-3xl p-4 shadow-lg'):
        ui.label('Agregar nueva herramienta').classes('text-2xl font-bold mb-4')
        
        name = ui.input(label='Nombre').classes('w-full mb-2')
        description = ui.input(label='Descripción').classes('w-full mb-4')
        
        ui.label('Parámetros (Esquema JSON):').classes('font-bold mb-2')
        default_schema = {
            "type": "object",
            "properties": {
                "param1": {
                    "type": "string",
                    "description": "Description of param1"
                },
                "param2": {
                    "type": "number",
                    "description": "Description of param2"
                }
            },
            "required": ["param1", "param2"]
        }
        json_editor = ui.codemirror(value=json.dumps(default_schema, indent=2), language='json').classes('w-full mb-4')
        
        with ui.tooltip('El esquema debe seguir la estructura: {"properties": {"param_name": {"type": "string|number|boolean|array|object", "description": "...", "default": "..."}}}'):
            ui.button('Ayuda', on_click=show_json_schema_help).classes('mb-2 bg-blue-500 text-white p-2 rounded')
        
        preview_button = ui.button('Vista previa de parámetros', on_click=lambda: toggle_preview(json_editor, preview_container, preview_button)).classes('mb-2 bg-green-500 text-white p-2 rounded')
        preview_container = ui.column().classes('w-full mb-4')
        preview_container.set_visibility(False)

        ui.label('Código Python:').classes('font-bold mb-2')
        default_python_code = '''def execute_tool(param1: str, param2: int):
    """
    Execute the tool with the given parameters.
    
    Args:
        param1 (str): Description of param1
        param2 (int): Description of param2
    
    Returns:
        str: The result of the tool execution
    """
    # Your code here
    result = f"Executed with param1={param1} and param2={param2}"
    return result'''
        
        python_editor = ui.codemirror(value=default_python_code, language='python').classes('w-full h-40 mb-4')
        
        ui.button('Validar Código', on_click=lambda: validate_python_code(python_editor.value)).classes('mb-4 bg-yellow-500 text-white p-2 rounded')

        with ui.row().classes('w-full justify-end'):
            ui.button('Cancelar', on_click=dialog.close).classes('mr-2 bg-gray-500 text-white p-2 rounded')
            ui.button('Agregar', on_click=lambda: add_tool_and_update(name.value, description.value, json_editor, python_editor, dialog, callback)
                    ).classes('bg-blue-500 text-white p-2 rounded')
    
    dialog.open()

def open_edit_tool_dialog(tool, callback):
    """
    Opens a dialog for editing an existing tool.
    
    Args:
        tool (dict): The tool to be edited.
        callback (function): Function to be called after successfully editing the tool.
    """
    with ui.dialog() as dialog, ui.card().classes('w-full max-w-3xl p-4 shadow-lg'):
        ui.label('Editar herramienta').classes('text-2xl font-bold mb-4')
        
        name = ui.input(label='Nombre', value=tool['name']).classes('w-full mb-2')
        description = ui.input(label='Descripción', value=tool['description']).classes('w-full mb-4')
        
        ui.label('Parámetros (Esquema JSON):').classes('font-bold mb-2')
        json_editor = ui.codemirror(value=json.dumps(tool['parameters'], indent=2), language='json').classes('w-full mb-4')
        
        with ui.tooltip('El esquema debe seguir la estructura: {"properties": {"param_name": {"type": "string|number|boolean|array|object", "description": "...", "default": "..."}}}'):
            ui.button('Ayuda', on_click=show_json_schema_help).classes('mb-2 bg-blue-500 text-white p-2 rounded')
        
        preview_button = ui.button('Vista previa de parámetros', on_click=lambda: toggle_preview(json_editor, preview_container, preview_button)).classes('mb-2 bg-green-500 text-white p-2 rounded')
        preview_container = ui.column().classes('w-full mb-4')
        preview_container.set_visibility(False)
        
        ui.label('Código Python:').classes('font-bold mb-2')
        python_editor = ui.codemirror(value=tool['code'], language='python').classes('w-full h-40 mb-4')
        
        ui.button('Validar Código', on_click=lambda: validate_python_code(python_editor.value)).classes('mb-4 bg-yellow-500 text-white p-2 rounded')

        with ui.row().classes('w-full justify-end'):
            ui.button('Cancelar', on_click=dialog.close).classes('mr-2 bg-gray-500 text-white p-2 rounded')
            ui.button('Guardar', on_click=lambda: edit_tool_and_update(tool['id'], name.value, description.value, json_editor, python_editor, dialog, callback, tool.get('type', 'custom'), active=tool.get('active', True))
                    ).classes('bg-blue-500 text-white p-2 rounded')
    
    dialog.open()

# End of file