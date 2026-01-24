"""
Bootloader Helper - Assist with Motorola bootloader unlock (official method).
"""

from .core import run_cmd, log


def motorola_unlock_helper():
    """Helper for Motorola bootloader unlock process."""
    print("\n=== Motorola Bootloader Unlock Helper ===")
    print("\nThis helper guides you through the OFFICIAL Motorola bootloader unlock process.")
    print("WARNING: Unlocking bootloader will void warranty and may brick device!")
    print("\nSteps:")
    print("1. Enable Developer Options on device")
    print("2. Enable 'OEM Unlocking' in Developer Options")
    print("3. Get unlock code from Motorola website")
    print("4. Boot device to fastboot mode")
    print("5. Run: fastboot oem unlock <code>")
    print("\nFor official unlock code, visit:")
    print("https://motorola-global-portal.custhelp.com/app/standalone/bootloader/unlock-your-device-a")
    
    choice = input("\nContinue? (yes/no): ").strip().lower()
    if choice != "yes":
        print("Cancelled")
        return
    
    # Check if device is in fastboot
    stdout, _, code = run_cmd(["fastboot", "devices"], check=False)
    if code != 0 or "fastboot" not in stdout.lower():
        log("Device not in fastboot mode!", "ERROR")
        log("Please boot device to fastboot mode first", "ERROR")
        return
    
    print("\nDevice detected in fastboot mode")
    unlock_code = input("Enter unlock code from Motorola: ").strip()
    
    if not unlock_code:
        log("No unlock code provided", "ERROR")
        return
    
    confirm = input(f"\nUnlock code: {unlock_code}\nProceed? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Cancelled")
        return
    
    log("Executing unlock command...")
    stdout, stderr, code = run_cmd(["fastboot", "oem", "unlock", unlock_code], check=False)
    
    if code == 0:
        log("Unlock command executed. Check device screen for confirmation.", "INFO")
    else:
        log(f"Unlock failed: {stderr}", "ERROR")


def bootloader_menu():
    """Interactive menu for bootloader tools."""
    while True:
        print("\n=== Bootloader Helper ===")
        print("1. Motorola Unlock Helper")
        print("0. Back")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            motorola_unlock_helper()
        elif choice == "0":
            break
        else:
            print("Invalid choice")
