from nicegui import ui
from mcp_open_client import state
from .tool_dialogs import open_edit_tool_dialog, validate_python_code, generate_preview

def render_default_tool(tool, container):
    with container:
        with ui.card().classes('app-tool-card app-default-tool-card'):
            with ui.row().classes('app-flex-row app-full-width app-space-between'):
                # Left side with tool info
                with ui.column().classes('app-flex-column app-flex-grow'):
                    # Tool name and type in one row
                    with ui.row().classes('app-flex-row app-items-center'):
                        ui.icon('verified').classes('app-icon-primary')
                        display_name = tool.get('original_name', tool['name'])
                        ui.label(display_name).classes('app-tool-name')
                        ui.label('Herramienta por defecto').classes('app-badge app-default-badge')
                        status_class = 'app-badge-success' if tool['active'] else 'app-badge-inactive'
                        status_text = 'Activa' if tool['active'] else 'Inactiva'
                        ui.label(status_text).classes(f'app-badge {status_class}')
                    
                    # Tool description
                    ui.label(tool['description']).classes('app-tool-description')
                
                # Right side with action buttons
                with ui.row().classes('app-flex-row app-items-center app-flex-shrink-0'):
                    # Active toggle with better styling
                    ui.switch('Activar', value=tool['active'],
                            on_change=lambda e, t_id=tool['id']: state.update_tool(t_id, is_active=e.value)
                            ).classes('app-switch')
                    
                    # Edit button (disabled for default tools)
                    edit_button = ui.button('Editar', icon='edit').classes('app-button app-edit-button')
                    edit_button.disable()
                    edit_button.tooltip('Las herramientas por defecto no se pueden editar')
                    
                    # Delete button (disabled for default tools)
                    delete_button = ui.button('Eliminar', icon='delete').classes('app-button app-delete-button')
                    delete_button.disable()
                    delete_button.tooltip('Las herramientas por defecto no se pueden eliminar')

def render_custom_tool(tool, container, update_callback, delete_callback):
    with container:
        with ui.card().classes('app-tool-card app-custom-tool-card'):
            with ui.row().classes('app-flex-row app-full-width app-space-between'):
                # Left side with tool info
                with ui.column().classes('app-flex-column app-flex-grow'):
                    # Tool name and type in one row
                    with ui.row().classes('app-flex-row app-items-center'):
                        ui.icon('build_circle').classes('app-icon-primary')
                        display_name = tool.get('original_name', tool['name'])
                        ui.label(display_name).classes('app-tool-name')
                        ui.label(f"Tipo: {tool.get('type', 'No especificado')}").classes('app-badge app-type-badge')
                        status_class = 'app-badge-success' if tool['active'] else 'app-badge-inactive'
                        status_text = 'Activa' if tool['active'] else 'Inactiva'
                        ui.label(status_text).classes(f'app-badge {status_class}')
                    
                    # Tool description
                    ui.label(tool['description']).classes('app-tool-description')
                    
                    # Parameter preview
                    with ui.expansion('Vista previa de parámetros').classes('app-expansion'):
                        ui.markdown(f"```\n{generate_preview(tool.get('parameters', {}))}\n```")
                    
                    # Code validation status
                    code_valid = validate_python_code(tool.get('code', ''), silent=True)
                    validation_class = 'app-badge-success' if code_valid else 'app-badge-error'
                    validation_text = 'Código válido' if code_valid else 'Código inválido'
                    ui.label(validation_text).classes(f'app-badge {validation_class}')
                
                # Right side with action buttons
                with ui.row().classes('app-flex-row app-items-center app-flex-shrink-0'):
                    # Active toggle with better styling
                    ui.switch('Activar', value=tool['active'],
                            on_change=lambda e, t_id=tool['id']: state.update_tool(t_id, is_active=e.value)
                            ).classes('app-switch')
                    
                    # Edit button
                    edit_button = ui.button('Editar', icon='edit',
                            on_click=lambda t=tool: open_edit_tool_dialog(t, update_callback)
                            ).classes('app-button app-edit-button')
                    
                    # Delete button
                    delete_button = ui.button('Eliminar', icon='delete',
                            on_click=lambda t=tool['id']: delete_callback(t)
                            ).classes('app-button app-delete-button')

def confirm_delete_tool(tool_id, update_callback):
    def delete_tool():
        if state.delete_tool_wrapper(tool_id):
            ui.notify('Herramienta eliminada correctamente', type='positive')
            update_callback()
        else:
            ui.notify('Error al eliminar la herramienta', type='negative')
        dialog.close()

    with ui.dialog() as dialog, ui.card():
        ui.label('¿Está seguro de que desea eliminar esta herramienta?')
        with ui.row():
            ui.button('Cancelar', on_click=dialog.close).classes('app-button app-cancel-button')
            ui.button('Eliminar', on_click=delete_tool).classes('app-button app-delete-button')
    dialog.open()