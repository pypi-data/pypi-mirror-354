# Main application entry point

import argparse
import logging
import os
import sys

from nicegui import ui

# Import our modules
from mcp_open_client.state import initialize_state
from mcp_open_client.state.core import app_state
from mcp_open_client.state.settings import load_settings
from mcp_open_client.state.conversations import initialize_conversations, CONVERSATIONS_PATH

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Add the project root directory to Python path
project_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

# Define the storage path for NiceGUI
NICEGUI_STORAGE_PATH = os.path.join(os.path.dirname(CONVERSATIONS_PATH), 'nicegui_storage')

from mcp_open_client.ui.layout import setup_ui
from mcp_open_client.ui.navigation import render_content
from mcp_open_client.ui.chat import render_chat_page  # type: ignore[import]
from mcp_open_client.ui.settings import render_settings_page  # type: ignore[import]
from mcp_open_client.ui.tools.tools_page import render_tools_page  # type: ignore[import]
from mcp_open_client.ui.theme import render_theme_page, apply_theme  # type: ignore[import]
from mcp_open_client.default_tools import get_default_tools  # type: ignore[import]

# Global variable to track if the app has been set up
app_setup_done: bool = False

def setup_app() -> None:
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
        default_tools = get_default_tools()  # type: ignore
        existing_tool_names = {tool['name'] for tool in app_state['tools']}
        for tool in default_tools:  # type: ignore
            if tool['name'] not in existing_tool_names:
                app_state['tools'].append(tool)  # type: ignore
    
    # Initialize state if not already done
    if not app_state['initialized']:
        # Redirect to initialization page
        ui.navigate.to('/_init_storage')
    
    # Setup page routing
    @ui.page('/')
    def index_page() -> None:  # type: ignore
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

def main() -> None:
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
    try:
        ui.run(
            title='MCP-open-client',
            favicon='assets/favicon.ico',  # Updated favicon path
            dark=True,
            reload=False,  # Changed to False to prevent reloading issues
            show=False,
            port=args.port,  # Use the port from command line arguments
            show_welcome_message=False,
            fullscreen=False,
            storage_secret='claude-chat-secret-key',  # Enables persistent storage
        )
    except OSError as e:
        if e.errno == 10048:  # Address already in use
            print(f"Error: Port {args.port} is already in use. Try using a different port.")
            print("You can specify a different port using the --port argument.")
            print("Example: python -m mcp_open_client.main --port 8083")
        else:
            print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    print("Application run completed")

# Allow running the module directly, with -m flag, or when imported
if __name__ in {"__main__", "__mp_main__", "mcp_open_client.main"}:
    print(f"__name__ is {__name__}, calling main()")
    main()
else:
    print(f"__name__ is {__name__}, not calling main()")
    setup_app()  # Ensure the app is set up even when imported