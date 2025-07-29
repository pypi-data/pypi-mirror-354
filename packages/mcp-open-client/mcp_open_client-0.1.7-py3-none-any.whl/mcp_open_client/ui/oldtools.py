# Tools UI components

from nicegui import ui
from mcp_open_client import state
import json
import asyncio

def render_tools_page(container):
    """Renders the tools page"""
    with container:
        # Page header with title and save button
        with ui.row().classes('app-flex-row app-full-width app-space-between'):
            ui.label('Herramientas').classes('app-page-title')
            ui.button('Guardar herramientas', icon='save', on_click=state.save_settings).classes('app-primary-button')
        
        # Default tools section
        with ui.card().classes('app-card'):
            with ui.row().classes('app-card-header app-default-header'):
                ui.label('Herramientas por defecto').classes('app-card-title')
                ui.icon('verified').classes('app-icon-large')
            
            # Container for the list of default tools
            default_tools_container = ui.column().classes('app-container')
        
        # Custom tools section
        with ui.card().classes('app-card'):
            with ui.row().classes('app-card-header app-custom-header'):
                ui.label('Herramientas personalizadas').classes('app-card-title')
                ui.icon('build').classes('app-icon-large')
            
            # Container for the list of custom tools
            custom_tools_container = ui.column().classes('app-container')
            
            # Function to update the tools list
            def update_tools_list():
                # Clear both containers
                default_tools_container.clear()
                custom_tools_container.clear()
                
                # Separate default and custom tools
                print("Filtering tools in update_tools_list()...")
                
                # Import default tool IDs directly from default_tools module
                from mcp_open_client.default_tools import DEFAULT_TOOLS
                default_tool_ids = [tool['id'] for tool in DEFAULT_TOOLS]
                print(f"Default tool IDs from DEFAULT_TOOLS: {default_tool_ids}")
                
                # Check if any tools in app_state match the default tool IDs
                app_state = state.get_app_state()
                default_tools = [tool for tool in app_state['tools'] if tool['id'] in default_tool_ids]
                custom_tools = [tool for tool in app_state['tools'] if tool['id'] not in default_tool_ids]
                
                # Debug: Print all tools in app_state with full details
                print(f"All tools in app_state: {len(app_state['tools'])}")
                for tool in app_state['tools']:
                    print(f"  - ID: {tool['id']}")
                    print(f"    Name: {tool['name']}")
                    print(f"    Type: {tool.get('type', 'unknown')}")
                    print(f"    Active: {tool.get('active', False)}")
                    print(f"    Is Default: {tool['id'] in default_tool_ids}")
                
                # Debug: Print tools count summary
                print(f"All tools: {len(app_state['tools'])}")
                print(f"Default tools: {len(default_tools)}")
                print(f"Custom tools: {len(custom_tools)}")
                
                # Display default tools
                if not default_tools:
                    with default_tools_container:
                        with ui.row().classes('app-empty-state'):
                            ui.icon('info').classes('app-icon-muted')
                            ui.label('No hay herramientas por defecto disponibles').classes('app-text-muted app-text-italic')
                else:
                    for tool in default_tools:
                        with default_tools_container:
                            with ui.card().classes('app-tool-card app-default-tool-card'):
                                with ui.row().classes('app-flex-row app-full-width app-space-between'):
                                    # Left side with tool info
                                    with ui.column().classes('app-flex-column app-flex-grow'):
                                        # Tool name and type in one row
                                        with ui.row().classes('app-flex-row app-items-center'):
                                            ui.icon('verified').classes('app-icon-primary')
                                            # Display original name if available, otherwise use name
                                            display_name = tool.get('original_name', tool['name'])
                                            ui.label(display_name).classes('app-tool-name')
                                            ui.label('Herramienta por defecto').classes('app-badge app-default-badge')
                                            # Status badge
                                            status_class = 'app-badge-success' if tool['active'] else 'app-badge-inactive'
                                            status_text = 'Activa' if tool['active'] else 'Inactiva'
                                            ui.label(status_text).classes(f'app-badge {status_class}')
                                        
                                        # Tool description
                                        ui.label(tool['description']).classes('app-tool-description')
                                    
                                    # Right side with action buttons
                                    with ui.row().classes('app-flex-row app-items-center app-flex-shrink-0'):
                                        # Active toggle with better styling
                                        ui.switch('Activar', value=tool['active'],
                                                on_change=lambda e, t_id=tool['id']: state.update_tool(t_id, active=e.value)
                                                ).classes('app-switch')
                                        
                                        # Edit button (disabled for default tools)
                                        edit_button = ui.button('Editar', icon='edit').classes('app-button app-edit-button')
                                        edit_button.disable()
                                        edit_button.tooltip('Las herramientas por defecto no se pueden editar')
                                        
                                        # Delete button (disabled for default tools)
                                        delete_button = ui.button('Eliminar', icon='delete').classes('app-button app-delete-button')
                                        delete_button.disable()
                                        delete_button.tooltip('Las herramientas por defecto no se pueden eliminar')
                
                # Display custom tools
                if not custom_tools:
                    with custom_tools_container:
                        with ui.row().classes('app-empty-state'):
                            ui.icon('info').classes('app-icon-muted')
                            ui.label('No hay herramientas personalizadas disponibles').classes('app-text-muted app-text-italic')
                else:
                    for tool in custom_tools:
                        with custom_tools_container:
                            with ui.card().classes('app-tool-card app-custom-tool-card'):
                                with ui.row().classes('app-flex-row app-full-width app-space-between'):
                                    # Left side with tool info
                                    with ui.column().classes('app-flex-column app-flex-grow'):
                                        # Tool name and type in one row
                                        with ui.row().classes('app-flex-row app-items-center'):
                                            ui.icon('build_circle').classes('app-icon-primary')
                                            # Display original name if available, otherwise use name
                                            display_name = tool.get('original_name', tool['name'])
                                            ui.label(display_name).classes('app-tool-name')
                                            ui.label(f"Tipo: {tool['type']}").classes('app-badge app-type-badge')
                                            # Status badge
                                            status_class = 'app-badge-success' if tool['active'] else 'app-badge-inactive'
                                            status_text = 'Activa' if tool['active'] else 'Inactiva'
                                            ui.label(status_text).classes(f'app-badge {status_class}')
                                        
                                        # Tool description
                                        ui.label(tool['description']).classes('app-tool-description')
                                    
                                    # Right side with action buttons
                                    with ui.row().classes('app-flex-row app-items-center app-flex-shrink-0'):
                                        # Active toggle with better styling
                                        ui.switch('Activar', value=tool['active'],
                                                on_change=lambda e, t_id=tool['id']: state.update_tool(t_id, active=e.value)
                                                ).classes('app-switch')
                                        
                                        # Edit button
                                        edit_button = ui.button('Editar', icon='edit',
                                                on_click=lambda t=tool: show_edit_tool_dialog(t, update_tools_list)
                                                ).classes('app-button app-edit-button')
                                        
                                        # Delete button
                                        delete_button = ui.button('Eliminar', icon='delete',
                                                on_click=lambda t=tool['id']: confirm_delete_tool(t, update_tools_list)
                                                ).classes('app-button app-delete-button')
            
            # Function to confirm tool deletion
            def confirm_delete_tool(tool_id, callback):
                with ui.dialog() as dialog, ui.card().classes('app-dialog-card'):
                    ui.label('Confirmar eliminación').classes('app-dialog-title')
                    ui.label('¿Estás seguro de que deseas eliminar esta herramienta? Esta acción no se puede deshacer.').classes('app-dialog-text')
                    
                    with ui.row().classes('app-dialog-actions'):
                        ui.button('Cancelar', on_click=dialog.close).classes('app-button app-cancel-button')
                        ui.button('Eliminar', on_click=lambda: delete_tool_and_update(tool_id, dialog, callback)
                                ).classes('app-button app-delete-button')
                
                dialog.open()
            
            # Function to delete a tool and update the list
            def delete_tool_and_update(tool_id, dialog, callback):
                if state.delete_tool(tool_id):
                    dialog.close()
                    callback()
                    ui.notify('Herramienta eliminada correctamente', type='positive')
            
            # Function to show edit tool dialog
            def show_edit_tool_dialog(tool, callback):
                with ui.dialog() as dialog, ui.card().classes('app-dialog-card app-dialog-large'):
                    # Display original name if available, otherwise use name
                    display_name = tool.get('original_name', tool['name'])
                    ui.label(f'Editar herramienta: {display_name}').classes('app-dialog-title')
                    
                    # Tool name and description
                    ui.label('Nombre:').classes('app-form-label')
                    tool_name_input = ui.input(value=display_name).classes('app-input')
                    
                    ui.label('Descripción:').classes('app-form-label')
                    tool_description_input = ui.textarea(value=tool['description']).classes('app-textarea')
                    
                    # Tool type
                    ui.label('Tipo:').classes('app-form-label')
                    tool_type_input = ui.select(
                        options={'function': 'Función'},
                        value=tool['type'],
                        label='Tipo de herramienta'
                    ).classes('app-select')
                    
                    # JSON Schema editor for parameters
                    ui.label('Parámetros (Esquema JSON):').classes('text-weight-bold')
                    
                    # Parse the parameters JSON
                    try:
                        parameters_json = json.loads(tool['parameters'])
                    except:
                        parameters_json = {
                            "type": "object",
                            "properties": {},
                            "required": [],
                            "additionalProperties": False
                        }
                    
                    parameters_editor = ui.json_editor(
                        {'content': {'json': parameters_json}},
                        on_change=lambda e: ui.notify('Esquema actualizado')
                    ).classes('app-json-editor')
                    
                    # Python code editor
                    ui.label('Código Python:').classes('app-form-label')
                    code_editor = ui.codemirror(
                        tool['code'],
                        language='python',
                        theme='basicLight',
                        line_wrapping=True
                    ).classes('app-code-editor')

                    # Validate Python code button
                    ui.button('Validar Código', on_click=lambda: validate_python_code(code_editor.value)).classes('app-button app-secondary-button')

                    # Function to validate Python code
                    def validate_python_code(code):
                        try:
                            compile(code, '<string>', 'exec')
                            ui.notify('Código Python válido', type='positive')
                        except SyntaxError as e:
                            ui.notify(f'Error de sintaxis: {str(e)}', type='negative')
                    
                    # Buttons
                    with ui.row().classes('app-dialog-actions'):
                        ui.button('Cancelar', on_click=dialog.close).classes('app-button app-cancel-button')
                        ui.button('Guardar cambios',
                                on_click=lambda: save_tool_changes(tool['id'], tool_name_input.value,
                                                                tool_description_input.value, tool_type_input.value,
                                                                parameters_editor, code_editor.value, dialog, callback)
                                ).classes('app-button app-primary-button')
                
                dialog.open()
            
            # Function to save tool changes
            async def save_tool_changes(tool_id, name, description, tool_type, parameters_editor, code, dialog, callback):
                try:
                    # Validate inputs
                    if not name or not description:
                        ui.notify('El nombre y la descripción son obligatorios', type='warning')
                        return
                    
                    # Validate tool name for API compatibility
                    from mcp_open_client.state import sanitize_function_name
                    sanitized_name = sanitize_function_name(name)
                    if name != sanitized_name:
                        ui.notify(
                            f"El nombre '{name}' contiene caracteres no válidos para la API. "
                            f"Se utilizará '{sanitized_name}' para compatibilidad con la API.",
                            type='warning'
                        )
                    
                    # Get schema JSON
                    parameters_json = await get_schema_json(parameters_editor)
                    parameters = json.dumps(parameters_json)
                    
                    # Update the tool
                    if state.update_tool(tool_id, name=name, description=description,
                                        tool_type=tool_type, parameters=parameters, code=code):
                        dialog.close()
                        callback()
                        ui.notify('Herramienta actualizada correctamente', type='positive')
                except Exception as e:
                    ui.notify(f'Error al actualizar la herramienta: {str(e)}', type='negative')
            
            # Initial update of the tools list
            update_tools_list()
        
        # Create new tool section
        with ui.card().classes('app-card'):
            with ui.row().classes('app-card-header app-custom-header'):
                ui.label('Crear nueva herramienta').classes('app-card-title')
                ui.icon('add_circle').classes('app-icon-large')
            
            with ui.column().classes('app-container app-form-container'):
                # Tool name and description
                # Tool name input (full width)
                ui.label('Nombre:').classes('app-form-label')
                tool_name_input = ui.input(placeholder='Nombre de la herramienta').classes('app-input')
                
                # Hidden tool type input (always "function")
                tool_type_input = ui.input(value='function').classes('hidden')
                
                # Description input
                ui.label('Descripción:').classes('app-form-label')
                tool_description_input = ui.textarea(placeholder='Descripción detallada de la herramienta y su funcionamiento').classes('app-textarea')
                
                # JSON Schema editor for parameters with improved guidance
                # Editors in a two-column layout with explicit display flex
                ui.label('Editores').classes('app-section-title')
                with ui.row().classes('app-flex-row app-full-width app-editors-container'):
                    # Left column - JSON Schema Editor
                    with ui.column().classes('app-editor-column'):
                        ui.label('Parámetros (Esquema JSON)').classes('app-form-label')
                        # Default schema with required "type": "object" field
                        default_schema = {
                            'type': 'object',
                            'properties': {
                                'query': {
                                    'type': 'string',
                                    'description': 'Consulta o parámetro principal'
                                },
                                'options': {
                                    'type': 'object',
                                    'properties': {
                                        'limit': {
                                            'type': 'number',
                                            'description': 'Número máximo de resultados'
                                        }
                                    }
                                }
                            },
                            'required': ['query'],
                            'additionalProperties': False
                        }
                        
                        parameters_editor = ui.json_editor(
                            {'content': {'json': default_schema}},
                            on_change=lambda e: ui.notify('Esquema actualizado')
                        ).classes('app-json-editor app-editor-large')
                    
                    # Right column - Python Code Editor
                    with ui.column().classes('app-editor-column'):
                        ui.label('Código Python').classes('app-form-label')
                        ui.label('Implementa la función execute_tool que recibirá los parámetros y devolverá el resultado').classes('app-help-text')
                        
                        code_template = """def execute_tool(params):
    \"\"\"Implementación de la herramienta
    
    Args:
        params (dict): Parámetros recibidos según el esquema JSON definido
        
    Returns:
        dict: Resultado de la ejecución de la herramienta
    \"\"\"
    # Extraer parámetros
    query = params.get('query', '')
    options = params.get('options', {})
    limit = options.get('limit', 10)
    
    # Lógica de la herramienta
    # Aquí implementa la funcionalidad principal
    
    # Ejemplo de respuesta
    result = f"Procesando consulta: {query} (límite: {limit})"
    
    # Devolver resultado estructurado
    return {
        "result": result,
        "timestamp": __import__('datetime').datetime.now().isoformat()
    }
"""
                        
                        code_editor = ui.codemirror(
                            code_template,
                            language='python',
                            theme='basicLight',
                            line_wrapping=True
                        ).classes('app-code-editor app-editor-large')
                
                # Button to create the tool
                # Button to create the tool
                async def create_new_tool():
                    name = tool_name_input.value
                    description = tool_description_input.value
                    tool_type = tool_type_input.value
                    
                    # Validate inputs
                    if not name or not description:
                        ui.notify('El nombre y la descripción son obligatorios', type='warning')
                        return
                    
                    # Validate tool name for API compatibility
                    from mcp_open_client.state import sanitize_function_name
                    sanitized_name = sanitize_function_name(name)
                    if name != sanitized_name:
                        ui.notify(
                            f"El nombre '{name}' contiene caracteres no válidos para la API. "
                            f"Se utilizará '{sanitized_name}' para compatibilidad con la API.",
                            type='warning'
                        )
                    
                    # Get code from editor
                    code = code_editor.value
                    
                    try:
                        # Use the helper function to get the schema JSON
                        parameters_json = await get_schema_json(parameters_editor)
                        
                        # Ensure the schema has the required "type": "object" field
                        if "type" not in parameters_json:
                            parameters_json["type"] = "object"
                        
                        # Convert to string for storage
                        parameters = json.dumps(parameters_json)
                        
                        # Create the tool
                        tool_id = state.create_tool(name, description, tool_type, parameters, code)
                        
                        # Clear inputs
                        tool_name_input.value = ''
                        tool_description_input.value = ''
                        
                        # Reset editors to default values
                        parameters_editor.run_editor_method('set', {
                            'type': 'object',
                            'properties': {},
                            'required': [],
                            'additionalProperties': False
                        })
                        code_editor.value = """def execute_tool(params):
    # Código para ejecutar la herramienta
    
    # Devolver resultado
    return {
        "result": "Éxito"
    }
"""
                        
                        # Update the tools list
                        update_tools_list()
                        
                        ui.notify('Herramienta creada correctamente', type='positive')
                        
                        # Scroll to top to see the new tool
                        ui.run_javascript('window.scrollTo(0, 0);')
                    except Exception as e:
                        ui.notify(f'Error al crear la herramienta: {str(e)}', type='negative')
                
                with ui.row().classes('app-form-actions'):
                    ui.button('Crear herramienta', icon='add_circle', on_click=create_new_tool).classes('app-button app-primary-button')
            
            # Helper function to get schema JSON from editor
            async def get_schema_json(editor):
                # Get the current value from the editor
                editor_value = await editor.run_editor_method('get')
                
                # Extract the JSON content
                if isinstance(editor_value, dict) and 'content' in editor_value and 'json' in editor_value['content']:
                    return editor_value['content']['json']
                else:
                    return {
                        "type": "object",
                        "properties": {},
                        "required": [],
                        "additionalProperties": False
                    }