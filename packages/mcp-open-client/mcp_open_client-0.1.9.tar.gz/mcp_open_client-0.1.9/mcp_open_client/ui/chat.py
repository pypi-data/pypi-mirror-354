# Chat UI components and functionality

from nicegui import ui
from mcp_open_client.state import core as state_core
from mcp_open_client.state import get_app_state, get_current_conversation, add_message_to_conversation
from mcp_open_client.state import conversations
import json

def render_chat_page(container):
    """Renders the chat page with simple layout like settings page"""
    container.clear()
    
    # Set the chat container to the provided container
    state_core.chat_container = container

    # Check if we have a current conversation
    app_state = get_app_state()
    current_conv = next((c for c in app_state['conversations']
                          if c['id'] == app_state['current_conversation_id']), None)
    
    if current_conv:
        with container:
            # Page title
            ui.label('Chat').classes('app-page-title')
            ui.label(f"Conversación: {current_conv['name']}").classes('app-text-caption')
            
            ui.separator().classes('app-separator')
            
            # Messages card - this will contain all messages
            with ui.card().classes('app-card').style('width: 100%;'):
                ui.label('Mensajes').classes('app-card-title')
                
                # Messages container with scroll
                state_core.messages_container = ui.column().classes('app-container app-messages-container').style('flex: 1; overflow-y: auto; padding: 16px; width: 100%; min-height: 0;')
                
                # Load existing messages
                render_messages()
                
                # Loading spinner (hidden by default)
                state_core.loading_spinner = ui.spinner(size='lg').classes('app-loading-spinner').style('display: none; margin: 16px auto;')
            
            # Input card - separate card for input
            with ui.card().classes('app-card').style('width: 100%;'):
                with ui.row().classes('app-container').style('width: 100%; gap: 12px; align-items: flex-end; display: flex;'):
                    # Chat input - takes most of the space
                    chat_input = ui.textarea(
                        placeholder='Escribe tu mensaje aquí...',
                        value=''
                    ).classes('app-textarea').style('flex: 1; min-height: 40px; max-height: 120px;')
                    
                    state_core.chat_input = chat_input
                    
                    # Send button - fixed width
                    send_button = ui.button(
                        'Enviar',
                        icon='send',
                        on_click=send_message
                    ).classes('app-primary-button').style('flex-shrink: 0; height: 36px; min-width: 100px; align-self: flex-end;')
                    state_core.send_button = send_button
                
                # Handle Enter key (Enter or Ctrl+Enter to send)
                def handle_keydown(e):
                    if e.args.get('key') == 'Enter':
                        # Prevent default behavior (new line) and send message
                        send_message()
                
                chat_input.on('keydown', handle_keydown)
    else:
        # No conversation selected, show welcome screen
        with container:
            ui.label('Chat').classes('app-page-title')
            ui.separator().classes('app-separator')
            
            with ui.card().classes('app-card'):
                with ui.column().classes('app-container').style('text-align: center; padding: 40px;'):
                    ui.label('Bienvenido a Claude Chat').classes('text-h4')
                    ui.label('Selecciona una conversación o crea una nueva para comenzar').classes('app-text-caption')
                    ui.button('Iniciar Nueva Conversación',
                             icon='add',
                             on_click=lambda: conversations.create_conversation("Nueva conversación")
                             ).classes('app-primary-button').style('margin-top: 20px;')

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
                from mcp_open_client.ui.message_formatting import format_message
                format_message(message)
        
        # Auto-scroll to bottom after rendering messages
        ui.run_javascript("""
            setTimeout(() => {
                const messagesContainer = document.querySelector('.app-messages-container');
                if (messagesContainer) {
                    messagesContainer.scrollTop = messagesContainer.scrollHeight;
                }
            }, 100);
        """)

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
                                const messagesContainer = document.querySelector('.app-messages-container');
                                if (messagesContainer) {
                                    messagesContainer.scrollTop = messagesContainer.scrollHeight;
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