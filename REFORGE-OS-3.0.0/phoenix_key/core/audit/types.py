"""
Audit Event Types - Canonical Definitions
"""
from dataclasses import dataclass
import time
from typing import Optional

@dataclass
class AuditEvent:
    """Canonical audit event - immutable after creation"""
    ts: int                    # unix timestamp
    actor: str                 # license subject or "system"
    action: str                # e.g. "run.clonezilla"
    feature: str
    result: str                # success | denied | error
    reason: Optional[str] = None
    prev_hash: Optional[str] = None
    hash: Optional[str] = None
    
    def __init__(self, actor: str, action: str, feature: str, result: str, 
                 reason: Optional[str] = None, prev_hash: Optional[str] = None):
        self.ts = int(time.time())
        self.actor = actor
        self.action = action
        self.feature = feature
        self.result = result
        self.reason = reason
        self.prev_hash = prev_hash
        self.hash = None  # Set by log.append()
