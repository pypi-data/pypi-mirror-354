"""
Model Data
==========

Definisi model data untuk berbagai komponen.
"""

from .completion_trigger import CompletionTrigger, TriggerType, CompletionTriggerManager, get_trigger_manager
from .checkpoint import CheckpointData, CheckpointType, CheckpointManager, get_checkpoint_manager

__all__ = [
    'CompletionTrigger',
    'TriggerType', 
    'CompletionTriggerManager',
    'get_trigger_manager',
    'CheckpointData',
    'CheckpointType',
    'CheckpointManager',
    'get_checkpoint_manager'
]
