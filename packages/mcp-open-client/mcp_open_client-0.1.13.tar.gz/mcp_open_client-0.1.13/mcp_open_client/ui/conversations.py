# Conversation management UI components

from nicegui import ui
from mcp_open_client import state
from mcp_open_client.state import get_app_state
from mcp_open_client.state import core as state_core

def update_conversation_list():
    """Updates the conversation list in the sidebar"""
    print("DEBUG: update_conversation_list() called")
    
    if state_core.conversations_container is None:
        print("DEBUG: conversations_container is None!")
        return
        
    print("DEBUG: Clearing conversations_container")
    state_core.conversations_container.clear()
    
    app_state = get_app_state()
    print(f"DEBUG: App state has {len(app_state['conversations'])} conversations in update_conversation_list")
    
    with state_core.conversations_container:
        for conv in app_state['conversations']:
            print(f"DEBUG: Rendering conversation: {conv['id']} - {conv['name']}")
            with ui.row().classes('app-flex-row app-full-width app-space-between app-nowrap'):
                # Truncate long conversation names
                display_name = conv['name']
                if len(display_name) > 15:
                    display_name = display_name[:12] + '...'
                    
                print(f"DEBUG: Display name: {display_name}")
                    
                # Highlight current conversation
                btn_classes = 'app-conversation-button'
                if conv['id'] == app_state['current_conversation_id']:
                    btn_classes += ' app-active-conversation'
                    
                print(f"DEBUG: Creating button with classes: {btn_classes}")
                ui.button(display_name,
                         on_click=lambda _=None, c=conv['id']: state.select_conversation(c)
                         ).classes(btn_classes)
                
                # Delete button - positioned next to conversation name
                print(f"DEBUG: Creating delete button")
                ui.button(icon='delete',
                         on_click=lambda _=None, c=conv['id']: state.delete_conversation(c)
                         ).classes('app-delete-button')
        
        print(f"DEBUG: Finished rendering {len(app_state['conversations'])} conversations")