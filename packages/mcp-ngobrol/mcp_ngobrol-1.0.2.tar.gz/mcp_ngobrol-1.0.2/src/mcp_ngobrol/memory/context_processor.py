#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Context Processor
=================

Process conversation context untuk generate contextual responses.
"""

import json
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from .session_memory import ConversationExchange, get_session_memory
from ..debug import server_debug_log as debug_log


@dataclass
class ConversationContext:
    """Processed conversation context"""
    session_id: str
    recent_exchanges: List[Dict[str, Any]]
    current_topics: List[str]
    user_patterns: Dict[str, Any]
    context_summary: str
    relevance_score: float
    suggestions: List[str]


class ContextProcessor:
    """
    Process conversation context untuk enhance responses
    """
    
    def __init__(self):
        self.session_memory = get_session_memory()
    
    def process_conversation_history(self, conversation_history: str, session_id: str = "default") -> ConversationContext:
        """
        Process conversation history dari JSON string
        
        Args:
            conversation_history: JSON string dengan format [{"user": str, "agent": str, "timestamp": float}]
            session_id: Session identifier
            
        Returns:
            ConversationContext: Processed context
        """
        try:
            # Parse conversation history
            if conversation_history:
                history_data = json.loads(conversation_history)
                
                # Add to session memory
                for exchange in history_data:
                    if "user" in exchange and "agent" in exchange:
                        # Extract topic dan intent
                        topic = self._extract_primary_topic(exchange["user"])
                        intent = self._detect_intent(exchange["user"])
                        
                        self.session_memory.add_exchange(
                            user_input=exchange["user"],
                            agent_response=exchange["agent"],
                            session_id=session_id,
                            topic=topic,
                            intent=intent
                        )
            
            # Get processed context
            return self._build_conversation_context(session_id)
            
        except Exception as e:
            debug_log(f"Error processing conversation history: {e}")
            return self._build_empty_context(session_id)
    
    def _build_conversation_context(self, session_id: str) -> ConversationContext:
        """Build conversation context dari session memory"""
        session_context = self.session_memory.get_conversation_context(session_id)
        
        # Generate context summary
        context_summary = self._generate_context_summary(session_context)
        
        # Calculate relevance score
        relevance_score = self._calculate_relevance_score(session_context)
        
        # Generate suggestions
        suggestions = self._generate_suggestions(session_context)
        
        return ConversationContext(
            session_id=session_id,
            recent_exchanges=session_context.get("recent_exchanges", []),
            current_topics=session_context.get("current_topics", []),
            user_patterns=session_context.get("user_patterns", {}),
            context_summary=context_summary,
            relevance_score=relevance_score,
            suggestions=suggestions
        )
    
    def _build_empty_context(self, session_id: str) -> ConversationContext:
        """Build empty context untuk fallback"""
        return ConversationContext(
            session_id=session_id,
            recent_exchanges=[],
            current_topics=[],
            user_patterns={},
            context_summary="No conversation history available.",
            relevance_score=0.0,
            suggestions=[]
        )
    
    def _extract_primary_topic(self, text: str) -> Optional[str]:
        """Extract primary topic dari text"""
        topics = self.session_memory.extract_topics_from_text(text)
        return topics[0] if topics else None
    
    def _detect_intent(self, text: str) -> Optional[str]:
        """Detect intent dari text"""
        return self.session_memory.detect_intent_from_text(text)
    
    def _generate_context_summary(self, session_context: Dict[str, Any]) -> str:
        """Generate human-readable context summary"""
        if not session_context.get("recent_exchanges"):
            return "No recent conversation history."
        
        summary_parts = []
        
        # Recent activity
        total_exchanges = session_context.get("total_exchanges", 0)
        if total_exchanges > 0:
            summary_parts.append(f"We've had {total_exchanges} exchanges in this conversation.")
        
        # Current topics
        topics = session_context.get("current_topics", [])
        if topics:
            summary_parts.append(f"We've been discussing: {', '.join(topics)}.")
        
        # Recent exchange context
        recent = session_context.get("recent_exchanges", [])
        if recent:
            last_exchange = recent[-1]
            if last_exchange.get("topic"):
                summary_parts.append(f"Most recently about {last_exchange['topic']}.")
        
        # User patterns
        patterns = session_context.get("user_patterns", {})
        if patterns:
            if "communication_style" in patterns:
                style = patterns["communication_style"]
                summary_parts.append(f"You prefer {style} communication.")
        
        return " ".join(summary_parts) if summary_parts else "Starting fresh conversation."
    
    def _calculate_relevance_score(self, session_context: Dict[str, Any]) -> float:
        """Calculate relevance score untuk context"""
        score = 0.0
        
        # Recent exchanges boost relevance
        recent_exchanges = session_context.get("recent_exchanges", [])
        if recent_exchanges:
            score += min(len(recent_exchanges) * 0.1, 0.5)  # Max 0.5 dari exchanges
        
        # Topics boost relevance
        topics = session_context.get("current_topics", [])
        if topics:
            score += min(len(topics) * 0.1, 0.3)  # Max 0.3 dari topics
        
        # User patterns boost relevance
        patterns = session_context.get("user_patterns", {})
        if patterns:
            score += min(len(patterns) * 0.05, 0.2)  # Max 0.2 dari patterns
        
        return min(score, 1.0)  # Cap at 1.0
    
    def _generate_suggestions(self, session_context: Dict[str, Any]) -> List[str]:
        """Generate contextual suggestions"""
        suggestions = []
        
        # Topic-based suggestions
        topics = session_context.get("current_topics", [])
        for topic in topics:
            if topic == "auto_completion":
                suggestions.append("Consider testing the auto-completion triggers we discussed")
            elif topic == "checkpoint":
                suggestions.append("You might want to create a checkpoint before making changes")
            elif topic == "configuration":
                suggestions.append("Review the configuration settings we modified")
            elif topic == "error":
                suggestions.append("Let's verify the error has been resolved")
        
        # Pattern-based suggestions
        patterns = session_context.get("user_patterns", {})
        if "prefers_detailed_explanations" in patterns:
            suggestions.append("I can provide more detailed explanations if needed")
        elif "prefers_concise_responses" in patterns:
            suggestions.append("I'll keep my responses concise as you prefer")
        
        # Recent exchange suggestions
        recent = session_context.get("recent_exchanges", [])
        if recent:
            last_exchange = recent[-1]
            if last_exchange.get("intent") == "question":
                suggestions.append("Feel free to ask follow-up questions")
            elif last_exchange.get("intent") == "complaint":
                suggestions.append("Let me know if the issue persists")
        
        return suggestions[:3]  # Limit to 3 suggestions
    
    def enhance_summary_with_context(self, original_summary: str, context: ConversationContext) -> str:
        """Enhance summary dengan conversation context"""
        if context.relevance_score < 0.3:
            # Low relevance, minimal enhancement
            return original_summary
        
        enhanced_parts = [original_summary]
        
        # Add context reference
        if context.context_summary and context.context_summary != "No recent conversation history.":
            enhanced_parts.append(f"\n\nContext: {context.context_summary}")
        
        # Add topic continuity
        if context.current_topics:
            enhanced_parts.append(f"This relates to our discussion about: {', '.join(context.current_topics)}")
        
        # Add suggestions if relevant
        if context.suggestions and context.relevance_score > 0.6:
            enhanced_parts.append(f"\nSuggestions: {'; '.join(context.suggestions)}")
        
        return "\n".join(enhanced_parts)
    
    def analyze_conversation_patterns(self, session_id: str = "default") -> Dict[str, Any]:
        """Analyze conversation patterns untuk learning"""
        session_context = self.session_memory.get_conversation_context(session_id)
        recent_exchanges = session_context.get("recent_exchanges", [])
        
        if not recent_exchanges:
            return {"patterns": {}, "insights": []}
        
        patterns = {}
        insights = []
        
        # Analyze communication style
        user_inputs = [ex.get("user", "") for ex in recent_exchanges]
        avg_length = sum(len(inp) for inp in user_inputs) / len(user_inputs)
        
        if avg_length < 50:
            patterns["communication_style"] = "concise"
            insights.append("User prefers concise communication")
        elif avg_length > 200:
            patterns["communication_style"] = "detailed"
            insights.append("User provides detailed input")
        else:
            patterns["communication_style"] = "balanced"
        
        # Analyze question patterns
        questions = [ex for ex in recent_exchanges if "?" in ex.get("user", "")]
        if len(questions) > len(recent_exchanges) * 0.6:
            patterns["interaction_style"] = "inquisitive"
            insights.append("User asks many questions")
        
        # Analyze topic consistency
        topics = [ex.get("topic") for ex in recent_exchanges if ex.get("topic")]
        if len(set(topics)) == 1 and len(topics) > 2:
            patterns["focus_style"] = "focused"
            insights.append("User stays focused on single topics")
        elif len(set(topics)) > len(topics) * 0.7:
            patterns["focus_style"] = "exploratory"
            insights.append("User explores multiple topics")
        
        return {
            "patterns": patterns,
            "insights": insights,
            "analysis_timestamp": time.time()
        }
    
    def get_contextual_response_hints(self, user_input: str, session_id: str = "default") -> Dict[str, Any]:
        """Get hints untuk generate contextual response"""
        context = self._build_conversation_context(session_id)
        
        # Detect current intent dan topic
        current_intent = self._detect_intent(user_input)
        current_topic = self._extract_primary_topic(user_input)
        
        hints = {
            "current_intent": current_intent,
            "current_topic": current_topic,
            "context_relevance": context.relevance_score,
            "suggested_tone": "neutral",
            "reference_previous": False,
            "include_suggestions": False
        }
        
        # Adjust based on context
        if context.relevance_score > 0.5:
            hints["reference_previous"] = True
            
        if context.relevance_score > 0.7:
            hints["include_suggestions"] = True
        
        # Adjust tone based on patterns
        patterns = context.user_patterns
        if patterns.get("communication_style") == "concise":
            hints["suggested_tone"] = "concise"
        elif patterns.get("communication_style") == "detailed":
            hints["suggested_tone"] = "detailed"
        
        # Topic continuity
        if current_topic in context.current_topics:
            hints["topic_continuation"] = True
            hints["previous_topic_context"] = context.current_topics
        
        return hints
