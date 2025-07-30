#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP Ngobrol Simple Launcher
===========================

Simple launcher untuk MCP Ngobrol tanpa emoji untuk kompatibilitas encoding.
"""

import sys
import os

# Project directory
PROJECT_DIR = r"C:\project\mcp-feedback-enhanced-2.3.0"
SRC_DIR = os.path.join(PROJECT_DIR, 'src')

# Add src to Python path
sys.path.insert(0, SRC_DIR)

# Set environment variables
os.environ['MCP_LANGUAGE'] = 'id'
os.environ['MCP_DEBUG'] = 'false'
os.environ['MCP_LOG_LEVEL'] = 'INFO'

def main():
    """Main launcher function"""
    try:
        # Change to project directory
        os.chdir(PROJECT_DIR)
        
        # Import dan set language
        from mcp_ngobrol.i18n import set_language
        set_language('id')

        # Import dan run server
        from mcp_ngobrol.server import main as server_main
        return server_main()
        
    except ImportError as e:
        print(f"Import error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
