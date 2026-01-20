"""Recovery Operations module - recovery mode guidance."""
from ..adb_utils import adb, check_device


def run_recovery_ops(profile: dict) -> None:
    """Provide recovery operations guidance."""
    if not check_device():
        print("ERROR: No Android device connected via ADB")
        return
    
    print("=== RECOVERY OPS ===")
    print()
    
    print("To enter recovery mode:")
    print("  adb reboot recovery")
    print()
    print("Once in recovery:")
    print("  - Use volume keys to navigate")
    print("  - Use power button to select")
    print("  - Look for 'Apply update from ADB' option")
    print("  - Use 'adb sideload <file.zip>' to flash")
    print()
    print("Stock recovery typically supports:")
    print("  - Factory reset")
    print("  - Clear cache")
    print("  - ADB sideload (if available)")
    print()
