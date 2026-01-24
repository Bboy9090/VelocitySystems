"""
Advanced Forensics - Deep memory analysis, app behavior tracking, security threat detection.
Revolutionary feature: Enterprise-grade forensics capabilities.
"""

import re
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from .core import run_cmd, log


class ForensicsEngine:
    """Advanced forensics analysis engine."""
    
    def analyze_memory(self) -> Dict[str, Any]:
        """
        Analyze device memory for anomalies and security issues.
        
        Returns:
            Memory analysis dictionary
        """
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "memory_info": {},
            "processes": [],
            "suspicious_processes": [],
            "memory_leaks": []
        }
        
        # Get memory info
        stdout, _, _ = run_cmd(["adb", "shell", "cat", "/proc/meminfo"], check=False)
        if stdout:
            mem_info = {}
            for line in stdout.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    key = key.strip()
                    value = value.strip().split()[0] if value.strip() else "0"
                    try:
                        mem_info[key] = int(value)
                    except:
                        mem_info[key] = value
            analysis["memory_info"] = mem_info
        
        # Get process list
        stdout, _, _ = run_cmd(["adb", "shell", "ps", "-A"], check=False)
        if stdout:
            processes = []
            for line in stdout.split("\n")[1:]:  # Skip header
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 2:
                        pid = parts[1]
                        name = parts[-1] if parts else "unknown"
                        processes.append({
                            "pid": pid,
                            "name": name
                        })
            analysis["processes"] = processes[:50]  # Top 50
        
        # Detect suspicious processes
        suspicious_patterns = [
            r"root", r"su", r"busybox", r"xposed", r"magisk"
        ]
        
        for process in analysis["processes"]:
            name = process.get("name", "").lower()
            for pattern in suspicious_patterns:
                if re.search(pattern, name):
                    analysis["suspicious_processes"].append({
                        "pid": process["pid"],
                        "name": process["name"],
                        "reason": f"Matches suspicious pattern: {pattern}"
                    })
                    break
        
        return analysis
    
    def analyze_apps(self) -> Dict[str, Any]:
        """
        Analyze installed apps for security and behavior.
        
        Returns:
            App analysis dictionary
        """
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "total_apps": 0,
            "system_apps": 0,
            "user_apps": 0,
            "suspicious_apps": [],
            "high_permission_apps": []
        }
        
        # Get all packages
        stdout, _, _ = run_cmd(["adb", "shell", "pm", "list", "packages"], check=False)
        if stdout:
            packages = [p.replace("package:", "").strip() for p in stdout.split("\n") if p.strip()]
            analysis["total_apps"] = len(packages)
            
            # Categorize
            system_packages = []
            user_packages = []
            
            for pkg in packages:
                stdout2, _, _ = run_cmd(["adb", "shell", "pm", "list", "packages", "-s", pkg], check=False)
                if stdout2 and pkg in stdout2:
                    system_packages.append(pkg)
                else:
                    user_packages.append(pkg)
            
            analysis["system_apps"] = len(system_packages)
            analysis["user_apps"] = len(user_packages)
            
            # Check for suspicious packages
            suspicious_keywords = [
                "hack", "crack", "root", "bypass", "unlock", "jailbreak"
            ]
            
            for pkg in user_packages:
                pkg_lower = pkg.lower()
                for keyword in suspicious_keywords:
                    if keyword in pkg_lower:
                        analysis["suspicious_apps"].append({
                            "package": pkg,
                            "reason": f"Contains suspicious keyword: {keyword}"
                        })
                        break
        
        return analysis
    
    def detect_threats(self) -> Dict[str, Any]:
        """
        Detect security threats and vulnerabilities.
        
        Returns:
            Threat detection dictionary
        """
        threats = {
            "timestamp": datetime.now().isoformat(),
            "threats_found": 0,
            "threats": [],
            "vulnerabilities": []
        }
        
        # Check root access
        stdout, _, _ = run_cmd(["adb", "shell", "su", "-c", "id"], check=False)
        if stdout and "uid=0" in stdout:
            threats["threats"].append({
                "type": "ROOT_ACCESS",
                "severity": "CRITICAL",
                "description": "Device has root access enabled",
                "risk": "High security risk - device can be compromised"
            })
            threats["threats_found"] += 1
        
        # Check developer options
        stdout, _, _ = run_cmd(["adb", "shell", "settings", "get", "global", "development_settings_enabled"], check=False)
        if stdout and "1" in stdout:
            threats["vulnerabilities"].append({
                "type": "DEVELOPER_OPTIONS_ENABLED",
                "severity": "MEDIUM",
                "description": "Developer options are enabled",
                "risk": "May expose device to debugging attacks"
            })
        
        # Check USB debugging
        stdout, _, _ = run_cmd(["adb", "shell", "settings", "get", "global", "adb_enabled"], check=False)
        if stdout and "1" in stdout:
            threats["vulnerabilities"].append({
                "type": "USB_DEBUGGING_ENABLED",
                "severity": "MEDIUM",
                "description": "USB debugging is enabled",
                "risk": "Device can be accessed via ADB if physical access is gained"
            })
        
        # Check for known malicious packages (simplified check)
        stdout, _, _ = run_cmd(["adb", "shell", "pm", "list", "packages"], check=False)
        if stdout:
            known_malicious = ["com.android.vending.billing", "com.unknown.source"]  # Example patterns
            packages = [p.replace("package:", "").strip() for p in stdout.split("\n") if p.strip()]
            
            for pkg in packages:
                for malicious in known_malicious:
                    if malicious in pkg.lower():
                        threats["threats"].append({
                            "type": "MALICIOUS_PACKAGE",
                            "severity": "HIGH",
                            "description": f"Potentially malicious package detected: {pkg}",
                            "risk": "May contain malware or unwanted software"
                        })
                        threats["threats_found"] += 1
                        break
        
        return threats
    
    def full_forensics_scan(self) -> Dict[str, Any]:
        """
        Run complete forensics scan.
        
        Returns:
            Complete forensics report
        """
        log("Starting full forensics scan...")
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "memory_analysis": self.analyze_memory(),
            "app_analysis": self.analyze_apps(),
            "threat_detection": self.detect_threats(),
            "summary": {}
        }
        
        # Generate summary
        report["summary"] = {
            "threats_found": report["threat_detection"]["threats_found"],
            "suspicious_processes": len(report["memory_analysis"]["suspicious_processes"]),
            "suspicious_apps": len(report["app_analysis"]["suspicious_apps"]),
            "total_apps": report["app_analysis"]["total_apps"],
            "vulnerabilities": len(report["threat_detection"]["vulnerabilities"])
        }
        
        return report


def forensics_menu():
    """Interactive menu for forensics tools."""
    forensics = ForensicsEngine()
    
    while True:
        print("\n=== Advanced Forensics ===")
        print("1. Analyze Memory")
        print("2. Analyze Apps")
        print("3. Detect Threats")
        print("4. Full Forensics Scan")
        print("0. Back")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            analysis = forensics.analyze_memory()
            print(f"\nMemory Analysis: {json.dumps(analysis, indent=2)}")
        elif choice == "2":
            analysis = forensics.analyze_apps()
            print(f"\nApp Analysis: {json.dumps(analysis, indent=2)}")
        elif choice == "3":
            threats = forensics.detect_threats()
            print(f"\nThreat Detection: {json.dumps(threats, indent=2)}")
        elif choice == "4":
            report = forensics.full_forensics_scan()
            print(f"\nForensics Report: {json.dumps(report, indent=2)}")
        elif choice == "0":
            break
        else:
            print("Invalid choice")
