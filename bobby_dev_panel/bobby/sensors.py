"""
Sensor Health Module - Collect sensor data and assess sensor health.
"""

from typing import Dict, Any, List
from .core import run_cmd, log


def collect_sensor_data() -> Dict[str, Any]:
    """
    Collect sensor information from device and test sensor health.
    
    Returns:
        Dictionary with sensor data and health assessment
    """
    sensors_info = {
        "sensors": [],
        "dead_count": 0,
        "total_count": 0,
        "health_status": "UNKNOWN",
        "sensor_details": []
    }
    
    # Get detailed sensor list using dumpsys sensorservice
    stdout, _, _ = run_cmd(["adb", "shell", "dumpsys", "sensorservice", "|", "grep", "-A", "5", "Sensor"], check=False)
    
    # Alternative: Get sensor list from /sys/class/sensors
    sensor_list_cmd = ["adb", "shell", "ls", "/sys/class/sensors", "2>/dev/null", "||", "dumpsys", "sensorservice"]
    stdout2, _, _ = run_cmd(["adb", "shell", "dumpsys", "sensorservice"], check=False)
    
    if stdout2:
        # Parse sensor information from dumpsys output
        sensor_details = []
        current_sensor = None
        sensor_count = 0
        
        for line in stdout2.split("\n"):
            line = line.strip()
            
            # Look for sensor entries
            if "Sensor" in line and ":" in line:
                # Extract sensor name
                if "name=" in line.lower():
                    try:
                        # Parse sensor name
                        parts = line.split("name=")
                        if len(parts) > 1:
                            sensor_name = parts[1].split(",")[0].strip()
                            sensor_count += 1
                            current_sensor = {
                                "name": sensor_name,
                                "index": sensor_count,
                                "status": "unknown"
                            }
                    except:
                        pass
            
            # Look for sensor state/status
            if current_sensor:
                if "state" in line.lower() or "status" in line.lower():
                    if "active" in line.lower() or "enabled" in line.lower():
                        current_sensor["status"] = "active"
                    elif "disabled" in line.lower() or "inactive" in line.lower():
                        current_sensor["status"] = "inactive"
                
                # Check for sensor values (indicates working sensor)
                if "value" in line.lower() or "data" in line.lower():
                    current_sensor["status"] = "active"
                    sensor_details.append(current_sensor)
                    current_sensor = None
        
        # Try to actually test sensors by reading from /sys/class/sensors
        # This is device-specific but works on many devices
        for i in range(10):  # Check first 10 potential sensor paths
            sensor_path = f"/sys/class/sensors/sensor{i}"
            stdout3, _, code = run_cmd(["adb", "shell", "test", "-d", sensor_path, "&&", "echo", "exists"], check=False)
            if "exists" in stdout3:
                # Try to read sensor value
                value_stdout, _, _ = run_cmd(["adb", "shell", "cat", f"{sensor_path}/name", "2>/dev/null"], check=False)
                if value_stdout.strip():
                    sensor_name = value_stdout.strip()
                    # Try to read actual value to test if sensor works
                    value_test, _, _ = run_cmd(["adb", "shell", "cat", f"{sensor_path}/*value*", "2>/dev/null", "|", "head", "-1"], check=False)
                    sensor_status = "active" if value_test.strip() else "unknown"
                    
                    sensor_details.append({
                        "name": sensor_name,
                        "path": sensor_path,
                        "status": sensor_status,
                        "has_value": bool(value_test.strip())
                    })
        
        # Count dead sensors (those with no values or inactive status)
        dead_sensors = [s for s in sensor_details if s.get("status") == "inactive" or (s.get("status") == "unknown" and not s.get("has_value"))]
        active_sensors = [s for s in sensor_details if s.get("status") == "active" or s.get("has_value")]
        
        sensors_info["total_count"] = len(sensor_details) if sensor_details else sensor_count
        sensors_info["dead_count"] = len(dead_sensors)
        sensors_info["sensor_details"] = sensor_details[:20]  # First 20 sensors
        sensors_info["sensors"] = {
            "active": [s["name"] for s in active_sensors[:10]],
            "dead": [s["name"] for s in dead_sensors[:10]]
        }
        
        # Health status
        total = sensors_info["total_count"]
        dead = sensors_info["dead_count"]
        
        if total == 0:
            sensors_info["health_status"] = "UNKNOWN"
        elif dead == 0:
            sensors_info["health_status"] = "EXCELLENT"
        elif dead <= 2:
            sensors_info["health_status"] = "GOOD"
        elif dead <= 5:
            sensors_info["health_status"] = "FAIR"
        else:
            sensors_info["health_status"] = "POOR"
    else:
        # Fallback: Basic detection if dumpsys doesn't work
        log("Could not get detailed sensor info, using basic detection", "WARNING")
        sensors_info["health_status"] = "UNKNOWN"
        sensors_info["total_count"] = 0
    
    return sensors_info


def get_sensor_health_summary() -> Dict[str, Any]:
    """
    Get sensor health summary for bench summary JSON.
    
    Returns:
        Dictionary with sensor health summary
    """
    data = collect_sensor_data()
    
    return {
        "dead_count": data.get("dead_count", 0),
        "total_count": data.get("total_count", 0),
        "health_status": data.get("health_status", "UNKNOWN")
    }
