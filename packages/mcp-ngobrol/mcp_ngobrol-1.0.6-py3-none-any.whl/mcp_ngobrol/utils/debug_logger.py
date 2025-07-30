#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug Logger Utility
===================

Simple debug logging utility untuk MCP Ngobrol.
"""

import os
import sys
import datetime
from typing import Any


def debug_log(message: Any, force: bool = False) -> None:
    """
    Log debug message jika debug mode aktif
    
    Args:
        message: Message to log
        force: Force log even if debug mode is off
    """
    # Check if debug mode is enabled
    debug_enabled = (
        os.getenv("MCP_DEBUG", "false").lower() in ("true", "1", "yes") or
        force
    )
    
    if not debug_enabled:
        return
    
    # Format timestamp
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    
    # Convert message to string
    if not isinstance(message, str):
        message = str(message)
    
    # Print with timestamp
    print(f"[{timestamp}] {message}", file=sys.stderr, flush=True)


def enable_debug():
    """Enable debug logging"""
    os.environ["MCP_DEBUG"] = "true"


def disable_debug():
    """Disable debug logging"""
    os.environ["MCP_DEBUG"] = "false"


def is_debug_enabled() -> bool:
    """Check if debug logging is enabled"""
    return os.getenv("MCP_DEBUG", "false").lower() in ("true", "1", "yes")
