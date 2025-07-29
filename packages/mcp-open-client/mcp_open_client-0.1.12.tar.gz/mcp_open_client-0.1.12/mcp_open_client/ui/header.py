# Header UI component

from nicegui import ui
from typing import Callable
from mcp_open_client.state import get_app_state, AppState

def create_header(left_drawer_toggle: Callable[[], None]) -> None:
    """Creates a clean header with the title 'MCP-open-client'"""
    with ui.header().classes('app-header mcp-header'):
        # Left section with menu button and logo
        with ui.row().classes('mcp-header-left'):
            ui.button(icon='menu', on_click=left_drawer_toggle).classes('mcp-menu-button')
            
            # Logo and title container
            with ui.row().classes('mcp-logo-container'):
                # Simple logo
                ui.icon('terminal').classes('mcp-logo-icon')
                
                # Title with tagline
                with ui.column().classes('mcp-title-container'):
                    ui.label('MCP-open-client').classes('mcp-header-title')
                    ui.label('Powerful AI Collaboration').classes('mcp-header-tagline')
        
        # Right section with controls
        with ui.row().classes('mcp-header-right'):
            # Status indicator
            with ui.element('div').classes('mcp-status-container'):
                ui.element('div').classes('mcp-status-dot')
                ui.label('Online').classes('mcp-status-text')
            
            # Buttons
            ui.button(icon='notifications', on_click=lambda: ui.notify('Notifications coming soon!')).classes('mcp-header-button')
            ui.button(icon='help_outline', on_click=lambda: ui.notify('Help center coming soon!')).classes('mcp-header-button')
            
            # Dark mode toggle
            with ui.row().classes('mcp-dark-mode-container'):
                ui.icon('dark_mode').classes('mcp-dark-mode-icon')
                
                def toggle_dark_mode() -> None:
                    value: bool = dark_switch.value
                    app_state: AppState = get_app_state()
                    app_state['settings']['dark_mode'] = value
                    ui.dark_mode().value = value
                    # Call save_settings without arguments
                    from mcp_open_client.state import settings
                    settings.save_settings()
                
                dark_switch: ui.switch = ui.switch('', value=get_app_state()['settings']['dark_mode']).classes('mcp-dark-switch')
                dark_switch.on('change', toggle_dark_mode)
    # Add CSS for the header with scroll elimination
    ui.add_head_html("""
    <style>
        /* Header styling - Updated for no-scroll flexbox layout */
        .mcp-header {
            background: #2b5876;
            color: white;
            padding: 1rem 1.5rem;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
            display: flex;
            justify-content: space-between;
            align-items: center;
            height: 64px;
            z-index: 100;
            width: 100%;
            flex-shrink: 0;
            overflow: hidden;
        }
        
        /* Header container styling for proper layout */
        .app-header {
            --header-height: 64px;
            height: var(--header-height) !important;
            flex-shrink: 0 !important;
            overflow: hidden !important;
        }
        
        /* Drawer positioning for no-scroll layout */
        .app-drawer {
            top: 0 !important;
            height: 100vh !important;
            overflow-y: auto !important;
            overflow-x: hidden !important;
        }
        
        .app-chat-container:empty {
            overflow: hidden;
        }
        
        .app-messages-container:empty {
            overflow: hidden;
        }
        
        /* Only show scrollbar when content overflows */
        .app-content-container {
            scrollbar-width: thin;
            scrollbar-color: rgba(0, 0, 0, 0.3) transparent;
        }
        
        .app-content-container::-webkit-scrollbar {
            width: 6px;
        }
        
        .app-content-container::-webkit-scrollbar-track {
            background: transparent;
        }
        
        .app-content-container::-webkit-scrollbar-thumb {
            background-color: rgba(0, 0, 0, 0.3);
            border-radius: 3px;
        }
        
        .app-content-container::-webkit-scrollbar-thumb:hover {
            background-color: rgba(0, 0, 0, 0.5);
        }
        
        /* Left section styling */
        .mcp-header-left {
            display: flex;
            align-items: center;
            gap: 1.2rem;
        }
        
        .mcp-menu-button {
            background: transparent !important;
            border: none !important;
            color: white !important;
            border-radius: 4px;
            padding: 8px 12px;
        }
        
        .mcp-menu-button:hover {
            background: rgba(255, 255, 255, 0.1) !important;
        }
        
        /* Logo container */
        .mcp-logo-container {
            display: flex;
            align-items: center;
            gap: 1.2rem;
            margin-left: 0.8rem;
        }
        
        .mcp-logo-icon {
            color: #64ffda;
            font-size: 1.5rem;
        }
        
        /* Title container with tagline */
        .mcp-title-container {
            display: flex;
            flex-direction: column;
            gap: 0.3rem;
        }
        
        .mcp-header-title {
            font-size: 1.5rem;
            font-weight: 700;
            letter-spacing: 0.5px;
            color: #ffffff;
            position: relative;
            margin: 0;
            padding: 0;
        }
        
        .mcp-header-tagline {
            font-size: 0.7rem;
            opacity: 0.7;
            letter-spacing: 0.5px;
            margin: 0;
            padding: 0;
        }
        
        /* Right section styling */
        .mcp-header-right {
            display: flex;
            align-items: center;
            gap: 1.5rem;
        }
        
        /* Status indicator */
        .mcp-status-container {
            display: flex;
            align-items: center;
            gap: 0.7rem;
            background: rgba(0, 0, 0, 0.2);
            padding: 6px 12px;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .mcp-status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: #4ade80;
        }
        
        .mcp-status-text {
            font-size: 0.7rem;
            font-weight: 500;
        }
        
        /* Version label styling */
        .mcp-version-label {
            font-size: 0.8rem;
            opacity: 0.7;
            padding: 2px 6px;
            border-radius: 4px;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
    </style>
    """)