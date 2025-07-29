# SecretButler

🔐 A local MCP (Model Context Protocol) server that manages API keys with user approval.

SecretButler provides a secure way to manage and share API keys with MCP clients like Claude Desktop. It runs as a local server with a GUI that requires explicit user approval before sharing any secrets.

## Features

- **Secure secret management**: Stores API keys locally in `~/.secretbutler.toml`
- **User approval required**: GUI popup asks for permission before sharing any secrets
- **MCP compatible**: Works with any MCP client
- **Easy configuration**: Simple TOML configuration file
- **macOS native**: Uses native macOS GUI components

## Installation

Install using `uvx` (recommended):

```bash
uvx secretbutler
```

Or install with pip:

```bash
pip install secretbutler
```

## Configuration

On first run, SecretButler will create a configuration file at `~/.secretbutler.toml` with example entries:

```toml
[secrets]
OPENAI_API_KEY = "sk-..."
ANTHROPIC_API_KEY = "sk-ant-..."
HF_API_KEY = "hf_..."
MODAL_SECRET = "ak-..."
```

Edit this file to add your actual API keys.

## Usage

### Running SecretButler

```bash
secretbutler
```

This will start both the GUI application and the MCP server.

### Using with Claude Desktop

Add this to your Claude Desktop MCP configuration (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "secretbutler": {
      "command": "uvx",
      "args": ["secretbutler"],
      "env": {
        "CLIENT_NAME": "Claude"
      }
    }
  }
}
```

### Available MCP Tools

- `list_secrets()`: Returns a list of available secret names (no approval required)
- `request_secrets(secret_names, client_name)`: Request specific secrets with user approval

## Security

- Secrets are stored locally in your home directory
- No secrets are shared without explicit user approval
- Each request shows which secrets are being requested and by which client
- GUI runs in the foreground with clear approval dialogs

## Requirements

- macOS (uses `rumps` for native GUI)
- Python 3.8+

## License

MIT License 