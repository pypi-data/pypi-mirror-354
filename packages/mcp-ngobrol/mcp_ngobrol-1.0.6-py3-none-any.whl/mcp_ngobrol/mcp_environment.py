#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP Environment Detection and Management
=======================================

Sistem untuk mendeteksi dan mengelola environment MCP.
"""

import os
import sys
import json
import subprocess
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path

from .utils.debug_logger import debug_log


class MCPEnvironment:
    """Manager untuk environment MCP"""
    
    def __init__(self):
        self.environment_type = self.detect_environment()
        self.mcp_available = self.check_mcp_availability()
        
    def detect_environment(self) -> str:
        """Deteksi jenis environment yang sedang digunakan"""
        # Check environment variables
        env_indicators = {
            "augment": ["AUGMENT_SESSION", "AUGMENT_CONFIG"],
            "cursor": ["CURSOR_SESSION", "CURSOR_CONFIG"],
            "windsurf": ["WINDSURF_SESSION", "WINDSURF_CONFIG"],
            "vscode": ["VSCODE_INJECTION", "VSCODE_PID"],
            "claude": ["CLAUDE_SESSION", "ANTHROPIC_API_KEY"],
            "chatgpt": ["OPENAI_API_KEY", "CHATGPT_SESSION"],
        }
        
        for env_type, indicators in env_indicators.items():
            if any(os.getenv(indicator) for indicator in indicators):
                debug_log(f"🔍 Environment detected via env vars: {env_type}")
                return env_type
        
        # Check process names
        try:
            import psutil
            current_processes = []
            for proc in psutil.process_iter(['name', 'cmdline']):
                try:
                    name = proc.info['name'].lower()
                    cmdline = ' '.join(proc.info['cmdline'] or []).lower()
                    current_processes.append((name, cmdline))
                except:
                    continue
            
            for name, cmdline in current_processes:
                if 'augment' in name or 'augment' in cmdline:
                    debug_log(f"🔍 Environment detected via process: augment")
                    return "augment"
                elif 'cursor' in name or 'cursor' in cmdline:
                    debug_log(f"🔍 Environment detected via process: cursor")
                    return "cursor"
                elif 'windsurf' in name or 'windsurf' in cmdline:
                    debug_log(f"🔍 Environment detected via process: windsurf")
                    return "windsurf"
                elif 'code' in name and 'vscode' in cmdline:
                    debug_log(f"🔍 Environment detected via process: vscode")
                    return "vscode"
        except ImportError:
            debug_log("⚠️ psutil not available for process detection")
        except Exception as e:
            debug_log(f"⚠️ Process detection failed: {e}")
        
        # Check current working directory patterns
        cwd = os.getcwd().lower()
        if 'augment' in cwd:
            return "augment"
        elif 'cursor' in cwd:
            return "cursor"
        elif 'windsurf' in cwd:
            return "windsurf"
        
        debug_log("🔍 Environment detected: generic")
        return "generic"
    
    def check_mcp_availability(self) -> bool:
        """Check apakah MCP tools tersedia di environment ini"""
        # Check for MCP-related environment variables
        mcp_indicators = [
            "MCP_SERVER_URL",
            "MCP_CONFIG_PATH", 
            "MCP_TOOLS_AVAILABLE",
            "FASTMCP_SERVER",
        ]
        
        if any(os.getenv(indicator) for indicator in mcp_indicators):
            debug_log("✅ MCP availability detected via environment variables")
            return True
        
        # Try to import MCP-related modules
        try:
            import mcp
            debug_log("✅ MCP module available")
            return True
        except ImportError:
            pass
        
        try:
            import fastmcp
            debug_log("✅ FastMCP module available")
            return True
        except ImportError:
            pass
        
        # Check if we can access MCP tools directly
        try:
            # This would only work if MCP tools are actually available
            # We'll implement a more sophisticated check later
            debug_log("🔍 Checking direct MCP tool access...")
            return False
        except:
            pass
        
        debug_log("❌ MCP not available in current environment")
        return False
    
    def get_environment_info(self) -> Dict[str, Any]:
        """Dapatkan informasi lengkap tentang environment"""
        return {
            "environment_type": self.environment_type,
            "mcp_available": self.mcp_available,
            "python_version": sys.version,
            "platform": sys.platform,
            "working_directory": os.getcwd(),
            "environment_variables": {
                key: value for key, value in os.environ.items()
                if any(keyword in key.lower() for keyword in ['mcp', 'augment', 'cursor', 'windsurf', 'claude', 'openai'])
            },
            "mcp_tools_status": self.check_mcp_tools_status(),
        }
    
    def check_mcp_tools_status(self) -> Dict[str, Any]:
        """Check status MCP tools yang tersedia"""
        tools_status = {
            "interactive_feedback": False,
            "feedback_simple": False,
            "create_checkpoint": False,
            "list_checkpoints": False,
            "get_system_info": False,
        }
        
        # Try to check if tools are actually callable
        # This is a placeholder - in a real MCP environment,
        # we would check the actual tool registry
        
        return {
            "available_tools": tools_status,
            "total_available": sum(tools_status.values()),
            "check_method": "placeholder",
            "last_check": "now",
        }
    
    def suggest_setup_method(self) -> Tuple[str, List[str]]:
        """Suggest setup method berdasarkan environment"""
        if self.environment_type == "augment":
            return "augment_config", [
                "Add MCP server configuration to Augment settings",
                "Use: Settings → MCP Configuration",
                "Add mcp-ngobrol server configuration",
                "Restart Augment Code IDE"
            ]
        elif self.environment_type == "cursor":
            return "cursor_config", [
                "Add MCP server configuration to Cursor settings",
                "Use: Settings → Extensions → MCP",
                "Add mcp-ngobrol server configuration",
                "Restart Cursor IDE"
            ]
        elif self.environment_type == "windsurf":
            return "windsurf_config", [
                "Add MCP server configuration to Windsurf settings",
                "Use: Settings → MCP Configuration",
                "Add mcp-ngobrol server configuration",
                "Restart Windsurf IDE"
            ]
        elif self.environment_type == "vscode":
            return "vscode_extension", [
                "Install MCP extension for VS Code",
                "Configure MCP server in extension settings",
                "Add mcp-ngobrol server configuration",
                "Restart VS Code"
            ]
        else:
            return "manual_setup", [
                "Create MCP configuration file manually",
                "Use: uvx mcp-ngobrol@latest setup",
                "Follow the generated instructions",
                "Configure your AI assistant manually"
            ]
    
    def generate_environment_report(self) -> str:
        """Generate laporan lengkap tentang environment"""
        info = self.get_environment_info()
        setup_method, steps = self.suggest_setup_method()
        
        report = f"""
🔍 MCP Environment Analysis Report
==================================

Environment Type: {info['environment_type']}
MCP Available: {'✅ Yes' if info['mcp_available'] else '❌ No'}
Platform: {info['platform']}
Python Version: {info['python_version'].split()[0]}

🛠️ MCP Tools Status:
Available Tools: {info['mcp_tools_status']['total_available']}/5
- interactive_feedback: {'✅' if info['mcp_tools_status']['available_tools']['interactive_feedback'] else '❌'}
- feedback_simple: {'✅' if info['mcp_tools_status']['available_tools']['feedback_simple'] else '❌'}
- create_checkpoint: {'✅' if info['mcp_tools_status']['available_tools']['create_checkpoint'] else '❌'}
- list_checkpoints: {'✅' if info['mcp_tools_status']['available_tools']['list_checkpoints'] else '❌'}
- get_system_info: {'✅' if info['mcp_tools_status']['available_tools']['get_system_info'] else '❌'}

🔧 Recommended Setup Method: {setup_method}
Steps:
"""
        for i, step in enumerate(steps, 1):
            report += f"{i}. {step}\n"
        
        if info['environment_variables']:
            report += f"\n🌍 Relevant Environment Variables:\n"
            for key, value in info['environment_variables'].items():
                report += f"- {key}: {value[:50]}{'...' if len(value) > 50 else ''}\n"
        
        return report


def get_environment_manager() -> MCPEnvironment:
    """Get singleton instance of MCPEnvironment"""
    if not hasattr(get_environment_manager, '_instance'):
        get_environment_manager._instance = MCPEnvironment()
    return get_environment_manager._instance


def print_environment_report():
    """Print environment analysis report"""
    env_manager = get_environment_manager()
    print(env_manager.generate_environment_report())


if __name__ == "__main__":
    print_environment_report()
