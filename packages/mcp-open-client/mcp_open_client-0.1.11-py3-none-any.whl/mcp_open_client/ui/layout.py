# UI layout components

from typing import Dict, Any, Callable
from nicegui import ui
# Removed direct import of Drawer
from mcp_open_client.state import conversations as state_conversations, core as state_core
from mcp_open_client.ui.navigation import change_page  # type: ignore
from mcp_open_client.ui.conversations import update_conversation_list
from mcp_open_client.ui.header import create_header  # type: ignore
from mcp_open_client.ui.footer import create_footer

# Type aliases
PageName = str
DrawerToggle = Callable[[], None]

# Type-safe wrappers
def change_page_wrapper(page_name: str) -> None:
    change_page(page_name)

def create_header_wrapper(left_drawer_toggle: DrawerToggle) -> None:
    create_header(left_drawer_toggle)

def setup_ui() -> None:
    """Sets up the main UI structure with proper height management"""
    
    # Create drawer (must be a direct child of the page)
    drawer: Any = ui.drawer(side='left', value=False).classes('app-drawer')
    
    # Create a function to toggle the drawer
    def toggle_drawer() -> None:
        """Toggle the visibility of the drawer."""
        drawer.toggle()  # type: ignore
    
    # Create header (must be a direct child of the page)
    create_header_wrapper(toggle_drawer)
    
    # Create main container that takes remaining space (direct child of the page)
    with ui.column().classes('app-main-container h-full flex flex-col'):
        # Create content container with proper height management - this will be used directly for chat
        state_core.content_container = ui.column().classes('app-content-container flex-grow overflow-auto min-h-0')
        
        # Set chat container to be the same as content container (no extra nesting)
        state_core.chat_container = state_core.content_container
    
    # Create footer (must be a direct child of the page)
    create_footer()
    
    # Create sidebar (must be a direct child of the page)
    create_sidebar(drawer)

def create_sidebar(drawer: Any) -> None:
    """
    Creates the sidebar navigation.

    Args:
        drawer (Drawer): The drawer element to populate with sidebar content.
    """
    # Add content to the drawer
    with drawer:
        ui.label('Claude Chat').classes('app-drawer-title')
        ui.separator()

        menu_buttons: Dict[str, Any] = {}
        
        with ui.column().classes('app-drawer-menu'):
            menu_buttons['chat'] = ui.button('Chat', icon='chat',
                                             on_click=lambda: change_page_wrapper('chat')).classes('app-menu-button')
            menu_buttons['settings'] = ui.button('Configuración', icon='settings',
                                                 on_click=lambda: change_page_wrapper('settings')).classes('app-menu-button')
            menu_buttons['tools'] = ui.button('Herramientas', icon='build',
                                              on_click=lambda: change_page_wrapper('tools')).classes('app-menu-button')
            menu_buttons['theme'] = ui.button('Tema', icon='brush',
                                              on_click=lambda: change_page_wrapper('theme')).classes('app-menu-button')
            
            ui.separator()
            
            # Conversations section
            ui.label('Conversaciones').classes('app-section-title')
            
            # Button to create a new conversation
            def create_new_conversation() -> None:
                """Creates a new conversation and updates the conversation list."""
                app_state: Dict[str, Any] = get_app_state()  # type: ignore
                new_name: str = f'Conversación {len(app_state.get("conversations", [])) + 1}'
                state_conversations.create_conversation(new_name)  # type: ignore
                update_conversation_list()
                
            # Enhanced new conversation button
            with ui.button('New Conversation', icon='add_comment',
                          on_click=create_new_conversation).classes('app-new-conversation-button'):
                with ui.tooltip('Start a new conversation'):
                    ui.label('Create a new chat session')
            
            # List of conversations with enhanced container
            state_core.conversations_container = ui.column().classes('app-conversations-container fade-in')
            
            # Load conversations from NiceGUI storage (now in page context)
            from mcp_open_client.state.conversations import load_conversations_from_storage
            print("DEBUG: About to load conversations from storage in layout.py")
            load_conversations_from_storage()
            
            # Initial update of conversation list
            print("DEBUG: About to update conversation list in layout.py")
            update_conversation_list()
            
            # Force UI refresh
            from mcp_open_client.state import get_app_state
            app_state = get_app_state()
            print(f"DEBUG: App state has {len(app_state['conversations'])} conversations")
            for conv in app_state['conversations']:
                print(f"DEBUG: Conversation: {conv['id']} - {conv['name']}")

def create_dashboard_content():
    """Create enhanced dashboard content with modern UI components"""
    with ui.column().classes('p-6 space-y-6 fade-in'):
        # Page header with breadcrumb and actions
        with ui.row().classes('w-full items-center justify-between mb-6'):
            with ui.column().classes('gap-1'):
                ui.label('Dashboard').classes('text-3xl font-bold text-gray-900')
                with ui.row().classes('items-center gap-2 text-sm text-gray-500'):
                    ui.icon('home').classes('text-sm')
                    ui.label('Home')
                    ui.icon('chevron_right').classes('text-xs')
                    ui.label('Dashboard')
            
            # Quick action buttons
            with ui.row().classes('gap-2'):
                ui.button('New Chat', icon='add_comment').props('color=primary')
                ui.button('Quick Connect', icon='link').props('color=secondary outline')
        
        # Enhanced stats cards with modern design
        with ui.row().classes('gap-6 w-full'):
            with ui.card().classes('flex-1 bg-gradient-to-r from-blue-500 to-purple-600 text-white'):
                with ui.card_section():
                    with ui.row().classes('items-center justify-between'):
                        with ui.column():
                            ui.label('Active Connections').classes('text-sm opacity-90')
                            ui.label('3').classes('text-3xl font-bold')
                            ui.label('+2 from yesterday').classes('text-xs opacity-75')
                        ui.icon('link').classes('text-4xl opacity-75')
            
            with ui.card().classes('flex-1 bg-gradient-to-r from-green-400 to-blue-500 text-white'):
                with ui.card_section():
                    with ui.row().classes('items-center justify-between'):
                        with ui.column():
                            ui.label('Available Tools').classes('text-sm opacity-90')
                            ui.label('12').classes('text-3xl font-bold')
                            ui.label('All systems ready').classes('text-xs opacity-75')
                        ui.icon('build_circle').classes('text-4xl opacity-75')
            
            with ui.card().classes('flex-1 bg-gradient-to-r from-purple-400 to-pink-400 text-white'):
                with ui.card_section():
                    with ui.row().classes('items-center justify-between'):
                        with ui.column():
                            ui.label('Messages Today').classes('text-sm opacity-90')
                            ui.label('47').classes('text-3xl font-bold')
                            ui.label('+12 from yesterday').classes('text-xs opacity-75')
                        ui.icon('chat_bubble').classes('text-4xl opacity-75')
        
        # Main content grid with timeline and quick actions
        with ui.grid(columns='2fr 1fr').classes('w-full gap-6'):
            # Recent activity with enhanced timeline
            with ui.card().classes('h-fit'):
                with ui.card_section():
                    ui.label('Recent Activity').classes('text-xl font-semibold mb-4')
                    
                    with ui.timeline(side='right').classes('w-full'):
                        ui.timeline_entry(
                            'Started new conversation about data analysis',
                            title='New Chat Session',
                            subtitle='2 minutes ago',
                            icon='chat'
                        )
                        ui.timeline_entry(
                            'File processing tool executed successfully',
                            title='Tool Execution',
                            subtitle='15 minutes ago',
                            icon='build_circle'
                        )
                        ui.timeline_entry(
                            'Connected to new MCP server',
                            title='Server Connection',
                            subtitle='1 hour ago',
                            icon='link'
                        )
                        ui.timeline_entry(
                            'Updated application settings',
                            title='Configuration',
                            subtitle='2 hours ago',
                            icon='settings'
                        )
            
            # Right sidebar with quick actions and system info
            with ui.column().classes('gap-4'):
                # Quick actions card
                with ui.card():
                    with ui.card_section():
                        ui.label('Quick Actions').classes('text-lg font-semibold mb-3')
                        with ui.column().classes('gap-2'):
                            ui.button('Start New Chat', icon='chat').classes('w-full').props('color=primary outline')
                            ui.button('Browse Tools', icon='explore').classes('w-full').props('color=secondary outline')
                            ui.button('View Settings', icon='settings').classes('w-full').props('color=grey outline')
                
                # System status card
                with ui.card():
                    with ui.card_section():
                        ui.label('System Status').classes('text-lg font-semibold mb-3')
                        with ui.column().classes('gap-3'):
                            with ui.row().classes('items-center justify-between'):
                                ui.label('Server Status')
                                ui.badge('Online').classes('bg-green-500 text-white')
                            
                            with ui.row().classes('items-center justify-between'):
                                ui.label('Memory Usage')
                                ui.label('45%').classes('text-sm text-gray-600')
                            
                            with ui.row().classes('items-center justify-between'):
                                ui.label('Active Sessions')
                                ui.label('3').classes('text-sm text-gray-600')
                            
                            ui.linear_progress(0.45).classes('mt-2')