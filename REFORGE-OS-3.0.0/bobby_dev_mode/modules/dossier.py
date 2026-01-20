"""Device Dossier module - comprehensive device information."""
from ..adb_utils import adb, check_device


def run_dossier(profile: dict) -> None:
    """Run device dossier collection."""
    if not check_device():
        print("ERROR: No Android device connected via ADB")
        return
    
    print("=== DEVICE DOSSIER ===")
    print()
    
    # Identity
    print("--- Identity ---")
    model = adb(["shell", "getprop", "ro.product.model"]).strip()
    device = adb(["shell", "getprop", "ro.product.device"]).strip()
    manufacturer = adb(["shell", "getprop", "ro.product.manufacturer"]).strip()
    brand = adb(["shell", "getprop", "ro.product.brand"]).strip()
    print(f"Model: {model}")
    print(f"Device: {device}")
    print(f"Manufacturer: {manufacturer}")
    print(f"Brand: {brand}")
    print()
    
    # Build Info
    print("--- Build Info ---")
    build_id = adb(["shell", "getprop", "ro.build.display.id"]).strip()
    android_version = adb(["shell", "getprop", "ro.build.version.release"]).strip()
    sdk = adb(["shell", "getprop", "ro.build.version.sdk"]).strip()
    print(f"Build ID: {build_id}")
    print(f"Android Version: {android_version}")
    print(f"SDK: {sdk}")
    print()
    
    # Security
    print("--- Security ---")
    bootloader = adb(["shell", "getprop", "ro.bootloader"]).strip()
    secure = adb(["shell", "getprop", "ro.secure"]).strip()
    verified = adb(["shell", "getprop", "ro.boot.verifiedbootstate"]).strip()
    print(f"Bootloader: {bootloader}")
    print(f"Secure: {secure}")
    print(f"Verified Boot: {verified}")
    print()
    
    # Hardware
    print("--- Hardware ---")
    cpu = adb(["shell", "getprop", "ro.product.cpu.abi"]).strip()
    ram = adb(["shell", "getprop", "ro.config.low_ram"]).strip()
    print(f"CPU ABI: {cpu}")
    print(f"Low RAM: {ram}")
    print()
    
    # Battery
    print("--- Battery ---")
    battery_level = adb(["shell", "dumpsys", "battery", "|", "grep", "level"]).strip()
    print(f"Battery: {battery_level}")
    print()
