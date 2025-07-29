# Conversation management functions
import uuid
import json
import os
from datetime import datetime
from . import core

# Path for storing conversations
CONVERSATIONS_PATH = os.path.join(os.path.expanduser("~"), ".mcp-open-client", "conversations")

# Make sure these functions are available for import
__all__ = [
    'initialize_conversations', 'load_conversations', 'load_conversation', 'save_conversation',
    'create_new_conversation', 'create_conversation', 'set_current_conversation', 'delete_conversation',
    'update_conversation_title', 'select_conversation', 'get_current_conversation', 'add_message_to_conversation',
    'add_message'
]

def initialize_conversations():
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

    # Load existing conversations
    load_conversations()
    
    # Update the conversation list in the sidebar
    from mcp_open_client.ui.conversations import update_conversation_list
    update_conversation_list()

def load_conversations():
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

def load_conversation(conversation_id):
    """Load a specific conversation by ID"""
    conversation_path = os.path.join(CONVERSATIONS_PATH, f"{conversation_id}.json")
    
    if not os.path.exists(conversation_path):
        return None
    
    try:
        with open(conversation_path, 'r', encoding='utf-8') as f:
            conversation = json.load(f)
            return conversation
    except Exception as e:
        print(f"Error loading conversation {conversation_id}: {e}")
        return None

def save_conversation(conversation_id=None):
    """Save the current conversation"""
    if conversation_id is None:
        conversation_id = core.app_state['current_conversation_id']
    
    if conversation_id is None:
        return
    
    # Find the conversation in the list
    conversation = None
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

def create_new_conversation():
    """Create a new conversation and set it as the current conversation"""
    # Generate a new conversation ID
    conversation_id = str(uuid.uuid4())
    
    # Create a new conversation object
    conversation = {
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

def create_conversation(name):
    """Crea una nueva conversación"""
    if name.strip():
        # Generate a new conversation ID
        conversation_id = str(uuid.uuid4())
        
        # Create a new conversation object
        conversation = {
            'id': conversation_id,
            'name': name.strip(),
            'messages': []
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
        ui.notify(f"Conversación '{name}' creada")
        
        # Update the conversation list in the sidebar
        from mcp_open_client.ui.conversations import update_conversation_list
        update_conversation_list()
        
        return conversation_id
    return None

def set_current_conversation(conversation_id):
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

def delete_conversation(conversation_id):
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

def update_conversation_title(conversation_id, title):
    """Update the title of a conversation"""
    for conversation in core.app_state['conversations']:
        if conversation['id'] == conversation_id:
            conversation['name'] = title
            save_conversation(conversation_id)
            save_conversations_to_storage()
            break

def select_conversation(conversation_id):
    """Selects a conversation"""
    # Set the current conversation
    set_current_conversation(conversation_id)
    
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

def get_current_conversation():
    """Returns the current conversation"""
    current_conv_id = core.app_state['current_conversation_id']
    return next((conv for conv in core.app_state['conversations'] if conv['id'] == current_conv_id), None)

def add_message_to_conversation(conversation_id, message):
    """Adds a message to the specified conversation"""
    for conv in core.app_state['conversations']:
        if conv['id'] == conversation_id:
            conv['messages'].append(message)
            save_conversation(conversation_id)
            break

def add_message(role, content):
    """Add a message to the current conversation"""
    message = {
        'role': role,
        'content': content,
        'timestamp': datetime.now().isoformat()
    }
    
    core.app_state['messages'].append(message)
    
    # Update the conversation messages
    if core.app_state['current_conversation_id']:
        for conversation in core.app_state['conversations']:
            if conversation['id'] == core.app_state['current_conversation_id']:
                conversation['messages'] = core.app_state['messages']
                save_conversation()
                save_conversations_to_storage()
                break

def save_conversations_to_storage():
    """Saves the current conversations to user storage"""
    from nicegui import app
    try:
        # Make sure we're only saving what we need to avoid large storage
        simplified_conversations = []
        for conv in core.app_state['conversations']:
            simplified_conversations.append({
                'id': conv['id'],
                'name': conv['name'],
                'messages': conv['messages']
            })
        
        # Save to user storage
        app.storage.user['conversations'] = simplified_conversations
        app.storage.user['current_conversation_id'] = core.app_state['current_conversation_id']
        app.storage.user['tools'] = core.app_state['tools']  # Save tools to storage
        return True
    except Exception as e:
        from nicegui import ui
        ui.notify(f"Error al guardar conversaciones: {str(e)}", type='negative')
        return False

def load_conversations_from_storage():
    """Loads conversations from user storage"""
    from nicegui import app
    try:
        if 'conversations' in app.storage.user:
            core.app_state['conversations'] = app.storage.user['conversations']
            if 'current_conversation_id' in app.storage.user:
                core.app_state['current_conversation_id'] = app.storage.user['current_conversation_id']
            if 'tools' in app.storage.user:
                core.app_state['tools'] = app.storage.user['tools']
            return True
        return False
    except Exception as e:
        from nicegui import ui
        ui.notify(f"Error al cargar conversaciones: {str(e)}", type='negative')
        return False