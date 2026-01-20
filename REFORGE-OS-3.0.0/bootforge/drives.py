"""Drive detection and probing."""
import os
import platform
import re
from dataclasses import dataclass
from typing import List, Optional, Dict

from .core import log, run_cmd


@dataclass
class DriveInfo:
    """Information about a physical drive."""
    id: str
    size_bytes: int
    model: str
    is_removable: bool
    is_ssd: Optional[bool]
    description: str


def list_drives() -> List[DriveInfo]:
    """List all physical drives on the system."""
    system = platform.system()
    log("Probing physical drives...")
    
    if system == "Darwin":  # macOS
        return _list_drives_macos()
    elif system == "Linux":
        return _list_drives_linux()
    elif system == "Windows":
        return _list_drives_windows()
    else:
        log(f"Unsupported platform: {system}")
        return []


def _list_drives_macos() -> List[DriveInfo]:
    """List drives on macOS using diskutil."""
    drives = []
    try:
        output = run_cmd(["diskutil", "list", "-plist", "physical"], check=False)
        # Parse diskutil output
        # For simplicity, use diskutil list first
        list_output = run_cmd(["diskutil", "list"], check=False)
        lines = list_output.splitlines()
        
        current_disk = None
        for line in lines:
            if line.startswith("/dev/disk"):
                parts = line.split()
                if len(parts) >= 2:
                    disk_id = parts[0]
                    # Get disk info
                    info_output = run_cmd(["diskutil", "info", disk_id], check=False)
                    size_match = re.search(r"Disk Size:\s+([\d,]+)\s+Bytes", info_output)
                    model_match = re.search(r"Device / Media Name:\s+(.+)", info_output)
                    removable_match = re.search(r"Removable Media:\s+(.+)", info_output)
                    
                    size_str = size_match.group(1).replace(",", "") if size_match else "0"
                    size_bytes = int(size_str)
                    model = model_match.group(1).strip() if model_match else "Unknown"
                    is_removable = (removable_match.group(1).strip() == "Removable") if removable_match else False
                    
                    drives.append(DriveInfo(
                        id=disk_id,
                        size_bytes=size_bytes,
                        model=model,
                        is_removable=is_removable,
                        is_ssd=None,  # Need to check separately
                        description=f"{model} ({size_bytes / (1024**3):.1f} GB)"
                    ))
    except Exception as e:
        log(f"Error listing macOS drives: {e}")
    
    return drives


def _list_drives_linux() -> List[DriveInfo]:
    """List drives on Linux using lsblk."""
    drives = []
    try:
        output = run_cmd(["lsblk", "-b", "-d", "-n", "-o", "NAME,SIZE,MODEL,ROTA,TYPE"], check=False)
        for line in output.strip().splitlines():
            if not line.strip():
                continue
            parts = line.split()
            if len(parts) >= 2:
                name = parts[0]
                size_bytes = int(parts[1])
                model = " ".join(parts[2:-2]) if len(parts) > 4 else "Unknown"
                rota = parts[-2] if len(parts) > 2 else "?"
                # rota=0 means SSD, rota=1 means HDD
                is_ssd = (rota == "0") if rota in ("0", "1") else None
                
                # Check if removable
                sys_path = f"/sys/block/{name}/removable"
                is_removable = False
                if os.path.exists(sys_path):
                    try:
                        with open(sys_path) as f:
                            is_removable = f.read().strip() == "1"
                    except:
                        pass
                
                drives.append(DriveInfo(
                    id=f"/dev/{name}",
                    size_bytes=size_bytes,
                    model=model,
                    is_removable=is_removable,
                    is_ssd=is_ssd,
                    description=f"{model} ({size_bytes / (1024**3):.1f} GB)"
                ))
    except Exception as e:
        log(f"Error listing Linux drives: {e}")
    
    return drives


def _list_drives_windows() -> List[DriveInfo]:
    """List drives on Windows using PowerShell."""
    drives = []
    try:
        ps_cmd = """
        Get-PhysicalDisk | ForEach-Object {
            "$($_.DeviceID)|$($_.Size)|$($_.Model)|$($_.MediaType)|$($_.BusType)"
        }
        """
        output = run_cmd(["powershell", "-Command", ps_cmd], check=False)
        for line in output.strip().splitlines():
            if not line.strip() or "|" not in line:
                continue
            parts = line.split("|")
            if len(parts) >= 5:
                device_id = parts[0]
                size_bytes = int(parts[1])
                model = parts[2]
                media_type = parts[3]
                bus_type = parts[4]
                
                is_ssd = (media_type == "SSD") if media_type in ("SSD", "HDD") else None
                is_removable = (bus_type in ("USB", "SD"))
                
                drives.append(DriveInfo(
                    id=f"\\\\.\\PhysicalDrive{device_id}",
                    size_bytes=size_bytes,
                    model=model,
                    is_removable=is_removable,
                    is_ssd=is_ssd,
                    description=f"{model} ({size_bytes / (1024**3):.1f} GB)"
                ))
    except Exception as e:
        log(f"Error listing Windows drives: {e}")
    
    return drives


def probe_drive(dev_id: str) -> Optional[Dict]:
    """Probe detailed information about a specific drive."""
    log(f"Probing drive: {dev_id}")
    # Implementation would gather more detailed info
    return {
        "id": dev_id,
        "status": "ok",
        "health_hints": []
    }


def smart_health(dev_id: str) -> Optional[str]:
    """Get SMART health status using smartctl if available."""
    if not os.path.exists("/usr/sbin/smartctl") and platform.system() != "Windows":
        return None
    
    try:
        # smartctl is typically at /usr/sbin/smartctl on Linux
        output = run_cmd(["smartctl", "-H", dev_id], check=False)
        return output
    except:
        return None
