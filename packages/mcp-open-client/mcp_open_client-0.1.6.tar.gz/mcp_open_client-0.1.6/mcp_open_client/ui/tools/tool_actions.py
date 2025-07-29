from nicegui import ui
from mcp_open_client import state
from mcp_open_client.default_tools import DEFAULT_TOOLS
from .tool_components import render_default_tool, render_custom_tool
from .tool_dialogs import open_add_tool_dialog, open_edit_tool_dialog

def update_tools_list(default_tools_container, custom_tools_container):
    from .tools_page import render_tools  # Import here to avoid circular import
    render_tools(default_tools_container, custom_tools_container)

def add_new_tool(default_tools_container, custom_tools_container):
    open_add_tool_dialog(lambda: update_tools_list(default_tools_container, custom_tools_container))

def edit_tool(tool, default_tools_container, custom_tools_container):
    open_edit_tool_dialog(tool, lambda: update_tools_list(default_tools_container, custom_tools_container))

def confirm_delete_tool(tool_id, default_tools_container, custom_tools_container):
    def delete_tool_and_update():
        if state.delete_tool(tool_id):
            update_tools_list(default_tools_container, custom_tools_container)
            ui.notify('Herramienta eliminada correctamente', type='positive')
        else:
            ui.notify('Error al eliminar la herramienta', type='negative')
        dialog.close()

    with ui.dialog() as dialog, ui.card().classes('app-dialog-card'):
        ui.label('Confirmar eliminación').classes('app-dialog-title')
        ui.label('¿Estás seguro de que deseas eliminar esta herramienta? Esta acción no se puede deshacer.').classes('app-dialog-text')
        
        with ui.row().classes('app-dialog-actions'):
            ui.button('Cancelar', on_click=dialog.close).classes('app-button app-cancel-button')
            ui.button('Eliminar', on_click=delete_tool_and_update).classes('app-button app-delete-button')
    
    dialog.open()