"""Core utilities for BootForge."""
import os
import subprocess
from datetime import datetime
from typing import Sequence, Union, Optional

LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "logs", "bootforge.log")
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

Cmd = Union[str, Sequence[str]]


def log(msg: str) -> None:
    """Log a message with timestamp."""
    ts = datetime.utcnow().isoformat(timespec="seconds") + "Z"
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def run_cmd(
    cmd: Cmd,
    *,
    capture_output: bool = True,
    check: bool = False,
    shell: bool = False
) -> str:
    """Run a shell command safely."""
    try:
        result = subprocess.run(
            cmd,
            shell=shell,
            capture_output=capture_output,
            text=True,
            check=check,
            timeout=300
        )
        if capture_output:
            return result.stdout
        return ""
    except subprocess.TimeoutExpired as e:
        log(f"TIMEOUT: {' '.join(cmd) if isinstance(cmd, (list, tuple)) else cmd}")
        raise
    except subprocess.CalledProcessError as e:
        log(f"ERROR: {' '.join(cmd) if isinstance(cmd, (list, tuple)) else cmd}: {e}")
        if capture_output and e.stdout:
            log(f"STDOUT: {e.stdout}")
        if capture_output and e.stderr:
            log(f"STDERR: {e.stderr}")
        if check:
            raise
        return e.stdout if capture_output else ""


def require_root_hint() -> None:
    """Warn if not running as root/admin."""
    import platform
    if platform.system() == "Windows":
        # Check for admin on Windows
        import ctypes
        if not ctypes.windll.shell32.IsUserAnAdmin():
            log("WARNING: May need administrator privileges for drive operations")
    else:
        # Check for root on Unix
        if os.geteuid() != 0:
            log("WARNING: May need root privileges for drive operations")
