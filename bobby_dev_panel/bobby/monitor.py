"""
Real-time Monitoring - Live streaming of device metrics.
"""

import time
import re
import threading
from typing import Dict, Any, Callable, Optional
from .core import run_cmd, log
from .report import _get_battery_snapshot


class DeviceMonitor:
    """Real-time device monitoring."""
    
    def __init__(self, interval: float = 1.0):
        """
        Initialize monitor.
        
        Args:
            interval: Update interval in seconds
        """
        self.interval = interval
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.callbacks: list[Callable[[Dict[str, Any]], None]] = []
    
    def add_callback(self, callback: Callable[[Dict[str, Any]], None]):
        """Add callback function to receive updates."""
        self.callbacks.append(callback)
    
    def _monitor_loop(self):
        """Main monitoring loop."""
        while self.running:
            metrics = self._collect_metrics()
            
            for callback in self.callbacks:
                try:
                    callback(metrics)
                except Exception as e:
                    log(f"Callback error: {e}", "ERROR")
            
            time.sleep(self.interval)
    
    def _collect_metrics(self) -> Dict[str, Any]:
        """Collect current device metrics."""
        metrics = {
            "timestamp": time.time(),
            "battery": {},
            "cpu": {},
            "memory": {},
            "thermal": {}
        }
        
        # Battery
        batt = _get_battery_snapshot()
        metrics["battery"] = {
            "level": batt.get("level"),
            "scale": batt.get("scale"),
            "level_percent": int((batt.get("level", 0) / batt.get("scale", 100)) * 100) if batt.get("scale") else None,
            "temperature": batt.get("temperature"),
            "status": batt.get("status")
        }
        
        # CPU - Get actual CPU usage percentage
        # Method 1: Use /proc/stat for accurate CPU calculation
        stdout, _, _ = run_cmd(["adb", "shell", "cat", "/proc/stat"], check=False)
        if stdout:
            # Parse first line (total CPU stats)
            for line in stdout.split("\n"):
                if line.startswith("cpu "):
                    parts = line.split()
                    if len(parts) >= 8:
                        # Calculate CPU usage: (idle_time / total_time) * 100
                        # CPU stats: user, nice, system, idle, iowait, irq, softirq
                        try:
                            user = int(parts[1])
                            nice = int(parts[2])
                            system = int(parts[3])
                            idle = int(parts[4])
                            iowait = int(parts[5]) if len(parts) > 5 else 0
                            
                            total = user + nice + system + idle + iowait
                            if total > 0:
                                idle_percent = (idle / total) * 100
                                cpu_usage = 100 - idle_percent
                                metrics["cpu"]["usage_percent"] = round(cpu_usage, 1)
                        except:
                            pass
                    break
        
        # Method 2: Fallback to dumpsys cpuinfo
        if "usage_percent" not in metrics["cpu"]:
            stdout, _, _ = run_cmd(["adb", "shell", "dumpsys", "cpuinfo"], check=False)
            if stdout:
                # Look for CPU usage in dumpsys output
                for line in stdout.split("\n"):
                    if "Load:" in line or "CPU:" in line:
                        # Try to extract percentage
                        import re
                        match = re.search(r'(\d+\.?\d*)%', line)
                        if match:
                            try:
                                metrics["cpu"]["usage_percent"] = float(match.group(1))
                            except:
                                pass
                        break
        
        # Method 3: Get top process info
        stdout, _, _ = run_cmd(["adb", "shell", "top", "-n", "1", "-d", "1"], check=False)
        if stdout:
            lines = stdout.split("\n")
            if len(lines) > 1:
                # Parse top output for top process
                top_line = lines[1] if len(lines) > 1 else ""
                if top_line:
                    parts = top_line.split()
                    if len(parts) >= 2:
                        metrics["cpu"]["top_process"] = parts[-1][:50] if parts else "N/A"
                        # Try to get CPU % from top output
                        for part in parts:
                            if "%" in part:
                                try:
                                    cpu_pct = float(part.replace("%", ""))
                                    if "usage_percent" not in metrics["cpu"]:
                                        metrics["cpu"]["usage_percent"] = cpu_pct
                                except:
                                    pass
        
        # Memory
        stdout, _, _ = run_cmd(["adb", "shell", "cat", "/proc/meminfo"], check=False)
        if stdout:
            for line in stdout.split("\n"):
                if "MemTotal:" in line:
                    try:
                        metrics["memory"]["total_kb"] = int(line.split()[1])
                    except:
                        pass
                elif "MemAvailable:" in line:
                    try:
                        metrics["memory"]["available_kb"] = int(line.split()[1])
                    except:
                        pass
        
        # Thermal
        stdout, _, _ = run_cmd(["adb", "shell", "cat", "/sys/class/thermal/thermal_zone0/temp"], check=False)
        if stdout.strip():
            try:
                temp_c = int(stdout.strip()) / 1000.0
                metrics["thermal"]["temp_c"] = temp_c
            except:
                pass
        
        return metrics
    
    def start(self):
        """Start monitoring."""
        if self.running:
            log("Monitor already running", "WARNING")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
        log("Monitor started")
    
    def stop(self):
        """Stop monitoring."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2.0)
        log("Monitor stopped")
    
    def stream_console(self, duration: Optional[float] = None):
        """
        Stream metrics to console.
        
        Args:
            duration: Duration in seconds (None for infinite)
        """
        start_time = time.time()
        
        def print_metrics(metrics: Dict[str, Any]):
            batt = metrics.get("battery", {})
            thermal = metrics.get("thermal", {})
            mem = metrics.get("memory", {})
            
            print(f"\r[Battery: {batt.get('level_percent', 'N/A')}%] "
                  f"[Temp: {thermal.get('temp_c', 'N/A')}°C] "
                  f"[Mem: {mem.get('available_kb', 0) // 1024}MB free]",
                  end="", flush=True)
        
        self.add_callback(print_metrics)
        self.start()
        
        try:
            if duration:
                time.sleep(duration)
            else:
                while True:
                    time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            self.stop()
            print()  # New line after streaming


def monitor_menu():
    """Interactive menu for monitoring tools."""
    monitor = DeviceMonitor(interval=1.0)
    
    while True:
        print("\n=== Real-time Monitoring ===")
        print("1. Stream to Console (10s)")
        print("2. Stream to Console (30s)")
        print("3. Stream to Console (Custom duration)")
        print("4. Stream to Console (Infinite - Ctrl+C to stop)")
        print("0. Back")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            monitor.stream_console(duration=10)
        elif choice == "2":
            monitor.stream_console(duration=30)
        elif choice == "3":
            duration = float(input("Duration (seconds): ").strip())
            monitor.stream_console(duration=duration)
        elif choice == "4":
            print("\nStreaming... (Press Ctrl+C to stop)")
            monitor.stream_console(duration=None)
        elif choice == "0":
            break
        else:
            print("Invalid choice")
