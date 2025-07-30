#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Model Trigger Auto-completion
=============================

Model untuk menangani trigger auto-completion yang akan otomatis memanggil
MCP feedback saat task selesai atau chat akan berakhir.
"""

import re
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import time


class TriggerType(Enum):
    """Tipe trigger auto-completion"""
    TASK_COMPLETION = "task_completion"
    CHAT_ENDING = "chat_ending"
    USER_PROMPT = "user_prompt"
    TIMEOUT = "timeout"
    CUSTOM = "custom"


@dataclass
class CompletionTrigger:
    """
    Model untuk trigger auto-completion
    """
    trigger_id: str
    trigger_type: TriggerType
    pattern: str
    description: str
    enabled: bool = True
    priority: int = 1  # 1 = highest priority
    case_sensitive: bool = False
    regex_enabled: bool = False
    callback: Optional[Callable] = None
    created_at: float = field(default_factory=time.time)
    last_triggered: Optional[float] = None
    trigger_count: int = 0


class CompletionTriggerManager:
    """
    Manager untuk mengelola trigger auto-completion
    """
    
    def __init__(self):
        self.triggers: Dict[str, CompletionTrigger] = {}
        self._initialize_default_triggers()
    
    def _initialize_default_triggers(self):
        """Inisialisasi trigger default"""
        default_triggers = [
            CompletionTrigger(
                trigger_id="task_complete_1",
                trigger_type=TriggerType.TASK_COMPLETION,
                pattern="task.*complete|completed.*task|finished.*task|task.*done",
                description="Deteksi task completion (bahasa Inggris)",
                regex_enabled=True,
                priority=1
            ),
            CompletionTrigger(
                trigger_id="task_complete_2",
                trigger_type=TriggerType.TASK_COMPLETION,
                pattern="tugas.*selesai|selesai.*tugas|tugas.*done|sudah.*selesai",
                description="Deteksi task completion (bahasa Indonesia)",
                regex_enabled=True,
                priority=1
            ),
            CompletionTrigger(
                trigger_id="keep_going",
                trigger_type=TriggerType.CHAT_ENDING,
                pattern="would you like me.*keep going|should I continue|anything else|need.*help",
                description="Deteksi pertanyaan lanjutan",
                regex_enabled=True,
                priority=2
            ),
            CompletionTrigger(
                trigger_id="keep_going_id",
                trigger_type=TriggerType.CHAT_ENDING,
                pattern="apakah.*lanjut|perlu.*bantuan|ada.*lagi|mau.*lanjut",
                description="Deteksi pertanyaan lanjutan (bahasa Indonesia)",
                regex_enabled=True,
                priority=2
            ),
            CompletionTrigger(
                trigger_id="implementation_done",
                trigger_type=TriggerType.TASK_COMPLETION,
                pattern="implementation.*complete|code.*ready|feature.*implemented|successfully.*added",
                description="Deteksi implementasi selesai",
                regex_enabled=True,
                priority=1
            ),
            CompletionTrigger(
                trigger_id="error_resolved",
                trigger_type=TriggerType.TASK_COMPLETION,
                pattern="error.*fixed|issue.*resolved|problem.*solved|bug.*fixed",
                description="Deteksi error/masalah terselesaikan",
                regex_enabled=True,
                priority=1
            )
        ]
        
        for trigger in default_triggers:
            self.triggers[trigger.trigger_id] = trigger
    
    def add_trigger(self, trigger: CompletionTrigger) -> bool:
        """
        Menambahkan trigger baru
        
        Args:
            trigger: Trigger yang akan ditambahkan
            
        Returns:
            bool: True jika berhasil ditambahkan
        """
        if trigger.trigger_id in self.triggers:
            return False
        
        self.triggers[trigger.trigger_id] = trigger
        return True
    
    def remove_trigger(self, trigger_id: str) -> bool:
        """
        Menghapus trigger
        
        Args:
            trigger_id: ID trigger yang akan dihapus
            
        Returns:
            bool: True jika berhasil dihapus
        """
        if trigger_id in self.triggers:
            del self.triggers[trigger_id]
            return True
        return False
    
    def enable_trigger(self, trigger_id: str) -> bool:
        """Mengaktifkan trigger"""
        if trigger_id in self.triggers:
            self.triggers[trigger_id].enabled = True
            return True
        return False
    
    def disable_trigger(self, trigger_id: str) -> bool:
        """Menonaktifkan trigger"""
        if trigger_id in self.triggers:
            self.triggers[trigger_id].enabled = False
            return True
        return False
    
    def check_triggers(self, text: str) -> List[CompletionTrigger]:
        """
        Memeriksa apakah text memicu trigger
        
        Args:
            text: Text yang akan diperiksa
            
        Returns:
            List[CompletionTrigger]: Daftar trigger yang terpicu
        """
        triggered = []
        
        for trigger in self.triggers.values():
            if not trigger.enabled:
                continue
                
            if self._match_pattern(text, trigger):
                trigger.last_triggered = time.time()
                trigger.trigger_count += 1
                triggered.append(trigger)
        
        # Sort berdasarkan priority (1 = highest)
        triggered.sort(key=lambda t: t.priority)
        return triggered
    
    def _match_pattern(self, text: str, trigger: CompletionTrigger) -> bool:
        """
        Memeriksa apakah text cocok dengan pattern trigger
        
        Args:
            text: Text yang akan diperiksa
            trigger: Trigger yang akan dicocokkan
            
        Returns:
            bool: True jika cocok
        """
        search_text = text if trigger.case_sensitive else text.lower()
        pattern = trigger.pattern if trigger.case_sensitive else trigger.pattern.lower()
        
        if trigger.regex_enabled:
            try:
                flags = 0 if trigger.case_sensitive else re.IGNORECASE
                return bool(re.search(pattern, search_text, flags))
            except re.error:
                # Jika regex error, fallback ke string matching
                return pattern in search_text
        else:
            return pattern in search_text
    
    def get_trigger(self, trigger_id: str) -> Optional[CompletionTrigger]:
        """Mendapatkan trigger berdasarkan ID"""
        return self.triggers.get(trigger_id)
    
    def get_all_triggers(self) -> List[CompletionTrigger]:
        """Mendapatkan semua trigger"""
        return list(self.triggers.values())
    
    def get_enabled_triggers(self) -> List[CompletionTrigger]:
        """Mendapatkan trigger yang aktif"""
        return [t for t in self.triggers.values() if t.enabled]
    
    def get_triggers_by_type(self, trigger_type: TriggerType) -> List[CompletionTrigger]:
        """Mendapatkan trigger berdasarkan tipe"""
        return [t for t in self.triggers.values() if t.trigger_type == trigger_type]
    
    def clear_all_triggers(self):
        """Menghapus semua trigger"""
        self.triggers.clear()
    
    def reset_to_defaults(self):
        """Reset ke trigger default"""
        self.triggers.clear()
        self._initialize_default_triggers()
    
    def get_statistics(self) -> Dict:
        """Mendapatkan statistik trigger"""
        total_triggers = len(self.triggers)
        enabled_triggers = len(self.get_enabled_triggers())
        total_triggered = sum(t.trigger_count for t in self.triggers.values())
        
        return {
            "total_triggers": total_triggers,
            "enabled_triggers": enabled_triggers,
            "disabled_triggers": total_triggers - enabled_triggers,
            "total_triggered": total_triggered,
            "triggers_by_type": {
                trigger_type.value: len(self.get_triggers_by_type(trigger_type))
                for trigger_type in TriggerType
            }
        }


# Global instance
_trigger_manager = None

def get_trigger_manager() -> CompletionTriggerManager:
    """Mendapatkan instance global trigger manager"""
    global _trigger_manager
    if _trigger_manager is None:
        _trigger_manager = CompletionTriggerManager()
    return _trigger_manager
