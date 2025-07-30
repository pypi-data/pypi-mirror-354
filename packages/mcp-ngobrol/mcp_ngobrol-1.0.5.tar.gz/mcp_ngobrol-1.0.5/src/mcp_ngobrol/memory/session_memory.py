#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session Memory
==============

In-memory storage untuk conversation context dalam session saat ini.
Reset setiap kali MCP restart - sesuai dengan nature stateless MCP.
"""

import time
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from collections import deque

from ..debug import server_debug_log as debug_log


@dataclass
class ConversationExchange:
    """Single exchange dalam conversation"""
    user_input: str
    agent_response: str
    timestamp: float
    topic: Optional[str] = None
    intent: Optional[str] = None
    sentiment: Optional[str] = None


@dataclass
class SessionContext:
    """Context untuk session saat ini"""
    session_id: str
    exchanges: deque = field(default_factory=lambda: deque(maxlen=20))  # Keep last 20 exchanges
    current_topics: List[str] = field(default_factory=list)
    user_patterns: Dict[str, Any] = field(default_factory=dict)
    preferences: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    last_activity: float = field(default_factory=time.time)


class SessionMemory:
    """
    In-memory session storage untuk conversation context
    
    Features:
    - Lightweight in-memory storage
    - Automatic cleanup
    - Topic tracking
    - Pattern detection
    - MCP-compliant (stateless)
    """
    
    def __init__(self, max_sessions: int = 10):
        self.sessions: Dict[str, SessionContext] = {}
        self.max_sessions = max_sessions
        self.current_session_id: Optional[str] = None
        
        debug_log("SessionMemory initialized")
    
    def get_or_create_session(self, session_id: str = "default") -> SessionContext:
        """Get atau create session context"""
        if session_id not in self.sessions:
            # Cleanup old sessions jika terlalu banyak
            if len(self.sessions) >= self.max_sessions:
                self._cleanup_old_sessions()
            
            self.sessions[session_id] = SessionContext(session_id=session_id)
            debug_log(f"Created new session: {session_id}")
        
        self.current_session_id = session_id
        self.sessions[session_id].last_activity = time.time()
        return self.sessions[session_id]
    
    def add_exchange(
        self, 
        user_input: str, 
        agent_response: str, 
        session_id: str = "default",
        topic: Optional[str] = None,
        intent: Optional[str] = None
    ) -> None:
        """Add conversation exchange ke session"""
        session = self.get_or_create_session(session_id)
        
        exchange = ConversationExchange(
            user_input=user_input,
            agent_response=agent_response,
            timestamp=time.time(),
            topic=topic,
            intent=intent
        )
        
        session.exchanges.append(exchange)
        
        # Update topics
        if topic and topic not in session.current_topics:
            session.current_topics.append(topic)
            # Keep only last 5 topics
            if len(session.current_topics) > 5:
                session.current_topics = session.current_topics[-5:]
        
        debug_log(f"Added exchange to session {session_id}: {len(session.exchanges)} total exchanges")
    
    def get_recent_exchanges(self, session_id: str = "default", limit: int = 10) -> List[ConversationExchange]:
        """Get recent exchanges dari session"""
        if session_id not in self.sessions:
            return []
        
        session = self.sessions[session_id]
        exchanges = list(session.exchanges)
        return exchanges[-limit:] if limit > 0 else exchanges
    
    def get_conversation_context(self, session_id: str = "default") -> Dict[str, Any]:
        """Get conversation context untuk session"""
        if session_id not in self.sessions:
            return {}
        
        session = self.sessions[session_id]
        recent_exchanges = list(session.exchanges)[-5:]  # Last 5 exchanges
        
        return {
            "session_id": session_id,
            "total_exchanges": len(session.exchanges),
            "recent_exchanges": [
                {
                    "user": ex.user_input[:100] + "..." if len(ex.user_input) > 100 else ex.user_input,
                    "agent": ex.agent_response[:100] + "..." if len(ex.agent_response) > 100 else ex.agent_response,
                    "timestamp": ex.timestamp,
                    "topic": ex.topic,
                    "intent": ex.intent
                }
                for ex in recent_exchanges
            ],
            "current_topics": session.current_topics,
            "user_patterns": session.user_patterns,
            "preferences": session.preferences,
            "session_duration": time.time() - session.created_at
        }
    
    def update_user_patterns(self, session_id: str, patterns: Dict[str, Any]) -> None:
        """Update user patterns untuk session"""
        session = self.get_or_create_session(session_id)
        session.user_patterns.update(patterns)
        debug_log(f"Updated user patterns for session {session_id}")
    
    def update_preferences(self, session_id: str, preferences: Dict[str, Any]) -> None:
        """Update user preferences untuk session"""
        session = self.get_or_create_session(session_id)
        session.preferences.update(preferences)
        debug_log(f"Updated preferences for session {session_id}")
    
    def get_context_summary(self, session_id: str = "default") -> str:
        """Get summary of conversation context"""
        if session_id not in self.sessions:
            return "No conversation history available."
        
        session = self.sessions[session_id]
        
        if not session.exchanges:
            return "No conversation history in this session."
        
        summary_parts = []
        
        # Recent topics
        if session.current_topics:
            summary_parts.append(f"Recent topics: {', '.join(session.current_topics)}")
        
        # Exchange count
        summary_parts.append(f"Total exchanges: {len(session.exchanges)}")
        
        # Last exchange info
        if session.exchanges:
            last_exchange = session.exchanges[-1]
            time_ago = int(time.time() - last_exchange.timestamp)
            summary_parts.append(f"Last activity: {time_ago} seconds ago")
        
        # User patterns
        if session.user_patterns:
            patterns = list(session.user_patterns.keys())[:3]  # Show first 3 patterns
            summary_parts.append(f"Detected patterns: {', '.join(patterns)}")
        
        return " | ".join(summary_parts)
    
    def extract_topics_from_text(self, text: str) -> List[str]:
        """Simple topic extraction dari text"""
        # Simple keyword-based topic detection
        topic_keywords = {
            "auto_completion": ["auto", "completion", "trigger", "automatic"],
            "checkpoint": ["checkpoint", "save", "restore", "backup"],
            "feedback": ["feedback", "response", "reply", "answer"],
            "configuration": ["config", "setting", "preference", "option"],
            "error": ["error", "bug", "issue", "problem", "fail"],
            "feature": ["feature", "functionality", "capability", "tool"],
            "performance": ["performance", "speed", "slow", "fast", "optimize"],
            "ui": ["interface", "gui", "web", "button", "tab", "window"]
        }
        
        text_lower = text.lower()
        detected_topics = []
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_topics.append(topic)
        
        return detected_topics
    
    def detect_intent_from_text(self, text: str) -> Optional[str]:
        """Simple intent detection dari text"""
        text_lower = text.lower()
        
        # Intent patterns
        if any(word in text_lower for word in ["how", "what", "why", "when", "where", "?"]):
            return "question"
        elif any(word in text_lower for word in ["please", "can you", "could you", "help"]):
            return "request"
        elif any(word in text_lower for word in ["error", "not working", "broken", "issue", "problem"]):
            return "complaint"
        elif any(word in text_lower for word in ["great", "good", "excellent", "perfect", "love", "awesome"]):
            return "praise"
        elif any(word in text_lower for word in ["thanks", "thank you", "appreciate"]):
            return "gratitude"
        else:
            return "statement"
    
    def _cleanup_old_sessions(self) -> None:
        """Cleanup sessions lama berdasarkan last activity"""
        if len(self.sessions) <= self.max_sessions:
            return
        
        # Sort by last activity
        sorted_sessions = sorted(
            self.sessions.items(),
            key=lambda x: x[1].last_activity
        )
        
        # Remove oldest sessions
        sessions_to_remove = len(self.sessions) - self.max_sessions + 1
        for session_id, _ in sorted_sessions[:sessions_to_remove]:
            del self.sessions[session_id]
            debug_log(f"Cleaned up old session: {session_id}")
    
    def clear_session(self, session_id: str) -> bool:
        """Clear specific session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            debug_log(f"Cleared session: {session_id}")
            return True
        return False
    
    def clear_all_sessions(self) -> None:
        """Clear all sessions"""
        self.sessions.clear()
        self.current_session_id = None
        debug_log("Cleared all sessions")
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Get statistics tentang sessions"""
        total_exchanges = sum(len(session.exchanges) for session in self.sessions.values())
        
        return {
            "total_sessions": len(self.sessions),
            "total_exchanges": total_exchanges,
            "current_session": self.current_session_id,
            "sessions": {
                session_id: {
                    "exchanges": len(session.exchanges),
                    "topics": len(session.current_topics),
                    "last_activity": session.last_activity,
                    "duration": time.time() - session.created_at
                }
                for session_id, session in self.sessions.items()
            }
        }


# Global session memory instance
_session_memory = None

def get_session_memory() -> SessionMemory:
    """Get global session memory instance"""
    global _session_memory
    if _session_memory is None:
        _session_memory = SessionMemory()
    return _session_memory
