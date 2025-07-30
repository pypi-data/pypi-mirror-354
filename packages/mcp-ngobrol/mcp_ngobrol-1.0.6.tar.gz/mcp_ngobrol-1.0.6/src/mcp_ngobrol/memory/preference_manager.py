#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
User Preferences Manager
========================

Optional lightweight user preferences management.
Stores preferences in simple JSON file - MCP compliant.
"""

import os
import json
import time
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict

from ..debug import server_debug_log as debug_log


@dataclass
class UserPreferences:
    """User preferences data structure"""
    communication_style: str = "balanced"  # concise, detailed, balanced
    technical_level: str = "intermediate"   # beginner, intermediate, expert
    response_format: str = "structured"     # structured, casual, formal
    verbosity: str = "medium"              # low, medium, high
    include_examples: bool = True
    include_suggestions: bool = True
    preferred_language: str = "auto"       # auto, en, id
    feedback_frequency: str = "normal"     # minimal, normal, frequent
    
    # Learning preferences
    learn_from_corrections: bool = True
    adapt_communication_style: bool = True
    remember_topics: bool = True
    
    # UI preferences
    show_context_info: bool = False
    show_debug_info: bool = False
    
    # Timestamps
    created_at: float = 0.0
    updated_at: float = 0.0
    
    def __post_init__(self):
        if self.created_at == 0.0:
            self.created_at = time.time()
        self.updated_at = time.time()


class PreferenceManager:
    """
    Manage user preferences dengan optional file persistence
    """
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file or os.path.expanduser("~/.mcp_feedback_preferences.json")
        self.preferences = self._load_preferences()
        self.is_dirty = False
    
    def _load_preferences(self) -> UserPreferences:
        """Load preferences dari file atau create default"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Convert dict to UserPreferences
                prefs = UserPreferences(**data)
                debug_log(f"Loaded user preferences from {self.config_file}")
                return prefs
                
        except Exception as e:
            debug_log(f"Error loading preferences: {e}")
        
        # Return default preferences
        debug_log("Using default user preferences")
        return UserPreferences()
    
    def save_preferences(self) -> bool:
        """Save preferences ke file"""
        try:
            # Create directory jika tidak ada
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            # Convert to dict dan save
            data = asdict(self.preferences)
            data['updated_at'] = time.time()
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.is_dirty = False
            debug_log(f"Saved user preferences to {self.config_file}")
            return True
            
        except Exception as e:
            debug_log(f"Error saving preferences: {e}")
            return False
    
    def update_preference(self, key: str, value: Any) -> bool:
        """Update single preference"""
        if hasattr(self.preferences, key):
            setattr(self.preferences, key, value)
            self.preferences.updated_at = time.time()
            self.is_dirty = True
            debug_log(f"Updated preference {key} = {value}")
            return True
        else:
            debug_log(f"Unknown preference key: {key}")
            return False
    
    def update_preferences(self, updates: Dict[str, Any]) -> int:
        """Update multiple preferences"""
        updated_count = 0
        
        for key, value in updates.items():
            if self.update_preference(key, value):
                updated_count += 1
        
        return updated_count
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get single preference value"""
        return getattr(self.preferences, key, default)
    
    def get_all_preferences(self) -> Dict[str, Any]:
        """Get all preferences sebagai dict"""
        return asdict(self.preferences)
    
    def reset_to_defaults(self) -> None:
        """Reset preferences ke default values"""
        self.preferences = UserPreferences()
        self.is_dirty = True
        debug_log("Reset preferences to defaults")
    
    def learn_from_interaction(self, interaction_data: Dict[str, Any]) -> None:
        """Learn preferences dari user interaction"""
        if not self.preferences.learn_from_corrections:
            return
        
        # Analyze interaction untuk detect preferences
        user_input = interaction_data.get("user_input", "")
        user_correction = interaction_data.get("user_correction", "")
        response_length = interaction_data.get("response_length", 0)
        
        # Learn communication style
        if user_correction:
            if "too long" in user_correction.lower() or "too detailed" in user_correction.lower():
                if self.preferences.communication_style != "concise":
                    self.update_preference("communication_style", "concise")
                    self.update_preference("verbosity", "low")
                    
            elif "more detail" in user_correction.lower() or "explain more" in user_correction.lower():
                if self.preferences.communication_style != "detailed":
                    self.update_preference("communication_style", "detailed")
                    self.update_preference("verbosity", "high")
        
        # Learn dari input length
        if len(user_input) < 50 and self.preferences.communication_style == "detailed":
            # User gives short input, might prefer concise responses
            self.update_preference("communication_style", "balanced")
        
        # Learn technical level
        technical_terms = ["api", "database", "algorithm", "implementation", "architecture"]
        if any(term in user_input.lower() for term in technical_terms):
            if self.preferences.technical_level == "beginner":
                self.update_preference("technical_level", "intermediate")
        
        # Auto-save jika ada perubahan
        if self.is_dirty:
            self.save_preferences()
    
    def get_response_style_hints(self) -> Dict[str, Any]:
        """Get hints untuk style response berdasarkan preferences"""
        return {
            "communication_style": self.preferences.communication_style,
            "technical_level": self.preferences.technical_level,
            "verbosity": self.preferences.verbosity,
            "include_examples": self.preferences.include_examples,
            "include_suggestions": self.preferences.include_suggestions,
            "response_format": self.preferences.response_format,
            "preferred_language": self.preferences.preferred_language
        }
    
    def adapt_response_to_preferences(self, base_response: str) -> str:
        """Adapt response berdasarkan user preferences"""
        if not self.preferences.adapt_communication_style:
            return base_response
        
        adapted_response = base_response
        
        # Adjust verbosity
        if self.preferences.verbosity == "low":
            # Make more concise
            lines = adapted_response.split('\n')
            # Keep only essential lines
            essential_lines = [line for line in lines if line.strip() and not line.startswith('Note:')]
            adapted_response = '\n'.join(essential_lines[:5])  # Limit to 5 lines
            
        elif self.preferences.verbosity == "high":
            # Add more detail jika response terlalu singkat
            if len(adapted_response) < 200:
                adapted_response += "\n\nLet me know if you need more detailed explanation or have any questions."
        
        # Adjust technical level
        if self.preferences.technical_level == "beginner":
            # Add explanations untuk technical terms
            technical_terms = {
                "API": "Application Programming Interface",
                "JSON": "JavaScript Object Notation (data format)",
                "MCP": "Model Context Protocol"
            }
            
            for term, explanation in technical_terms.items():
                if term in adapted_response and explanation not in adapted_response:
                    adapted_response = adapted_response.replace(
                        term, 
                        f"{term} ({explanation})"
                    )
        
        # Add examples jika diminta
        if self.preferences.include_examples and "example" not in adapted_response.lower():
            if len(adapted_response) < 500:  # Only for shorter responses
                adapted_response += "\n\nExample: " + self._generate_simple_example(adapted_response)
        
        return adapted_response
    
    def _generate_simple_example(self, response: str) -> str:
        """Generate simple example berdasarkan response content"""
        response_lower = response.lower()
        
        if "checkpoint" in response_lower:
            return "create_checkpoint(name='Before major changes', description='Safety checkpoint')"
        elif "auto" in response_lower and "completion" in response_lower:
            return "enable_auto_completion() to start automatic feedback triggers"
        elif "feedback" in response_lower:
            return "interactive_feedback(summary='Task completed successfully')"
        else:
            return "Use the appropriate MCP tool for your specific task"
    
    def get_preferences_summary(self) -> str:
        """Get human-readable summary of current preferences"""
        prefs = self.preferences
        
        summary_parts = [
            f"Communication: {prefs.communication_style}",
            f"Technical level: {prefs.technical_level}",
            f"Verbosity: {prefs.verbosity}",
            f"Language: {prefs.preferred_language}"
        ]
        
        features = []
        if prefs.include_examples:
            features.append("examples")
        if prefs.include_suggestions:
            features.append("suggestions")
        if prefs.learn_from_corrections:
            features.append("learning")
        
        if features:
            summary_parts.append(f"Features: {', '.join(features)}")
        
        return " | ".join(summary_parts)
    
    def export_preferences(self) -> str:
        """Export preferences sebagai JSON string"""
        return json.dumps(asdict(self.preferences), indent=2, ensure_ascii=False)
    
    def import_preferences(self, json_data: str) -> bool:
        """Import preferences dari JSON string"""
        try:
            data = json.loads(json_data)
            self.preferences = UserPreferences(**data)
            self.is_dirty = True
            debug_log("Imported user preferences from JSON")
            return True
        except Exception as e:
            debug_log(f"Error importing preferences: {e}")
            return False


# Global preference manager instance
_preference_manager = None

def get_user_preferences() -> PreferenceManager:
    """Get global preference manager instance"""
    global _preference_manager
    if _preference_manager is None:
        _preference_manager = PreferenceManager()
    return _preference_manager
