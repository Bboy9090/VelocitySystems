"""
Logs and Evidence - Collect basic logs and package lists.
"""

from typing import Dict, Any
from .core import run_cmd, log


def collect_basic_logs() -> Dict[str, Any]:
    """
    Collect basic logs and package lists.
    
    Returns:
        Dictionary with logs and package info
    """
    logs_data = {
        "packages": [],
        "logcat_sample": ""
    }
    
    # Get package list
    stdout, _, _ = run_cmd(["adb", "shell", "pm", "list", "packages"], check=False)
    if stdout:
        packages = [p.replace("package:", "").strip() for p in stdout.split("\n") if p.strip()]
        logs_data["packages"] = packages[:100]  # First 100 packages
        logs_data["package_count"] = len(packages)
    
    # Get logcat sample (last 50 lines)
    stdout, _, _ = run_cmd(["adb", "logcat", "-d", "-t", "50"], check=False)
    if stdout:
        logs_data["logcat_sample"] = stdout[:2000]  # First 2KB
    
    return logs_data
