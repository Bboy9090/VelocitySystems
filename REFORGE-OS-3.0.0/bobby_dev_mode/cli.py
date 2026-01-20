#!/usr/bin/env python3
"""Bobby Dev Mode CLI."""
import argparse
import json
import os
import sys
from io import StringIO
from contextlib import redirect_stdout

from .modules import MODULES


BASE_DIR = os.path.dirname(__file__)
PROFILE_DIR = os.path.join(BASE_DIR, "profiles")


def load_profile(name: str) -> dict:
    """Load a device profile."""
    profile_path = os.path.join(PROFILE_DIR, f"{name}.json")
    if not os.path.exists(profile_path):
        profile_path = os.path.join(PROFILE_DIR, name)
        if not os.path.exists(profile_path):
            raise FileNotFoundError(f"Profile not found: {name}")
    
    with open(profile_path, "r", encoding="utf-8") as f:
        return json.load(f)


def list_profiles() -> None:
    """List available profiles."""
    profiles = []
    for filename in os.listdir(PROFILE_DIR):
        if filename.endswith(".json"):
            profiles.append(filename[:-5])
    
    print("\n=== AVAILABLE PROFILES ===")
    for profile in profiles:
        print(f"  {profile}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Bobby Dev Mode")
    parser.add_argument("--profile", "-p", help="Device profile name")
    parser.add_argument("--module", "-m", help="Module to run", default="dossier")
    parser.add_argument("--list-profiles", action="store_true", help="List profiles")
    parser.add_argument("--list-modules", action="store_true", help="List modules")
    
    args = parser.parse_args(argv)
    
    if args.list_profiles:
        list_profiles()
        return
    
    if args.list_modules:
        print("\n=== AVAILABLE MODULES ===")
        for module in MODULES.keys():
            print(f"  {module}")
        return
    
    if not args.profile:
        print("ERROR: --profile is required")
        parser.print_help()
        sys.exit(1)
    
    try:
        profile = load_profile(args.profile)
        module_func = MODULES.get(args.module)
        if not module_func:
            print(f"ERROR: Unknown module: {args.module}")
            sys.exit(1)
        
        module_func(profile)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
