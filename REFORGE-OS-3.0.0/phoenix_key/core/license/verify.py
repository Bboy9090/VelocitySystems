"""
License Verification - Offline-Capable Authority
"""
import json
import hmac
import hashlib
import base64
import time
from typing import Optional
from .types import License

def verify_license(token: str, key: bytes) -> Optional[License]:
    """
    Verify a license token offline.
    
    Returns License object if valid, None otherwise.
    """
    try:
        raw = base64.urlsafe_b64decode(token.encode())
        data, sig = raw.rsplit(b".", 1)
        
        good = hmac.new(key, data, hashlib.sha256).digest()
        if not hmac.compare_digest(sig, good):
            return None
        
        payload = json.loads(data.decode())
        
        # Check expiry
        if payload.get("expires_at") and time.time() > payload["expires_at"]:
            return None
        
        return License(
            license_id=payload.get("license_id", ""),
            subject=payload.get("subject", ""),
            org_id=payload.get("org_id"),
            tier=payload.get("tier", "free"),
            seats=payload.get("seats", 1),
            capabilities=payload.get("capabilities", []),
            issued_at=payload.get("issued_at", 0),
            expires_at=payload.get("expires_at"),
            issuer_id=payload.get("issuer_id", ""),
            env=payload.get("env", "PROD")
        )
    except Exception:
        return None
