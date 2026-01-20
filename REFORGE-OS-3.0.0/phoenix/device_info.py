"""Device information gathering for recipe matching."""
import platform
from typing import Dict, Any

from ..bootforge.drives import list_drives


def get_host_profile() -> Dict[str, Any]:
    """Get host machine profile."""
    return {
        "platform": platform.system(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version()
    }


def get_target_profile(device_id: Optional[str] = None) -> Dict[str, Any]:
    """Get target device profile."""
    drives = list_drives()
    
    if device_id:
        # Find specific device
        for drive in drives:
            if drive.id == device_id:
                return {
                    "id": drive.id,
                    "model": drive.model,
                    "size_bytes": drive.size_bytes,
                    "is_ssd": drive.is_ssd,
                    "is_removable": drive.is_removable
                }
    
    # Return first drive if no device specified
    if drives:
        drive = drives[0]
        return {
            "id": drive.id,
            "model": drive.model,
            "size_bytes": drive.size_bytes,
            "is_ssd": drive.is_ssd,
            "is_removable": drive.is_removable
        }
    
    return {}
