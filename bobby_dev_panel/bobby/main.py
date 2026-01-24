#!/usr/bin/env python3
"""
Bobby Dev Panel - Main entry point
Device Diagnostics & Control for Android/iOS
"""

import sys
from .core import check_device, log
from .platform import detect_platform, detect_all_devices, Platform, check_platform_tools
from .dossier import dossier_menu
from .warhammer import warhammer_menu
from .dark_lab import darklab_menu
from .forbidden import forbidden_menu
from .logs_evidence import collect_basic_logs
from .bootloader_helper import bootloader_menu
from .intake import intake_menu
from .report import report_menu
from .history import history_menu
from .evidence import evidence_menu
from .export import export_menu
from .monitor import monitor_menu
from .optimize import optimize_menu
from .ai_engine import ai_menu
from .fleet import fleet_menu
from .forensics import forensics_menu


def main_menu():
    """Main interactive menu."""
    while True:
        # Detect platform
        platform = detect_platform()
        platform_str = platform.value.upper() if platform != Platform.UNKNOWN else "UNKNOWN"
        
        print("\n" + "=" * 50)
        print("  BOBBY DEV PANEL - Pandora Codex")
        print(f"  Platform: {platform_str}")
        print("=" * 50)
        print("1. Dossier (Device Info)")
        print("2. Warhammer (Debloat)")
        print("3. Dark Lab (Stress Tests)")
        print("4. Forbidden (Deep Introspection)")
        print("5. Logs & Evidence")
        print("6. Bootloader Helper")
        print("7. Intake (Full Preset)")
        print("8. Report (Bench Summary)")
        print("9. History (Device Tracking)")
        print("10. Evidence (Immutable Logs)")
        print("11. Export (HTML/CSV Reports)")
        print("12. Monitor (Real-time Metrics)")
        print("13. Optimize (Recommendations)")
        print("14. AI Engine (Predictive Analytics)")
        print("15. Fleet Management (Multi-Device)")
        print("16. Forensics (Advanced Analysis)")
        print("0. Exit")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            dossier_menu()
        elif choice == "2":
            warhammer_menu()
        elif choice == "3":
            darklab_menu()
        elif choice == "4":
            forbidden_menu()
        elif choice == "5":
            result = collect_basic_logs()
            print(f"\nLogs: {result}")
        elif choice == "6":
            bootloader_menu()
        elif choice == "7":
            intake_menu()
        elif choice == "8":
            report_menu()
        elif choice == "9":
            history_menu()
        elif choice == "10":
            evidence_menu()
        elif choice == "11":
            export_menu()
        elif choice == "12":
            monitor_menu()
        elif choice == "13":
            optimize_menu()
        elif choice == "14":
            ai_menu()
        elif choice == "15":
            fleet_menu()
        elif choice == "16":
            forensics_menu()
        elif choice == "0":
            print("\nExiting...")
            break
        else:
            print("Invalid choice")


def main():
    """Main entry point."""
    # Check for any device (Android or iOS)
    has_android = check_device(platform="android")
    has_ios = check_device(platform="ios")
    
    if not has_android and not has_ios:
        log("No device connected!", "ERROR")
        log("Please connect an Android device (with USB debugging) or iOS device", "ERROR")
        
        # Check what tools are available
        tools = check_platform_tools()
        if not tools["adb"] and not tools["ideviceinfo"]:
            log("\nRequired tools not found:", "ERROR")
            if not tools["adb"]:
                log("  - ADB (Android Debug Bridge) not installed", "ERROR")
            if not tools["ideviceinfo"]:
                log("  - libimobiledevice not installed (for iOS support)", "ERROR")
            log("\nInstall instructions:", "INFO")
            log("  Android: https://developer.android.com/studio/releases/platform-tools", "INFO")
            log("  iOS: brew install libimobiledevice (macOS) or apt-get install libimobiledevice (Linux)", "INFO")
        sys.exit(1)
    
    # Show detected devices
    devices = detect_all_devices()
    if devices:
        log(f"\nDetected {len(devices)} device(s):", "INFO")
        for device in devices:
            log(f"  - {device['platform'].upper()}: {device['model']} ({device['serial'][:20]}...)", "INFO")
    
    main_menu()


if __name__ == "__main__":
    main()
