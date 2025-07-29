# SecretButler 🗝️

> A secure local MCP server for managing API keys with user approval

[![Install MCP Server](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/install-mcp?name=SecretButler&config=eyJjb21tYW5kIjoidXZ4IHNlY3JldGJ1dGxlciIsImVudiI6eyJDTElFTlRfTkFNRSI6IkNsYXVkZSJ9fQ%3D%3D)

<div align="center">
  <img src="./assets/logo.png" alt="SecretButler Logo" width="225">
</div>

## Overview

SecretButler provides a secure way to manage and share API keys with MCP clients like Claude Desktop and Cursor. It runs as a local server with a native GUI that requires explicit user approval before sharing any secrets.

<div align="center">
  <img src="./assets/example.png" alt="SecretButler Example" width="400">
</div>

## ✨ Features

- 🔒 **Secure**: Stores API keys locally in `~/.secretbutler.toml`
- 👤 **User-controlled**: GUI popup requires explicit approval for each request
- 🔌 **MCP compatible**: Works with any MCP client
- ⚙️ **Easy setup**: Simple TOML configuration
- 🍎 **Native macOS**: Uses native macOS GUI components

## 🚀 Installation

Add to your MCP client configuration:

```json
{
    "mcpServers": {
        "SecretButler": {
            "command": "uvx",
            "args": ["secretbutler"],
            "env": {
                "CLIENT_NAME": "Claude"
            }
        }
    }
}
```

## ⚙️ Configuration

On first run, SecretButler creates `~/.secretbutler.toml`:

```toml
[secrets]
OPENAI_API_KEY = "sk-..."
ANTHROPIC_API_KEY = "sk-ant-..."
HF_API_KEY = "hf_..."
```

Simply edit this file to add your API keys.

## 🛠️ MCP Tools

| Tool | Description |
|------|-------------|
| `list_secrets()` | Returns available secret names (no approval needed) |
| `request_secrets(secret_names, client_name)` | Request specific secrets with user approval |

## 🔐 Security

- ✅ Secrets stored locally only
- ✅ No sharing without explicit approval  
- ✅ Clear approval dialogs show requested secrets and client
- ✅ Foreground GUI prevents unauthorized access

## 📄 License

MIT License 