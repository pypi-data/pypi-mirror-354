# Chat UI components and functionality

from nicegui import ui
from mcp_open_client.state import core as state_core
from mcp_open_client.state import get_app_state, get_current_conversation, add_message_to_conversation
from mcp_open_client.state import conversations
import json

def render_chat_page(container):
    """Renders the chat page"""
    # Clear previous content
    state_core.chat_container.clear()

    # Check if we have a current conversation
    app_state = get_app_state()
    current_conv = next((c for c in app_state['conversations']
                          if c['id'] == app_state['current_conversation_id']), None)
    
    if current_conv:
        with state_core.chat_container:
            # Display existing conversation
            ui.label(f"Conversación: {current_conv['name']}")
            
            # Chat messages container
            state_core.messages_container = ui.column().classes('app-messages-container')
            render_messages()
            
            # Loading spinner (hidden by default)
            state_core.loading_spinner = ui.spinner(size='lg').classes('app-loading-spinner').style('display: none')
            
            # Input area
            with ui.row().classes('app-chat-input-container'):
                state_core.chat_input = ui.input(placeholder='Escribe un mensaje...').classes('app-chat-input')
                
                # Add event handler for Enter key
                def on_enter(_):
                    send_message()
                
                state_core.chat_input.on('keydown.enter', on_enter)
                    
                state_core.send_button = ui.button('Enviar', icon='send', on_click=send_message).classes('app-send-button')
    else:
        # No conversation selected, show welcome screen
        with state_core.chat_container:
            with ui.column().classes('app-flex-column app-full-width app-center-content').style('margin-bottom: 0; padding-bottom: 0;'):
                ui.label('Bienvenido a Claude Chat').classes('text-h4 app-welcome-title')
                ui.button('Iniciar Nueva Conversación',
                         icon='add',
                         on_click=lambda: conversations.create_conversation("Nueva conversación")
                         ).classes('text-h6')

def render_messages():
    """Renders the messages in the current conversation"""
    if state_core.messages_container is None:
        return
    
    state_core.messages_container.clear()
    
    app_state = get_app_state()
    current_conv = next((c for c in app_state['conversations']
                        if c['id'] == app_state['current_conversation_id']), None)
    
    if current_conv:
        with state_core.messages_container:
            for message in current_conv['messages']:
                from mcp_open_client.ui.common import format_message
                format_message(message)

def send_message():
    """Sends a message to the API and updates the UI"""
    if state_core.chat_input is None or not state_core.chat_input.value.strip():
        return
    
    message_text = state_core.chat_input.value.strip()
    state_core.chat_input.value = ''
    
    # Add user message to conversation
    app_state = get_app_state()
    current_conv = next((c for c in app_state['conversations']
                        if c['id'] == app_state['current_conversation_id']), None)
    
    if current_conv:
        user_message = {'role': 'user', 'content': message_text}
        current_conv['messages'].append(user_message)
        
        # Save to user storage
        conversations.save_conversations_to_storage()
        
        render_messages()
        
        # Show loading spinner and disable input
        if hasattr(state_core, 'loading_spinner') and state_core.loading_spinner:
            state_core.loading_spinner.style('display: flex')
        if hasattr(state_core, 'chat_input') and state_core.chat_input:
            state_core.chat_input.disable()
        if hasattr(state_core, 'send_button') and state_core.send_button:
            state_core.send_button.disable()
        
        # Create message history for API
        # Add system prompt as the first message
        system_prompt = app_state['settings']['system_prompt']
        messages = [{'role': 'system', 'content': system_prompt}]
        
        # Add conversation messages with validation
        for m in current_conv['messages']:
            msg = {'role': m['role']}
            
            # Ensure content is never null
            msg['content'] = m.get('content', "")
            if msg['content'] is None:
                msg['content'] = ""
            
            # Add tool_calls if present
            if 'tool_calls' in m:
                msg['tool_calls'] = m['tool_calls']
            
            # Add name if present (for tool responses)
            if 'name' in m:
                msg['name'] = m['name']
                
            # Add tool_call_id if present (for tool responses)
            if 'tool_call_id' in m:
                msg['tool_call_id'] = m['tool_call_id']
            
            messages.append(msg)
        
        # Call API asynchronously
        async def get_response():
            try:
                # Get active tools
                active_tools = []
                for tool in app_state['tools']:
                    if tool.get('active', True):
                        # Parse parameters
                        if isinstance(tool["parameters"], str):
                            params = json.loads(tool["parameters"])
                        else:
                            params = tool["parameters"]
                        
                        # Ensure parameters has the required "type": "object" field
                        if "type" not in params:
                            params["type"] = "object"
                        
                        # Format tool according to OpenAI function calling format
                        active_tools.append({
                            "type": "function",
                            "function": {
                                "name": tool["name"],
                                "description": tool["description"],
                                "parameters": params
                            }
                        })
                
                # Check if API is initialized, if not try to initialize it
                from mcp_open_client.state import core, api as state_api
                if core.api is None:
                    print("API is None, trying to initialize it")
                    core.api = state_api.initialize_api()
                    
                    # If still None after initialization attempt, show error and return
                    if core.api is None:
                        ui.notify('Error: API not initialized. Please check your settings.', type='negative')
                        if hasattr(state_core, 'loading_spinner') and state_core.loading_spinner:
                            state_core.loading_spinner.style('display: none')
                        if hasattr(state_core, 'chat_input') and state_core.chat_input:
                            state_core.chat_input.enable()
                        if hasattr(state_core, 'send_button') and state_core.send_button:
                            state_core.send_button.enable()
                        return
                
                success, content, has_tool_calls = await core.api.send_message(
                    messages=messages,
                    model=app_state['settings']['model'],
                    temperature=app_state['settings']['temperature'],
                    max_tokens=app_state['settings']['max_tokens'],
                    tools=active_tools if active_tools else None
                )
                
                if success:
                    # Always add the assistant's response to the conversation
                    # For tool calls, this will be the final response after processing the tool results
                    assistant_message = {'role': 'assistant', 'content': content}
                    current_conv['messages'].append(assistant_message)
                    
                    # Save to user storage
                    conversations.save_conversations_to_storage()
                    
                    render_messages()
                    
                    # Scroll to bottom
                    if state_core.chat_container:
                        ui.run_javascript('''
                            setTimeout(() => {
                                const chatContainer = document.querySelector('.overflow-y-auto');
                                if (chatContainer) {
                                    chatContainer.scrollTop = chatContainer.scrollHeight;
                                }
                            }, 100);
                        ''')
                else:
                    ui.notify('Error al obtener respuesta', type='negative')
            finally:
                # Hide loading spinner and re-enable input
                if hasattr(state_core, 'loading_spinner') and state_core.loading_spinner:
                    state_core.loading_spinner.style('display: none')
                if hasattr(state_core, 'chat_input') and state_core.chat_input:
                    state_core.chat_input.enable()
                if hasattr(state_core, 'send_button') and state_core.send_button:
                    state_core.send_button.enable()
        
        ui.timer(0.5, get_response, once=True)