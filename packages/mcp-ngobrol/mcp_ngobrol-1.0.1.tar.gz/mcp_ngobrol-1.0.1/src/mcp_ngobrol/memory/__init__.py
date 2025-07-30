#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Memory System
=============

In-memory conversation context and user preference management for MCP Feedback Enhanced.
Designed to be lightweight and MCP-compliant (stateless with optional persistence).
"""

from .session_memory import SessionMemory, get_session_memory
from .context_processor import ContextProcessor, ConversationContext
from .preference_manager import UserPreferences, get_user_preferences
from .response_enhancer import ResponseEnhancer, enhance_response_with_context

__all__ = [
    'SessionMemory',
    'get_session_memory',
    'ContextProcessor', 
    'ConversationContext',
    'UserPreferences',
    'get_user_preferences',
    'ResponseEnhancer',
    'enhance_response_with_context'
]
