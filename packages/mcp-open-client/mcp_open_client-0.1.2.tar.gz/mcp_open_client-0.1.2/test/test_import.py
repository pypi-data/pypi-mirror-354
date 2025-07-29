"""
Test script to verify the mcp-open-client package can be imported and used programmatically.
"""

# Test importing the main module
print("Testing imports...")
try:
    import mcp_open_client
    print(f"✅ Successfully imported mcp_open_client (version: {mcp_open_client.__version__})")
    
    from mcp_open_client import main, state, api
    print("✅ Successfully imported main modules")
    
    from mcp_open_client.ui import common, chat, settings, tools
    print("✅ Successfully imported UI modules")
    
    print("\nAll imports successful!")
    print("\nPackage structure is correct and the package is properly installed.")
    print("\nTo use the package in your code:")
    print("  1. Import the main function: from mcp_open_client.main import main")
    print("  2. Call the main function with optional arguments: main(port=8080)")
    print("\nOr run directly from command line: mcp-open-client --port 8080")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please make sure the package is installed correctly.")