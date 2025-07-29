# MCP Open Client

A NiceGUI-based chat application for Claude and other OpenAI-compatible APIs. Version 0.1.1.

## Features

- Chat interface for Claude and other OpenAI-compatible APIs
- Support for custom tools and function calling
- Conversation management
- Settings customization
- Dark mode support

## Installation

You can install the latest version of the package from PyPI:

```bash
pip install mcp-open-client
```

To install a specific version:

```bash
pip install mcp-open-client==0.1.1
```

Or install the latest development version directly from GitHub:

```bash
pip install git+https://github.com/alejoair/mcp-open-client.git
```

For development installation:

```bash
# Clone the repository
git clone https://github.com/alejoair/mcp-open-client.git
cd mcp-open-client

# Install in development mode
python install_dev.py
```

## Usage

After installation, you can run the application with:

```bash
mcp-open-client [--port PORT] [--host HOST]
```

Command-line options:
- `--port PORT`: Specify the port to run the application on (default: 8081)
- `--host HOST`: Specify the host to run the application on (default: 0.0.0.0)

Or from Python:

```python
from mcp_open_client.main import main

if __name__ == "__main__":
    main(port=8081, host="0.0.0.0")
```

## Configuration

The application stores its configuration in the user's home directory at `~/mcp-open-client/config/`.
The following files are created:

- `user_settings.json`: Contains user settings like API key, model, etc.
- `user_tools.json`: Contains custom tools created by the user

### API Configuration

To use the application, you need to configure your API key in the settings. The application supports:

- OpenAI API (ChatGPT, GPT-4)
- Anthropic API (Claude)
- Any OpenAI-compatible API endpoint

## Package Structure

```
mcp_open_client/
├── __init__.py           # Package initialization with version info
├── main.py               # Main entry point
├── api.py                # API client implementation
├── state.py              # Application state management
├── ui/                   # UI components
│   ├── __init__.py       # UI package initialization
│   ├── common.py         # Common UI elements
│   ├── chat.py           # Chat interface
│   ├── settings.py       # Settings interface
│   └── tools.py          # Tools interface
├── assets/               # Static assets
│   └── favicon           # Application favicon
└── settings/             # Default settings
    ├── default_settings.json  # Default application settings
    └── default_tools.json     # Default tools configuration
```

## Development

To set up the development environment:

1. Clone the repository: `git clone https://github.com/alejoair/mcp-open-client.git`
2. Navigate to the project directory: `cd mcp-open-client`
3. Install in development mode: `python install_dev.py`
4. Run the application: `python -m mcp_open_client.main`

### Testing

To verify the package installation:

```bash
python test_import.py
```

## API Reference

### Main Module

```python
from mcp_open_client.main import main

# Run the application with custom settings
main(port=8080, host="127.0.0.1")
```

### State Module

```python
from mcp_open_client.state import State

# Access the application state
state = State()
```

### API Module

```python
from mcp_open_client.api import ChatAPI

# Create a chat API instance
api = ChatAPI()
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.