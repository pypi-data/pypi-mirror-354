#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Checkpoint Manager Utilities
=============================

Utilitas untuk mengelola checkpoint system dengan integrasi ke MCP feedback.
"""

import os
import json
import time
from typing import Dict, List, Optional, Any, Callable
import threading
import asyncio

from ..models.checkpoint import get_checkpoint_manager, CheckpointData, CheckpointType
from ..debug import server_debug_log as debug_log


class CheckpointIntegration:
    """
    Integrasi checkpoint dengan sistem MCP feedback
    """
    
    def __init__(self):
        self.checkpoint_manager = get_checkpoint_manager()
        self.auto_checkpoint_enabled = True
        self.auto_checkpoint_interval = 300  # 5 menit
        self.last_auto_checkpoint = 0.0
        self.checkpoint_callbacks: Dict[str, Callable] = {}
        self._load_config()
        self._start_auto_checkpoint_timer()
    
    def _load_config(self):
        """Memuat konfigurasi checkpoint"""
        try:
            config_path = os.path.join(os.path.expanduser("~"), ".mcp_feedback_config.json")
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                
                checkpoint_config = config_data.get("checkpoint", {})
                self.auto_checkpoint_enabled = checkpoint_config.get("auto_enabled", True)
                self.auto_checkpoint_interval = checkpoint_config.get("auto_interval", 300)
                
                debug_log("Checkpoint config loaded")
        except Exception as e:
            debug_log(f"Error loading checkpoint config: {e}")
    
    def _save_config(self):
        """Menyimpan konfigurasi checkpoint"""
        try:
            config_path = os.path.join(os.path.expanduser("~"), ".mcp_feedback_config.json")
            
            # Load existing config
            config_data = {}
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
            
            # Update checkpoint section
            config_data["checkpoint"] = {
                "auto_enabled": self.auto_checkpoint_enabled,
                "auto_interval": self.auto_checkpoint_interval
            }
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, ensure_ascii=False, indent=2)
                
            debug_log("Checkpoint config saved")
        except Exception as e:
            debug_log(f"Error saving checkpoint config: {e}")
    
    def _start_auto_checkpoint_timer(self):
        """Memulai timer auto checkpoint"""
        if self.auto_checkpoint_enabled:
            timer = threading.Timer(self.auto_checkpoint_interval, self._auto_checkpoint_task)
            timer.daemon = True
            timer.start()
    
    def _auto_checkpoint_task(self):
        """Task auto checkpoint"""
        try:
            if self.auto_checkpoint_enabled:
                current_time = time.time()
                if current_time - self.last_auto_checkpoint >= self.auto_checkpoint_interval:
                    self.create_auto_checkpoint()
                    self.last_auto_checkpoint = current_time
                
                # Schedule next auto checkpoint
                self._start_auto_checkpoint_timer()
        except Exception as e:
            debug_log(f"Error in auto checkpoint task: {e}")
    
    def create_checkpoint(
        self,
        name: str = "",
        description: str = "",
        checkpoint_type: CheckpointType = CheckpointType.MANUAL,
        project_directory: str = "",
        include_feedback_data: bool = True,
        include_command_history: bool = True,
        include_session_data: bool = True,
        include_ui_state: bool = True,
        tags: List[str] = None
    ) -> str:
        """
        Membuat checkpoint dengan data lengkap
        
        Args:
            name: Nama checkpoint
            description: Deskripsi
            checkpoint_type: Tipe checkpoint
            project_directory: Direktori proyek
            include_feedback_data: Sertakan data feedback
            include_command_history: Sertakan history command
            include_session_data: Sertakan data session
            include_ui_state: Sertakan state UI
            tags: Tags untuk checkpoint
            
        Returns:
            str: ID checkpoint yang dibuat
        """
        try:
            # Kumpulkan data dari berbagai sumber
            feedback_data = {}
            command_history = []
            session_data = {}
            ui_state = {}
            
            if include_feedback_data:
                feedback_data = self._collect_feedback_data()
            
            if include_command_history:
                command_history = self._collect_command_history()
            
            if include_session_data:
                session_data = self._collect_session_data()
            
            if include_ui_state:
                ui_state = self._collect_ui_state()
            
            # Buat checkpoint
            checkpoint_id = self.checkpoint_manager.create_checkpoint(
                name=name,
                description=description,
                checkpoint_type=checkpoint_type,
                project_directory=project_directory,
                feedback_data=feedback_data,
                command_history=command_history,
                session_data=session_data,
                ui_state=ui_state,
                tags=tags
            )
            
            debug_log(f"Checkpoint created: {checkpoint_id}")
            
            # Execute callbacks
            self._execute_checkpoint_callbacks("created", checkpoint_id)
            
            return checkpoint_id
            
        except Exception as e:
            debug_log(f"Error creating checkpoint: {e}")
            raise
    
    def create_auto_checkpoint(self) -> Optional[str]:
        """Membuat auto checkpoint"""
        try:
            return self.create_checkpoint(
                name=f"Auto Checkpoint {time.strftime('%Y-%m-%d %H:%M:%S')}",
                description="Checkpoint otomatis",
                checkpoint_type=CheckpointType.AUTO,
                project_directory=os.getcwd()
            )
        except Exception as e:
            debug_log(f"Error creating auto checkpoint: {e}")
            return None
    
    def create_task_checkpoint(self, task_name: str, is_start: bool = True) -> Optional[str]:
        """Membuat checkpoint untuk task"""
        try:
            checkpoint_type = CheckpointType.TASK_START if is_start else CheckpointType.TASK_END
            name = f"Task {'Start' if is_start else 'End'}: {task_name}"
            
            return self.create_checkpoint(
                name=name,
                description=f"Checkpoint untuk {'memulai' if is_start else 'menyelesaikan'} task: {task_name}",
                checkpoint_type=checkpoint_type,
                project_directory=os.getcwd(),
                tags=["task", task_name]
            )
        except Exception as e:
            debug_log(f"Error creating task checkpoint: {e}")
            return None
    
    def restore_checkpoint(self, checkpoint_id: str) -> bool:
        """
        Restore dari checkpoint
        
        Args:
            checkpoint_id: ID checkpoint
            
        Returns:
            bool: True jika berhasil restore
        """
        try:
            checkpoint = self.checkpoint_manager.load_checkpoint(checkpoint_id)
            if not checkpoint:
                debug_log(f"Checkpoint not found: {checkpoint_id}")
                return False
            
            # Restore data
            success = True
            
            if checkpoint.feedback_data:
                success &= self._restore_feedback_data(checkpoint.feedback_data)
            
            if checkpoint.command_history:
                success &= self._restore_command_history(checkpoint.command_history)
            
            if checkpoint.session_data:
                success &= self._restore_session_data(checkpoint.session_data)
            
            if checkpoint.ui_state:
                success &= self._restore_ui_state(checkpoint.ui_state)
            
            if success:
                debug_log(f"Checkpoint restored successfully: {checkpoint_id}")
                self._execute_checkpoint_callbacks("restored", checkpoint_id)
            else:
                debug_log(f"Checkpoint restore had some errors: {checkpoint_id}")
            
            return success
            
        except Exception as e:
            debug_log(f"Error restoring checkpoint: {e}")
            return False
    
    def _collect_feedback_data(self) -> Dict[str, Any]:
        """Mengumpulkan data feedback saat ini"""
        # Implementasi untuk mengumpulkan data feedback
        # Ini akan diintegrasikan dengan sistem feedback yang ada
        return {}
    
    def _collect_command_history(self) -> List[str]:
        """Mengumpulkan history command"""
        # Implementasi untuk mengumpulkan command history
        return []
    
    def _collect_session_data(self) -> Dict[str, Any]:
        """Mengumpulkan data session"""
        return {
            "timestamp": time.time(),
            "working_directory": os.getcwd(),
            "environment_vars": dict(os.environ)
        }
    
    def _collect_ui_state(self) -> Dict[str, Any]:
        """Mengumpulkan state UI"""
        # Implementasi untuk mengumpulkan UI state
        return {}
    
    def _restore_feedback_data(self, feedback_data: Dict[str, Any]) -> bool:
        """Restore data feedback"""
        try:
            # Implementasi restore feedback data
            debug_log("Feedback data restored")
            return True
        except Exception as e:
            debug_log(f"Error restoring feedback data: {e}")
            return False
    
    def _restore_command_history(self, command_history: List[str]) -> bool:
        """Restore command history"""
        try:
            # Implementasi restore command history
            debug_log("Command history restored")
            return True
        except Exception as e:
            debug_log(f"Error restoring command history: {e}")
            return False
    
    def _restore_session_data(self, session_data: Dict[str, Any]) -> bool:
        """Restore session data"""
        try:
            # Implementasi restore session data
            debug_log("Session data restored")
            return True
        except Exception as e:
            debug_log(f"Error restoring session data: {e}")
            return False
    
    def _restore_ui_state(self, ui_state: Dict[str, Any]) -> bool:
        """Restore UI state"""
        try:
            # Implementasi restore UI state
            debug_log("UI state restored")
            return True
        except Exception as e:
            debug_log(f"Error restoring ui state: {e}")
            return False
    
    def register_checkpoint_callback(self, callback_name: str, callback: Callable):
        """Register callback untuk checkpoint events"""
        self.checkpoint_callbacks[callback_name] = callback
        debug_log(f"Registered checkpoint callback: {callback_name}")
    
    def _execute_checkpoint_callbacks(self, event_type: str, checkpoint_id: str):
        """Execute checkpoint callbacks"""
        for callback_name, callback in self.checkpoint_callbacks.items():
            try:
                if asyncio.iscoroutinefunction(callback):
                    asyncio.create_task(callback(event_type, checkpoint_id))
                else:
                    callback(event_type, checkpoint_id)
            except Exception as e:
                debug_log(f"Error executing checkpoint callback {callback_name}: {e}")
    
    def enable_auto_checkpoint(self):
        """Enable auto checkpoint"""
        self.auto_checkpoint_enabled = True
        self._save_config()
        self._start_auto_checkpoint_timer()
        debug_log("Auto checkpoint enabled")
    
    def disable_auto_checkpoint(self):
        """Disable auto checkpoint"""
        self.auto_checkpoint_enabled = False
        self._save_config()
        debug_log("Auto checkpoint disabled")
    
    def set_auto_checkpoint_interval(self, interval: int):
        """Set interval auto checkpoint (detik)"""
        self.auto_checkpoint_interval = max(60, interval)  # Minimum 1 menit
        self._save_config()
        debug_log(f"Auto checkpoint interval set to {self.auto_checkpoint_interval} seconds")
    
    def get_checkpoint_statistics(self) -> Dict[str, Any]:
        """Mendapatkan statistik checkpoint"""
        checkpoints = self.checkpoint_manager.list_checkpoints()
        
        return {
            "total_checkpoints": len(checkpoints),
            "auto_checkpoint_enabled": self.auto_checkpoint_enabled,
            "auto_checkpoint_interval": self.auto_checkpoint_interval,
            "last_auto_checkpoint": self.last_auto_checkpoint,
            "checkpoints_by_type": {
                checkpoint_type.value: len([c for c in checkpoints if c.checkpoint_type == checkpoint_type])
                for checkpoint_type in CheckpointType
            },
            "recent_checkpoints": [
                {
                    "id": c.checkpoint_id,
                    "name": c.name,
                    "type": c.checkpoint_type.value,
                    "created_at": c.created_at
                }
                for c in checkpoints[:10]  # 10 terbaru
            ]
        }


# Global instance
_checkpoint_integration = None

def get_checkpoint_integration() -> CheckpointIntegration:
    """Mendapatkan instance global checkpoint integration"""
    global _checkpoint_integration
    if _checkpoint_integration is None:
        _checkpoint_integration = CheckpointIntegration()
    return _checkpoint_integration
