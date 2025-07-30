#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto-completion System
======================

Sistem untuk otomatis memanggil MCP feedback saat task selesai atau chat akan berakhir.
Menggunakan pattern detection dan callback system.
"""

import asyncio
import threading
import time
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
import json
import os

from ..models.completion_trigger import get_trigger_manager, CompletionTrigger, TriggerType
from ..debug import server_debug_log as debug_log


@dataclass
class AutoCompletionConfig:
    """Konfigurasi auto-completion"""
    enabled: bool = True
    auto_trigger_delay: float = 3.0  # Delay sebelum trigger (lebih lama)
    max_triggers_per_session: int = 8  # Maksimal trigger per session (lebih banyak)
    cooldown_period: float = 60.0  # Cooldown antar trigger (lebih lama)
    require_confirmation: bool = False  # Perlu konfirmasi user
    save_trigger_history: bool = True  # Simpan history trigger


class AutoCompletionSystem:
    """
    Sistem auto-completion yang menangani trigger otomatis untuk MCP feedback
    """
    
    def __init__(self):
        self.config = AutoCompletionConfig()
        self.trigger_manager = get_trigger_manager()
        self.callbacks: Dict[str, Callable] = {}
        self.trigger_history: List[Dict] = []
        self.session_trigger_count = 0
        self.last_trigger_time = 0.0
        self.is_enabled = True
        self._load_config()
    
    def _load_config(self):
        """Memuat konfigurasi dari file"""
        try:
            config_path = os.path.join(os.path.expanduser("~"), ".mcp_feedback_config.json")
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                
                auto_completion_config = config_data.get("auto_completion", {})
                
                self.config.enabled = auto_completion_config.get("enabled", True)
                self.config.auto_trigger_delay = auto_completion_config.get("auto_trigger_delay", 2.0)
                self.config.max_triggers_per_session = auto_completion_config.get("max_triggers_per_session", 5)
                self.config.cooldown_period = auto_completion_config.get("cooldown_period", 30.0)
                self.config.require_confirmation = auto_completion_config.get("require_confirmation", False)
                self.config.save_trigger_history = auto_completion_config.get("save_trigger_history", True)
                
                debug_log("Auto-completion config loaded from file")
        except Exception as e:
            debug_log(f"Error loading auto-completion config: {e}")
    
    def _save_config(self):
        """Menyimpan konfigurasi ke file"""
        try:
            config_path = os.path.join(os.path.expanduser("~"), ".mcp_feedback_config.json")
            
            # Load existing config
            config_data = {}
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
            
            # Update auto-completion section
            config_data["auto_completion"] = {
                "enabled": self.config.enabled,
                "auto_trigger_delay": self.config.auto_trigger_delay,
                "max_triggers_per_session": self.config.max_triggers_per_session,
                "cooldown_period": self.config.cooldown_period,
                "require_confirmation": self.config.require_confirmation,
                "save_trigger_history": self.config.save_trigger_history
            }
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, ensure_ascii=False, indent=2)
                
            debug_log("Auto-completion config saved to file")
        except Exception as e:
            debug_log(f"Error saving auto-completion config: {e}")
    
    def register_callback(self, callback_name: str, callback: Callable):
        """
        Mendaftarkan callback untuk auto-completion
        
        Args:
            callback_name: Nama callback
            callback: Fungsi callback
        """
        self.callbacks[callback_name] = callback
        debug_log(f"Registered auto-completion callback: {callback_name}")
    
    def unregister_callback(self, callback_name: str):
        """Menghapus callback"""
        if callback_name in self.callbacks:
            del self.callbacks[callback_name]
            debug_log(f"Unregistered auto-completion callback: {callback_name}")
    
    def check_and_trigger(self, text: str, context: Dict[str, Any] = None) -> bool:
        """
        Memeriksa text dan trigger callback jika cocok
        
        Args:
            text: Text yang akan diperiksa
            context: Context tambahan
            
        Returns:
            bool: True jika ada trigger yang dipicu
        """
        if not self.is_enabled or not self.config.enabled:
            return False
        
        # Check cooldown
        current_time = time.time()
        if current_time - self.last_trigger_time < self.config.cooldown_period:
            debug_log(f"Auto-completion in cooldown period")
            return False
        
        # Check session limit
        if self.session_trigger_count >= self.config.max_triggers_per_session:
            debug_log(f"Auto-completion session limit reached")
            return False
        
        # Check triggers
        triggered = self.trigger_manager.check_triggers(text)
        if not triggered:
            return False
        
        debug_log(f"Auto-completion triggered by: {[t.trigger_id for t in triggered]}")
        
        # Execute dengan delay
        if self.config.auto_trigger_delay > 0:
            threading.Timer(
                self.config.auto_trigger_delay,
                self._execute_triggers,
                args=(triggered, text, context or {})
            ).start()
        else:
            self._execute_triggers(triggered, text, context or {})
        
        return True
    
    def _execute_triggers(self, triggers: List[CompletionTrigger], text: str, context: Dict[str, Any]):
        """Eksekusi triggers"""
        try:
            current_time = time.time()
            self.last_trigger_time = current_time
            self.session_trigger_count += 1
            
            # Log trigger history
            if self.config.save_trigger_history:
                trigger_record = {
                    "timestamp": current_time,
                    "triggers": [t.trigger_id for t in triggers],
                    "text": text[:200],  # Limit text length
                    "context": context
                }
                self.trigger_history.append(trigger_record)
                
                # Keep only last 100 records
                if len(self.trigger_history) > 100:
                    self.trigger_history = self.trigger_history[-100:]
            
            # Execute callbacks
            for callback_name, callback in self.callbacks.items():
                try:
                    if asyncio.iscoroutinefunction(callback):
                        # Async callback
                        asyncio.create_task(callback(triggers, text, context))
                    else:
                        # Sync callback
                        callback(triggers, text, context)
                    
                    debug_log(f"Executed auto-completion callback: {callback_name}")
                except Exception as e:
                    debug_log(f"Error executing callback {callback_name}: {e}")
        
        except Exception as e:
            debug_log(f"Error executing triggers: {e}")
    
    def enable(self):
        """Mengaktifkan auto-completion"""
        self.is_enabled = True
        self.config.enabled = True
        self._save_config()
        debug_log("Auto-completion enabled")
    
    def disable(self):
        """Menonaktifkan auto-completion"""
        self.is_enabled = False
        self.config.enabled = False
        self._save_config()
        debug_log("Auto-completion disabled")
    
    def reset_session(self):
        """Reset session counter"""
        self.session_trigger_count = 0
        debug_log("Auto-completion session reset")
    
    def get_config(self) -> AutoCompletionConfig:
        """Mendapatkan konfigurasi saat ini"""
        return self.config
    
    def update_config(self, **kwargs):
        """Update konfigurasi"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
        
        self._save_config()
        debug_log(f"Auto-completion config updated: {kwargs}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Mendapatkan statistik auto-completion"""
        return {
            "enabled": self.is_enabled and self.config.enabled,
            "session_trigger_count": self.session_trigger_count,
            "total_trigger_history": len(self.trigger_history),
            "last_trigger_time": self.last_trigger_time,
            "registered_callbacks": list(self.callbacks.keys()),
            "trigger_manager_stats": self.trigger_manager.get_statistics(),
            "config": {
                "auto_trigger_delay": self.config.auto_trigger_delay,
                "max_triggers_per_session": self.config.max_triggers_per_session,
                "cooldown_period": self.config.cooldown_period,
                "require_confirmation": self.config.require_confirmation
            }
        }
    
    def get_trigger_history(self, limit: int = 50) -> List[Dict]:
        """Mendapatkan history trigger"""
        return self.trigger_history[-limit:] if limit > 0 else self.trigger_history
    
    def clear_trigger_history(self):
        """Menghapus history trigger"""
        self.trigger_history.clear()
        debug_log("Auto-completion trigger history cleared")


# Global instance
_auto_completion_system = None

def get_auto_completion_system() -> AutoCompletionSystem:
    """Mendapatkan instance global auto-completion system"""
    global _auto_completion_system
    if _auto_completion_system is None:
        _auto_completion_system = AutoCompletionSystem()
    return _auto_completion_system


# Convenience functions
def register_auto_completion_callback(callback_name: str, callback: Callable):
    """Register callback untuk auto-completion"""
    system = get_auto_completion_system()
    system.register_callback(callback_name, callback)


def check_auto_completion(text: str, context: Dict[str, Any] = None) -> bool:
    """Check dan trigger auto-completion"""
    system = get_auto_completion_system()
    return system.check_and_trigger(text, context)


def enable_auto_completion():
    """Enable auto-completion"""
    system = get_auto_completion_system()
    system.enable()


def disable_auto_completion():
    """Disable auto-completion"""
    system = get_auto_completion_system()
    system.disable()
