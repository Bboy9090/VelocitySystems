"""Dark Lab module - performance and thermal testing."""
from ..adb_utils import adb, check_device
import time


def run_dark_lab(profile: dict) -> None:
    """Run performance and thermal tests."""
    if not check_device():
        print("ERROR: No Android device connected via ADB")
        return
    
    print("=== DARK LAB – THERMAL / I/O / CPU ===")
    print()
    
    # Thermal paths from profile
    thermal_paths = profile.get("thermal_paths", [])
    if thermal_paths:
        print("--- Thermal Zones ---")
        for path in thermal_paths:
            temp = adb(["shell", "cat", path]).strip()
            print(f"{path}: {temp}")
        print()
    
    # CPU info
    print("--- CPU Info ---")
    cpu_info = adb(["shell", "cat", "/proc/cpuinfo", "|", "head", "-20"]).strip()
    print(cpu_info)
    print()
    
    # I/O stats
    print("--- I/O Stats ---")
    io_stats = adb(["shell", "cat", "/proc/diskstats"]).strip()
    print(io_stats[:500])  # First 500 chars
    print()
