"""
License Signing - Canonical Authority
"""
import json
import hmac
import hashlib
import base64
import time
from .types import License

def sign_license(lic: License, key: bytes) -> str:
    """
    Sign a license with HMAC-SHA256.
    
    Returns base64url-encoded token: <payload>.<signature>
    """
    payload = {
        "license_id": lic.license_id,
        "subject": lic.subject,
        "org_id": lic.org_id,
        "tier": lic.tier,
        "seats": lic.seats,
        "capabilities": lic.capabilities,
        "issued_at": lic.issued_at or int(time.time()),
        "expires_at": lic.expires_at,
        "issuer_id": lic.issuer_id,
        "env": lic.env
    }
    
    raw = json.dumps(payload, separators=(',', ':'), sort_keys=True).encode()
    sig = hmac.new(key, raw, hashlib.sha256).digest()
    
    token = base64.urlsafe_b64encode(raw + b"." + sig).decode()
    return token
