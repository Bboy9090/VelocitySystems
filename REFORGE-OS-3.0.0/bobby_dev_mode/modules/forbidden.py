"""Forbidden Chamber module - security and encryption analysis."""
from ..adb_utils import adb, check_device


def run_forbidden(profile: dict) -> None:
    """Run security and encryption analysis."""
    if not check_device():
        print("ERROR: No Android device connected via ADB")
        return
    
    print("=== FORBIDDEN CHAMBER – SECURITY / ENCRYPTION ===")
    print()
    
    # Encryption state
    print("--- Encryption State ---")
    crypto = adb(["shell", "getprop", "ro.crypto.state"]).strip()
    crypto_type = adb(["shell", "getprop", "ro.crypto.type"]).strip()
    print(f"Crypto State: {crypto}")
    print(f"Crypto Type: {crypto_type}")
    print()
    
    # Security patch
    print("--- Security Patch ---")
    patch = adb(["shell", "getprop", "ro.build.version.security_patch"]).strip()
    print(f"Security Patch: {patch}")
    print()
    
    # Partitions
    print("--- Partitions ---")
    mounts = adb(["shell", "mount"]).strip()
    print(mounts[:500])  # First 500 chars
    print()
