# Main application entry point

import os
import sys
import argparse
from nicegui import ui

# Add the project root directory to Python path
project_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

# Import our modules
from mcp_open_client.state import initialize_state
from mcp_open_client.state.core import app_state
from mcp_open_client.state.settings import load_settings
from mcp_open_client.state.conversations import initialize_conversations, CONVERSATIONS_PATH
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the storage path for NiceGUI
NICEGUI_STORAGE_PATH = os.path.join(os.path.dirname(CONVERSATIONS_PATH), 'nicegui_storage')
from mcp_open_client.ui.layout import setup_ui
from mcp_open_client.ui.navigation import render_content
from mcp_open_client.ui.chat import render_chat_page
from mcp_open_client.ui.settings import render_settings_page
from mcp_open_client.ui.tools import render_tools_page
from mcp_open_client.ui.theme import render_theme_page, apply_theme
from mcp_open_client.default_tools import get_default_tools

# Global variable to track if the app has been set up
app_setup_done = False

def setup_app():
    """Setup the application"""
    global app_setup_done
    if app_setup_done:
        return
    
    # Load settings
    load_settings()
    logging.info("Settings loaded successfully")
    
    # Initialize all state components
    initialize_state()
    
    # Initialize conversations
    initialize_conversations()
    logging.info("Conversations initialized successfully")
    
    # Setup page configuration
    # Commented out favicon-related code until favicon files are available
    # app.add_static_files('/favicon', 'assets/favicon')
    ui.page_title('Claude Chat')
    # ui.add_head_html('<link rel="icon" href="/favicon/favicon.ico" sizes="any">')
    # ui.add_head_html('<link rel="apple-touch-icon" href="/favicon/apple-touch-icon.png">')
    
    # Add CSP meta tag to allow unsafe-eval for Pyodide
    ui.add_head_html('<meta http-equiv="Content-Security-Policy" content="script-src \'self\' \'unsafe-inline\' \'unsafe-eval\' https://cdn.jsdelivr.net;">')
    
    # Add default tools to app state if no tools are loaded
    if not app_state['tools']:
        app_state['tools'] = get_default_tools()
    else:
        # Merge default tools with loaded tools, avoiding duplicates
        default_tools = get_default_tools()
        existing_tool_names = {tool['name'] for tool in app_state['tools']}
        for tool in default_tools:
            if tool['name'] not in existing_tool_names:
                app_state['tools'].append(tool)
    
    # Initialize state if not already done
    if not app_state['initialized']:
        # Redirect to initialization page
        ui.navigate.to('/_init_storage')
    
    # Setup page routing
    @ui.page('/')
    def index_page():
        """Main application page"""
        # Setup the UI structure
        setup_ui()
        
        # Register page renderers
        app_state['page_renderers'] = {
            'chat': render_chat_page,
            'settings': render_settings_page,
            'tools': render_tools_page,
            'theme': render_theme_page
        }
        
        # Apply custom theme
        apply_theme()
        
        # Render initial content (default to chat page)
        if not app_state['current_page']:
            app_state['current_page'] = 'chat'
        
        render_content()

    app_setup_done = True

def main():
    """Main entry point for the application"""
    print("Starting main function")
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Claude Chat Application')
    parser.add_argument('--port', type=int, default=8082, help='Port to run the application on')
    args = parser.parse_args()
    
    # Change the working directory to the project root
    os.chdir(project_root)
    
    print("Setting up the application")
    # Setup the application
    setup_app()
    
    print("Running the application")
    # Run the application
    ui.run(
        title='MCP-open-client',
        favicon='assets/favicon.ico',  # Updated favicon path
        dark=True,
        reload=False,  # Changed to False to prevent reloading issues
        show=True,
        port=args.port,  # Use the port from command line arguments
        native=True,
        show_welcome_message=True,
        fullscreen=True,
        storage_secret='claude-chat-secret-key',  # Added for app.storage.user functionality
    )

    # Configure NiceGUI storage after ui.run
    from nicegui import app
    app.storage.default().set_storage_location(NICEGUI_STORAGE_PATH)
    print("Application run completed")

# Allow running the module directly, with -m flag, or when imported
if __name__ in {"__main__", "__mp_main__", "mcp_open_client.main"}:
    print(f"__name__ is {__name__}, calling main()")
    main()
else:
    print(f"__name__ is {__name__}, not calling main()")
    setup_app()  # Ensure the app is set up even when imported