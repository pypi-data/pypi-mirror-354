#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP Auto-Setup System
====================

Sistem untuk otomatis mengkonfigurasi MCP tools di environment yang berbeda.
"""

import os
import sys
import json
import subprocess
import asyncio
from typing import Dict, Any, Optional, List
from pathlib import Path

from .utils.debug_logger import debug_log


class MCPAutoSetup:
    """Sistem auto-setup untuk MCP tools"""
    
    def __init__(self):
        self.config_paths = [
            # Augment Code IDE
            os.path.expanduser("~/.config/augment/mcp.json"),
            os.path.expanduser("~/AppData/Roaming/Augment/mcp.json"),
            
            # Cursor IDE
            os.path.expanduser("~/.cursor/mcp.json"),
            os.path.expanduser("~/AppData/Roaming/Cursor/mcp.json"),
            
            # Windsurf IDE
            os.path.expanduser("~/.windsurf/mcp.json"),
            os.path.expanduser("~/AppData/Roaming/Windsurf/mcp.json"),
            
            # Generic MCP config
            os.path.expanduser("~/.mcp/config.json"),
            "./mcp-config.json",
        ]
        
    def detect_environment(self) -> str:
        """Deteksi environment yang sedang digunakan"""
        # Check environment variables
        if os.getenv("AUGMENT_SESSION"):
            return "augment"
        elif os.getenv("CURSOR_SESSION"):
            return "cursor"
        elif os.getenv("WINDSURF_SESSION"):
            return "windsurf"
        elif os.getenv("VSCODE_INJECTION"):
            return "vscode"
        
        # Check process names
        try:
            import psutil
            for proc in psutil.process_iter(['name']):
                name = proc.info['name'].lower()
                if 'augment' in name:
                    return "augment"
                elif 'cursor' in name:
                    return "cursor"
                elif 'windsurf' in name:
                    return "windsurf"
        except:
            pass
            
        return "generic"
    
    def get_mcp_config(self, environment: str = None) -> Dict[str, Any]:
        """Generate MCP configuration untuk environment"""
        if environment is None:
            environment = self.detect_environment()
            
        base_config = {
            "mcpServers": {
                "mcp-ngobrol": {
                    "command": "uvx",
                    "args": ["mcp-ngobrol@1.0.6"],
                    "env": {
                        "MCP_LANGUAGE": "id",
                        "MCP_DEBUG": "false",
                        "PYTHONIOENCODING": "utf-8"
                    },
                    "timeout": 300,
                    "autoApprove": ["interactive_feedback", "feedback_simple"]
                }
            }
        }
        
        # Environment-specific adjustments
        if environment == "augment":
            base_config["mcpServers"]["mcp-ngobrol"]["timeout"] = 600
            base_config["mcpServers"]["mcp-ngobrol"]["autoApprove"].extend([
                "create_checkpoint", "list_checkpoints", "get_system_info"
            ])
        elif environment == "cursor":
            base_config["mcpServers"]["mcp-ngobrol"]["env"]["MCP_DEBUG"] = "true"
        
        return base_config
    
    def find_existing_config(self) -> Optional[str]:
        """Cari konfigurasi MCP yang sudah ada"""
        for config_path in self.config_paths:
            if os.path.exists(config_path):
                debug_log(f"🔍 Found existing MCP config: {config_path}")
                return config_path
        return None
    
    def create_config_file(self, config_path: str, config: Dict[str, Any]) -> bool:
        """Buat file konfigurasi MCP"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            
            # Write config
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            debug_log(f"✅ Created MCP config: {config_path}")
            return True
        except Exception as e:
            debug_log(f"❌ Failed to create config {config_path}: {e}")
            return False
    
    def update_existing_config(self, config_path: str, new_config: Dict[str, Any]) -> bool:
        """Update konfigurasi MCP yang sudah ada"""
        try:
            # Read existing config
            with open(config_path, 'r', encoding='utf-8') as f:
                existing_config = json.load(f)
            
            # Merge configurations
            if "mcpServers" not in existing_config:
                existing_config["mcpServers"] = {}
            
            existing_config["mcpServers"].update(new_config["mcpServers"])
            
            # Write updated config
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(existing_config, f, indent=2, ensure_ascii=False)
            
            debug_log(f"✅ Updated MCP config: {config_path}")
            return True
        except Exception as e:
            debug_log(f"❌ Failed to update config {config_path}: {e}")
            return False
    
    def setup_mcp_config(self, force: bool = False) -> bool:
        """Setup MCP configuration"""
        debug_log("🔧 Setting up MCP configuration...")
        
        environment = self.detect_environment()
        debug_log(f"🔍 Detected environment: {environment}")
        
        config = self.get_mcp_config(environment)
        
        # Find existing config
        existing_config_path = self.find_existing_config()
        
        if existing_config_path and not force:
            # Update existing config
            return self.update_existing_config(existing_config_path, config)
        else:
            # Create new config
            if environment == "augment":
                config_path = os.path.expanduser("~/.config/augment/mcp.json")
            elif environment == "cursor":
                config_path = os.path.expanduser("~/.cursor/mcp.json")
            elif environment == "windsurf":
                config_path = os.path.expanduser("~/.windsurf/mcp.json")
            else:
                config_path = "./mcp-config.json"
            
            return self.create_config_file(config_path, config)
    
    async def test_mcp_connection(self) -> bool:
        """Test MCP connection"""
        debug_log("🧪 Testing MCP connection...")
        
        try:
            # Try to start MCP server
            process = await asyncio.create_subprocess_exec(
                "uvx", "mcp-ngobrol@1.0.6", "server",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Wait a bit for server to start
            await asyncio.sleep(2)
            
            # Check if process is still running
            if process.returncode is None:
                debug_log("✅ MCP server started successfully")
                process.terminate()
                await process.wait()
                return True
            else:
                debug_log("❌ MCP server failed to start")
                return False
                
        except Exception as e:
            debug_log(f"❌ MCP connection test failed: {e}")
            return False
    
    def generate_setup_instructions(self) -> str:
        """Generate setup instructions untuk user"""
        environment = self.detect_environment()
        config = self.get_mcp_config(environment)
        
        instructions = f"""
🔧 MCP Ngobrol v1.0.6 Setup Instructions
========================================

Environment detected: {environment}

1. Add this configuration to your MCP settings:

{json.dumps(config, indent=2, ensure_ascii=False)}

2. Restart your AI assistant

3. Test with: interactive_feedback tool

4. For manual setup, save the config to:
   - Augment: ~/.config/augment/mcp.json
   - Cursor: ~/.cursor/mcp.json
   - Windsurf: ~/.windsurf/mcp.json
   - Generic: ./mcp-config.json

🎯 Available Tools:
- interactive_feedback (main tool)
- feedback_simple (simplified)
- create_checkpoint (manual checkpoint)
- list_checkpoints (list checkpoints)
- get_system_info (system info)
"""
        return instructions


def auto_setup_mcp() -> bool:
    """Auto-setup MCP configuration"""
    setup = MCPAutoSetup()
    return setup.setup_mcp_config()


def print_setup_instructions():
    """Print setup instructions"""
    setup = MCPAutoSetup()
    print(setup.generate_setup_instructions())


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "instructions":
        print_setup_instructions()
    else:
        success = auto_setup_mcp()
        if success:
            print("✅ MCP configuration setup completed!")
        else:
            print("❌ MCP configuration setup failed!")
            print_setup_instructions()
