"""
Optimization Recommendations - Analyze device and suggest improvements.
"""

from typing import Dict, Any, List
from .core import log
from .report import generate_bench_summary
from .dossier import collect_dossier
from .forbidden import show_boot_security


def generate_recommendations() -> List[Dict[str, Any]]:
    """
    Generate optimization recommendations based on device state.
    
    Returns:
        List of recommendation dictionaries
    """
    recommendations = []
    summary = generate_bench_summary()
    
    # Battery recommendations
    battery_health = summary.get("battery_health", {})
    battery_percent = battery_health.get("percent_estimate")
    
    if battery_percent is not None:
        if battery_percent < 60:
            recommendations.append({
                "category": "battery",
                "severity": "high",
                "title": "Battery Health Critical",
                "description": f"Battery health is at {battery_percent}%. Consider battery replacement.",
                "action": "Monitor battery degradation and plan for replacement"
            })
        elif battery_percent < 70:
            recommendations.append({
                "category": "battery",
                "severity": "medium",
                "title": "Battery Health Degrading",
                "description": f"Battery health is at {battery_percent}%. Monitor closely.",
                "action": "Optimize charging habits, avoid deep discharges"
            })
    
    cycles = battery_health.get("cycle_count")
    if cycles and cycles >= 500:
        recommendations.append({
            "category": "battery",
            "severity": "medium",
            "title": "High Cycle Count",
            "description": f"Battery has {cycles} charge cycles. Performance may degrade.",
            "action": "Consider battery replacement if experiencing issues"
        })
    
    # Performance recommendations
    performance = summary.get("performance", {})
    io_grade = performance.get("io_grade")
    
    if io_grade == "DEGRADED":
        recommendations.append({
            "category": "performance",
            "severity": "high",
            "title": "Storage Performance Degraded",
            "description": "Storage I/O performance is below acceptable levels.",
            "action": "Check storage health, consider factory reset or storage replacement"
        })
    elif io_grade == "OK":
        recommendations.append({
            "category": "performance",
            "severity": "low",
            "title": "Storage Performance Acceptable",
            "description": "Storage performance is acceptable but could be improved.",
            "action": "Consider clearing cache, removing unused apps"
        })
    
    # Security recommendations
    security = summary.get("security", {})
    verified_boot = security.get("verified_boot_state", "").lower()
    bootloader_locked = security.get("bootloader_locked", "")
    
    if verified_boot != "green":
        recommendations.append({
            "category": "security",
            "severity": "high",
            "title": "Verified Boot Not Green",
            "description": "Device verified boot state is not green. Security may be compromised.",
            "action": "Investigate boot state, consider reflashing stock firmware"
        })
    
    if bootloader_locked and bootloader_locked.strip() == "0":
        recommendations.append({
            "category": "security",
            "severity": "medium",
            "title": "Bootloader Unlocked",
            "description": "Bootloader is unlocked. Device security is reduced.",
            "action": "Lock bootloader if security is a priority (will wipe data)"
        })
    
    # Sensor recommendations
    sensors = summary.get("sensors", {})
    dead_count = sensors.get("dead_count", 0)
    
    if dead_count > 5:
        recommendations.append({
            "category": "hardware",
            "severity": "high",
            "title": "Multiple Dead Sensors",
            "description": f"{dead_count} sensors are not functioning properly.",
            "action": "Hardware inspection recommended, may need repair"
        })
    elif dead_count > 0:
        recommendations.append({
            "category": "hardware",
            "severity": "low",
            "title": "Some Sensors Not Working",
            "description": f"{dead_count} sensor(s) may not be functioning.",
            "action": "Monitor sensor functionality, may be software issue"
        })
    
    # Health score recommendations
    health_score = summary.get("health_score", {})
    overall = health_score.get("overall", 0)
    
    if overall < 60:
        recommendations.append({
            "category": "overall",
            "severity": "high",
            "title": "Overall Health Score Low",
            "description": f"Device health score is {overall}/100. Multiple issues detected.",
            "action": "Review all recommendations and address critical issues"
        })
    elif overall < 75:
        recommendations.append({
            "category": "overall",
            "severity": "medium",
            "title": "Overall Health Score Moderate",
            "description": f"Device health score is {overall}/100. Some improvements recommended.",
            "action": "Address medium and high priority recommendations"
        })
    
    return recommendations


def optimize_menu():
    """Interactive menu for optimization tools."""
    while True:
        print("\n=== Optimization Recommendations ===")
        print("1. Generate Recommendations")
        print("2. Show Recommendations by Category")
        print("3. Show Critical Recommendations Only")
        print("0. Back")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            recommendations = generate_recommendations()
            print(f"\nFound {len(recommendations)} recommendations:")
            for i, rec in enumerate(recommendations, 1):
                severity_icon = "🔴" if rec["severity"] == "high" else "🟡" if rec["severity"] == "medium" else "🟢"
                print(f"\n{i}. {severity_icon} [{rec['category'].upper()}] {rec['title']}")
                print(f"   {rec['description']}")
                print(f"   Action: {rec['action']}")
        elif choice == "2":
            recommendations = generate_recommendations()
            by_category = {}
            for rec in recommendations:
                cat = rec["category"]
                if cat not in by_category:
                    by_category[cat] = []
                by_category[cat].append(rec)
            
            for category, recs in by_category.items():
                print(f"\n=== {category.upper()} ===")
                for rec in recs:
                    severity_icon = "🔴" if rec["severity"] == "high" else "🟡" if rec["severity"] == "medium" else "🟢"
                    print(f"{severity_icon} {rec['title']}: {rec['description']}")
        elif choice == "3":
            recommendations = generate_recommendations()
            critical = [r for r in recommendations if r["severity"] == "high"]
            print(f"\nFound {len(critical)} critical recommendations:")
            for i, rec in enumerate(critical, 1):
                print(f"\n{i}. 🔴 {rec['title']}")
                print(f"   {rec['description']}")
                print(f"   Action: {rec['action']}")
        elif choice == "0":
            break
        else:
            print("Invalid choice")
