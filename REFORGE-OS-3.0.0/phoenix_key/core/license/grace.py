"""
License Grace Period - Grace Over Destruction
"""
import time

def in_grace(expires_at: Optional[int], grace_seconds: int = 604800) -> bool:
    """
    Check if license is in grace period (default 7 days).
    
    Grace period allows degraded operation, not bricking.
    """
    if not expires_at:
        return False
    
    now = time.time()
    if now <= expires_at:
        return False  # Not expired yet
    
    return (now - expires_at) <= grace_seconds
