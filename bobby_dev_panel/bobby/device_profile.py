"""
Device Profile - Detect device brand/model and recommend debloat profiles.
"""

from typing import Dict, Any, Optional
from .core import run_cmd, get_model


def detect_device_profile() -> Dict[str, Any]:
    """
    Detect device brand/model and recommend debloat profile.
    
    Returns:
        Dictionary with device profile info and recommendations
    """
    profile = {
        "brand": None,
        "model": None,
        "recommended_profile": None
    }
    
    # Get manufacturer
    stdout, _, _ = run_cmd(["adb", "shell", "getprop", "ro.product.manufacturer"], check=False)
    brand = stdout.strip().lower() if stdout.strip() else None
    profile["brand"] = brand
    
    # Get model
    model = get_model()
    if model:
        model_lower = model.lower()
        profile["model"] = model
        
        # Recommend profile based on brand/model
        if "samsung" in brand or "samsung" in model_lower:
            profile["recommended_profile"] = "samsung_light"
        elif "motorola" in brand or "moto" in model_lower:
            profile["recommended_profile"] = "motorola_light"
        else:
            profile["recommended_profile"] = "generic_light"
    
    return profile
