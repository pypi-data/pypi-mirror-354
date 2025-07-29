# UI layout components

from nicegui import ui
from mcp_open_client.state import get_app_state
from mcp_open_client.state import conversations as state_conversations
from mcp_open_client.state import core as state_core
from mcp_open_client.ui.navigation import change_page
from mcp_open_client.ui.conversations import conversations_container, update_conversation_list
from mcp_open_client.ui.header import create_header
from mcp_open_client.ui.footer import create_footer

def setup_ui():
    """Sets up the main UI structure"""
    # Create drawer (must be a direct child of the page)
    drawer = ui.left_drawer(value=False).classes('app-drawer')
    
    # Create a function to toggle the drawer
    def toggle_drawer():
        drawer.toggle()
    
    # Create header (must be a direct child of the page)
    create_header(toggle_drawer)
    
    # Create main container (direct child of the page)
    with ui.column().classes('app-main-container flex-grow flex flex-col'):
        # Create content container
        state_core.content_container = ui.column().classes('app-content-container flex-grow overflow-auto')
        
        # Create chat container inside content container
        with state_core.content_container:
            state_core.chat_container = ui.column().classes('app-chat-container')
    
    # Create sidebar (must be a direct child of the page)
    create_sidebar(drawer)
    
    # Create footer (must be a direct child of the page)
    create_footer()

def create_sidebar(drawer):
    """Creates the sidebar navigation"""
    # Add content to the drawer
    with drawer:
        ui.label('Claude Chat').classes('app-drawer-title')
        ui.separator()
        
        with ui.column().classes('app-drawer-menu'):
            ui.button('Chat', icon='chat', on_click=lambda: change_page('chat')).classes('app-menu-button')
            ui.button('Configuración', icon='settings', on_click=lambda: change_page('settings')).classes('app-menu-button')
            ui.button('Herramientas', icon='build', on_click=lambda: change_page('tools')).classes('app-menu-button')
            ui.button('Tema', icon='brush', on_click=lambda: change_page('theme')).classes('app-menu-button')
            
            ui.separator()
            
            # Conversations section
            ui.label('Conversaciones').classes('app-section-title')
            
            # Button to create a new conversation
            def create_new_conversation():
                app_state = get_app_state()
                new_name = f"Conversación {len(app_state['conversations']) + 1}"
                state_conversations.create_conversation(new_name)
                update_conversation_list()
                
            ui.button('Nueva conversación', icon='add', on_click=create_new_conversation).classes('app-new-conversation-button')
            
            # List of conversations
            global conversations_container
            conversations_container = ui.column().classes('app-conversations-container')
            
            # Initial update of conversation list
            update_conversation_list()