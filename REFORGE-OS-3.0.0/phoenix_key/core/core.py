"""
Phoenix Core - Single Entry Point
==================================
All surfaces (UI, API, CLI, USB) must call this.
No business logic outside /core.
"""
import os
import pathlib
from typing import Optional
import sys
import pathlib

# Add parent to path for imports
_parent = pathlib.Path(__file__).parent.parent
if str(_parent) not in sys.path:
    sys.path.insert(0, str(_parent))

from core.license.types import License
from core.license.verify import verify_license
from core.license.grace import in_grace
from core.license.revoke import is_revoked_issuer, is_revoked_license, load_revocation_bundle
from core.entitlement.enforce import is_allowed
from core.audit.log import append as audit_append
from core.audit.types import AuditEvent

class PhoenixCore:
    """
    Canonical authority for licensing, entitlement, and audit.
    
    This is the law. Everything else is a client.
    """
    
    def __init__(self, signing_key: bytes, audit_path: str = "/var/log/phoenix-audit.log"):
        self.signing_key = signing_key
        self.audit_path = audit_path
        
        # Load revocation bundle if exists
        revoke_path = os.getenv("PHOENIX_REVOCATION_BUNDLE", 
                                "/sysresccd/autorun/phoenix/revocations.bundle")
        load_revocation_bundle(revoke_path)
    
    def authorize(self, token: Optional[str], feature: str, actor: str = "system") -> License:
        """
        Authorize feature access.
        
        Returns License if authorized.
        Raises PermissionError if denied.
        """
        # Free tier check (no token required)
        if is_allowed(feature, "free"):
            lic = License(
                license_id="free",
                subject="free",
                tier="free",
                seats=1,
                issuer_id="system"
            )
            audit_append(
                AuditEvent(actor, f"authorize.{feature}", feature, "success"),
                self.audit_path
            )
            return lic
        
        # Require token for Pro/Enterprise features
        if not token:
            audit_append(
                AuditEvent(actor, f"authorize.{feature}", feature, "denied", "no_token"),
                self.audit_path
            )
            raise PermissionError(f"License required for feature: {feature}")
        
        # Verify license
        lic = verify_license(token, self.signing_key)
        if not lic:
            audit_append(
                AuditEvent(actor, f"authorize.{feature}", feature, "denied", "invalid_token"),
                self.audit_path
            )
            raise PermissionError("Invalid license")
        
        # Check revocation
        if is_revoked_issuer(lic.issuer_id) or is_revoked_license(lic.license_id):
            audit_append(
                AuditEvent(actor, f"authorize.{feature}", feature, "denied", "revoked"),
                self.audit_path
            )
            raise PermissionError("License revoked")
        
        # Check expiry (with grace)
        if lic.expires_at:
            if not in_grace(lic.expires_at):
                audit_append(
                    AuditEvent(actor, f"authorize.{feature}", feature, "denied", "expired"),
                    self.audit_path
                )
                raise PermissionError("License expired")
        
        # Check entitlement
        if not is_allowed(feature, lic.tier):
            audit_append(
                AuditEvent(actor, f"authorize.{feature}", feature, "denied", "insufficient_tier"),
                self.audit_path
            )
            raise PermissionError(f"Feature requires higher tier: {feature}")
        
        # Authorized
        audit_append(
            AuditEvent(actor, f"authorize.{feature}", feature, "success"),
            self.audit_path
        )
        return lic

# Global instance (initialized at startup)
_core: Optional[PhoenixCore] = None

def init_core(signing_key: bytes, audit_path: str = "/var/log/phoenix-audit.log"):
    """Initialize global core instance"""
    global _core
    _core = PhoenixCore(signing_key, audit_path)

def get_core() -> PhoenixCore:
    """Get global core instance"""
    if _core is None:
        # Fallback: use env var or default
        key_hex = os.getenv("LICENSE_SIGNING_KEY", "devkey" * 8)
        key = bytes.fromhex(key_hex) if len(key_hex) == 64 else key_hex.encode()
        init_core(key)
    return _core
