"""
License Types - Canonical Definitions
"""
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class License:
    """Canonical license object - immutable after creation"""
    license_id: str
    subject: str              # email or org identifier
    org_id: Optional[str] = None
    tier: str = "free"        # free | pro | enterprise
    seats: int = 1
    capabilities: List[str] = None
    issued_at: int = 0        # unix timestamp
    expires_at: Optional[int] = None
    issuer_id: str = ""
    env: str = "PROD"         # PROD | STAGING | DEV | AIRGAP
    
    def __post_init__(self):
        if self.capabilities is None:
            self.capabilities = []
