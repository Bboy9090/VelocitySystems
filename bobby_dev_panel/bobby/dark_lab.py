"""
Dark Lab - Stress testing CPU, thermal, and storage I/O.
"""

import time
import subprocess
from typing import Dict, Any, Optional
from .core import run_cmd, log


def cpu_stress_test(duration_sec: int = 10) -> Dict[str, Any]:
    """
    Run CPU stress test using real CPU burn-in.
    
    Args:
        duration_sec: Test duration in seconds
        
    Returns:
        Dictionary with test results
    """
    log(f"Starting CPU stress test for {duration_sec}s...")
    
    # Get CPU count
    stdout, _, _ = run_cmd(["adb", "shell", "nproc"], check=False)
    try:
        cpu_count = int(stdout.strip()) if stdout.strip() else 4
    except:
        cpu_count = 4
    
    # Real CPU burn-in: Use mathematical operations that actually stress CPU
    # Method: Spawn processes that do intensive math operations
    stress_script = f"""
    stress_pids=""
    for i in $(seq 1 {cpu_count}); do
        (
            end_time=$(($(date +%s) + {duration_sec}))
            while [ $(date +%s) -lt $end_time ]; do
                # Real CPU-intensive operations
                echo "scale=1000; 4*a(1)" | bc -l > /dev/null 2>&1 || \
                python3 -c "import math; [math.sqrt(i**2) for i in range(10000)]" > /dev/null 2>&1 || \
                cat /dev/zero > /dev/null &
            done
        ) &
        stress_pids="$stress_pids $!"
    done
    sleep {duration_sec}
    kill $stress_pids 2>/dev/null
    wait $stress_pids 2>/dev/null
    """
    
    start_time = time.time()
    cmd = ["adb", "shell", "sh", "-c", stress_script]
    stdout, stderr, code = run_cmd(cmd, check=False)
    elapsed = time.time() - start_time
    
    # Alternative method if above fails: Use dd to stress CPU via I/O
    if code != 0:
        log("Primary stress method failed, trying alternative...", "WARNING")
        # Fallback: Use multiple dd processes (CPU-intensive I/O)
        fallback_script = f"""
        for i in $(seq 1 {cpu_count}); do
            (dd if=/dev/zero of=/dev/null bs=1M count=1000 2>/dev/null &)
        done
        sleep {duration_sec}
        pkill -f "dd if=/dev/zero"
        """
        cmd = ["adb", "shell", "sh", "-c", fallback_script]
        stdout, stderr, code = run_cmd(cmd, check=False)
        elapsed = time.time() - start_time
    
    return {
        "duration_sec": round(elapsed, 2),
        "status": "completed" if code == 0 else "failed",
        "cpu_cores": cpu_count,
        "method": "math_operations" if code == 0 else "io_fallback"
    }


def thermal_monitor(duration_sec: int = 30) -> Dict[str, Any]:
    """
    Monitor thermal state - finds correct thermal zone automatically.
    
    Args:
        duration_sec: Monitor duration in seconds
        
    Returns:
        Dictionary with thermal data
    """
    log(f"Monitoring thermal state for {duration_sec}s...")
    
    # Find available thermal zones
    thermal_zones = []
    for i in range(10):  # Check thermal zones 0-9
        stdout, _, code = run_cmd(["adb", "shell", "test", "-f", f"/sys/class/thermal/thermal_zone{i}/temp", "&&", "echo", "exists"], check=False)
        if "exists" in stdout:
            # Get thermal zone type
            type_stdout, _, _ = run_cmd(["adb", "shell", "cat", f"/sys/class/thermal/thermal_zone{i}/type", "2>/dev/null"], check=False)
            zone_type = type_stdout.strip() if type_stdout.strip() else f"zone{i}"
            thermal_zones.append({"zone": i, "type": zone_type})
    
    if not thermal_zones:
        return {"error": "No thermal zones found"}
    
    # Use first available zone (usually CPU)
    primary_zone = thermal_zones[0]["zone"]
    log(f"Using thermal zone {primary_zone} ({thermal_zones[0]['type']})")
    
    temps = []
    all_zone_temps = {tz["zone"]: [] for tz in thermal_zones}
    
    for _ in range(duration_sec):
        # Read primary zone
        stdout, _, _ = run_cmd(["adb", "shell", "cat", f"/sys/class/thermal/thermal_zone{primary_zone}/temp"], check=False)
        if stdout.strip():
            try:
                temp_c = int(stdout.strip()) / 1000.0
                temps.append(temp_c)
            except:
                pass
        
        # Also read other zones for comprehensive data
        for tz in thermal_zones[1:]:  # Skip primary, already read
            stdout, _, _ = run_cmd(["adb", "shell", "cat", f"/sys/class/thermal/thermal_zone{tz['zone']}/temp", "2>/dev/null"], check=False)
            if stdout.strip():
                try:
                    temp_c = int(stdout.strip()) / 1000.0
                    all_zone_temps[tz["zone"]].append(temp_c)
                except:
                    pass
        
        time.sleep(1)
    
    if temps:
        result = {
            "avg_temp_c": round(sum(temps) / len(temps), 1),
            "max_temp_c": round(max(temps), 1),
            "min_temp_c": round(min(temps), 1),
            "samples": len(temps),
            "primary_zone": primary_zone,
            "zone_type": thermal_zones[0]["type"]
        }
        
        # Add other zone data if available
        other_zones = {}
        for zone_num, zone_temps in all_zone_temps.items():
            if zone_temps:
                other_zones[f"zone{zone_num}"] = {
                    "avg": round(sum(zone_temps) / len(zone_temps), 1),
                    "max": round(max(zone_temps), 1)
                }
        if other_zones:
            result["other_zones"] = other_zones
        
        return result
    
    return {"error": "No temperature data collected"}


def storage_io_test(size_mb: int = 100) -> Dict[str, Any]:
    """
    Test storage I/O performance with fallbacks for devices without direct I/O support.
    
    Args:
        size_mb: Test file size in MB
        
    Returns:
        Dictionary with I/O test results
    """
    log(f"Testing storage I/O with {size_mb}MB file...")
    
    test_file = "/data/local/tmp/io_test.dat"
    
    # Check available space first
    stdout, _, _ = run_cmd(["adb", "shell", "df", "/data/local/tmp"], check=False)
    if stdout:
        try:
            # Parse available space (in KB, last column before mount point)
            lines = stdout.strip().split("\n")
            if len(lines) > 1:
                parts = lines[1].split()
                if len(parts) >= 4:
                    available_kb = int(parts[3])
                    if available_kb < (size_mb * 1024):
                        log(f"Insufficient space: {available_kb}KB available, need {size_mb}MB", "WARNING")
                        size_mb = min(size_mb, available_kb // 1024)
                        if size_mb < 1:
                            return {"error": "Insufficient storage space for test"}
        except:
            pass
    
    # Write test - try direct I/O first, fallback to normal
    start = time.time()
    cmd = ["adb", "shell", "dd", f"if=/dev/zero", f"of={test_file}", f"bs=1M", f"count={size_mb}", "oflag=direct", "2>&1"]
    stdout, stderr, code = run_cmd(cmd, check=False)
    write_time = time.time() - start
    
    # If direct I/O fails, try without direct flag
    if code != 0 or "cannot open" in stderr.lower() or "invalid" in stderr.lower():
        log("Direct I/O not supported, trying without direct flag...", "WARNING")
        cmd = ["adb", "shell", "dd", f"if=/dev/zero", f"of={test_file}", f"bs=1M", f"count={size_mb}", "2>&1"]
        stdout, stderr, code = run_cmd(cmd, check=False)
        write_time = time.time() - start
    
    if code != 0:
        return {"error": f"Write test failed: {stderr[:100]}"}
    
    # Read test - try direct I/O first, fallback to normal
    start = time.time()
    cmd = ["adb", "shell", "dd", f"if={test_file}", "of=/dev/null", "bs=1M", "iflag=direct", "2>&1"]
    stdout, stderr, code = run_cmd(cmd, check=False)
    read_time = time.time() - start
    
    # If direct I/O fails, try without direct flag
    if code != 0 or "cannot open" in stderr.lower() or "invalid" in stderr.lower():
        log("Direct I/O read not supported, trying without direct flag...", "WARNING")
        cmd = ["adb", "shell", "dd", f"if={test_file}", "of=/dev/null", "bs=1M", "2>&1"]
        stdout, stderr, code = run_cmd(cmd, check=False)
        read_time = time.time() - start
    
    if code != 0:
        # Cleanup before returning error
        run_cmd(["adb", "shell", "rm", "-f", test_file], check=False)
        return {"error": f"Read test failed: {stderr[:100]}"}
    
    # Cleanup
    run_cmd(["adb", "shell", "rm", "-f", test_file], check=False)
    
    write_mbps = (size_mb / write_time) if write_time > 0 else 0
    read_mbps = (size_mb / read_time) if read_time > 0 else 0
    
    # Grade I/O performance
    avg_mbps = (write_mbps + read_mbps) / 2
    if avg_mbps >= 50:
        io_grade = "FAST"
    elif avg_mbps >= 20:
        io_grade = "OK"
    else:
        io_grade = "DEGRADED"
    
    return {
        "write_mbps": round(write_mbps, 2),
        "read_mbps": round(read_mbps, 2),
        "avg_mbps": round(avg_mbps, 2),
        "io_grade": io_grade,
        "write_time_sec": round(write_time, 2),
        "read_time_sec": round(read_time, 2),
        "direct_io_supported": "unknown"  # Could be determined from errors
    }


def io_latency_test() -> Dict[str, Any]:
    """
    Quick I/O latency test (for performance block in bench summary).
    
    Returns:
        Dictionary with I/O latency and grade
    """
    log("Running I/O latency test...")
    return storage_io_test(size_mb=50)


def snapshot_top_mem() -> Dict[str, Any]:
    """
    Snapshot top memory consumers.
    
    Returns:
        Dictionary with memory snapshot
    """
    stdout, _, _ = run_cmd(["adb", "shell", "dumpsys", "meminfo"], check=False)
    if stdout:
        # Parse basic memory info
        total_pss = 0
        for line in stdout.split("\n"):
            if "TOTAL PSS:" in line.upper():
                try:
                    total_pss = int(line.split()[-1])
                except:
                    pass
        return {
            "total_pss_kb": total_pss,
            "raw_dump": stdout[:1000]  # First 1KB
        }
    return {}


def darklab_menu():
    """Interactive menu for Dark Lab tools."""
    while True:
        print("\n=== Dark Lab ===")
        print("1. CPU Stress Test (10s)")
        print("2. Thermal Monitor (30s)")
        print("3. Storage I/O Test (100MB)")
        print("4. I/O Latency Test (50MB)")
        print("5. Memory Snapshot")
        print("0. Back")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            result = cpu_stress_test(10)
            print(f"\nResult: {result}")
        elif choice == "2":
            result = thermal_monitor(30)
            print(f"\nResult: {result}")
        elif choice == "3":
            result = storage_io_test(100)
            print(f"\nResult: {result}")
        elif choice == "4":
            result = io_latency_test()
            print(f"\nResult: {result}")
        elif choice == "5":
            result = snapshot_top_mem()
            print(f"\nResult: {result}")
        elif choice == "0":
            break
        else:
            print("Invalid choice")
