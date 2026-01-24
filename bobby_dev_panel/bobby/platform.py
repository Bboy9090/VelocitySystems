"""
Platform Detection and Abstraction Layer
Supports: All Android devices + iOS devices (iPhone, iPad)
"""

import subprocess
import re
from typing import Dict, Any, Optional, List, Tuple
from enum import Enum
from .core import run_cmd, log


class Platform(Enum):
    """Supported platforms."""
    ANDROID = "android"
    IOS = "ios"
    UNKNOWN = "unknown"


class DeviceType(Enum):
    """Device types."""
    PHONE = "phone"
    TABLET = "tablet"
    UNKNOWN = "unknown"


def detect_platform() -> Platform:
    """
    Detect connected platform (Android or iOS).
    
    Returns:
        Platform enum
    """
    # Check for Android device
    stdout, _, code = run_cmd(["adb", "devices"], check=False)
    if code == 0 and stdout:
        lines = [l.strip() for l in stdout.split("\n") if l.strip()]
        devices = [l for l in lines[1:] if l and "device" in l and not l.startswith("*")]
        if devices:
            return Platform.ANDROID
    
    # Check for iOS device
    stdout, _, code = run_cmd(["idevice_id", "-l"], check=False)
    if code == 0 and stdout.strip():
        return Platform.IOS
    
    # Try alternative iOS detection
    stdout, _, code = run_cmd(["ideviceinfo", "-u", "auto"], check=False)
    if code == 0 and stdout:
        return Platform.IOS
    
    return Platform.UNKNOWN


def detect_all_devices() -> List[Dict[str, Any]]:
    """
    Detect all connected devices (Android and iOS).
    
    Returns:
        List of device dictionaries with platform info
    """
    devices = []
    
    # Android devices
    stdout, _, code = run_cmd(["adb", "devices", "-l"], check=False)
    if code == 0 and stdout:
        lines = [l.strip() for l in stdout.split("\n") if l.strip()]
        for line in lines[1:]:  # Skip header
            if "device" in line and not line.startswith("*"):
                parts = line.split()
                if len(parts) >= 2:
                    serial = parts[0]
                    # Get model
                    model_stdout, _, _ = run_cmd(["adb", "-s", serial, "shell", "getprop", "ro.product.model"], check=False)
                    model = model_stdout.strip() if model_stdout.strip() else "Unknown"
                    
                    devices.append({
                        "platform": Platform.ANDROID.value,
                        "serial": serial,
                        "udid": serial,  # Android uses serial
                        "model": model,
                        "type": DeviceType.PHONE.value,  # Default, can be detected
                        "status": "connected"
                    })
    
    # iOS devices
    stdout, _, code = run_cmd(["idevice_id", "-l"], check=False)
    if code == 0 and stdout:
        udids = [udid.strip() for udid in stdout.split("\n") if udid.strip()]
        for udid in udids:
            # Get device info
            info_stdout, _, _ = run_cmd(["ideviceinfo", "-u", udid], check=False)
            model = "Unknown"
            device_type = DeviceType.PHONE.value
            
            if info_stdout:
                # Parse model name
                for line in info_stdout.split("\n"):
                    if "ProductType" in line or "DeviceName" in line:
                        model = line.split(":")[-1].strip() if ":" in line else "Unknown"
                    if "ProductType" in line:
                        product_type = line.split(":")[-1].strip() if ":" in line else ""
                        if "iPad" in product_type:
                            device_type = DeviceType.TABLET.value
            
            devices.append({
                "platform": Platform.IOS.value,
                "serial": udid,  # iOS uses UDID
                "udid": udid,
                "model": model,
                "type": device_type,
                "status": "connected"
            })
    
    return devices


def get_device_info(device_serial: Optional[str] = None, platform: Optional[Platform] = None) -> Dict[str, Any]:
    """
    Get device information for Android or iOS.
    
    Args:
        device_serial: Device serial/UDID
        platform: Platform (auto-detected if None)
        
    Returns:
        Device information dictionary
    """
    if platform is None:
        platform = detect_platform()
    
    info = {
        "platform": platform.value,
        "serial": device_serial,
        "model": None,
        "manufacturer": None,
        "os_version": None,
        "device_type": None
    }
    
    if platform == Platform.ANDROID:
        # Android info
        adb_cmd = ["adb", "-s", device_serial] if device_serial else ["adb"]
        
        stdout, _, _ = run_cmd(adb_cmd + ["shell", "getprop", "ro.product.model"], check=False)
        info["model"] = stdout.strip() if stdout.strip() else None
        
        stdout, _, _ = run_cmd(adb_cmd + ["shell", "getprop", "ro.product.manufacturer"], check=False)
        info["manufacturer"] = stdout.strip() if stdout.strip() else None
        
        stdout, _, _ = run_cmd(adb_cmd + ["shell", "getprop", "ro.build.version.release"], check=False)
        info["os_version"] = stdout.strip() if stdout.strip() else None
        
        # Detect device type (phone vs tablet)
        stdout, _, _ = run_cmd(adb_cmd + ["shell", "getprop", "ro.build.characteristics"], check=False)
        if "tablet" in stdout.lower():
            info["device_type"] = DeviceType.TABLET.value
        else:
            info["device_type"] = DeviceType.PHONE.value
    
    elif platform == Platform.IOS:
        # iOS info
        idevice_cmd = ["ideviceinfo", "-u", device_serial] if device_serial else ["ideviceinfo", "-u", "auto"]
        
        stdout, _, _ = run_cmd(idevice_cmd, check=False)
        if stdout:
            for line in stdout.split("\n"):
                if "ProductType" in line:
                    info["model"] = line.split(":")[-1].strip() if ":" in line else None
                elif "DeviceName" in line:
                    if not info["model"]:
                        info["model"] = line.split(":")[-1].strip() if ":" in line else None
                elif "ProductVersion" in line:
                    info["os_version"] = line.split(":")[-1].strip() if ":" in line else None
                elif "DeviceClass" in line:
                    device_class = line.split(":")[-1].strip() if ":" in line else ""
                    if "iPad" in device_class:
                        info["device_type"] = DeviceType.TABLET.value
                    else:
                        info["device_type"] = DeviceType.PHONE.value
            
            info["manufacturer"] = "Apple"
    
    return info


def run_platform_cmd(cmd_type: str, device_serial: Optional[str] = None, 
                     platform: Optional[Platform] = None, **kwargs) -> Tuple[str, str, int]:
    """
    Run platform-agnostic command.
    
    Args:
        cmd_type: Command type ('getprop', 'shell', 'info', etc.)
        device_serial: Device serial/UDID
        platform: Platform (auto-detected if None)
        **kwargs: Additional command-specific parameters
        
    Returns:
        (stdout, stderr, returncode)
    """
    if platform is None:
        platform = detect_platform()
    
    if platform == Platform.ANDROID:
        return _run_android_cmd(cmd_type, device_serial, **kwargs)
    elif platform == Platform.IOS:
        return _run_ios_cmd(cmd_type, device_serial, **kwargs)
    else:
        return ("", "Unknown platform", 1)


def _run_android_cmd(cmd_type: str, device_serial: Optional[str], **kwargs) -> Tuple[str, str, int]:
    """Run Android-specific command."""
    adb_cmd = ["adb", "-s", device_serial] if device_serial else ["adb"]
    
    if cmd_type == "getprop":
        prop = kwargs.get("property", "")
        return run_cmd(adb_cmd + ["shell", "getprop", prop], check=False)
    elif cmd_type == "shell":
        shell_cmd = kwargs.get("command", "")
        return run_cmd(adb_cmd + ["shell"] + shell_cmd.split(), check=False)
    elif cmd_type == "dumpsys":
        service = kwargs.get("service", "")
        return run_cmd(adb_cmd + ["shell", "dumpsys", service], check=False)
    else:
        return ("", f"Unknown Android command: {cmd_type}", 1)


def _run_ios_cmd(cmd_type: str, device_serial: Optional[str], **kwargs) -> Tuple[str, str, int]:
    """Run iOS-specific command."""
    idevice_cmd = ["ideviceinfo", "-u", device_serial] if device_serial else ["ideviceinfo", "-u", "auto"]
    
    if cmd_type == "info":
        key = kwargs.get("key", "")
        if key:
            idevice_cmd.extend(["-k", key])
        return run_cmd(idevice_cmd, check=False)
    elif cmd_type == "battery":
        # iOS battery info
        return run_cmd(["ideviceinfo", "-u", device_serial if device_serial else "auto", "-k", "BatteryCurrentCapacity"], check=False)
    elif cmd_type == "shell":
        # iOS shell (requires jailbreak)
        command = kwargs.get("command", "")
        return run_cmd(["idevicesyslog", "-u", device_serial if device_serial else "auto"], check=False)
    else:
        return ("", f"Unknown iOS command: {cmd_type}", 1)


def check_platform_tools() -> Dict[str, bool]:
    """
    Check if required platform tools are installed.
    
    Returns:
        Dictionary with tool availability
    """
    tools = {
        "adb": False,
        "fastboot": False,
        "idevice_id": False,
        "ideviceinfo": False,
        "ideviceinstaller": False
    }
    
    # Check ADB
    stdout, _, code = run_cmd(["adb", "version"], check=False)
    tools["adb"] = code == 0
    
    # Check Fastboot
    stdout, _, code = run_cmd(["fastboot", "--version"], check=False)
    tools["fastboot"] = code == 0
    
    # Check libimobiledevice tools
    stdout, _, code = run_cmd(["idevice_id", "--version"], check=False)
    tools["idevice_id"] = code == 0
    
    stdout, _, code = run_cmd(["ideviceinfo", "--version"], check=False)
    tools["ideviceinfo"] = code == 0
    
    stdout, _, code = run_cmd(["ideviceinstaller", "--version"], check=False)
    tools["ideviceinstaller"] = code == 0
    
    return tools


def get_supported_oems() -> List[str]:
    """
    Get list of supported Android OEMs (all major manufacturers).
    
    Returns:
        List of OEM names
    """
    return [
        "Samsung", "Motorola", "Google", "OnePlus", "Xiaomi", "Huawei", 
        "Oppo", "Vivo", "Realme", "Sony", "LG", "HTC", "Nokia", "Asus",
        "Lenovo", "ZTE", "TCL", "Alcatel", "Tecno", "Infinix", "Generic"
    ]


def detect_oem(device_serial: Optional[str] = None) -> Optional[str]:
    """
    Detect Android OEM manufacturer.
    
    Args:
        device_serial: Device serial
        
    Returns:
        OEM name or None
    """
    adb_cmd = ["adb", "-s", device_serial] if device_serial else ["adb"]
    
    stdout, _, _ = run_cmd(adb_cmd + ["shell", "getprop", "ro.product.manufacturer"], check=False)
    manufacturer = stdout.strip().lower() if stdout.strip() else ""
    
    # Map to standard names
    oem_map = {
        "samsung": "Samsung",
        "motorola": "Motorola",
        "moto": "Motorola",
        "google": "Google",
        "oneplus": "OnePlus",
        "xiaomi": "Xiaomi",
        "redmi": "Xiaomi",
        "huawei": "Huawei",
        "honor": "Huawei",
        "oppo": "Oppo",
        "vivo": "Vivo",
        "realme": "Realme",
        "sony": "Sony",
        "lg": "LG",
        "htc": "HTC",
        "nokia": "Nokia",
        "asus": "Asus",
        "lenovo": "Lenovo",
        "zte": "ZTE",
        "tcl": "TCL",
        "alcatel": "Alcatel",
        "tecno": "Tecno",
        "infinix": "Infinix"
    }
    
    for key, value in oem_map.items():
        if key in manufacturer:
            return value
    
    return "Generic" if manufacturer else None
