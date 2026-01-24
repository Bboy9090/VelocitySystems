"""
iOS Device Dossier - Collect device information for iOS devices.
"""

from typing import Dict, Any, Optional
from .core import run_cmd, log
from .platform import Platform, get_device_info, run_platform_cmd


def collect_ios_dossier(device_udid: Optional[str] = None) -> Dict[str, Any]:
    """
    Collect comprehensive iOS device dossier.
    
    Args:
        device_udid: iOS device UDID (optional)
        
    Returns:
        Dictionary with device identity, build, hardware, battery info
    """
    dossier = {
        "identity": {},
        "build": {},
        "hardware": {},
        "battery": {}
    }
    
    idevice_cmd = ["ideviceinfo", "-u", device_udid] if device_udid else ["ideviceinfo", "-u", "auto"]
    
    # Get device info
    stdout, _, _ = run_cmd(idevice_cmd, check=False)
    
    if stdout:
        info_dict = {}
        for line in stdout.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                info_dict[key] = value
        
        # Identity
        dossier["identity"]["model"] = info_dict.get("ProductType") or info_dict.get("DeviceName")
        dossier["identity"]["manufacturer"] = "Apple"
        dossier["identity"]["udid"] = info_dict.get("UniqueDeviceID") or device_udid
        dossier["identity"]["serial"] = info_dict.get("SerialNumber")
        dossier["identity"]["imei"] = info_dict.get("InternationalMobileEquipmentIdentity")
        
        # Build
        dossier["build"]["ios_version"] = info_dict.get("ProductVersion")
        dossier["build"]["build_version"] = info_dict.get("BuildVersion")
        dossier["build"]["device_class"] = info_dict.get("DeviceClass")
        
        # Hardware
        dossier["hardware"]["cpu_architecture"] = info_dict.get("CPUArchitecture")
        dossier["hardware"]["hardware_model"] = info_dict.get("HardwareModel")
        dossier["hardware"]["chip_id"] = info_dict.get("ChipID")
        dossier["hardware"]["board_id"] = info_dict.get("BoardId")
        dossier["hardware"]["ecid"] = info_dict.get("UniqueChipID")
        
        # Battery (if available - requires specific keys)
        battery_capacity = info_dict.get("BatteryCurrentCapacity")
        if battery_capacity:
            dossier["battery"]["current_capacity"] = battery_capacity
        
        battery_design = info_dict.get("DesignCapacity")
        if battery_design:
            dossier["battery"]["design_capacity"] = battery_design
        
        # Try to get more battery info
        for key in ["BatteryIsCharging", "BatteryIsFullyCharged", "BatteryTemperature"]:
            if key in info_dict:
                dossier["battery"][key.lower().replace("battery", "").replace("is", "")] = info_dict[key]
    
    return dossier


def get_ios_battery_info(device_udid: Optional[str] = None) -> Dict[str, Any]:
    """
    Get iOS battery information.
    
    Args:
        device_udid: iOS device UDID
        
    Returns:
        Battery information dictionary
    """
    battery_info = {}
    
    idevice_cmd = ["ideviceinfo", "-u", device_udid] if device_udid else ["ideviceinfo", "-u", "auto"]
    
    # Battery-related keys
    battery_keys = [
        "BatteryCurrentCapacity",
        "DesignCapacity",
        "FullChargeCapacity",
        "BatteryIsCharging",
        "BatteryIsFullyCharged",
        "BatteryTemperature",
        "CycleCount"
    ]
    
    for key in battery_keys:
        stdout, _, _ = run_cmd(idevice_cmd + ["-k", key], check=False)
        if stdout.strip():
            value = stdout.strip()
            # Try to convert to number if possible
            try:
                if "." in value:
                    battery_info[key.lower()] = float(value)
                else:
                    battery_info[key.lower()] = int(value)
            except:
                battery_info[key.lower()] = value
    
    return battery_info


def get_ios_security_info(device_udid: Optional[str] = None) -> Dict[str, Any]:
    """
    Get iOS security information.
    
    Args:
        device_udid: iOS device UDID
        
    Returns:
        Security information dictionary
    """
    security_info = {}
    
    idevice_cmd = ["ideviceinfo", "-u", device_udid] if device_udid else ["ideviceinfo", "-u", "auto"]
    
    # Security-related keys
    security_keys = [
        "ActivationState",
        "ActivationStateAcknowledged",
        "BasebandVersion",
        "BootNonce",
        "DeviceCertificate",
        "DevicePublicKey",
        "HardwareModel",
        "ProductionSOC",
        "SecureBootPolicy"
    ]
    
    stdout, _, _ = run_cmd(idevice_cmd, check=False)
    if stdout:
        for line in stdout.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                if key in security_keys:
                    security_info[key.lower()] = value
    
    return security_info
