# Tools UI components

from nicegui import ui
from mcp_open_client import state
from mcp_open_client.default_tools import DEFAULT_TOOLS
from .tool_components import render_default_tool, render_custom_tool
from .tool_actions import update_tools_list, add_new_tool, edit_tool
from .tool_components import confirm_delete_tool

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
            
            # Add New Tool button
            ui.button('Agregar nueva herramienta', icon='add', on_click=lambda: add_new_tool(default_tools_container, custom_tools_container)).classes('app-primary-button')
            
            # Container for the list of custom tools
            custom_tools_container = ui.column().classes('app-container')
        
        # Update tools list
        update_tools_list(default_tools_container, custom_tools_container)

def render_tools(default_tools_container, custom_tools_container):
    """Renders the list of tools in the UI"""
    default_tools_container.clear()
    custom_tools_container.clear()

    app_state = state.get_app_state()
    default_tool_ids = [tool['id'] for tool in DEFAULT_TOOLS]

    for tool in app_state['tools']:
        if tool['id'] in default_tool_ids:
            render_default_tool(tool, default_tools_container)
        else:
            render_custom_tool(tool, custom_tools_container,
                               lambda t=tool: edit_tool(t, default_tools_container, custom_tools_container),
                               lambda t_id=tool['id']: confirm_delete_tool(t_id, lambda: update_tools_list(default_tools_container, custom_tools_container)))

# Update the update_tools_list function in tool_actions.py to use this render_tools function