"""
Audit Sealing - Forensic-Grade Snapshots
"""
import hashlib
import json
import pathlib
import time
from typing import Optional

def seal(path: str, output_path: Optional[str] = None) -> str:
    """
    Create tamper-evident seal of audit log.
    
    Returns seal hash.
    """
    if not pathlib.Path(path).exists():
        return ""
    
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for line in f:
            h.update(line)
    
    seal_hash = h.hexdigest()
    
    if output_path:
        seal_data = {
            "seal_hash": seal_hash,
            "timestamp": int(time.time()),
            "log_path": path
        }
        with open(output_path, 'w') as f:
            json.dump(seal_data, f)
    
    return seal_hash
