"""
Audit Logging - Tamper-Evident, Append-Only
"""
import json
import hashlib
import pathlib
from typing import Optional
from .types import AuditEvent

def hash_event(event_dict: dict) -> str:
    """Compute SHA-256 hash of event"""
    h = hashlib.sha256()
    h.update(json.dumps(event_dict, sort_keys=True).encode())
    return h.hexdigest()

def append(event: AuditEvent, path: str):
    """
    Append audit event with hash chaining.
    
    Creates tamper-evident chain:
    - Each event includes hash of previous event
    - Each event has its own hash
    - Tampering breaks the chain
    """
    # Read previous hash
    prev_hash = None
    if pathlib.Path(path).exists():
        try:
            with open(path, 'rb') as f:
                lines = f.readlines()
                if lines:
                    last = json.loads(lines[-1].decode())
                    prev_hash = last.get("hash")
        except Exception:
            pass
    
    event.prev_hash = prev_hash
    
    # Compute this event's hash
    event_dict = {
        "ts": event.ts,
        "actor": event.actor,
        "action": event.action,
        "feature": event.feature,
        "result": event.result,
        "reason": event.reason,
        "prev_hash": prev_hash
    }
    event.hash = hash_event(event_dict)
    
    # Append to log
    event_dict["hash"] = event.hash
    with open(path, "a") as f:
        f.write(json.dumps(event_dict) + "\n")
