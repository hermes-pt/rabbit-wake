"""
Sync state management for tracking sync progress
"""

import json
from datetime import datetime
from typing import Optional, Dict, Any

from wake.db import SessionLocal, SyncState


class SyncStateManager:
    """Manages sync state for resumable syncing"""
    
    @staticmethod
    def get_or_create(sync_type: str) -> SyncState:
        """Get or create sync state for a given type"""
        with SessionLocal() as db:
            state = db.query(SyncState).filter_by(sync_type=sync_type).first()
            if not state:
                state = SyncState(sync_type=sync_type)
                db.add(state)
                db.commit()
                db.refresh(state)
            return state
    
    @staticmethod
    def start_sync(sync_type: str, reset: bool = False) -> SyncState:
        """Mark sync as started"""
        with SessionLocal() as db:
            state = db.query(SyncState).filter_by(sync_type=sync_type).first()
            if not state:
                state = SyncState(sync_type=sync_type)
            
            if reset:
                state.last_page = 0
                state.last_sku = None
                state.total_synced = 0
                state.error_message = None
            
            state.status = "running"
            state.started_at = datetime.now()
            state.completed_at = None
            
            db.add(state)
            db.commit()
            db.refresh(state)
            return state
    
    @staticmethod
    def update_progress(sync_type: str, page: int, last_sku: str = None, 
                       items_synced: int = 0, extra_data: Dict[str, Any] = None):
        """Update sync progress"""
        with SessionLocal() as db:
            state = db.query(SyncState).filter_by(sync_type=sync_type).first()
            if state:
                state.last_page = page
                if last_sku:
                    state.last_sku = last_sku
                state.total_synced += items_synced
                
                if extra_data:
                    state.extra_data = json.dumps(extra_data)
                
                db.commit()
    
    @staticmethod
    def complete_sync(sync_type: str, total_synced: int = None):
        """Mark sync as completed"""
        with SessionLocal() as db:
            state = db.query(SyncState).filter_by(sync_type=sync_type).first()
            if state:
                state.status = "completed"
                state.completed_at = datetime.now()
                if total_synced is not None:
                    state.total_synced = total_synced
                db.commit()
    
    @staticmethod
    def fail_sync(sync_type: str, error_message: str):
        """Mark sync as failed"""
        with SessionLocal() as db:
            state = db.query(SyncState).filter_by(sync_type=sync_type).first()
            if state:
                state.status = "failed"
                state.error_message = error_message
                db.commit()
    
    @staticmethod
    def get_resume_point(sync_type: str) -> Dict[str, Any]:
        """Get resume point for a sync type"""
        with SessionLocal() as db:
            state = db.query(SyncState).filter_by(sync_type=sync_type).first()
            if not state:
                return {"page": 1, "last_sku": None, "total_synced": 0}
            
            # If completed or idle, start from beginning
            if state.status in ["completed", "idle"]:
                return {"page": 1, "last_sku": None, "total_synced": 0}
            
            # Resume from last page
            resume_page = state.last_page + 1 if state.last_page > 0 else 1
            
            return {
                "page": resume_page,
                "last_sku": state.last_sku,
                "total_synced": state.total_synced,
                "status": state.status,
                "started_at": state.started_at,
                "extra_data": json.loads(state.extra_data) if state.extra_data else {}
            }
    
    @staticmethod
    def get_all_states() -> Dict[str, Dict[str, Any]]:
        """Get all sync states"""
        with SessionLocal() as db:
            states = db.query(SyncState).all()
            result = {}
            for state in states:
                result[state.sync_type] = {
                    "status": state.status,
                    "last_page": state.last_page,
                    "last_sku": state.last_sku,
                    "total_synced": state.total_synced,
                    "started_at": state.started_at,
                    "completed_at": state.completed_at,
                    "error_message": state.error_message
                }
            return result