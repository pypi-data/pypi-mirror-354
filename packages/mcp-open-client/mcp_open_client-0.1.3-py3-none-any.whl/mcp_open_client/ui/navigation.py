# Navigation functionality

from nicegui import ui
from mcp_open_client.state import get_app_state
from mcp_open_client.ui.conversations import update_conversation_list

def render_content():
    """Renders the appropriate content based on the current page"""
    app_state = get_app_state()
    from mcp_open_client.state import core
    
    if not hasattr(core, 'content_container') or core.content_container is None:
        return
    
    core.content_container.clear()
    
    current_page = app_state['current_page']
    if current_page == 'chat':
        from mcp_open_client.ui.chat import render_chat_page
        render_chat_page(core.content_container)
    elif current_page == 'settings':
        from mcp_open_client.ui.settings import render_settings_page
        render_settings_page(core.content_container)
    elif current_page == 'tools':
        from mcp_open_client.ui.tools import render_tools_page
        render_tools_page(core.content_container)
    elif current_page == 'theme':
        from mcp_open_client.ui.theme import render_theme_page
        render_theme_page(core.content_container)

def change_page(page_name):
    """Changes the current page"""
    app_state = get_app_state()
    app_state['current_page'] = page_name
    render_content()
    ui.notify(f'Página cambiada a: {page_name}')
    
    # Directly update conversation list
    update_conversation_list()