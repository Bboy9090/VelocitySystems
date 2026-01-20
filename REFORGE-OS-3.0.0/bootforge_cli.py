#!/usr/bin/env python3
"""BootForge CLI - Safe drive imaging tool."""
import sys
import json
import argparse
from bootforge.core import log
from bootforge.drives import list_drives, probe_drive, smart_health
from bootforge.imager import write_image


def _fmt_gb(bytes_val: int) -> str:
    """Format bytes as GB."""
    return f"{bytes_val / (1024**3):.1f}"


def cmd_list(args):
    """List all drives."""
    drives = list_drives()
    if args.json:
        print(json.dumps([{
            "id": d.id,
            "size_bytes": d.size_bytes,
            "size_gb": d.size_bytes / (1024**3),
            "model": d.model,
            "is_removable": d.is_removable,
            "is_ssd": d.is_ssd,
            "description": d.description
        } for d in drives], indent=2))
    else:
        print("\n=== PHYSICAL DRIVES ===")
        for d in drives:
            ssd_str = "SSD" if d.is_ssd else ("HDD" if d.is_ssd is False else "?")
            rem_str = "Removable" if d.is_removable else "Fixed"
            print(f"{d.id:20} {_fmt_gb(d.size_bytes):>8} GB  {ssd_str:>4}  {rem_str:10}  {d.model}")


def cmd_probe(args):
    """Probe a specific drive."""
    info = probe_drive(args.device)
    if args.json:
        print(json.dumps(info, indent=2))
    else:
        print(f"\n=== DRIVE INFO: {args.device} ===")
        print(json.dumps(info, indent=2))


def cmd_smart(args):
    """Get SMART health for a drive."""
    health = smart_health(args.device)
    if health:
        print(health)
    else:
        print("SMART not available for this drive/system")


def cmd_write(args):
    """Write an image to a drive."""
    if not args.yes:
        print(f"WARNING: This will overwrite all data on {args.target}!")
        print(f"Image: {args.image}")
        confirm = input("Type 'YES' to continue: ")
        if confirm != "YES":
            print("Cancelled.")
            return
    
    result = write_image(args.image, args.target, verify=args.verify)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result["success"]:
            print("✓ Image written successfully")
            if result.get("verified"):
                print("✓ Hash verification passed")


def main():
    parser = argparse.ArgumentParser(description="BootForge - Safe drive imaging")
    subparsers = parser.add_subparsers(dest="command", help="Command")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List drives")
    list_parser.add_argument("--json", action="store_true", help="JSON output")
    
    # Probe command
    probe_parser = subparsers.add_parser("probe", help="Probe drive")
    probe_parser.add_argument("device", help="Device path")
    probe_parser.add_argument("--json", action="store_true", help="JSON output")
    
    # SMART command
    smart_parser = subparsers.add_parser("smart", help="SMART health")
    smart_parser.add_argument("device", help="Device path")
    
    # Write command
    write_parser = subparsers.add_parser("write", help="Write image")
    write_parser.add_argument("image", help="Image file path")
    write_parser.add_argument("target", help="Target device path")
    write_parser.add_argument("--verify", action="store_true", default=True, help="Verify hash")
    write_parser.add_argument("--no-verify", dest="verify", action="store_false", help="Skip verification")
    write_parser.add_argument("--yes", action="store_true", help="Skip confirmation")
    write_parser.add_argument("--json", action="store_true", help="JSON output")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        if args.command == "list":
            cmd_list(args)
        elif args.command == "probe":
            cmd_probe(args)
        elif args.command == "smart":
            cmd_smart(args)
        elif args.command == "write":
            cmd_write(args)
    except Exception as e:
        log(f"Error: {e}")
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
