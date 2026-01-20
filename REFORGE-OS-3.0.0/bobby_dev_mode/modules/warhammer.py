"""Debloat Warhammer module - safe package removal."""
from ..adb_utils import adb, check_device


def run_warhammer(profile: dict) -> None:
    """Run debloat operations based on profile."""
    if not check_device():
        print("ERROR: No Android device connected via ADB")
        return
    
    print("=== DEBLOAT WARHAMMER ===")
    print()
    
    packages = profile.get("debloat_packages", [])
    if not packages:
        print("No debloat packages specified in profile")
        return
    
    print(f"Found {len(packages)} packages to disable")
    print()
    
    for pkg in packages:
        print(f"Disabling: {pkg}")
        result = adb(["shell", "pm", "disable-user", "--user", "0", pkg])
        if "successfully" in result.lower() or "new state: disabled" in result.lower():
            print(f"  ✓ Disabled")
        else:
            print(f"  ✗ Failed or already disabled")
        print()
