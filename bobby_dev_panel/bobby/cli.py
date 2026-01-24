"""
CLI entry point for Bobby Dev Panel.
Can be used as: python -m bobby.cli or bobby-dev-panel
"""

import sys
import argparse
from .main import main, main_menu
from .core import check_device, log
from .report import generate_bench_summary
from .intake import full_intake


def cli_main():
    """CLI entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description="Bobby Dev Panel - Device Diagnostics & Control",
        prog="bobby-dev-panel"
    )
    
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Run in interactive mode (default)"
    )
    
    parser.add_argument(
        "--bench-summary",
        "-b",
        action="store_true",
        help="Generate bench summary JSON and exit"
    )
    
    parser.add_argument(
        "--intake",
        action="store_true",
        help="Run full intake and exit"
    )
    
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Output file for bench summary or intake"
    )
    
    parser.add_argument(
        "--check-device",
        "-c",
        action="store_true",
        help="Check if device is connected and exit"
    )
    
    args = parser.parse_args()
    
    # Check device first (unless just checking)
    if not args.check_device and not check_device():
        log("No device connected via ADB!", "ERROR")
        log("Please connect a device and enable USB debugging", "ERROR")
        sys.exit(1)
    
    # Handle different modes
    if args.check_device:
        if check_device():
            log("Device connected", "INFO")
            sys.exit(0)
        else:
            log("No device connected", "ERROR")
            sys.exit(1)
    
    if args.bench_summary:
        summary = generate_bench_summary()
        if args.output:
            import json
            with open(args.output, "w") as f:
                json.dump(summary, f, indent=2)
            log(f"Bench summary saved to {args.output}", "INFO")
        else:
            import json
            print(json.dumps(summary, indent=2))
        sys.exit(0)
    
    if args.intake:
        intake_data = full_intake(output_file=args.output)
        if not args.output:
            import json
            print(json.dumps(intake_data, indent=2))
        sys.exit(0)
    
    # Default: interactive mode
    main_menu()


if __name__ == "__main__":
    cli_main()
