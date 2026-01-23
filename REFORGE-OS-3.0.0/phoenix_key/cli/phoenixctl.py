#!/usr/bin/env python3
"""
Phoenix Key CLI - Canonical Enforcement
========================================
Command-line interface that calls /core (never bypasses).
"""
import argparse
import sys
import os
import pathlib

# Add core to path
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from core.core import get_core, init_core
from core.license.verify import verify_license
from core.audit.seal import seal

def load_license() -> str:
    """Load license from environment or file"""
    # Try environment
    token = os.getenv("PHOENIX_LICENSE", "")
    if token:
        return token
    
    # Try standard locations
    paths = [
        "/forge_state/license.lic",
        "/sysresccd/autorun/phoenix/license.lic",
        pathlib.Path.home() / ".phoenix" / "license.lic"
    ]
    
    for p in paths:
        if pathlib.Path(p).exists():
            return pathlib.Path(p).read_text().strip()
    
    return ""

def cmd_status(args):
    """Show license status"""
    token = load_license()
    if not token:
        print("No license found. Running in FREE mode.")
        return
    
    key = os.getenv("LICENSE_SIGNING_KEY", "devkey" * 8)
    if len(key) == 64:
        key_bytes = bytes.fromhex(key)
    else:
        key_bytes = key.encode()
    
    lic = verify_license(token, key_bytes)
    if not lic:
        print("Invalid license token.")
        return
    
    print(f"License ID: {lic.license_id}")
    print(f"Subject: {lic.subject}")
    print(f"Tier: {lic.tier.upper()}")
    print(f"Seats: {lic.seats}")
    if lic.expires_at:
        from datetime import datetime
        exp = datetime.fromtimestamp(lic.expires_at)
        print(f"Expires: {exp}")

def cmd_run(args):
    """Run a tool with canonical authorization"""
    token = load_license()
    feature = args.feature
    
    # Initialize core
    key = os.getenv("LICENSE_SIGNING_KEY", "devkey" * 8)
    if len(key) == 64:
        key_bytes = bytes.fromhex(key)
    else:
        key_bytes = key.encode()
    
    init_core(key_bytes)
    core = get_core()
    
    try:
        lic = core.authorize(token, feature, actor=os.getenv("USER", "cli"))
        print(f"Authorized as {lic.tier.upper()}")
        
        # Execute command
        import subprocess
        subprocess.run(args.cmd, shell=True)
    except PermissionError as e:
        print(f"Permission denied: {e}", file=sys.stderr)
        sys.exit(1)

def cmd_audit_export(args):
    """Export audit log (Enterprise only)"""
    token = load_license()
    
    key = os.getenv("LICENSE_SIGNING_KEY", "devkey" * 8)
    if len(key) == 64:
        key_bytes = bytes.fromhex(key)
    else:
        key_bytes = key.encode()
    
    init_core(key_bytes)
    core = get_core()
    
    try:
        lic = core.authorize(token, "audit_export", actor=os.getenv("USER", "cli"))
        
        audit_path = args.log or "/var/log/phoenix-audit.log"
        if not pathlib.Path(audit_path).exists():
            print(f"Audit log not found: {audit_path}")
            return
        
        seal_hash = seal(audit_path, f"{audit_path}.seal")
        print(f"Audit log sealed: {seal_hash}")
        print(f"Log: {audit_path}")
        print(f"Seal: {audit_path}.seal")
    except PermissionError:
        print("Enterprise license required for audit export.", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Phoenix Key CLI")
    sub = parser.add_subparsers(dest="cmd")
    
    # Status
    sub.add_parser("status", help="Show license status")
    
    # Run
    run_parser = sub.add_parser("run", help="Run tool with authorization")
    run_parser.add_argument("feature", help="Feature name")
    run_parser.add_argument("cmd", nargs=argparse.REMAINDER, help="Command to run")
    
    # Audit
    audit_parser = sub.add_parser("audit-export", help="Export audit log")
    audit_parser.add_argument("--log", help="Audit log path", default="/var/log/phoenix-audit.log")
    
    args = parser.parse_args()
    
    if args.cmd == "status":
        cmd_status(args)
    elif args.cmd == "run":
        cmd_run(args)
    elif args.cmd == "audit-export":
        cmd_audit_export(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
