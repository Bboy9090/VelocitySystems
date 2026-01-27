#!/bin/bash

#
# iOS Firmware Restore Script
# Uses libimobiledevice tools to restore iOS devices
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if libimobiledevice is installed
check_tools() {
    local missing_tools=()
    
    if ! command -v idevice_id &> /dev/null; then
        missing_tools+=("idevice_id")
    fi
    
    if ! command -v ideviceinfo &> /dev/null; then
        missing_tools+=("ideviceinfo")
    fi
    
    if ! command -v idevicerestore &> /dev/null; then
        missing_tools+=("idevicerestore")
    fi
    
    if ! command -v ideviceenterrecovery &> /dev/null; then
        missing_tools+=("ideviceenterrecovery")
    fi
    
    if [ ${#missing_tools[@]} -ne 0 ]; then
        print_error "Missing required tools: ${missing_tools[*]}"
        print_error "Please install libimobiledevice:"
        print_error "  macOS: brew install libimobiledevice ideviceinstaller"
        print_error "  Linux: apt-get install libimobiledevice-tools"
        exit 1
    fi
}

# Function to list connected iOS devices
list_devices() {
    print_status "Checking for connected iOS devices..."
    idevice_id -l
}

# Function to get device info
get_device_info() {
    local device=$1
    print_status "Device Information:"
    ideviceinfo -u "$device" | grep -E "DeviceName|ProductType|ProductVersion|SerialNumber"
}

# Function to enter recovery mode
enter_recovery() {
    local device=$1
    print_status "Entering recovery mode..."
    ideviceenterrecovery "$device"
    print_status "Device should now be in recovery mode"
}

# Function to enter DFU mode (manual)
enter_dfu() {
    print_status "To enter DFU mode, follow these steps:"
    echo ""
    echo "For iPhone 8 and later:"
    echo "  1. Connect device to computer"
    echo "  2. Press and quickly release Volume Up button"
    echo "  3. Press and quickly release Volume Down button"
    echo "  4. Press and hold Side button until screen goes black"
    echo "  5. While holding Side button, press and hold Volume Down for 5 seconds"
    echo "  6. Release Side button but keep holding Volume Down for another 5 seconds"
    echo ""
    echo "For iPhone 7/7 Plus:"
    echo "  1. Connect device to computer"
    echo "  2. Press and hold Side and Volume Down buttons for 8 seconds"
    echo "  3. Release Side button but keep holding Volume Down for 5 more seconds"
    echo ""
    echo "For iPhone 6s and earlier:"
    echo "  1. Connect device to computer"
    echo "  2. Press and hold Home and Power buttons for 8 seconds"
    echo "  3. Release Power button but keep holding Home for 5 more seconds"
    echo ""
    print_warning "The screen should be completely black when in DFU mode"
    echo ""
    echo -n "Press Enter when device is in DFU mode..."
    read
}

# Function to restore iOS firmware
restore_firmware() {
    local device=$1
    local ipsw=$2
    
    if [ ! -f "$ipsw" ]; then
        print_error "IPSW file not found: $ipsw"
        return 1
    fi
    
    print_status "Starting iOS restore..."
    print_warning "This will ERASE ALL DATA on the device!"
    print_warning "Press Ctrl+C to cancel, or Enter to continue..."
    read
    
    print_status "Restoring firmware (this may take 10-30 minutes)..."
    idevicerestore -u "$device" "$ipsw"
    
    if [ $? -eq 0 ]; then
        print_status "Restore completed successfully!"
        print_status "Device will reboot. Set it up when it's ready."
        return 0
    else
        print_error "Restore failed!"
        return 1
    fi
}

# Function to restore without updating
restore_no_update() {
    local device=$1
    local ipsw=$2
    
    if [ ! -f "$ipsw" ]; then
        print_error "IPSW file not found: $ipsw"
        return 1
    fi
    
    print_status "Starting iOS restore (no update)..."
    print_warning "This will restore the device to the same iOS version"
    print_warning "Press Ctrl+C to cancel, or Enter to continue..."
    read
    
    idevicerestore -u "$device" -l "$ipsw"
    
    if [ $? -eq 0 ]; then
        print_status "Restore completed successfully!"
        return 0
    else
        print_error "Restore failed!"
        return 1
    fi
}

# Function to create backup
create_backup() {
    local device=$1
    local backup_dir=$2
    
    if [ -z "$backup_dir" ]; then
        backup_dir="$HOME/ios_backups/backup_$(date +%Y%m%d_%H%M%S)"
    fi
    
    mkdir -p "$backup_dir"
    
    print_status "Creating backup to: $backup_dir"
    print_status "This may take a while depending on data size..."
    
    idevicebackup2 -u "$device" backup "$backup_dir"
    
    if [ $? -eq 0 ]; then
        print_status "Backup completed successfully!"
        print_status "Backup location: $backup_dir"
        return 0
    else
        print_error "Backup failed!"
        return 1
    fi
}

# Function to check recovery mode status
check_mode() {
    print_status "Checking device mode..."
    
    # Check for normal mode
    if idevice_id -l 2>/dev/null | grep -q .; then
        print_status "Device is in NORMAL mode"
        return 0
    fi
    
    # Check for recovery mode
    if idevicerestore -l 2>/dev/null | grep -q "recovery"; then
        print_status "Device is in RECOVERY mode"
        return 1
    fi
    
    # Check for DFU mode
    if idevicerestore -l 2>/dev/null | grep -q "dfu"; then
        print_status "Device is in DFU mode"
        return 2
    fi
    
    print_warning "Cannot determine device mode"
    return 3
}

# Main menu
show_menu() {
    echo ""
    echo "======================================"
    echo "   iOS Firmware Restore Tool"
    echo "======================================"
    echo "1. List connected devices"
    echo "2. Get device info"
    echo "3. Enter Recovery mode"
    echo "4. Enter DFU mode (manual)"
    echo "5. Check device mode"
    echo "6. Restore firmware (update)"
    echo "7. Restore firmware (no update)"
    echo "8. Create backup"
    echo "9. Exit"
    echo "======================================"
    echo -n "Select option: "
}

# Main script
main() {
    check_tools
    
    if [ "$1" == "--help" ] || [ "$1" == "-h" ]; then
        echo "Usage: $0 [device_udid] [ipsw_path]"
        echo ""
        echo "Options:"
        echo "  --help, -h     Show this help message"
        echo ""
        echo "Examples:"
        echo "  $0                                    # Interactive mode"
        echo "  $0 ABC123 /path/to/firmware.ipsw     # Restore firmware"
        exit 0
    fi
    
    if [ "$1" ] && [ "$2" ]; then
        # Non-interactive mode
        device=$1
        ipsw=$2
        print_status "Restoring firmware on device $device from $ipsw"
        restore_firmware "$device" "$ipsw"
        exit 0
    fi
    
    # Interactive mode
    while true; do
        show_menu
        read option
        
        case $option in
            1)
                list_devices
                ;;
            2)
                echo -n "Enter device UDID (or press Enter for first device): "
                read device
                if [ -z "$device" ]; then
                    device=$(idevice_id -l | head -n1)
                fi
                get_device_info "$device"
                ;;
            3)
                echo -n "Enter device UDID: "
                read device
                enter_recovery "$device"
                ;;
            4)
                enter_dfu
                ;;
            5)
                check_mode
                ;;
            6)
                echo -n "Enter device UDID: "
                read device
                echo -n "Enter IPSW path: "
                read ipsw
                restore_firmware "$device" "$ipsw"
                ;;
            7)
                echo -n "Enter device UDID: "
                read device
                echo -n "Enter IPSW path: "
                read ipsw
                restore_no_update "$device" "$ipsw"
                ;;
            8)
                echo -n "Enter device UDID: "
                read device
                echo -n "Enter backup directory (or press Enter for default): "
                read backup_dir
                create_backup "$device" "$backup_dir"
                ;;
            9)
                print_status "Exiting..."
                exit 0
                ;;
            *)
                print_error "Invalid option"
                ;;
        esac
    done
}

main "$@"
