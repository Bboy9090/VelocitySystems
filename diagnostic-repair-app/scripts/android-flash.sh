#!/bin/bash

#
# Android Firmware Flashing Script
# Uses fastboot to flash firmware partitions
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

# Check if fastboot is installed
if ! command -v fastboot &> /dev/null; then
    print_error "fastboot is not installed. Please install Android platform-tools."
    exit 1
fi

# Function to list fastboot devices
list_devices() {
    print_status "Checking for devices in fastboot mode..."
    fastboot devices
}

# Function to reboot to fastboot mode
reboot_to_fastboot() {
    local device_id=$1
    print_status "Rebooting device to fastboot mode..."
    adb -s "$device_id" reboot bootloader
    print_status "Waiting for device to enter fastboot mode..."
    sleep 5
}

# Function to flash a single partition
flash_partition() {
    local device=$1
    local partition=$2
    local image=$3
    
    if [ ! -f "$image" ]; then
        print_error "Image file not found: $image"
        return 1
    fi
    
    print_status "Flashing $partition..."
    fastboot -s "$device" flash "$partition" "$image"
    
    if [ $? -eq 0 ]; then
        print_status "Successfully flashed $partition"
        return 0
    else
        print_error "Failed to flash $partition"
        return 1
    fi
}

# Function to flash all partitions from a directory
flash_all() {
    local device=$1
    local firmware_dir=$2
    
    if [ ! -d "$firmware_dir" ]; then
        print_error "Firmware directory not found: $firmware_dir"
        exit 1
    fi
    
    cd "$firmware_dir"
    
    # Check if flash-all script exists
    if [ -f "flash-all.sh" ]; then
        print_status "Found flash-all.sh script. Using it..."
        bash flash-all.sh
        return $?
    fi
    
    # Manual flashing
    print_status "Starting firmware flash process..."
    
    # Common partitions
    partitions=("boot" "system" "vendor" "recovery" "userdata" "cache")
    
    for partition in "${partitions[@]}"; do
        image_file="${partition}.img"
        if [ -f "$image_file" ]; then
            flash_partition "$device" "$partition" "$image_file"
        else
            print_warning "Image not found for $partition, skipping..."
        fi
    done
    
    print_status "Firmware flashing completed!"
}

# Function to unlock bootloader
unlock_bootloader() {
    local device=$1
    print_warning "Unlocking bootloader will ERASE ALL DATA!"
    print_warning "Press Ctrl+C to cancel, or Enter to continue..."
    read
    
    print_status "Unlocking bootloader..."
    fastboot -s "$device" oem unlock
    
    print_status "Follow on-screen instructions on the device to confirm."
}

# Function to lock bootloader
lock_bootloader() {
    local device=$1
    print_warning "Locking bootloader will ERASE ALL DATA!"
    print_warning "Press Ctrl+C to cancel, or Enter to continue..."
    read
    
    print_status "Locking bootloader..."
    fastboot -s "$device" oem lock
}

# Function to erase partition
erase_partition() {
    local device=$1
    local partition=$2
    
    print_status "Erasing partition: $partition"
    fastboot -s "$device" erase "$partition"
}

# Function to format userdata
format_userdata() {
    local device=$1
    print_warning "This will ERASE ALL USER DATA!"
    print_warning "Press Ctrl+C to cancel, or Enter to continue..."
    read
    
    print_status "Formatting userdata..."
    fastboot -s "$device" format userdata
}

# Function to reboot device
reboot_device() {
    local device=$1
    print_status "Rebooting device..."
    fastboot -s "$device" reboot
}

# Main menu
show_menu() {
    echo ""
    echo "======================================"
    echo "  Android Firmware Flashing Tool"
    echo "======================================"
    echo "1. List fastboot devices"
    echo "2. Flash single partition"
    echo "3. Flash all partitions"
    echo "4. Unlock bootloader"
    echo "5. Lock bootloader"
    echo "6. Erase partition"
    echo "7. Format userdata"
    echo "8. Reboot device"
    echo "9. Exit"
    echo "======================================"
    echo -n "Select option: "
}

# Main script
main() {
    if [ "$1" == "--help" ] || [ "$1" == "-h" ]; then
        echo "Usage: $0 [device_id] [firmware_directory]"
        echo ""
        echo "Options:"
        echo "  --help, -h     Show this help message"
        echo ""
        echo "Examples:"
        echo "  $0                                    # Interactive mode"
        echo "  $0 ABC123 /path/to/firmware          # Flash firmware"
        exit 0
    fi
    
    if [ "$1" ] && [ "$2" ]; then
        # Non-interactive mode
        device=$1
        firmware_dir=$2
        print_status "Flashing firmware on device $device from $firmware_dir"
        flash_all "$device" "$firmware_dir"
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
                echo -n "Enter device ID: "
                read device
                echo -n "Enter partition name: "
                read partition
                echo -n "Enter image path: "
                read image
                flash_partition "$device" "$partition" "$image"
                ;;
            3)
                echo -n "Enter device ID: "
                read device
                echo -n "Enter firmware directory: "
                read firmware_dir
                flash_all "$device" "$firmware_dir"
                ;;
            4)
                echo -n "Enter device ID: "
                read device
                unlock_bootloader "$device"
                ;;
            5)
                echo -n "Enter device ID: "
                read device
                lock_bootloader "$device"
                ;;
            6)
                echo -n "Enter device ID: "
                read device
                echo -n "Enter partition name: "
                read partition
                erase_partition "$device" "$partition"
                ;;
            7)
                echo -n "Enter device ID: "
                read device
                format_userdata "$device"
                ;;
            8)
                echo -n "Enter device ID: "
                read device
                reboot_device "$device"
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
