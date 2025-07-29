# Common UI components and functions
# This file is maintained for backward compatibility
# The functionality has been refactored into separate modules:
# - layout.py: UI layout components (setup_ui, create_sidebar)
# - header.py: Header component (create_header)
# - navigation.py: Page navigation functionality (render_content, change_page)
# - conversations.py: Conversation list management (update_conversation_list)
# - message_formatting.py: Message parsing and display (parse_message_content, format_message)

# Re-export all functions from the refactored modules
from mcp_open_client.ui.layout import setup_ui, create_sidebar
from mcp_open_client.ui.navigation import render_content, change_page
from mcp_open_client.ui.conversations import update_conversation_list, conversations_container
from mcp_open_client.ui.message_formatting import parse_message_content, format_message
from mcp_open_client.ui.header import create_header

# For backward compatibility, ensure that any code that imports from common.py
# will continue to work without changes