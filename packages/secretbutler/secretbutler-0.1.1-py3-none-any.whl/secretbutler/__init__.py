#!/usr/bin/env python3
"""
SecretButlerMCP - A local MCP server that manages API keys with user approval.
"""

import os
import sys
import threading
import subprocess
import queue
from pathlib import Path
from typing import Dict, List, Optional

import rumps
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
        with open(CONFIG_PATH, 'w') as f:
            toml.dump(example_config, f)
        print(f"Created example config at {CONFIG_PATH}")
    
    def get_available_secrets(self) -> List[str]:
        """Return list of available secret names"""
        return list(self.secrets.keys())
    
    def get_secrets(self, secret_names: List[str]) -> Dict[str, str]:
        """Get specific secrets by name"""
        return {name: self.secrets[name] for name in secret_names if name in self.secrets}

class SecretButlerApp(rumps.App):
    def __init__(self, butler: SecretButler):
        super().__init__("🗝️", quit_button=None)
        self.butler = butler
        self.approval_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.menu = [
            rumps.MenuItem("Show Config File", callback=self.show_config),
            rumps.separator,
            rumps.MenuItem("Quit", callback=self.quit_app)
        ]

        # Start timer to check for approval requests
        self.approval_timer = rumps.Timer(self.check_approval_queue, 0.1)
        self.approval_timer.start()

    def show_config(self, _):
        """Open config file location in Finder"""
        subprocess.run(["open", "-R", str(CONFIG_PATH)])

    def quit_app(self, _):
        """Quit the application"""
        rumps.quit_application()

    def check_approval_queue(self, _):
        """Check for approval requests from background threads"""
        try:
            while True:
                request = self.approval_queue.get_nowait()
                client_name, secret_names = request

                secrets_text = ", ".join(secret_names)
                response = rumps.alert(
                    title="Secret Access Request",
                    message=f"{client_name} is requesting access to:\n\n{secrets_text}",
                    ok="Approve",
                    cancel="Deny"
                )

                # Put result back
                self.result_queue.put(response == 1)

        except queue.Empty:
            pass

    def request_approval(self, client_name: str, secret_names: List[str]) -> bool:
        """Show approval dialog for secret access request (thread-safe)"""
        # Put request in queue
        self.approval_queue.put((client_name, secret_names))

        # Wait for result
        return self.result_queue.get(timeout=30)  # 30 second timeout

# Global butler instance
butler = SecretButler()
app = SecretButlerApp(butler)

# MCP Server Setup
mcp = FastMCP("SecretButlerMCP")

@mcp.tool()
def list_secrets() -> List[str]:
    """List all available secret names (no approval required)"""
    butler.load_secrets()  # Reload in case config changed
    return butler.get_available_secrets()

@mcp.tool()
def request_secrets(secret_names: List[str], client_name: Optional[str] = None) -> Dict[str, str]:
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
    
    # Request approval via GUI (thread-safe)
    try:
        approved = app.request_approval(client_name, requested_secrets)
    except queue.Empty:
        # Timeout - deny by default
        return {}
    
    if approved:
        return butler.get_secrets(requested_secrets)
    else:
        return {}

def run_mcp_server():
    """Run the MCP server in a separate thread"""
    mcp.run(transport="stdio")

def main():
    print("🔐 SecretButlerMCP starting...")
    print(f"Config file: {CONFIG_PATH}")
    
    # Start MCP server in background thread
    mcp_thread = threading.Thread(target=run_mcp_server, daemon=True)
    mcp_thread.start()
    
    # Run the GUI app (this blocks)
    app.run()

if __name__ == "__main__":
    main() 
