"""
License Revocation - Canonical Authority
"""
import json
import pathlib
from typing import Set

# In-memory revocation set (loaded from bundle)
REVOKED_ISSUERS: Set[str] = set()
REVOKED_LICENSES: Set[str] = set()

def load_revocation_bundle(path: str):
    """Load revocation bundle from file (offline-capable)"""
    global REVOKED_ISSUERS, REVOKED_LICENSES
    
    if not pathlib.Path(path).exists():
        return
    
    try:
        with open(path, 'r') as f:
            bundle = json.load(f)
        
        REVOKED_ISSUERS.update(bundle.get("revoked_issuers", []))
        REVOKED_LICENSES.update(bundle.get("revoked_licenses", []))
    except Exception:
        pass

def revoke_issuer(issuer_id: str):
    """Revoke an issuer key"""
    REVOKED_ISSUERS.add(issuer_id)

def revoke_license(license_id: str):
    """Revoke a license"""
    REVOKED_LICENSES.add(license_id)

def is_revoked_issuer(issuer_id: str) -> bool:
    """Check if issuer is revoked"""
    return issuer_id in REVOKED_ISSUERS

def is_revoked_license(license_id: str) -> bool:
    """Check if license is revoked"""
    return license_id in REVOKED_LICENSES
