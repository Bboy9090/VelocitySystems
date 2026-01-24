"""
Intake - Full intake preset (dossier, forbidden, dark lab snapshot, logs, bench summary).
"""

import json
from datetime import datetime
from .core import log, check_device
from .platform import detect_platform, Platform
from .dossier import collect_dossier
from .forbidden import forbidden_full_scan
from .dark_lab import snapshot_top_mem, io_latency_test
from .logs_evidence import collect_basic_logs
from .report import generate_bench_summary
from .evidence import EvidenceChain


def full_intake(output_file: str = None, add_evidence: bool = True) -> dict:
    """
    Run full intake preset.
    
    Args:
        output_file: Optional file path to save JSON output
        
    Returns:
        Dictionary with full intake data
    """
    # Check for any device (Android or iOS)
    has_android = check_device(platform="android")
    has_ios = check_device(platform="ios")
    
    if not has_android and not has_ios:
        log("No device connected!", "ERROR")
        return {}
    
    platform = detect_platform()
    log(f"Detected platform: {platform.value.upper()}")
    
    log("Starting full intake...")
    
    intake_data = {
        "timestamp": datetime.now().isoformat(),
        "dossier": {},
        "forbidden": {},
        "dark_lab": {},
        "logs": {},
        "bench_summary": {}
    }
    
    # Dossier
    log("Collecting dossier...")
    intake_data["dossier"] = collect_dossier()
    
    # Forbidden (Android only)
    if platform == Platform.ANDROID:
        log("Running forbidden scan...")
        intake_data["forbidden"] = forbidden_full_scan()
    else:
        log("Forbidden scan not available on iOS (security restrictions)")
        intake_data["forbidden"] = {"message": "Not available on iOS"}
    
    # Dark Lab snapshot (Android only)
    if platform == Platform.ANDROID:
        log("Taking Dark Lab snapshot...")
        intake_data["dark_lab"] = {
            "memory_snapshot": snapshot_top_mem(),
            "io_test": io_latency_test()
        }
    else:
        log("Dark Lab tests not available on iOS (requires jailbreak)")
        intake_data["dark_lab"] = {"message": "Not available on iOS without jailbreak"}
    
    # Logs (Android only, iOS limited)
    if platform == Platform.ANDROID:
        log("Collecting logs...")
        intake_data["logs"] = collect_basic_logs()
    else:
        log("Log collection limited on iOS")
        intake_data["logs"] = {"message": "Limited log access on iOS"}
    
    # Bench summary (includes battery health, health score, performance, sensors)
    log("Generating bench summary...")
    intake_data["bench_summary"] = generate_bench_summary()
    
    # Add to evidence chain if requested
    if add_evidence:
        try:
            evidence = EvidenceChain()
            evidence.add_evidence(
                event_type="full_intake",
                data=intake_data,
                description=f"Full intake for device {intake_data.get('bench_summary', {}).get('device', {}).get('serial', 'unknown')}"
            )
            log("Intake added to evidence chain")
        except Exception as e:
            log(f"Failed to add evidence: {e}", "WARNING")
    
    # Save to file if requested
    if output_file:
        with open(output_file, "w") as f:
            json.dump(intake_data, f, indent=2)
        log(f"Intake data saved to {output_file}")
    
    log("Full intake complete!")
    return intake_data


def intake_menu():
    """Interactive menu for intake tools."""
    while True:
        print("\n=== Intake ===")
        print("1. Full Intake (all modules)")
        print("2. Full Intake (save to file)")
        print("0. Back")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            result = full_intake()
            print("\n=== Intake Complete ===")
            print(json.dumps(result, indent=2))
        elif choice == "2":
            filename = input("Output filename (default: intake_<timestamp>.json): ").strip()
            if not filename:
                filename = f"intake_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            result = full_intake(output_file=filename)
            print(f"\nIntake saved to {filename}")
        elif choice == "0":
            break
        else:
            print("Invalid choice")
