#!/usr/bin/env python3
"""Bobby Dev Mode API CLI - JSON interface for Tauri."""
import json
import os
import sys
from io import StringIO
from contextlib import redirect_stdout
from datetime import datetime

from .modules import MODULES
from .cli import load_profile, list_profiles as _list_profiles


def list_profiles_json():
    """List profiles as JSON."""
    profiles = []
    profile_dir = os.path.join(os.path.dirname(__file__), "profiles")
    for filename in os.listdir(profile_dir):
        if filename.endswith(".json"):
            profile_key = filename[:-5]
            try:
                profile = load_profile(profile_key)
                profiles.append({
                    "key": profile_key,
                    "name": profile.get("name", profile_key),
                    "brand": profile.get("brand", "Unknown")
                })
            except:
                pass
    return profiles


def run_module_json(profile_name: str, module: str):
    """Run a module and return JSON output."""
    try:
        profile = load_profile(profile_name)
        module_func = MODULES.get(module)
        if not module_func:
            return {
                "error": f"Unknown module: {module}",
                "profile": profile_name,
                "module": module,
                "output": ""
            }
        
        # Capture output
        buf = StringIO()
        with redirect_stdout(buf):
            module_func(profile)
        output = buf.getvalue()
        
        # Save to history (if history module exists)
        try:
            from ..history.manager import save_devmode_run
            profile["id"] = profile_name
            ticket_id = save_devmode_run(profile, module, output)
        except:
            ticket_id = None
        
        return {
            "profile": profile_name,
            "module": module,
            "output": output,
            "ticket_id": ticket_id
        }
    except Exception as e:
        return {
            "error": str(e),
            "profile": profile_name,
            "module": module,
            "output": ""
        }


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Command required"}))
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "list-profiles":
        profiles = list_profiles_json()
        print(json.dumps(profiles, indent=2))
    elif cmd == "list-modules":
        modules = list(MODULES.keys())
        print(json.dumps(modules, indent=2))
    elif cmd == "run":
        if len(sys.argv) < 4:
            print(json.dumps({"error": "Usage: run <profile> <module>"}))
            sys.exit(1)
        profile_name = sys.argv[2]
        module = sys.argv[3]
        result = run_module_json(profile_name, module)
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps({"error": f"Unknown command: {cmd}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
