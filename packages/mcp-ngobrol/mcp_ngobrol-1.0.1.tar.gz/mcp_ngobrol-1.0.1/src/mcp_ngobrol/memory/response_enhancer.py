#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Response Enhancer
=================

Enhance responses dengan conversation context dan user preferences.
"""

import json
import re
from typing import Dict, Any, List, Optional

from .context_processor import ContextProcessor, ConversationContext
from .preference_manager import get_user_preferences
from .session_memory import get_session_memory
from ..debug import server_debug_log as debug_log


class ResponseEnhancer:
    """
    Enhance responses dengan context awareness dan user preferences
    """
    
    def __init__(self):
        self.context_processor = ContextProcessor()
        self.preference_manager = get_user_preferences()
        self.session_memory = get_session_memory()
    
    def enhance_response(
        self, 
        base_response: str, 
        conversation_history: str = "[]",
        user_preferences: str = "{}",
        session_id: str = "default"
    ) -> str:
        """
        Main method untuk enhance response dengan context dan preferences
        
        Args:
            base_response: Original response
            conversation_history: JSON conversation history
            user_preferences: JSON user preferences
            session_id: Session identifier
            
        Returns:
            Enhanced response
        """
        try:
            # Process conversation context
            context = self.context_processor.process_conversation_history(
                conversation_history, session_id
            )
            
            # Parse user preferences
            prefs = self._parse_user_preferences(user_preferences)
            
            # Enhance response step by step
            enhanced = base_response
            enhanced = self._add_context_awareness(enhanced, context)
            enhanced = self._adapt_to_preferences(enhanced, prefs)
            enhanced = self._add_contextual_suggestions(enhanced, context)
            enhanced = self._format_response(enhanced, prefs)
            
            debug_log(f"Enhanced response for session {session_id}")
            return enhanced
            
        except Exception as e:
            debug_log(f"Error enhancing response: {e}")
            return base_response  # Fallback to original
    
    def _parse_user_preferences(self, user_preferences: str) -> Dict[str, Any]:
        """Parse user preferences dari JSON string"""
        try:
            if user_preferences:
                return json.loads(user_preferences)
        except Exception:
            pass
        
        # Fallback to current preferences
        return self.preference_manager.get_all_preferences()
    
    def _add_context_awareness(self, response: str, context: ConversationContext) -> str:
        """Add context awareness ke response"""
        if context.relevance_score < 0.3:
            return response  # Low relevance, no context addition
        
        enhanced_parts = [response]
        
        # Add context reference jika relevant
        if context.relevance_score > 0.5 and context.current_topics:
            topic_context = self._generate_topic_context(context.current_topics)
            if topic_context:
                enhanced_parts.append(f"\n💡 Context: {topic_context}")
        
        # Add continuity reference
        if context.relevance_score > 0.6 and len(context.recent_exchanges) > 1:
            continuity = self._generate_continuity_reference(context.recent_exchanges)
            if continuity:
                enhanced_parts.append(f"\n🔗 {continuity}")
        
        return "\n".join(enhanced_parts)
    
    def _adapt_to_preferences(self, response: str, preferences: Dict[str, Any]) -> str:
        """Adapt response berdasarkan user preferences"""
        adapted = response
        
        # Communication style adaptation
        comm_style = preferences.get("communication_style", "balanced")
        if comm_style == "concise":
            adapted = self._make_concise(adapted)
        elif comm_style == "detailed":
            adapted = self._add_detail(adapted)
        
        # Technical level adaptation
        tech_level = preferences.get("technical_level", "intermediate")
        if tech_level == "beginner":
            adapted = self._simplify_technical_terms(adapted)
        elif tech_level == "expert":
            adapted = self._add_technical_depth(adapted)
        
        # Verbosity adaptation
        verbosity = preferences.get("verbosity", "medium")
        if verbosity == "low":
            adapted = self._reduce_verbosity(adapted)
        elif verbosity == "high":
            adapted = self._increase_verbosity(adapted)
        
        return adapted
    
    def _add_contextual_suggestions(self, response: str, context: ConversationContext) -> str:
        """Add contextual suggestions berdasarkan conversation"""
        if not context.suggestions or context.relevance_score < 0.5:
            return response
        
        # Add suggestions jika response belum terlalu panjang
        if len(response) < 800:
            suggestions_text = "\n\n💡 Suggestions:\n" + "\n".join(f"• {s}" for s in context.suggestions[:3])
            return response + suggestions_text
        
        return response
    
    def _format_response(self, response: str, preferences: Dict[str, Any]) -> str:
        """Format response berdasarkan preferences"""
        response_format = preferences.get("response_format", "structured")
        
        if response_format == "casual":
            return self._make_casual(response)
        elif response_format == "formal":
            return self._make_formal(response)
        else:  # structured
            return self._structure_response(response)
    
    def _generate_topic_context(self, topics: List[str]) -> str:
        """Generate topic context reference"""
        if not topics:
            return ""
        
        if len(topics) == 1:
            return f"Continuing our discussion about {topics[0]}"
        else:
            return f"Building on our discussion about {', '.join(topics[:-1])} and {topics[-1]}"
    
    def _generate_continuity_reference(self, recent_exchanges: List[Dict[str, Any]]) -> str:
        """Generate continuity reference"""
        if len(recent_exchanges) < 2:
            return ""
        
        last_exchange = recent_exchanges[-1]
        last_topic = last_exchange.get("topic")
        
        if last_topic:
            return f"Following up on the {last_topic} topic from our previous exchange"
        else:
            return "Continuing from where we left off"
    
    def _make_concise(self, response: str) -> str:
        """Make response more concise"""
        lines = response.split('\n')
        
        # Remove empty lines dan redundant content
        essential_lines = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('Note:') and not line.startswith('Remember:'):
                essential_lines.append(line)
        
        # Limit to essential information
        if len(essential_lines) > 5:
            essential_lines = essential_lines[:5]
            essential_lines.append("...")
        
        return '\n'.join(essential_lines)
    
    def _add_detail(self, response: str) -> str:
        """Add more detail ke response"""
        if len(response) < 200:
            # Add explanatory details
            detailed_parts = [response]
            
            if "checkpoint" in response.lower():
                detailed_parts.append("\nCheckpoints allow you to save the current state and restore it later if needed.")
            
            if "auto" in response.lower() and "completion" in response.lower():
                detailed_parts.append("\nAuto-completion automatically triggers feedback when certain patterns are detected in the conversation.")
            
            if len(detailed_parts) == 1:  # No specific details added
                detailed_parts.append("\nLet me know if you need more detailed explanation about any aspect.")
            
            return '\n'.join(detailed_parts)
        
        return response
    
    def _simplify_technical_terms(self, response: str) -> str:
        """Simplify technical terms untuk beginners"""
        # Dictionary of technical terms dan explanations
        simplifications = {
            r'\bAPI\b': 'API (a way for programs to communicate)',
            r'\bJSON\b': 'JSON (a data format)',
            r'\bMCP\b': 'MCP (Model Context Protocol - the system we\'re using)',
            r'\bcheckpoint\b': 'checkpoint (a saved state)',
            r'\btrigger\b': 'trigger (an automatic activation)',
            r'\bcallback\b': 'callback (a response function)',
            r'\bparameter\b': 'parameter (an input value)'
        }
        
        simplified = response
        for pattern, replacement in simplifications.items():
            simplified = re.sub(pattern, replacement, simplified, flags=re.IGNORECASE)
        
        return simplified
    
    def _add_technical_depth(self, response: str) -> str:
        """Add technical depth untuk expert users"""
        if len(response) < 300:
            # Add technical details
            technical_parts = [response]
            
            if "checkpoint" in response.lower():
                technical_parts.append("\nTechnical: Checkpoints use JSON serialization with MD5 checksums for file integrity verification.")
            
            if "memory" in response.lower():
                technical_parts.append("\nTechnical: Memory system uses in-memory deque structures with configurable retention policies.")
            
            return '\n'.join(technical_parts)
        
        return response
    
    def _reduce_verbosity(self, response: str) -> str:
        """Reduce verbosity"""
        # Remove verbose phrases
        verbose_patterns = [
            r'\bLet me know if you need.*?\.',
            r'\bFeel free to.*?\.',
            r'\bPlease don\'t hesitate.*?\.',
            r'\bI hope this helps.*?\.'
        ]
        
        reduced = response
        for pattern in verbose_patterns:
            reduced = re.sub(pattern, '', reduced, flags=re.IGNORECASE)
        
        # Clean up extra whitespace
        reduced = re.sub(r'\n\s*\n', '\n', reduced)
        return reduced.strip()
    
    def _increase_verbosity(self, response: str) -> str:
        """Increase verbosity"""
        if len(response) < 400:
            verbose_parts = [response]
            verbose_parts.append("\nI hope this information is helpful. Please let me know if you have any questions or need clarification on any point.")
            return '\n'.join(verbose_parts)
        
        return response
    
    def _make_casual(self, response: str) -> str:
        """Make response more casual"""
        casual = response
        
        # Replace formal phrases dengan casual ones
        casual_replacements = {
            r'\bPlease\b': 'Just',
            r'\bYou may\b': 'You can',
            r'\bI recommend\b': 'I\'d suggest',
            r'\bIt is advisable\b': 'It\'s good to',
            r'\bFurthermore\b': 'Also',
            r'\bHowever\b': 'But'
        }
        
        for formal, casual_replacement in casual_replacements.items():
            casual = re.sub(formal, casual_replacement, casual, flags=re.IGNORECASE)
        
        return casual
    
    def _make_formal(self, response: str) -> str:
        """Make response more formal"""
        formal = response
        
        # Replace casual phrases dengan formal ones
        formal_replacements = {
            r'\bJust\b': 'Please',
            r'\bYou can\b': 'You may',
            r'\bI\'d suggest\b': 'I recommend',
            r'\bIt\'s good to\b': 'It is advisable to',
            r'\bAlso\b': 'Furthermore',
            r'\bBut\b': 'However'
        }
        
        for casual, formal_replacement in formal_replacements.items():
            formal = re.sub(casual, formal_replacement, formal, flags=re.IGNORECASE)
        
        return formal
    
    def _structure_response(self, response: str) -> str:
        """Structure response dengan clear formatting"""
        lines = response.split('\n')
        structured_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Add structure markers
            if line.startswith('Context:'):
                structured_lines.append(f"📋 {line}")
            elif line.startswith('Suggestions:'):
                structured_lines.append(f"💡 {line}")
            elif line.startswith('Technical:'):
                structured_lines.append(f"🔧 {line}")
            elif line.startswith('Note:'):
                structured_lines.append(f"ℹ️ {line}")
            else:
                structured_lines.append(line)
        
        return '\n'.join(structured_lines)


# Convenience function
def enhance_response_with_context(
    base_response: str,
    conversation_history: str = "[]",
    user_preferences: str = "{}",
    session_id: str = "default"
) -> str:
    """
    Convenience function untuk enhance response
    """
    enhancer = ResponseEnhancer()
    return enhancer.enhance_response(
        base_response, conversation_history, user_preferences, session_id
    )
