"""
Device dossier collection - identity, build, hardware, battery info.
Supports: All Android devices + iOS devices
"""

from typing import Dict, Any, Optional
from .core import run_cmd, log
from .platform import detect_platform, Platform, get_device_info
from .ios_dossier import collect_ios_dossier


def collect_dossier(device_serial: Optional[str] = None) -> Dict[str, Any]:
    """
    Collect comprehensive device dossier (Android or iOS).
    
    Args:
        device_serial: Device serial/UDID (optional)
        
    Returns:
        Dictionary with device identity, build, hardware, battery info
    """
    # Detect platform
    platform = detect_platform()
    
    if platform == Platform.IOS:
        return collect_ios_dossier(device_serial)
    
    # Android dossier
    dossier = {
        "identity": {},
        "build": {},
        "hardware": {},
        "battery": {}
    }
    
    adb_cmd = ["adb", "-s", device_serial] if device_serial else ["adb"]
    
    # Identity
    stdout, _, _ = run_cmd(adb_cmd + ["shell", "getprop", "ro.product.model"], check=False)
    dossier["identity"]["model"] = stdout.strip() if stdout.strip() else None
    
    stdout, _, _ = run_cmd(adb_cmd + ["shell", "getprop", "ro.product.manufacturer"], check=False)
    dossier["identity"]["manufacturer"] = stdout.strip() if stdout.strip() else None
    
    if device_serial:
        dossier["identity"]["serial"] = device_serial
    else:
        stdout, _, _ = run_cmd(adb_cmd + ["get-serialno"], check=False)
        dossier["identity"]["serial"] = stdout.strip() if stdout.strip() else None
    
    # Build
    stdout, _, _ = run_cmd(adb_cmd + ["shell", "getprop", "ro.build.id"], check=False)
    dossier["build"]["build_id"] = stdout.strip() if stdout.strip() else None
    
    stdout, _, _ = run_cmd(adb_cmd + ["shell", "getprop", "ro.build.version.release"], check=False)
    dossier["build"]["android_version"] = stdout.strip() if stdout.strip() else None
    
    stdout, _, _ = run_cmd(adb_cmd + ["shell", "getprop", "ro.build.version.sdk"], check=False)
    dossier["build"]["sdk_version"] = stdout.strip() if stdout.strip() else None
    
    # Hardware
    stdout, _, _ = run_cmd(adb_cmd + ["shell", "getprop", "ro.product.cpu.abi"], check=False)
    dossier["hardware"]["cpu_abi"] = stdout.strip() if stdout.strip() else None
    
    stdout, _, _ = run_cmd(adb_cmd + ["shell", "cat", "/proc/cpuinfo"], check=False)
    if stdout:
        lines = stdout.split("\n")
        for line in lines:
            if "processor" in line.lower():
                dossier["hardware"]["cpu_cores"] = dossier["hardware"].get("cpu_cores", 0) + 1
    
    # Battery
    stdout, _, _ = run_cmd(adb_cmd + ["shell", "dumpsys", "battery"], check=False)
    if stdout:
        batt = {}
        for line in stdout.split("\n"):
            line = line.strip()
            if ":" in line:
                key, val = line.split(":", 1)
                key = key.strip().lower().replace(" ", "_")
                val = val.strip()
                try:
                    if val.isdigit():
                        batt[key] = int(val)
                    elif val.replace(".", "").isdigit():
                        batt[key] = float(val)
                    else:
                        batt[key] = val
                except:
                    batt[key] = val
        dossier["battery"] = batt
    
    return dossier


def dossier_menu():
    """Interactive menu for dossier tools."""
    while True:
        print("\n=== Dossier ===")
        print("1. Collect Full Dossier")
        print("0. Back")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            result = collect_dossier()
            print(f"\nDossier: {result}")
        elif choice == "0":
            break
        else:
            print("Invalid choice")
