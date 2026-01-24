"""
Core helper functions for ADB commands, logging, and device checks.
"""

import subprocess
import sys
from typing import Optional, Dict, Any, Tuple, List


def log(msg: str, level: str = "INFO"):
    """Print formatted log message."""
    prefix = f"[{level}]"
    print(f"{prefix} {msg}", file=sys.stderr if level == "ERROR" else sys.stdout)


def run_cmd(cmd: List[str], check: bool = True, device_serial: Optional[str] = None) -> Tuple[str, str, int]:
    """
    Run a command and return (stdout, stderr, returncode).
    
    Args:
        cmd: Command as list of strings
        check: If True, raise on non-zero return code
        device_serial: Optional device serial to target specific device
        
    Returns:
        (stdout, stderr, returncode)
    """
    # If device_serial provided and command starts with 'adb', inject -s flag
    if device_serial and len(cmd) > 0 and cmd[0] == "adb":
        # Check if -s flag already present
        if "-s" not in cmd:
            cmd = [cmd[0], "-s", device_serial] + cmd[1:]
        # If -s present but different serial, replace it
        elif "-s" in cmd:
            idx = cmd.index("-s")
            if idx + 1 < len(cmd):
                cmd[idx + 1] = device_serial
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        if check and result.returncode != 0:
            log(f"Command failed: {' '.join(cmd)}", "ERROR")
            log(f"Error: {result.stderr}", "ERROR")
        return (result.stdout, result.stderr, result.returncode)
    except subprocess.TimeoutExpired:
        log(f"Command timed out: {' '.join(cmd)}", "ERROR")
        return ("", "Timeout", 1)
    except Exception as e:
        log(f"Command error: {e}", "ERROR")
        return ("", str(e), 1)


def check_device(platform: Optional[str] = None) -> bool:
    """
    Check if a device is connected (Android or iOS).
    
    Args:
        platform: Platform to check ("android", "ios", or None for auto-detect)
        
    Returns:
        True if device connected
    """
    if platform is None or platform == "android":
        # Check Android
        stdout, _, code = run_cmd(["adb", "devices"], check=False)
        if code == 0 and stdout:
            lines = [l.strip() for l in stdout.split("\n") if l.strip()]
            devices = [l for l in lines[1:] if l and "device" in l and not l.startswith("*")]
            if devices:
                return True
    
    if platform is None or platform == "ios":
        # Check iOS
        stdout, _, code = run_cmd(["idevice_id", "-l"], check=False)
        if code == 0 and stdout.strip():
            return True
    
    return False


def get_model() -> Optional[str]:
    """Get device model via ADB."""
    stdout, _, code = run_cmd(["adb", "shell", "getprop", "ro.product.model"], check=False)
    if code == 0 and stdout.strip():
        return stdout.strip()
    return None


def get_serial() -> Optional[str]:
    """Get device serial number via ADB."""
    stdout, _, code = run_cmd(["adb", "get-serialno"], check=False)
    if code == 0 and stdout.strip():
        return stdout.strip()
    return None
