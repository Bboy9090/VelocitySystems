"""
Warhammer - Debloat Android devices with preset profiles.
"""

from typing import Dict, Any, List
from .core import run_cmd, log


# Debloat profiles
DEBLOAT_PROFILES = {
    "samsung_light": {
        "name": "Samsung Light",
        "packages": [
            "com.samsung.android.bixby.agent",
            "com.samsung.android.bixby.wakeup",
            "com.samsung.android.app.spage"
        ]
    },
    "samsung_aggressive": {
        "name": "Samsung Aggressive",
        "packages": [
            "com.samsung.android.bixby.agent",
            "com.samsung.android.bixby.wakeup",
            "com.samsung.android.app.spage",
            "com.samsung.android.app.sbrowser",
            "com.samsung.android.email.provider"
        ]
    },
    "motorola_light": {
        "name": "Motorola Light",
        "packages": [
            "com.motorola.moto",
            "com.motorola.timeweatherwidget"
        ]
    },
    "generic_light": {
        "name": "Generic Light",
        "packages": []
    }
}


def show_profiles():
    """Display available debloat profiles."""
    print("\n=== Available Debloat Profiles ===")
    for key, profile in DEBLOAT_PROFILES.items():
        print(f"\n{key}: {profile['name']}")
        print(f"  Packages: {len(profile['packages'])}")


def preview_profile(profile_key: str) -> List[str]:
    """Preview packages that would be disabled in a profile."""
    profile = DEBLOAT_PROFILES.get(profile_key)
    if not profile:
        log(f"Profile not found: {profile_key}", "ERROR")
        return []
    return profile.get("packages", [])


def apply_profile(profile_key: str, dry_run: bool = True) -> Dict[str, Any]:
    """
    Apply a debloat profile.
    
    Args:
        profile_key: Profile key to apply
        dry_run: If True, only preview changes
        
    Returns:
        Dictionary with results
    """
    profile = DEBLOAT_PROFILES.get(profile_key)
    if not profile:
        return {"error": f"Profile not found: {profile_key}"}
    
    packages = profile.get("packages", [])
    results = {
        "profile": profile_key,
        "dry_run": dry_run,
        "packages": [],
        "success_count": 0,
        "failed_count": 0
    }
    
    for pkg in packages:
        if dry_run:
            log(f"[DRY RUN] Would disable: {pkg}")
            results["packages"].append({"package": pkg, "status": "would_disable"})
        else:
            stdout, stderr, code = run_cmd(["adb", "shell", "pm", "disable-user", pkg], check=False)
            if code == 0:
                log(f"Disabled: {pkg}")
                results["packages"].append({"package": pkg, "status": "disabled"})
                results["success_count"] += 1
            else:
                log(f"Failed to disable: {pkg}", "ERROR")
                results["packages"].append({"package": pkg, "status": "failed"})
                results["failed_count"] += 1
    
    return results


def warhammer_menu():
    """Interactive menu for Warhammer tools."""
    while True:
        print("\n=== Warhammer (Debloat) ===")
        print("1. Show Profiles")
        print("2. Preview Profile")
        print("3. Apply Profile (Dry Run)")
        print("4. Apply Profile (Live)")
        print("0. Back")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            show_profiles()
        elif choice == "2":
            profile_key = input("Profile key: ").strip()
            packages = preview_profile(profile_key)
            print(f"\nPackages: {packages}")
        elif choice == "3":
            profile_key = input("Profile key: ").strip()
            result = apply_profile(profile_key, dry_run=True)
            print(f"\nResult: {result}")
        elif choice == "4":
            profile_key = input("Profile key: ").strip()
            confirm = input("Are you sure? (yes/no): ").strip().lower()
            if confirm == "yes":
                result = apply_profile(profile_key, dry_run=False)
                print(f"\nResult: {result}")
            else:
                print("Cancelled")
        elif choice == "0":
            break
        else:
            print("Invalid choice")
