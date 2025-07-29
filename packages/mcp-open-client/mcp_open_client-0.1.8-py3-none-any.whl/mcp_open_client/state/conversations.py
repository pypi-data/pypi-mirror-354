# Conversation management functions
import uuid
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from . import core

# Path for storing conversations
CONVERSATIONS_PATH = os.path.join(os.path.expanduser("~"), ".mcp-open-client", "conversations")

# Make sure these functions are available for import
__all__ = [
    'initialize_conversations', 'load_conversations', 'load_conversation', 'save_conversation',
    'create_new_conversation', 'create_conversation', 'set_current_conversation', 'delete_conversation',
    'update_conversation_title', 'select_conversation', 'get_current_conversation',
    'add_message_to_conversation', 'add_message', 'save_conversations_to_storage', 'load_conversations_from_storage'
]

def initialize_conversations() -> None:
    """Initialize conversations directory and load existing conversations"""
    # Create conversations directory if it doesn't exist
    try:
        os.makedirs(CONVERSATIONS_PATH, exist_ok=True)
    except OSError as e:
        print(f"Error creating conversations directory: {e}")
        return

    # Check if the directory is writable
    if not os.access(CONVERSATIONS_PATH, os.W_OK):
        print(f"Error: The conversations directory {CONVERSATIONS_PATH} is not writable.")
        return

    # Load existing conversations from files only during initialization
    # NiceGUI storage will be loaded later when in page context
    load_conversations()
    
    # Update the conversation list in the sidebar
    from mcp_open_client.ui.conversations import update_conversation_list
    update_conversation_list()

def load_conversations() -> None:
    """Load all conversations from the conversations directory"""
    core.app_state['conversations'] = []
    
    if not os.path.exists(CONVERSATIONS_PATH):
        return
    
    for filename in os.listdir(CONVERSATIONS_PATH):
        if filename.endswith('.json'):
            conversation_id = filename[:-5]  # Remove .json extension
            conversation = load_conversation(conversation_id)
            if conversation:
                core.app_state['conversations'].append(conversation)
    
    # Sort conversations by last_updated
    core.app_state['conversations'].sort(key=lambda x: x.get('last_updated', ''), reverse=True)

def load_conversation(conversation_id: str) -> Optional[Dict[str, Any]]:
    """Load a specific conversation by ID"""
    conversation_path = os.path.join(CONVERSATIONS_PATH, f"{conversation_id}.json")
    
    if not os.path.exists(conversation_path):
        return None
    
    try:
        with open(conversation_path, 'r', encoding='utf-8') as f:
            conversation: Dict[str, Any] = json.load(f)
            return conversation
    except Exception as e:
        print(f"Error loading conversation {conversation_id}: {e}")
        return None

def save_conversation(conversation_id: Optional[str] = None) -> None:
    """Save the current conversation"""
    if conversation_id is None:
        conversation_id = core.app_state['current_conversation_id']
    
    if conversation_id is None:
        return
    
    # Find the conversation in the list
    conversation: Optional[Dict[str, Any]] = None
    for conv in core.app_state['conversations']:
        if conv['id'] == conversation_id:
            conversation = conv
            break
    
    if conversation is None:
        return
    
    # Update the last_updated field
    conversation['last_updated'] = datetime.now().isoformat()
    
    # Save the conversation to a file
    conversation_path = os.path.join(CONVERSATIONS_PATH, f"{conversation_id}.json")
    
    try:
        with open(conversation_path, 'w', encoding='utf-8') as f:
            json.dump(conversation, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving conversation {conversation_id}: {e}")

def create_new_conversation() -> str:
    """Create a new conversation and set it as the current conversation"""
    # Generate a new conversation ID
    conversation_id = str(uuid.uuid4())
    
    # Create a new conversation object
    conversation: Dict[str, Any] = {
        'id': conversation_id,
        'name': 'New Conversation',
        'messages': [],
        'created_at': datetime.now().isoformat(),
        'last_updated': datetime.now().isoformat()
    }
    
    # Add the conversation to the list
    core.app_state['conversations'].append(conversation)
    
    # Set the current conversation ID
    core.app_state['current_conversation_id'] = conversation_id
    
    # Clear the messages
    core.app_state['messages'] = []
    
    # Save the conversation
    save_conversation(conversation_id)
    
    return conversation_id

def create_conversation(name: str) -> Optional[str]:
    """Create a new conversation"""
    if name.strip():
        # Generate a new conversation ID
        conversation_id = str(uuid.uuid4())
        
        # Create a new conversation object
        conversation: Dict[str, Any] = {
            'id': conversation_id,
            'name': name.strip(),
            'messages': [],
            'created_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat()
        }
        
        # Add the conversation to the list
        core.app_state['conversations'].append(conversation)
        
        # Set the current conversation ID
        core.app_state['current_conversation_id'] = conversation_id
        
        # Clear the messages
        core.app_state['messages'] = []
        
        # Save the conversation to file
        save_conversation(conversation_id)
        
        # Save to NiceGUI storage
        save_conversations_to_storage()
        
        # Update UI
        from mcp_open_client.ui.navigation import render_content
        render_content()
        
        from nicegui import ui
        ui.notify(f"Conversation '{name}' created")
        
        # Update the conversation list in the sidebar
        from mcp_open_client.ui.conversations import update_conversation_list
        update_conversation_list()
        
        return conversation_id
    return None

def set_current_conversation(conversation_id: str) -> None:
    """Set the current conversation and load its messages"""
    # Save the current conversation first
    if core.app_state['current_conversation_id']:
        save_conversation(core.app_state['current_conversation_id'])
    
    # Set the new conversation ID
    core.app_state['current_conversation_id'] = conversation_id
    
    # Load the conversation messages
    conversation = load_conversation(conversation_id)
    if conversation:
        core.app_state['messages'] = conversation.get('messages', [])
    else:
        core.app_state['messages'] = []

def delete_conversation(conversation_id: str) -> None:
    """Delete a conversation by ID"""
    # Remove the conversation from the list
    core.app_state['conversations'] = [
        conv for conv in core.app_state['conversations']
        if conv['id'] != conversation_id
    ]
    
    # If the deleted conversation was the current one, create a new conversation
    if core.app_state['current_conversation_id'] == conversation_id:
        create_new_conversation()
    
    # Delete the conversation file
    conversation_path = os.path.join(CONVERSATIONS_PATH, f"{conversation_id}.json")
    if os.path.exists(conversation_path):
        try:
            os.remove(conversation_path)
        except Exception as e:
            print(f"Error deleting conversation file {conversation_id}: {e}")
    
    # Save to NiceGUI storage
    save_conversations_to_storage()
    
    # Update the conversation list in the sidebar
    from mcp_open_client.ui.conversations import update_conversation_list
    update_conversation_list()
    
    # Trigger UI update to show the updated conversation list
    from mcp_open_client.ui.navigation import render_content
    render_content()
    
    # Show notification
    from nicegui import ui
    ui.notify("Conversation deleted")

def update_conversation_title(conversation_id: str, title: str) -> None:
    """Update the title of a conversation"""
    for conversation in core.app_state['conversations']:
        if conversation['id'] == conversation_id:
            conversation['name'] = title
            save_conversation(conversation_id)
            save_conversations_to_storage()
            break

def select_conversation(conversation_id: str) -> None:
    """Selects a conversation"""
    # Set the current conversation
    set_current_conversation(conversation_id)
    
    # Find the conversation and update the messages in the conversation object
    conversation = load_conversation(conversation_id)
    if conversation:
        # Update the conversation in the app_state list
        for i, conv in enumerate(core.app_state['conversations']):
            if conv['id'] == conversation_id:
                core.app_state['conversations'][i] = conversation
                break
    
    # Save to NiceGUI storage
    save_conversations_to_storage()
    
    # Trigger UI update to show the selected conversation
    from mcp_open_client.ui.navigation import render_content
    render_content()
    
    # Update the conversation list in the sidebar
    from mcp_open_client.ui.conversations import update_conversation_list
    update_conversation_list()
    
    from nicegui import ui
    ui.notify(f"Conversación seleccionada")

def get_current_conversation() -> Optional[Dict[str, Any]]:
    """Returns the current conversation"""
    current_conv_id = core.app_state['current_conversation_id']
    return next((conv for conv in core.app_state['conversations'] if conv['id'] == current_conv_id), None)

def add_message_to_conversation(conversation_id: str, message: Dict[str, Any]) -> None:
    """Add a message to a specific conversation"""
    conversation = load_conversation(conversation_id)
    if conversation:
        conversation['messages'].append(message)
        conversation['last_updated'] = datetime.now().isoformat()
        save_conversation(conversation_id)

def add_message(message: Dict[str, Any]) -> None:
    """Add a message to the current conversation"""
    current_conversation_id = core.app_state['current_conversation_id']
    if current_conversation_id:
        add_message_to_conversation(current_conversation_id, message)

def save_conversations_to_storage() -> None:
    """Save all conversations to storage"""
    try:
        from nicegui import app
        
        # Save conversations list to NiceGUI storage
        conversations_data = []
        for conv in core.app_state['conversations']:
            conversations_data.append({
                'id': conv['id'],
                'name': conv['name'],
                'created_at': conv['created_at'],
                'last_updated': conv['last_updated']
            })
        
        # Store in NiceGUI persistent storage
        app.storage.user['conversations'] = conversations_data
        app.storage.user['current_conversation_id'] = core.app_state['current_conversation_id']
        
        print(f"Saved {len(conversations_data)} conversations to storage")
        
    except Exception as e:
        print(f"Error saving conversations to storage: {e}")
        # Fallback: conversations are still saved to files via save_conversation()

def load_conversations_from_storage() -> None:
    """Load conversations from NiceGUI storage (must be called within page context)"""
    try:
        from nicegui import app
        
        # Check if we're in a page context
        if not hasattr(app, 'storage') or not hasattr(app.storage, 'user'):
            print("Not in page context, loading from files instead")
            load_conversations()
            return
        
        # Get conversations from NiceGUI storage
        stored_conversations = app.storage.user.get('conversations', [])
        stored_current_id = app.storage.user.get('current_conversation_id', None)
        
        if stored_conversations:
            print(f"Found {len(stored_conversations)} conversations in NiceGUI storage")
            
            # Load full conversations from files (storage only has metadata)
            loaded_conversations = []
            for stored_conv in stored_conversations:
                print(f"DEBUG: Attempting to load conversation {stored_conv['id']}")
                full_conv = load_conversation(stored_conv['id'])
                if full_conv:
                    print(f"DEBUG: Successfully loaded conversation {stored_conv['id']}")
                    loaded_conversations.append(full_conv)
                else:
                    print(f"DEBUG: Failed to load conversation {stored_conv['id']}")
            
            # Replace app_state conversations with loaded ones (no merge, no duplicates)
            core.app_state['conversations'] = loaded_conversations
            
            # Set current conversation if available
            if stored_current_id:
                core.app_state['current_conversation_id'] = stored_current_id
                print(f"DEBUG: Set current conversation ID to {stored_current_id}")
                
            # Sort conversations by last_updated
            core.app_state['conversations'].sort(key=lambda x: x.get('last_updated', ''), reverse=True)
            
            print(f"Loaded {len(core.app_state['conversations'])} conversations from storage")
            
            # Debug: Print loaded conversation IDs
            for conv in core.app_state['conversations']:
                print(f"DEBUG: Loaded conversation in app_state: {conv['id']} - {conv['name']}")
        else:
            print("No conversations found in NiceGUI storage, loading from files")
            # If no storage, load from files as fallback
            load_conversations()
            
    except Exception as e:
        print(f"Error loading conversations from storage: {e}")
        # Fallback to file-based loading
        load_conversations()
