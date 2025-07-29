# Footer UI component

from nicegui import ui
from mcp_open_client import state

def create_footer():
    """Creates a clean footer that complements the header"""
    with ui.footer().classes('app-footer mcp-footer'):
        # Left section with copyright and version
        with ui.row().classes('mcp-footer-left'):
            ui.label('© 2025 MCP-open-client').classes('mcp-footer-copyright')
            ui.element('div').classes('mcp-footer-spacer')
            ui.label('v1.0.0').classes('mcp-footer-version')
        
        # Center section with links
        with ui.row().classes('mcp-footer-center'):
            ui.link('Documentación', 'https://github.com/your-repo/docs').classes('mcp-footer-link')
            ui.element('div').classes('mcp-footer-dot')
            ui.link('GitHub', 'https://github.com/your-repo').classes('mcp-footer-link')
            ui.element('div').classes('mcp-footer-dot')
            ui.link('Soporte', 'mailto:support@example.com').classes('mcp-footer-link')
        
        # Right section with social links
        with ui.row().classes('mcp-footer-right'):
            ui.button(icon='code', on_click=lambda: ui.open('https://github.com/your-repo')).classes('mcp-footer-button')
            ui.button(icon='mail', on_click=lambda: ui.open('mailto:contact@example.com')).classes('mcp-footer-button')
            ui.button(icon='help', on_click=lambda: ui.notify('Centro de ayuda próximamente')).classes('mcp-footer-button')

    # Add CSS for the footer
    ui.add_head_html("""
    <style>
        /* Footer styling */
        .mcp-footer {
            background: #2b5876;
            color: white;
            padding: 1rem 1.5rem;
            box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.2);
            display: flex;
            justify-content: space-between;
            align-items: center;
            height: 60px;
            z-index: 100;
            width: 100%;
            position: fixed;
            bottom: 0;
            left: 0;
            margin-top: 0;
        }
        
        /* Ensure content doesn't get hidden behind the footer */
        .app-content-container {
            padding-bottom: 60px !important;
        }
        
        /* Footer spacing only */
        .app-footer {
            /* Footer styles remain unchanged */
        }
        
        /* Left section styling */
        .mcp-footer-left {
            display: flex;
            align-items: center;
            gap: 0.8rem;
        }
        
        .mcp-footer-copyright {
            font-size: 0.8rem;
            opacity: 0.8;
            margin: 0;
            padding: 0;
        }
        
        .mcp-footer-version {
            font-size: 0.7rem;
            opacity: 0.7;
            padding: 2px 6px;
            border-radius: 4px;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        .mcp-footer-spacer {
            width: 0.5rem;
        }
        
        /* Center section styling */
        .mcp-footer-center {
            display: flex;
            align-items: center;
            gap: 0.8rem;
        }
        
        .mcp-footer-link {
            font-size: 0.8rem;
            color: white !important;
            opacity: 0.8;
            text-decoration: none !important;
            transition: opacity 0.2s;
        }
        
        .mcp-footer-link:hover {
            opacity: 1;
            text-decoration: underline !important;
        }
        
        .mcp-footer-dot {
            width: 4px;
            height: 4px;
            border-radius: 50%;
            background-color: rgba(255, 255, 255, 0.5);
        }
        
        /* Right section styling */
        .mcp-footer-right {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .mcp-footer-button {
            background: transparent !important;
            border: none !important;
            color: white !important;
            width: 32px;
            height: 32px;
            border-radius: 4px;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .mcp-footer-button:hover {
            background: rgba(255, 255, 255, 0.1) !important;
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .mcp-footer-center {
                display: none;
            }
        }
        
        @media (max-width: 480px) {
            .mcp-footer-version {
                display: none;
            }
            
            .mcp-footer-copyright {
                font-size: 0.7rem;
            }
        }
        
        /* Dark mode specific adjustments */
        .dark .mcp-footer {
            background: #1a1a2e;
        }
    </style>
    """)