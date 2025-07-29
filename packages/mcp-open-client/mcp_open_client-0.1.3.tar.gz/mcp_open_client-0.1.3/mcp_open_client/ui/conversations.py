# Conversation management UI components

from nicegui import ui
from mcp_open_client import state
from mcp_open_client.state import get_app_state

# Global reference to the conversations container
conversations_container = None

def update_conversation_list():
    """Updates the conversation list in the sidebar"""
    global conversations_container
    if conversations_container is None:
        return
        
    conversations_container.clear()
    
    app_state = get_app_state()
    with conversations_container:
        for conv in app_state['conversations']:
            with ui.row().classes('app-flex-row app-full-width app-space-between app-nowrap'):
                # Truncate long conversation names
                display_name = conv['name']
                if len(display_name) > 15:
                    display_name = display_name[:12] + '...'
                    
                # Highlight current conversation
                btn_classes = 'app-conversation-button'
                if conv['id'] == app_state['current_conversation_id']:
                    btn_classes += ' app-active-conversation'
                    
                ui.button(display_name,
                         on_click=lambda c=conv['id']: state.select_conversation(c)
                         ).classes(btn_classes)
                
                # Delete button - positioned next to conversation name
                ui.button(icon='delete',
                         on_click=lambda c=conv['id']: state.delete_conversation(c)
                         ).classes('app-delete-button')