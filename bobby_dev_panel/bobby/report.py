"""
Report generation - Bench summary JSON with battery health and health score.
"""

import json
from datetime import datetime
from typing import Dict, Any, Optional
from .core import run_cmd, log
from .dossier import collect_dossier
from .forbidden import show_boot_security, show_battery
from .dark_lab import io_latency_test
from .sensors import get_sensor_health_summary
from .platform import detect_platform, Platform
from .ios_dossier import get_ios_battery_info, get_ios_security_info


def _get_battery_snapshot() -> Dict[str, Any]:
    """Get current battery snapshot."""
    return show_battery()


def _estimate_battery_health(batt: dict) -> dict:
    """
    Estimate battery health from battery data.
    
    Args:
        batt: Battery data dictionary
        
    Returns:
        Dictionary with battery health estimate
    """
    design = batt.get("charge_full_design")
    full = batt.get("charge_full")
    cycles_raw = batt.get("cycle_count")

    health_percent = None
    cycles = None

    def _to_float(x):
        try:
            return float(str(x).strip())
        except Exception:
            return None

    design_f = _to_float(design)
    full_f = _to_float(full)
    cycles_f = _to_float(cycles_raw)

    if design_f and full_f and design_f > 0:
        ratio = full_f / design_f
        ratio = max(0.0, min(ratio, 1.1))
        health_percent = int(ratio * 100)

    if cycles_f is not None:
        cycles = int(cycles_f)

    if health_percent is None:
        condition = "UNKNOWN"
    elif health_percent >= 90:
        condition = "EXCELLENT"
    elif health_percent >= 80:
        condition = "GOOD"
    elif health_percent >= 70:
        condition = "FAIR"
    elif health_percent >= 60:
        condition = "WEAK"
    else:
        condition = "POOR"

    cycle_hint = None
    if cycles is not None:
        if cycles >= 800:
            cycle_hint = "VERY_HIGH"
        elif cycles >= 500:
            cycle_hint = "HIGH"
        elif cycles >= 300:
            cycle_hint = "MODERATE"
        else:
            cycle_hint = "LOW"

    out = {
        "percent_estimate": health_percent,
        "condition": condition,
    }
    if cycles is not None:
        out["cycle_count"] = cycles
    if cycle_hint is not None:
        out["cycle_hint"] = cycle_hint

    if "level" in batt and "scale" in batt:
        try:
            out["current_level_percent"] = int(
                (batt["level"] / batt["scale"]) * 100
            )
        except Exception:
            pass
    if "temperature_c" in batt:
        out["temperature_c"] = batt["temperature_c"]

    return out


def _compute_health_score(summary: dict) -> dict:
    """
    Compute overall health score and sub-scores.
    
    Args:
        summary: Bench summary dictionary
        
    Returns:
        Dictionary with health scores
    """
    battery_score = 75
    security_score = 85
    performance_score = 80
    sensors_score = 80

    # Battery score
    bh = summary.get("battery_health", {})
    hp = bh.get("percent_estimate")
    if isinstance(hp, int):
        battery_score = max(20, min(hp, 100))

    # Security score
    sec = summary.get("security", {})
    verified = sec.get("verified_boot_state")
    vbmeta_state = sec.get("vbmeta_device_state")
    bootlock = sec.get("bootloader_locked")

    security_score = 90
    if verified and verified.lower() != "green":
        security_score = 70
    if vbmeta_state and vbmeta_state.lower() != "locked":
        security_score = min(security_score, 70)
    if bootlock and bootlock.strip() == "0":
        security_score = 60

    # Performance score (from I/O test)
    perf = summary.get("performance", {})
    io_grade = perf.get("io_grade")
    if io_grade == "FAST":
        performance_score = 90
    elif io_grade == "OK":
        performance_score = 80
    elif io_grade == "DEGRADED":
        performance_score = 65
    else:
        performance_score = 75  # Default if no data

    # Sensors score
    sens = summary.get("sensors", {})
    dead_sensors = sens.get("dead_count", 0)
    if dead_sensors == 0:
        sensors_score = 90
    elif dead_sensors <= 2:
        sensors_score = 75
    else:
        sensors_score = 60

    # Weighted overall score
    weights = {
        "battery": 0.35,
        "security": 0.30,
        "performance": 0.20,
        "sensors": 0.15,
    }
    overall = int(
        battery_score * weights["battery"]
        + security_score * weights["security"]
        + performance_score * weights["performance"]
        + sensors_score * weights["sensors"]
    )

    return {
        "overall": overall,
        "battery": battery_score,
        "security": security_score,
        "performance": performance_score,
        "sensors": sensors_score,
    }


def generate_bench_summary(device_serial: Optional[str] = None) -> Dict[str, Any]:
    """
    Generate comprehensive bench summary JSON.
    
    Args:
        device_serial: Optional device serial to target specific device
        
    Returns:
        Dictionary with complete bench summary
    """
    log("Generating bench summary...")
    
    # Switch to specific device if serial provided
    adb_prefix = ["adb", "-s", device_serial] if device_serial else ["adb"]
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "device": {},
        "battery_health": {},
        "security": {},
        "performance": {},
        "sensors": {},
        "health_score": {}
    }
    
    # Detect platform
    platform = detect_platform()
    
    # Device info
    dossier = collect_dossier(device_serial=device_serial)
    summary["device"] = {
        "platform": platform.value,
        "model": dossier.get("identity", {}).get("model"),
        "manufacturer": dossier.get("identity", {}).get("manufacturer"),
        "serial": dossier.get("identity", {}).get("serial") or dossier.get("identity", {}).get("udid"),
        "os_version": dossier.get("build", {}).get("android_version") or dossier.get("build", {}).get("ios_version")
    }
    
    # Battery health
    if platform == Platform.IOS:
        # iOS battery
        ios_batt = get_ios_battery_info(device_serial)
        if ios_batt:
            # Convert iOS battery format to Android-like format for compatibility
            batt_snapshot = {
                "charge_full": ios_batt.get("fullchargecapacity"),
                "charge_full_design": ios_batt.get("designcapacity"),
                "level": ios_batt.get("batterycurrentcapacity"),
                "scale": 100,
                "cycle_count": ios_batt.get("cyclecount")
            }
            summary["battery_health"] = _estimate_battery_health(batt_snapshot)
        else:
            summary["battery_health"] = {"condition": "UNKNOWN", "message": "Battery data not available"}
    else:
        # Android battery
        batt_snapshot = _get_battery_snapshot()
        summary["battery_health"] = _estimate_battery_health(batt_snapshot)
    
    # Security
    if platform == Platform.IOS:
        summary["security"] = get_ios_security_info(device_serial)
    else:
        summary["security"] = show_boot_security()
    
    # Performance (I/O test) - Android only
    if platform == Platform.ANDROID:
        log("Running I/O latency test for performance block...")
        io_result = io_latency_test()
        summary["performance"] = {
            "io_grade": io_result.get("io_grade", "UNKNOWN"),
            "avg_mbps": io_result.get("avg_mbps"),
            "write_mbps": io_result.get("write_mbps"),
            "read_mbps": io_result.get("read_mbps")
        }
    else:
        # iOS doesn't support I/O tests without jailbreak
        summary["performance"] = {
            "io_grade": "N/A",
            "message": "I/O tests require jailbreak on iOS"
        }
    
    # Sensors - Android only
    if platform == Platform.ANDROID:
        log("Collecting sensor health data...")
        summary["sensors"] = get_sensor_health_summary()
    else:
        # iOS sensors not accessible without jailbreak
        summary["sensors"] = {
            "health_status": "UNKNOWN",
            "message": "Sensor data requires jailbreak on iOS"
        }
    
    # Health score
    summary["health_score"] = _compute_health_score(summary)
    
    return summary


def report_menu():
    """Interactive menu for report generation."""
    while True:
        print("\n=== Report ===")
        print("1. Generate Bench Summary (JSON)")
        print("2. Generate Bench Summary (Pretty Print)")
        print("0. Back")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            summary = generate_bench_summary()
            print(json.dumps(summary, indent=2))
        elif choice == "2":
            summary = generate_bench_summary()
            print("\n=== Bench Summary ===")
            print(json.dumps(summary, indent=2))
        elif choice == "0":
            break
        else:
            print("Invalid choice")
