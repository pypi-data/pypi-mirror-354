# Header UI component

from nicegui import ui
from mcp_open_client.state import get_app_state

def create_header(left_drawer_toggle):
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
                dark_switch = ui.switch('', value=get_app_state()['settings']['dark_mode']).classes('mcp-dark-switch')
            
            @dark_switch.on_value_change
            def toggle_dark_mode():
                value = dark_switch.value
                app_state = get_app_state()
                app_state['settings']['dark_mode'] = value
                ui.dark_mode().value = value
                # We need to update the save_settings function call
                from mcp_open_client.state import settings
                settings.save_settings(app_state)

    # Add simplified CSS for the header
    ui.add_head_html("""
    <style>
        /* Header styling */
        .mcp-header {
            background: #2b5876;
            color: white;
            padding: 1.5rem 1.5rem 1.5rem 1.5rem;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
            display: flex;
            justify-content: space-between;
            align-items: center;
            height: 90px;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 100;
            width: 100%;
            margin-bottom: 15px;
        }
        
        /* Layout adjustments for fixed header */
        body {
            overflow-y: hidden;
            height: 100vh;
            margin: 0;
            padding: 0;
        }
        
        .q-page {
            height: calc(100vh - 90px);
            overflow-y: auto;
            padding-top: 105px;
        }
        
        .app-drawer {
            top: 90px !important;
            height: calc(100vh - 90px) !important;
        }
        
        .app-content-container {
            margin-top: 15px !important;
            padding-top: 15px !important;
            height: calc(100vh - 90px);
            overflow-y: auto;
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
        
        .mcp-header-spacer {
            width: 1rem;
        }
        
        /* Interactive header buttons */
        .mcp-header-button {
            background: transparent !important;
            border: none !important;
            color: white !important;
            width: 36px;
            height: 36px;
            border-radius: 4px;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .mcp-header-button:hover {
            background: rgba(255, 255, 255, 0.1) !important;
        }
        
        /* Dark mode toggle styling */
        .mcp-dark-mode-container {
            display: flex;
            align-items: center;
            gap: 0.7rem;
            background: rgba(0, 0, 0, 0.2);
            padding: 6px 14px;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .mcp-dark-mode-container:hover {
            background: rgba(0, 0, 0, 0.3);
        }
        
        .mcp-dark-mode-icon {
            color: #64ffda;
            font-size: 1.2rem;
        }
        
        .mcp-dark-switch .q-toggle__inner {
            color: #64ffda !important;
        }
        
        /* Responsive adjustments */
        @media (max-width: 600px) {
            .mcp-version-label {
                display: none;
            }
            
            .mcp-header-title {
                font-size: 1.2rem;
            }
            
            .mcp-header-tagline {
                display: none;
            }
        }
        
        /* Dark mode specific adjustments */
        .dark .mcp-header {
            background: #1a1a2e;
        }
        
        .dark .mcp-dark-mode-container {
            background: rgba(255, 255, 255, 0.1);
        }
    </style>
    """)