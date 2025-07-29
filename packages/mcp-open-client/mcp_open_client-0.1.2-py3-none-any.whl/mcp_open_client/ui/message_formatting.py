# Message parsing and formatting

from nicegui import ui
import json
import re

def parse_message_content(content):
    """
    Parses message content to identify code blocks and other markdown elements.
    Returns a list of content blocks with their type and content.
    """
    # Ensure content is a string
    if not content or not isinstance(content, str):
        return [{'type': 'text', 'content': "Usando herramientas..."}]
    
    # Regex to match code blocks with language specification
    # Format: ```language\ncode\n```
    code_block_pattern = r'```(\w*)\n([\s\S]*?)\n```'
    
    try:
        blocks = []
        last_end = 0
        
        # Find all code blocks
        for match in re.finditer(code_block_pattern, content):
            # Add text before the code block
            if match.start() > last_end:
                text_content = content[last_end:match.start()]
                if text_content.strip():
                    blocks.append({'type': 'text', 'content': text_content})
            
            # Add the code block
            language = match.group(1) or 'python'  # Default to python if no language specified
            code = match.group(2)
            blocks.append({'type': 'code', 'content': code, 'language': language})
            
            last_end = match.end()
        
        # Add remaining text after the last code block
        if last_end < len(content):
            blocks.append({'type': 'text', 'content': content[last_end:]})
        
        # If no code blocks were found, treat the entire content as markdown
        if not blocks:
            blocks.append({'type': 'text', 'content': content})
        
        return blocks
    except Exception as e:
        # If any error occurs during parsing, return a safe fallback
        print(f"Error parsing message content: {e}")
        return [{'type': 'text', 'content': content}]

def format_message(message):
    """Formats a message for display"""
    is_user = message['role'] == 'user'
    is_tool = message['role'] == 'tool'
    
    # Handle tool calls
    if 'tool_calls' in message and message['tool_calls']:
        # Display the tool call message
        with ui.card().classes('app-card app-tool-call-card'):
            ui.label('Claude está usando una herramienta:').classes('app-text-bold')
            
            for tool_call in message['tool_calls']:
                ui.label(f"Herramienta: {tool_call['function']['name']}").classes('app-margin-left-md')
                
                # Parse the arguments JSON string
                try:
                    args = json.loads(tool_call['function']['arguments'])
                    formatted_args = json.dumps(args, indent=2, ensure_ascii=False)
                except:
                    formatted_args = tool_call['function']['arguments']
                    
                ui.label(f"Argumentos: {formatted_args}").classes('app-margin-left-md app-text-break-all app-whitespace-pre-wrap')
        return
    
    # Handle tool responses
    if is_tool:
        with ui.card().classes('app-card app-tool-response-card'):
            ui.label(f"Respuesta de herramienta: {message['name']}").classes('app-text-bold')
            ui.label(message['content']).classes('app-margin-left-md app-text-break-all app-whitespace-pre-wrap')
        return
    
    # Handle regular messages with enhanced rendering
    content = message.get('content') or "Usando herramientas..."
    
    # Parse the message content into blocks
    blocks = parse_message_content(content)
    
    # For simple text messages without code blocks, use the standard chat_message
    if len(blocks) == 1 and blocks[0]['type'] == 'text':
        ui.chat_message(
            name='Tú' if is_user else 'Claude',
            sent=is_user,
            text=blocks[0]['content']
        ).classes('app-message app-full-width')
    else:
        # For messages with code blocks or multiple blocks, use the context manager approach
        with ui.chat_message(
            name='Tú' if is_user else 'Claude',
            sent=is_user,
            text=""  # Empty text, we'll add content inside
        ).classes('app-message app-full-width'):
            # Render each block with appropriate component
            for block in blocks:
                if block['type'] == 'code':
                    ui.code(
                        content=block['content'],
                        language=block['language']
                    ).classes('app-code-block')
                else:
                    ui.markdown(
                        block['content'],
                        extras=['fenced-code-blocks', 'tables', 'mermaid']
                    ).classes('app-markdown-block')