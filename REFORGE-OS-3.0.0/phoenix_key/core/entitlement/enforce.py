"""
Entitlement Enforcement - Feature Gating Authority
"""
import json
import pathlib
from typing import Dict, List

# Load matrix once
_MATRIX: Dict[str, List[str]] = {}

def _load_matrix():
    """Load entitlement matrix from JSON"""
    global _MATRIX
    if _MATRIX:
        return
    
    matrix_path = pathlib.Path(__file__).parent / "matrix.json"
    with open(matrix_path, 'r') as f:
        _MATRIX.update(json.load(f))

def is_allowed(feature: str, tier: str) -> bool:
    """
    Check if feature is allowed for tier.
    
    Returns True if:
    - Tier has "*" (all features)
    - Feature is explicitly listed for tier
    """
    _load_matrix()
    
    allowed = _MATRIX.get(tier, [])
    
    # Wildcard means all features
    if "*" in allowed:
        return True
    
    return feature in allowed

def get_capabilities(tier: str) -> List[str]:
    """Get list of capabilities for tier"""
    _load_matrix()
    return _MATRIX.get(tier, [])
