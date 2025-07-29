#!/usr/bin/env python3
"""
SecretButlerMCP - A local MCP server that manages API keys with user approval.
Run with: uv run --with fastmcp --with toml python secretbutler.py
"""

import os
import sys
import signal
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

import toml
from fastmcp import FastMCP

# Configuration
CONFIG_PATH = Path.home() / ".secretbutler.toml"


class SecretButler:
    def __init__(self):
        self.secrets: Dict[str, str] = {}
        self.load_secrets()

    def load_secrets(self):
        """Load secrets from ~/.secretbutler.toml"""
        if CONFIG_PATH.exists():
            try:
                data = toml.load(CONFIG_PATH)
                self.secrets = data.get("secrets", {})
            except Exception as e:
                print(f"Error loading secrets: {e}")
                self.secrets = {}
        else:
            # Create example config file
            self.create_example_config()

    def create_example_config(self):
        """Create an example config file"""
        example_config = {
            "secrets": {
                "OPENAI_API_KEY": "sk-...",
                "ANTHROPIC_API_KEY": "sk-ant-...",
                "HF_API_KEY": "hf_...",
                "MODAL_SECRET": "ak-...",
            }
        }

        CONFIG_PATH.parent.mkdir(exist_ok=True)
        with open(CONFIG_PATH, "w") as f:
            toml.dump(example_config, f)
        print(f"Created example config at {CONFIG_PATH}")

    def get_available_secrets(self) -> List[str]:
        """Return list of available secret names"""
        return list(self.secrets.keys())

    def get_secrets(self, secret_names: List[str]) -> Dict[str, str]:
        """Get specific secrets by name"""
        return {
            name: self.secrets[name] for name in secret_names if name in self.secrets
        }


def show_approval_dialog(client_name: str, secret_names: List[str]) -> bool:
    """Show native approval dialog using AppleScript"""
    secrets_text = ", ".join(secret_names)

    # Create AppleScript for native dialog
    script = f"""
    display dialog "{client_name} is requesting access to:

{secrets_text}

Approve this request?" ¬
        with title "🔐 Secret Access Request" ¬
        buttons {{"Deny", "Approve"}} ¬
        default button "Approve" ¬
        with icon caution
    """

    try:
        # Run AppleScript
        result = subprocess.run(
            ["osascript", "-e", script], capture_output=True, text=True, timeout=30
        )

        # Check if user clicked "Approve"
        return "Approve" in result.stdout

    except subprocess.TimeoutExpired:
        print("Dialog timed out")
        return False
    except Exception as e:
        print(f"Error showing dialog: {e}")
        return False


# Global butler instance
butler = SecretButler()

# MCP Server Setup
mcp = FastMCP("SecretButlerMCP")


@mcp.tool()
def list_secrets() -> List[str]:
    """List all available secret names (no approval required)"""
    butler.load_secrets()  # Reload in case config changed
    return butler.get_available_secrets()


@mcp.tool()
def request_secrets(
    secret_names: List[str], client_name: Optional[str] = None
) -> Dict[str, str]:
    """Request specific secrets with user approval"""
    if not secret_names:
        return {}

    # Get client name from environment or use default
    if client_name is None:
        client_name = os.environ.get("CLIENT_NAME", "Unknown Client")

    # Filter to only existing secrets
    available_secrets = butler.get_available_secrets()
    requested_secrets = [name for name in secret_names if name in available_secrets]

    if not requested_secrets:
        return {}

    # Show approval dialog
    try:
        approved = show_approval_dialog(client_name, requested_secrets)
    except Exception as e:
        print(f"Error showing approval dialog: {e}")
        raise Exception(f"Failed to show approval dialog: {e}")

    if approved:
        return butler.get_secrets(requested_secrets)
    else:
        # User explicitly denied access
        secrets_list = ", ".join(requested_secrets)
        raise Exception(f"User denied access to secrets: {secrets_list}")


def main():
    print("🔐 SecretButlerMCP starting...")
    print(f"Config file: {CONFIG_PATH}")
    print("Running headless - approval dialogs will appear when needed")

    try:
        # Run MCP server (this blocks)
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        print("\n🔐 SecretButler shutting down...")


if __name__ == "__main__":
    main()
