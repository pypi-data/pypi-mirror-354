"""
Termux-specific configuration and compatibility layer.
Handles platform-specific issues when running in Android/Termux environment.
"""

import os
import sys
from typing import Dict, Any

def is_termux() -> bool:
    """Check if running in Termux environment."""
    return (
        os.environ.get('PREFIX', '').startswith('/data/data/com.termux') or
        os.path.exists('/data/data/com.termux') or
        'com.termux' in os.environ.get('PREFIX', '') or
        hasattr(sys, 'getandroidapilevel')  # Additional Android detection
    )

def setup_termux_environment():
    """Setup environment variables needed for Termux compatibility."""
    if is_termux():
        # Fix ANDROID_APP_PATH for webview compatibility
        if not os.environ.get('ANDROID_APP_PATH'):
            # Use a safe default path in Termux
            app_path = os.environ.get('HOME', '/data/data/com.termux/files/home')
            os.environ['ANDROID_APP_PATH'] = app_path
            
        # Ensure we have a valid HOME directory
        if not os.environ.get('HOME'):
            os.environ['HOME'] = '/data/data/com.termux/files/home'
            
        # Set up temporary directory if not available
        if not os.environ.get('TMPDIR'):
            os.environ['TMPDIR'] = '/data/data/com.termux/files/usr/tmp'

def patch_webview_for_termux():
    """Patch webview module to work in Termux environment."""
    if not is_termux():
        return
        
    try:
        import webview.util
        
        # Store original function
        original_get_app_root = webview.util.get_app_root
        
        def safe_get_app_root():
            """Safe version of get_app_root for Termux."""
            try:
                result = original_get_app_root()
                if result is None:
                    # Fallback to HOME directory
                    return os.environ.get('HOME', '/data/data/com.termux/files/home')
                return result
            except Exception:
                # If anything fails, return HOME directory
                return os.environ.get('HOME', '/data/data/com.termux/files/home')
        
        # Patch the function
        webview.util.get_app_root = safe_get_app_root
        
        # Also patch base_uri to handle None values
        original_base_uri = webview.util.base_uri
        
        def safe_base_uri(relative_path: str = '') -> str:
            """Safe version of base_uri for Termux."""
            try:
                base_path = safe_get_app_root()
                if base_path is None:
                    base_path = os.environ.get('HOME', '/data/data/com.termux/files/home')
                
                if not os.path.exists(base_path):
                    # Create the directory if it doesn't exist
                    os.makedirs(base_path, exist_ok=True)
                
                return f'file://{os.path.join(base_path, relative_path)}'
            except Exception as e:
                # Fallback to a safe default
                fallback_path = '/data/data/com.termux/files/home'
                return f'file://{os.path.join(fallback_path, relative_path)}'
        
        webview.util.base_uri = safe_base_uri
        
    except ImportError:
        # webview not available, which is fine
        pass
    except Exception as e:
        print(f"Warning: Could not patch webview for Termux: {e}")

def get_termux_safe_nicegui_config() -> Dict[str, Any]:
    """Get NiceGUI configuration safe for Termux environment."""
    config = {
        'show': False,  # Don't auto-open browser in Termux
        'reload': False,  # Disable auto-reload in Termux
        'favicon': None,  # Avoid favicon issues
    }
    
    # Avoid webview in Termux as it's not supported
    if is_termux():
        config.update({
            'native': False,
            'show_welcome_message': False,
        })
    
    return config

def check_webview_availability() -> bool:
    """Check if webview is available and working."""
    if is_termux():
        # Try to patch webview first
        patch_webview_for_termux()
    
    try:
        import webview
        # Try to call a basic function to see if it works
        webview.util.get_app_root()
        return True
    except ImportError:
        return False
    except Exception as e:
        print(f"Webview error: {e}")
        return False

def get_safe_port() -> int:
    """Get a safe port for NiceGUI in Termux."""
    # Use a higher port range that's typically available in Termux
    return int(os.environ.get('NICEGUI_PORT', '8080'))

def log_termux_info():
    """Log Termux environment information for debugging."""
    if is_termux():
        print("Running in Termux environment")
        print(f"PREFIX: {os.environ.get('PREFIX', 'Not set')}")
        print(f"HOME: {os.environ.get('HOME', 'Not set')}")
        print(f"TMPDIR: {os.environ.get('TMPDIR', 'Not set')}")
        print(f"ANDROID_APP_PATH: {os.environ.get('ANDROID_APP_PATH', 'Not set')}")
        print(f"Webview available: {check_webview_availability()}")

def initialize_termux_compatibility():
    """Initialize all Termux compatibility fixes."""
    if is_termux():
        setup_termux_environment()
        patch_webview_for_termux()