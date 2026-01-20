"""Fastboot Arsenal module - fastboot/flash guidance."""
from ..adb_utils import adb, fastboot, check_device


def run_fastboot_arsenal(profile: dict) -> None:
    """Provide fastboot/flash guidance based on profile."""
    if not check_device():
        print("ERROR: No Android device connected via ADB")
        return
    
    print("=== FASTBOOT / FLASH ARSENAL ===")
    print()
    
    style = (profile.get("fastboot_style") or "standard").lower()
    print(f"Device Fastboot Style: {style}")
    print()
    
    if style == "standard":
        print("Standard fastboot commands available:")
        print("  fastboot devices")
        print("  fastboot reboot")
        print("  fastboot reboot recovery")
    elif style == "samsung":
        print("Samsung devices require Odin or SamFW tool")
        print("Standard fastboot may not be available")
    elif style == "xiaomi":
        print("Xiaomi devices may require unlocked bootloader")
        print("  fastboot oem unlock")
    else:
        print(f"Device-specific fastboot behavior: {style}")
    print()
