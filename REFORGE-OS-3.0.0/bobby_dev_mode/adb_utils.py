"""ADB utilities for Android device interaction."""
import subprocess
from typing import List, Optional


def run(cmd: List[str], check: bool = False) -> str:
    """Run an ADB/Fastboot command."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=check,
            timeout=60
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stdout + e.stderr
    except subprocess.TimeoutExpired:
        return "TIMEOUT"


def adb(args: List[str], check: bool = False) -> str:
    """Run an ADB command."""
    return run(["adb"] + args, check=check)


def fastboot(args: List[str], check: bool = False) -> str:
    """Run a Fastboot command."""
    return run(["fastboot"] + args, check=check)


def check_device() -> bool:
    """Check if an Android device is connected via ADB."""
    output = adb(["devices"])
    lines = output.strip().splitlines()[1:]  # Skip header
    for line in lines:
        if line.strip() and "device" in line and "offline" not in line:
            return True
    return False
