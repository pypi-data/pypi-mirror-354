#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto-completion Routes
======================

Routes untuk mengelola auto-completion dan checkpoint melalui Web UI.
"""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
import time

from ...utils.auto_completion import get_auto_completion_system
from ...utils.checkpoint_manager import get_checkpoint_integration
from ...models.completion_trigger import TriggerType
from ...models.checkpoint import CheckpointType
from ...debug import server_debug_log as debug_log


# Pydantic models untuk request/response
class TriggerTestRequest(BaseModel):
    text: str


class AutoCompletionConfigRequest(BaseModel):
    auto_trigger_delay: Optional[float] = None
    max_triggers_per_session: Optional[int] = None
    cooldown_period: Optional[float] = None
    require_confirmation: Optional[bool] = None


class CheckpointCreateRequest(BaseModel):
    name: Optional[str] = ""
    description: Optional[str] = ""
    project_directory: Optional[str] = "."
    tags: Optional[List[str]] = []


class CheckpointListRequest(BaseModel):
    project_directory: Optional[str] = ""
    checkpoint_type: Optional[str] = ""
    limit: Optional[int] = 20


# Router instance
router = APIRouter(prefix="/api/auto-completion", tags=["auto-completion"])


@router.get("/status")
async def get_auto_completion_status():
    """Mendapatkan status auto-completion dan checkpoint"""
    try:
        auto_completion_system = get_auto_completion_system()
        checkpoint_integration = get_checkpoint_integration()
        
        auto_stats = auto_completion_system.get_statistics()
        checkpoint_stats = checkpoint_integration.get_checkpoint_statistics()
        
        return {
            "success": True,
            "data": {
                "auto_completion": auto_stats,
                "checkpoint": checkpoint_stats,
                "integration_status": {
                    "auto_completion_enabled": auto_stats["enabled"],
                    "checkpoint_auto_enabled": checkpoint_stats["auto_checkpoint_enabled"],
                    "registered_callbacks": len(auto_completion_system.callbacks),
                    "checkpoint_callbacks": len(checkpoint_integration.checkpoint_callbacks)
                }
            }
        }
    except Exception as e:
        debug_log(f"Error getting auto-completion status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/enable")
async def enable_auto_completion():
    """Mengaktifkan auto-completion"""
    try:
        auto_completion_system = get_auto_completion_system()
        auto_completion_system.enable()
        
        stats = auto_completion_system.get_statistics()
        
        return {
            "success": True,
            "message": "Auto-completion enabled",
            "data": stats
        }
    except Exception as e:
        debug_log(f"Error enabling auto-completion: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/disable")
async def disable_auto_completion():
    """Menonaktifkan auto-completion"""
    try:
        auto_completion_system = get_auto_completion_system()
        auto_completion_system.disable()
        
        return {
            "success": True,
            "message": "Auto-completion disabled"
        }
    except Exception as e:
        debug_log(f"Error disabling auto-completion: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reset-session")
async def reset_auto_completion_session():
    """Reset session auto-completion"""
    try:
        auto_completion_system = get_auto_completion_system()
        auto_completion_system.reset_session()
        
        return {
            "success": True,
            "message": "Auto-completion session reset"
        }
    except Exception as e:
        debug_log(f"Error resetting auto-completion session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test-trigger")
async def test_trigger(request: TriggerTestRequest):
    """Test trigger auto-completion"""
    try:
        auto_completion_system = get_auto_completion_system()
        triggered = auto_completion_system.trigger_manager.check_triggers(request.text)
        
        result = {
            "text": request.text,
            "triggered": len(triggered) > 0,
            "trigger_count": len(triggered),
            "triggers": [
                {
                    "id": t.trigger_id,
                    "type": t.trigger_type.value,
                    "description": t.description,
                    "pattern": t.pattern
                }
                for t in triggered
            ]
        }
        
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        debug_log(f"Error testing trigger: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/config")
async def update_auto_completion_config(request: AutoCompletionConfigRequest):
    """Update konfigurasi auto-completion"""
    try:
        auto_completion_system = get_auto_completion_system()
        
        # Update config dengan nilai yang diberikan
        config_updates = {}
        if request.auto_trigger_delay is not None:
            config_updates["auto_trigger_delay"] = request.auto_trigger_delay
        if request.max_triggers_per_session is not None:
            config_updates["max_triggers_per_session"] = request.max_triggers_per_session
        if request.cooldown_period is not None:
            config_updates["cooldown_period"] = request.cooldown_period
        if request.require_confirmation is not None:
            config_updates["require_confirmation"] = request.require_confirmation
        
        auto_completion_system.update_config(**config_updates)
        
        return {
            "success": True,
            "message": "Configuration updated",
            "data": auto_completion_system.get_config().__dict__
        }
    except Exception as e:
        debug_log(f"Error updating auto-completion config: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history")
async def get_trigger_history(limit: int = 50):
    """Mendapatkan history trigger"""
    try:
        auto_completion_system = get_auto_completion_system()
        history = auto_completion_system.get_trigger_history(limit)
        
        # Format history untuk response
        formatted_history = []
        for record in history:
            formatted_history.append({
                "timestamp": record["timestamp"],
                "timestamp_str": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(record["timestamp"])),
                "triggers": record["triggers"],
                "text": record["text"],
                "context": record.get("context", {})
            })
        
        return {
            "success": True,
            "data": {
                "history": formatted_history,
                "total": len(formatted_history)
            }
        }
    except Exception as e:
        debug_log(f"Error getting trigger history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/history")
async def clear_trigger_history():
    """Menghapus history trigger"""
    try:
        auto_completion_system = get_auto_completion_system()
        auto_completion_system.clear_trigger_history()
        
        return {
            "success": True,
            "message": "Trigger history cleared"
        }
    except Exception as e:
        debug_log(f"Error clearing trigger history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Checkpoint routes
@router.post("/checkpoint/create")
async def create_checkpoint(request: CheckpointCreateRequest):
    """Membuat checkpoint"""
    try:
        checkpoint_integration = get_checkpoint_integration()
        
        checkpoint_id = checkpoint_integration.create_checkpoint(
            name=request.name or f"Manual Checkpoint {time.strftime('%Y-%m-%d %H:%M:%S')}",
            description=request.description,
            checkpoint_type=CheckpointType.MANUAL,
            project_directory=request.project_directory,
            tags=request.tags
        )
        
        checkpoint_info = checkpoint_integration.checkpoint_manager.get_checkpoint_info(checkpoint_id)
        
        return {
            "success": True,
            "message": f"Checkpoint created: {checkpoint_info['name']}",
            "data": {
                "checkpoint_id": checkpoint_id,
                "checkpoint_info": checkpoint_info
            }
        }
    except Exception as e:
        debug_log(f"Error creating checkpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/checkpoint/list")
async def list_checkpoints(
    project_directory: Optional[str] = "",
    checkpoint_type: Optional[str] = "",
    limit: int = 20
):
    """Mendapatkan daftar checkpoint"""
    try:
        checkpoint_integration = get_checkpoint_integration()
        
        # Parse checkpoint type
        filter_type = None
        if checkpoint_type:
            try:
                filter_type = CheckpointType(checkpoint_type.lower())
            except ValueError:
                pass
        
        # Get checkpoints
        checkpoints = checkpoint_integration.checkpoint_manager.list_checkpoints(
            checkpoint_type=filter_type,
            project_directory=project_directory if project_directory else None
        )
        
        # Limit results
        checkpoints = checkpoints[:limit]
        
        # Format results
        checkpoint_list = []
        for checkpoint in checkpoints:
            info = checkpoint_integration.checkpoint_manager.get_checkpoint_info(checkpoint.checkpoint_id)
            checkpoint_list.append(info)
        
        return {
            "success": True,
            "data": {
                "checkpoints": checkpoint_list,
                "total": len(checkpoint_list),
                "filters": {
                    "project_directory": project_directory,
                    "checkpoint_type": checkpoint_type,
                    "limit": limit
                }
            }
        }
    except Exception as e:
        debug_log(f"Error listing checkpoints: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/checkpoint/{checkpoint_id}/restore")
async def restore_checkpoint(checkpoint_id: str):
    """Restore checkpoint"""
    try:
        checkpoint_integration = get_checkpoint_integration()
        success = checkpoint_integration.restore_checkpoint(checkpoint_id)
        
        if success:
            checkpoint_info = checkpoint_integration.checkpoint_manager.get_checkpoint_info(checkpoint_id)
            return {
                "success": True,
                "message": f"Checkpoint restored: {checkpoint_info['name'] if checkpoint_info else checkpoint_id}",
                "data": {
                    "checkpoint_id": checkpoint_id,
                    "checkpoint_info": checkpoint_info
                }
            }
        else:
            return {
                "success": False,
                "message": "Failed to restore checkpoint. Checkpoint may not exist or be corrupted."
            }
    except Exception as e:
        debug_log(f"Error restoring checkpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/checkpoint/{checkpoint_id}")
async def delete_checkpoint(checkpoint_id: str):
    """Menghapus checkpoint"""
    try:
        checkpoint_integration = get_checkpoint_integration()
        success = checkpoint_integration.checkpoint_manager.delete_checkpoint(checkpoint_id)
        
        if success:
            return {
                "success": True,
                "message": f"Checkpoint deleted: {checkpoint_id}"
            }
        else:
            return {
                "success": False,
                "message": "Checkpoint not found"
            }
    except Exception as e:
        debug_log(f"Error deleting checkpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/checkpoint/auto/enable")
async def enable_auto_checkpoint():
    """Enable auto checkpoint"""
    try:
        checkpoint_integration = get_checkpoint_integration()
        checkpoint_integration.enable_auto_checkpoint()
        
        return {
            "success": True,
            "message": "Auto checkpoint enabled"
        }
    except Exception as e:
        debug_log(f"Error enabling auto checkpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/checkpoint/auto/disable")
async def disable_auto_checkpoint():
    """Disable auto checkpoint"""
    try:
        checkpoint_integration = get_checkpoint_integration()
        checkpoint_integration.disable_auto_checkpoint()
        
        return {
            "success": True,
            "message": "Auto checkpoint disabled"
        }
    except Exception as e:
        debug_log(f"Error disabling auto checkpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/checkpoint/auto/interval")
async def set_auto_checkpoint_interval(interval: int):
    """Set auto checkpoint interval"""
    try:
        checkpoint_integration = get_checkpoint_integration()
        checkpoint_integration.set_auto_checkpoint_interval(interval)
        
        return {
            "success": True,
            "message": f"Auto checkpoint interval set to {interval} seconds"
        }
    except Exception as e:
        debug_log(f"Error setting auto checkpoint interval: {e}")
        raise HTTPException(status_code=500, detail=str(e))
