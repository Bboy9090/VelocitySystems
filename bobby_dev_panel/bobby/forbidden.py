"""
Forbidden - Deep introspection of boot/security, SELinux, encryption, partitions, battery.
"""

from typing import Dict, Any
from .core import run_cmd, log


def show_boot_security() -> Dict[str, Any]:
    """Collect boot and security information."""
    info = {}
    
    # Verified boot state
    stdout, _, _ = run_cmd(["adb", "shell", "getprop", "ro.boot.verifiedbootstate"], check=False)
    info["verified_boot_state"] = stdout.strip() if stdout.strip() else None
    
    # VBMeta state
    stdout, _, _ = run_cmd(["adb", "shell", "getprop", "ro.boot.vbmeta.device_state"], check=False)
    info["vbmeta_device_state"] = stdout.strip() if stdout.strip() else None
    
    # Bootloader lock state
    stdout, _, _ = run_cmd(["adb", "shell", "getprop", "ro.boot.flash.locked"], check=False)
    info["bootloader_locked"] = stdout.strip() if stdout.strip() else None
    
    # If bootloader_locked is empty, try alternative
    if not info["bootloader_locked"]:
        stdout, _, _ = run_cmd(["adb", "shell", "getprop", "ro.boot.veritymode"], check=False)
        info["bootloader_locked"] = stdout.strip() if stdout.strip() else None
    
    return info


def show_selinux() -> Dict[str, Any]:
    """Collect SELinux information."""
    info = {}
    
    stdout, _, _ = run_cmd(["adb", "shell", "getenforce"], check=False)
    info["enforce_mode"] = stdout.strip() if stdout.strip() else None
    
    stdout, _, _ = run_cmd(["adb", "shell", "getprop", "ro.build.selinux"], check=False)
    info["selinux_build"] = stdout.strip() if stdout.strip() else None
    
    return info


def show_encryption() -> Dict[str, Any]:
    """Collect encryption information."""
    info = {}
    
    stdout, _, _ = run_cmd(["adb", "shell", "getprop", "ro.crypto.state"], check=False)
    info["crypto_state"] = stdout.strip() if stdout.strip() else None
    
    stdout, _, _ = run_cmd(["adb", "shell", "getprop", "ro.crypto.type"], check=False)
    info["crypto_type"] = stdout.strip() if stdout.strip() else None
    
    return info


def show_partitions() -> Dict[str, Any]:
    """Collect partition information."""
    info = {}
    
    stdout, _, _ = run_cmd(["adb", "shell", "lsblk"], check=False)
    if stdout:
        info["lsblk_output"] = stdout[:500]  # First 500 chars
    
    stdout, _, _ = run_cmd(["adb", "shell", "df", "-h"], check=False)
    if stdout:
        info["df_output"] = stdout[:500]
    
    return info


def show_battery() -> Dict[str, Any]:
    """Collect detailed battery information."""
    info = {}
    
    stdout, _, _ = run_cmd(["adb", "shell", "dumpsys", "battery"], check=False)
    if stdout:
        for line in stdout.split("\n"):
            line = line.strip()
            if ":" in line:
                key, val = line.split(":", 1)
                key = key.strip().lower().replace(" ", "_")
                val = val.strip()
                try:
                    if val.isdigit():
                        info[key] = int(val)
                    elif val.replace(".", "").replace("-", "").isdigit():
                        info[key] = float(val)
                    else:
                        info[key] = val
                except:
                    info[key] = val
    
    return info


def forbidden_full_scan() -> Dict[str, Any]:
    """Run full forbidden scan."""
    log("Running forbidden full scan...")
    
    return {
        "boot_security": show_boot_security(),
        "selinux": show_selinux(),
        "encryption": show_encryption(),
        "partitions": show_partitions(),
        "battery": show_battery()
    }


def forbidden_menu():
    """Interactive menu for Forbidden tools."""
    while True:
        print("\n=== Forbidden ===")
        print("1. Boot/Security Info")
        print("2. SELinux Info")
        print("3. Encryption Info")
        print("4. Partitions Info")
        print("5. Battery Info")
        print("6. Full Scan")
        print("0. Back")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            result = show_boot_security()
            print(f"\nResult: {result}")
        elif choice == "2":
            result = show_selinux()
            print(f"\nResult: {result}")
        elif choice == "3":
            result = show_encryption()
            print(f"\nResult: {result}")
        elif choice == "4":
            result = show_partitions()
            print(f"\nResult: {result}")
        elif choice == "5":
            result = show_battery()
            print(f"\nResult: {result}")
        elif choice == "6":
            result = forbidden_full_scan()
            print(f"\nResult: {result}")
        elif choice == "0":
            break
        else:
            print("Invalid choice")
