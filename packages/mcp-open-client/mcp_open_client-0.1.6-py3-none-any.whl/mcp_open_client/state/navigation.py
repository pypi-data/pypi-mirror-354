# Navigation management functions
from . import core

def register_page_renderer(page_name, renderer_function):
    """Register a function to render a specific page"""
    core.app_state['page_renderers'][page_name] = renderer_function

def navigate_to(page_name):
    """Navigate to a specific page"""
    if page_name in core.app_state['page_renderers']:
        # Update the current page
        core.app_state['current_page'] = page_name
        
        # Clear the content container
        if core.content_container:
            core.content_container.clear()
        
        # Call the page renderer function
        renderer = core.app_state['page_renderers'][page_name]
        renderer()
        
        return True
    else:
        print(f"Page '{page_name}' not found")
        return False

def get_current_page():
    """Get the name of the current page"""
    return core.app_state['current_page']

def initialize_navigation(content_container_ref):
    """Initialize navigation with the content container reference"""
    core.content_container = content_container_ref