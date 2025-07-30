#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP Feedback Enhanced Launcher
==============================

Direct launcher untuk MCP Feedback Enhanced tanpa perlu install package.
"""

import sys
import os

# Add src to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

def main():
    """Main launcher function"""
    try:
        # Import dan run server
        from mcp_feedback_enhanced.server import main as server_main
        return server_main()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print(f"Current directory: {os.getcwd()}")
        print(f"Python path: {sys.path}")
        print(f"Src directory exists: {os.path.exists(src_dir)}")
        if os.path.exists(src_dir):
            print(f"Src contents: {os.listdir(src_dir)}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting MCP server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
