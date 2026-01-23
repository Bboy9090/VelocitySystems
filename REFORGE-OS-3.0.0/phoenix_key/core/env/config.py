"""
Environment Configuration - No Logic Drift
"""
import os

ENV = os.getenv("PHOENIX_ENV", "DEV")

CONFIG = {
    "DEV": {
        "audit": False,
        "strict_license": False,
        "grace_period": 86400 * 30  # 30 days
    },
    "STAGING": {
        "audit": True,
        "strict_license": True,
        "grace_period": 86400 * 7  # 7 days
    },
    "PROD": {
        "audit": True,
        "strict_license": True,
        "grace_period": 86400 * 7  # 7 days
    },
    "AIRGAP": {
        "audit": True,
        "strict_license": True,
        "grace_period": 86400 * 7  # 7 days
    }
}

def get_config():
    """Get configuration for current environment"""
    return CONFIG.get(ENV, CONFIG["DEV"])
