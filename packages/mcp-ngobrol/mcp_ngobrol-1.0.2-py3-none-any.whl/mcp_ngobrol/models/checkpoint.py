#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Model Checkpoint System
=======================

Model untuk sistem checkpoint yang memungkinkan menyimpan dan melanjutkan
state aplikasi dari titik tertentu.
"""

import json
import os
import time
import uuid
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
import hashlib


class CheckpointType(Enum):
    """Tipe checkpoint"""
    MANUAL = "manual"           # Checkpoint manual oleh user
    AUTO = "auto"              # Checkpoint otomatis
    TASK_START = "task_start"  # Checkpoint saat mulai task
    TASK_END = "task_end"      # Checkpoint saat selesai task
    ERROR = "error"            # Checkpoint saat terjadi error
    MILESTONE = "milestone"    # Checkpoint milestone penting


@dataclass
class CheckpointData:
    """
    Data yang disimpan dalam checkpoint
    """
    checkpoint_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    checkpoint_type: CheckpointType = CheckpointType.MANUAL
    name: str = ""
    description: str = ""
    created_at: float = field(default_factory=time.time)
    project_directory: str = ""
    
    # State data
    feedback_data: Dict[str, Any] = field(default_factory=dict)
    command_history: List[str] = field(default_factory=list)
    session_data: Dict[str, Any] = field(default_factory=dict)
    ui_state: Dict[str, Any] = field(default_factory=dict)
    
    # Metadata
    tags: List[str] = field(default_factory=list)
    file_checksums: Dict[str, str] = field(default_factory=dict)
    environment_info: Dict[str, Any] = field(default_factory=dict)
    
    # Status
    is_valid: bool = True
    last_accessed: float = field(default_factory=time.time)
    access_count: int = 0


class CheckpointManager:
    """
    Manager untuk mengelola sistem checkpoint
    """
    
    def __init__(self, checkpoint_dir: str = None):
        self.checkpoint_dir = checkpoint_dir or self._get_default_checkpoint_dir()
        self.checkpoints: Dict[str, CheckpointData] = {}
        self._ensure_checkpoint_dir()
        self._load_existing_checkpoints()
    
    def _get_default_checkpoint_dir(self) -> str:
        """Mendapatkan direktori default untuk checkpoint"""
        import tempfile
        return os.path.join(tempfile.gettempdir(), "mcp_feedback_checkpoints")
    
    def _ensure_checkpoint_dir(self):
        """Memastikan direktori checkpoint ada"""
        os.makedirs(self.checkpoint_dir, exist_ok=True)
    
    def _load_existing_checkpoints(self):
        """Memuat checkpoint yang sudah ada"""
        if not os.path.exists(self.checkpoint_dir):
            return
        
        for filename in os.listdir(self.checkpoint_dir):
            if filename.endswith('.checkpoint'):
                try:
                    filepath = os.path.join(self.checkpoint_dir, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    checkpoint = CheckpointData(**data)
                    self.checkpoints[checkpoint.checkpoint_id] = checkpoint
                except Exception as e:
                    print(f"Error loading checkpoint {filename}: {e}")
    
    def create_checkpoint(
        self,
        name: str = "",
        description: str = "",
        checkpoint_type: CheckpointType = CheckpointType.MANUAL,
        project_directory: str = "",
        feedback_data: Dict[str, Any] = None,
        command_history: List[str] = None,
        session_data: Dict[str, Any] = None,
        ui_state: Dict[str, Any] = None,
        tags: List[str] = None
    ) -> str:
        """
        Membuat checkpoint baru
        
        Args:
            name: Nama checkpoint
            description: Deskripsi checkpoint
            checkpoint_type: Tipe checkpoint
            project_directory: Direktori proyek
            feedback_data: Data feedback
            command_history: History command
            session_data: Data session
            ui_state: State UI
            tags: Tags untuk checkpoint
            
        Returns:
            str: ID checkpoint yang dibuat
        """
        checkpoint = CheckpointData(
            checkpoint_type=checkpoint_type,
            name=name or f"Checkpoint {time.strftime('%Y-%m-%d %H:%M:%S')}",
            description=description,
            project_directory=project_directory,
            feedback_data=feedback_data or {},
            command_history=command_history or [],
            session_data=session_data or {},
            ui_state=ui_state or {},
            tags=tags or [],
            environment_info=self._get_environment_info()
        )
        
        # Generate file checksums jika ada project directory
        if project_directory and os.path.exists(project_directory):
            checkpoint.file_checksums = self._generate_file_checksums(project_directory)
        
        # Simpan checkpoint
        self.checkpoints[checkpoint.checkpoint_id] = checkpoint
        self._save_checkpoint(checkpoint)
        
        return checkpoint.checkpoint_id
    
    def load_checkpoint(self, checkpoint_id: str) -> Optional[CheckpointData]:
        """
        Memuat checkpoint berdasarkan ID
        
        Args:
            checkpoint_id: ID checkpoint
            
        Returns:
            Optional[CheckpointData]: Data checkpoint atau None jika tidak ditemukan
        """
        if checkpoint_id not in self.checkpoints:
            return None
        
        checkpoint = self.checkpoints[checkpoint_id]
        checkpoint.last_accessed = time.time()
        checkpoint.access_count += 1
        
        # Update checkpoint file
        self._save_checkpoint(checkpoint)
        
        return checkpoint
    
    def delete_checkpoint(self, checkpoint_id: str) -> bool:
        """
        Menghapus checkpoint
        
        Args:
            checkpoint_id: ID checkpoint
            
        Returns:
            bool: True jika berhasil dihapus
        """
        if checkpoint_id not in self.checkpoints:
            return False
        
        # Hapus file
        filepath = os.path.join(self.checkpoint_dir, f"{checkpoint_id}.checkpoint")
        if os.path.exists(filepath):
            os.remove(filepath)
        
        # Hapus dari memory
        del self.checkpoints[checkpoint_id]
        
        return True
    
    def list_checkpoints(
        self,
        checkpoint_type: Optional[CheckpointType] = None,
        project_directory: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> List[CheckpointData]:
        """
        Mendapatkan daftar checkpoint dengan filter
        
        Args:
            checkpoint_type: Filter berdasarkan tipe
            project_directory: Filter berdasarkan direktori proyek
            tags: Filter berdasarkan tags
            
        Returns:
            List[CheckpointData]: Daftar checkpoint
        """
        checkpoints = list(self.checkpoints.values())
        
        # Filter berdasarkan tipe
        if checkpoint_type:
            checkpoints = [c for c in checkpoints if c.checkpoint_type == checkpoint_type]
        
        # Filter berdasarkan project directory
        if project_directory:
            checkpoints = [c for c in checkpoints if c.project_directory == project_directory]
        
        # Filter berdasarkan tags
        if tags:
            checkpoints = [c for c in checkpoints if any(tag in c.tags for tag in tags)]
        
        # Sort berdasarkan created_at (terbaru dulu)
        checkpoints.sort(key=lambda c: c.created_at, reverse=True)
        
        return checkpoints
    
    def get_checkpoint_info(self, checkpoint_id: str) -> Optional[Dict[str, Any]]:
        """Mendapatkan informasi checkpoint"""
        checkpoint = self.checkpoints.get(checkpoint_id)
        if not checkpoint:
            return None
        
        return {
            "id": checkpoint.checkpoint_id,
            "name": checkpoint.name,
            "description": checkpoint.description,
            "type": checkpoint.checkpoint_type.value,
            "created_at": checkpoint.created_at,
            "created_at_str": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(checkpoint.created_at)),
            "last_accessed": checkpoint.last_accessed,
            "last_accessed_str": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(checkpoint.last_accessed)),
            "access_count": checkpoint.access_count,
            "project_directory": checkpoint.project_directory,
            "tags": checkpoint.tags,
            "is_valid": checkpoint.is_valid,
            "file_count": len(checkpoint.file_checksums),
            "has_feedback_data": bool(checkpoint.feedback_data),
            "command_count": len(checkpoint.command_history)
        }
    
    def _save_checkpoint(self, checkpoint: CheckpointData):
        """Menyimpan checkpoint ke file"""
        filepath = os.path.join(self.checkpoint_dir, f"{checkpoint.checkpoint_id}.checkpoint")
        
        # Convert dataclass to dict
        data = asdict(checkpoint)
        
        # Convert enum to string
        data['checkpoint_type'] = checkpoint.checkpoint_type.value
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _generate_file_checksums(self, directory: str) -> Dict[str, str]:
        """Generate checksums untuk file dalam direktori"""
        checksums = {}
        
        try:
            for root, dirs, files in os.walk(directory):
                # Skip hidden directories dan __pycache__
                dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
                
                for file in files:
                    if file.startswith('.') or file.endswith('.pyc'):
                        continue
                    
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'rb') as f:
                            content = f.read()
                        
                        # Generate MD5 checksum
                        checksum = hashlib.md5(content).hexdigest()
                        relative_path = os.path.relpath(filepath, directory)
                        checksums[relative_path] = checksum
                    except Exception:
                        continue
        except Exception:
            pass
        
        return checksums
    
    def _get_environment_info(self) -> Dict[str, Any]:
        """Mendapatkan informasi environment"""
        import sys
        import platform
        
        return {
            "python_version": sys.version,
            "platform": platform.platform(),
            "timestamp": time.time(),
            "working_directory": os.getcwd()
        }
    
    def cleanup_old_checkpoints(self, max_age_days: int = 30, max_count: int = 100):
        """
        Membersihkan checkpoint lama
        
        Args:
            max_age_days: Umur maksimal checkpoint (hari)
            max_count: Jumlah maksimal checkpoint
        """
        current_time = time.time()
        max_age_seconds = max_age_days * 24 * 60 * 60
        
        # Hapus checkpoint yang terlalu lama
        to_delete = []
        for checkpoint_id, checkpoint in self.checkpoints.items():
            if current_time - checkpoint.created_at > max_age_seconds:
                to_delete.append(checkpoint_id)
        
        for checkpoint_id in to_delete:
            self.delete_checkpoint(checkpoint_id)
        
        # Hapus checkpoint berlebih (keep yang terbaru)
        if len(self.checkpoints) > max_count:
            sorted_checkpoints = sorted(
                self.checkpoints.items(),
                key=lambda x: x[1].created_at,
                reverse=True
            )
            
            for checkpoint_id, _ in sorted_checkpoints[max_count:]:
                self.delete_checkpoint(checkpoint_id)


# Global instance
_checkpoint_manager = None

def get_checkpoint_manager() -> CheckpointManager:
    """Mendapatkan instance global checkpoint manager"""
    global _checkpoint_manager
    if _checkpoint_manager is None:
        _checkpoint_manager = CheckpointManager()
    return _checkpoint_manager
