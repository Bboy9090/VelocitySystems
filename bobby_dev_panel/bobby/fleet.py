"""
Fleet Management - Multi-device operations, batch processing, device comparison.
Revolutionary feature: Enterprise-scale device management.
"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from .core import run_cmd, log, get_serial
from .report import generate_bench_summary
from .history import DeviceHistory


class FleetManager:
    """Manage multiple devices simultaneously."""
    
    def __init__(self):
        """Initialize fleet manager."""
        self.history = DeviceHistory()
    
    def list_devices(self) -> List[Dict[str, Any]]:
        """
        List all connected devices.
        
        Returns:
            List of device information dictionaries
        """
        devices = []
        stdout, _, code = run_cmd(["adb", "devices", "-l"], check=False)
        
        if code == 0 and stdout:
            lines = stdout.strip().split("\n")[1:]  # Skip header
            for line in lines:
                if line.strip() and "device" in line:
                    parts = line.split()
                    if len(parts) >= 2:
                        serial = parts[0]
                        model_info = " ".join(parts[2:]) if len(parts) > 2 else ""
                        
                        # Get model
                        model_stdout, _, _ = run_cmd(["adb", "-s", serial, "shell", "getprop", "ro.product.model"], check=False)
                        model = model_stdout.strip() if model_stdout.strip() else "Unknown"
                        
                        devices.append({
                            "serial": serial,
                            "model": model,
                            "status": "device",
                            "info": model_info
                        })
        
        return devices
    
    def batch_intake(self, device_serials: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Run intake on multiple devices.
        
        Args:
            device_serials: List of device serials (None for all connected)
            
        Returns:
            Dictionary with results for each device
        """
        if device_serials is None:
            devices = self.list_devices()
            device_serials = [d["serial"] for d in devices]
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "devices_processed": 0,
            "devices_failed": 0,
            "results": {}
        }
        
        for serial in device_serials:
            log(f"Processing device: {serial}")
            try:
                # Switch to device
                run_cmd(["adb", "-s", serial, "wait-for-device"], check=False)
                
                # Generate summary with device serial
                summary = generate_bench_summary(device_serial=serial)
                
                # Save to history
                snapshot_id = self.history.save_snapshot(device_serial=serial)
                
                results["results"][serial] = {
                    "status": "success",
                    "snapshot_id": snapshot_id,
                    "summary": summary
                }
                results["devices_processed"] += 1
                
            except Exception as e:
                log(f"Failed to process {serial}: {e}", "ERROR")
                results["results"][serial] = {
                    "status": "failed",
                    "error": str(e)
                }
                results["devices_failed"] += 1
        
        return results
    
    def compare_devices(self, device_serials: List[str]) -> Dict[str, Any]:
        """
        Compare multiple devices.
        
        Args:
            device_serials: List of device serials to compare
            
        Returns:
            Comparison dictionary
        """
        comparison = {
            "timestamp": datetime.now().isoformat(),
            "devices": device_serials,
            "comparison": {}
        }
        
        device_data = {}
        
        for serial in device_serials:
            # Get latest snapshot
            snapshots = self.history.get_snapshots(device_serial=serial, limit=1)
            if snapshots:
                device_data[serial] = snapshots[0]["snapshot_data"]
        
        if not device_data:
            return {"error": "No data available for comparison"}
        
        # Compare key metrics
        metrics = [
            ("health_score", "overall"),
            ("battery_health", "percent_estimate"),
            ("performance", "io_grade"),
            ("performance", "avg_mbps"),
        ]
        
        for section, key in metrics:
            comparison["comparison"][f"{section}.{key}"] = {}
            for serial, data in device_data.items():
                value = data.get(section, {}).get(key)
                comparison["comparison"][f"{section}.{key}"][serial] = value
        
        # Find best/worst
        health_scores = {}
        for serial, data in device_data.items():
            health_scores[serial] = data.get("health_score", {}).get("overall", 0)
        
        if health_scores:
            best_serial = max(health_scores, key=health_scores.get)
            worst_serial = min(health_scores, key=health_scores.get)
            
            comparison["best_device"] = {
                "serial": best_serial,
                "health_score": health_scores[best_serial]
            }
            comparison["worst_device"] = {
                "serial": worst_serial,
                "health_score": health_scores[worst_serial]
            }
        
        return comparison
    
    def fleet_dashboard(self) -> Dict[str, Any]:
        """
        Generate fleet-wide dashboard.
        
        Returns:
            Dashboard dictionary with fleet statistics
        """
        devices = self.list_devices()
        
        dashboard = {
            "timestamp": datetime.now().isoformat(),
            "total_devices": len(devices),
            "devices": [],
            "fleet_stats": {
                "avg_health_score": 0,
                "devices_critical": 0,
                "devices_healthy": 0
            }
        }
        
        health_scores = []
        
        for device in devices:
            serial = device["serial"]
            snapshots = self.history.get_snapshots(device_serial=serial, limit=1)
            
            device_info = {
                "serial": serial,
                "model": device["model"],
                "status": device["status"]
            }
            
            if snapshots:
                snapshot = snapshots[0]
                health_score = snapshot.get("health_score_overall")
                device_info["health_score"] = health_score
                device_info["battery_health"] = snapshot.get("battery_health_percent")
                device_info["last_snapshot"] = snapshot.get("timestamp")
                
                if health_score is not None:
                    health_scores.append(health_score)
                    if health_score < 60:
                        dashboard["fleet_stats"]["devices_critical"] += 1
                    elif health_score >= 80:
                        dashboard["fleet_stats"]["devices_healthy"] += 1
            
            dashboard["devices"].append(device_info)
        
        if health_scores:
            dashboard["fleet_stats"]["avg_health_score"] = round(
                sum(health_scores) / len(health_scores), 1
            )
        
        return dashboard


def fleet_menu():
    """Interactive menu for fleet management."""
    fleet = FleetManager()
    
    while True:
        print("\n=== Fleet Management ===")
        print("1. List Connected Devices")
        print("2. Batch Intake (All Devices)")
        print("3. Compare Devices")
        print("4. Fleet Dashboard")
        print("0. Back")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            devices = fleet.list_devices()
            print(f"\nFound {len(devices)} device(s):")
            for device in devices:
                print(f"  {device['serial']} - {device['model']}")
        elif choice == "2":
            print("\nRunning batch intake on all devices...")
            results = fleet.batch_intake()
            print(f"\nProcessed: {results['devices_processed']}")
            print(f"Failed: {results['devices_failed']}")
        elif choice == "3":
            devices = fleet.list_devices()
            if len(devices) < 2:
                print("\nNeed at least 2 devices to compare")
            else:
                print("\nAvailable devices:")
                for i, device in enumerate(devices):
                    print(f"{i+1}. {device['serial']} - {device['model']}")
                selected = input("\nEnter device serials (comma-separated): ").strip().split(",")
                selected = [s.strip() for s in selected]
                comparison = fleet.compare_devices(selected)
                print(f"\nComparison: {json.dumps(comparison, indent=2)}")
        elif choice == "4":
            dashboard = fleet.fleet_dashboard()
            print(f"\nFleet Dashboard:")
            print(f"Total Devices: {dashboard['total_devices']}")
            print(f"Avg Health Score: {dashboard['fleet_stats']['avg_health_score']}")
            print(f"Critical: {dashboard['fleet_stats']['devices_critical']}")
            print(f"Healthy: {dashboard['fleet_stats']['devices_healthy']}")
        elif choice == "0":
            break
        else:
            print("Invalid choice")
