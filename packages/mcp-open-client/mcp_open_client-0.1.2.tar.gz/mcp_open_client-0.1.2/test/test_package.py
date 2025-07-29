#!/usr/bin/env python3
"""
Test script to verify that the mcp-open-client package works correctly.
"""

try:
    # Import the main module
    from mcp_open_client.main import main
    print("✅ Successfully imported mcp_open_client.main")
    
    # Import other modules
    from mcp_open_client import state
    print("✅ Successfully imported mcp_open_client.state")
    
    from mcp_open_client.api import ChatAPI
    print("✅ Successfully imported mcp_open_client.api.ChatAPI")
    
    from mcp_open_client.ui.common import setup_ui
    print("✅ Successfully imported mcp_open_client.ui.common")
    
    from mcp_open_client.ui.chat import render_chat_page
    print("✅ Successfully imported mcp_open_client.ui.chat")
    
    from mcp_open_client.ui.settings import render_settings_page
    print("✅ Successfully imported mcp_open_client.ui.settings")
    
    from mcp_open_client.ui.tools import render_tools_page
    print("✅ Successfully imported mcp_open_client.ui.tools")
    
    print("\n🎉 All imports successful! The package structure is correct.")
    
    # Check if the entry point is defined correctly
    print("\nTo run the application, use one of the following methods:")
    print("1. Command line: mcp-open-client")
    print("2. Python: python -m mcp_open_client.main")
    print("3. Direct import: from mcp_open_client.main import main; main()")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("\nPossible solutions:")
    print("1. Make sure you've installed the package with 'pip install -e .'")
    print("2. Check that all files are in the correct locations")
    print("3. Verify that all import statements use the correct paths")

if __name__ == "__main__":
    print("\nTo run the application, execute: python -m mcp_open_client.main")