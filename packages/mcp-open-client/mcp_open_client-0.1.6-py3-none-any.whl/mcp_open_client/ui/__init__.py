# UI package initialization

# Re-export functions from the refactored modules to maintain backward compatibility
from mcp_open_client.ui.layout import setup_ui, create_sidebar
from mcp_open_client.ui.navigation import render_content, change_page
from mcp_open_client.ui.conversations import update_conversation_list, conversations_container
from mcp_open_client.ui.message_formatting import parse_message_content, format_message