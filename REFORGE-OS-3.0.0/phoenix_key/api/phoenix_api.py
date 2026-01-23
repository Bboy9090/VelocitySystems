#!/usr/bin/env python3
"""
Phoenix Key Backend API – Enterprise Edition
----------------------------------------------
Serves the React web GUI (dist/) and provides tool endpoints
with canonical licensing, entitlement, and audit enforcement.
"""

from flask import Flask, jsonify, send_from_directory, request
import subprocess
import os
import threading
import logging
import pathlib
import sys

# Add core to path
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from core.core import get_core, init_core
from core.license.types import License
from core.audit.seal import seal

app = Flask(__name__, static_folder="dist", static_url_path="/")

# -------------------------------------------------------------
# Configuration
# -------------------------------------------------------------
PHOENIX_ROOT = pathlib.Path(__file__).resolve().parent.parent
TOOLS_PATH = PHOENIX_ROOT / "tools"
LOG_PATH = "/var/log/phoenix-api.log"
AUDIT_PATH = "/var/log/phoenix-audit.log"

# Initialize canonical core
LICENSE_KEY = os.environ.get("LICENSE_SIGNING_KEY", "devkey" * 8)
if len(LICENSE_KEY) == 64:
    key = bytes.fromhex(LICENSE_KEY)
else:
    key = LICENSE_KEY.encode()

init_core(key, AUDIT_PATH)
core = get_core()

# -------------------------------------------------------------
# Logging
# -------------------------------------------------------------
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def run_command(cmd: str, feature: str = "unknown"):
    """Run a shell command asynchronously with audit logging"""
    logging.info(f"Executing: {cmd}")
    try:
        out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
        logging.info(out)
        return out
    except subprocess.CalledProcessError as e:
        logging.error(e.output)
        return e.output

def get_license_token() -> str:
    """Extract license token from request"""
    return (request.headers.get("X-License", "") or 
            request.args.get("license", "") or
            request.json.get("license", "") if request.is_json else "")

# -------------------------------------------------------------
# API ROUTES
# -------------------------------------------------------------

@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "version": "1.0.0"})

@app.route("/api/license/status")
def license_status():
    """Get current license status"""
    token = get_license_token()
    if not token:
        return jsonify({"active": False, "tier": "free"})
    
    try:
        lic = core.authorize(token, "boot")  # Minimal check
        return jsonify({
            "active": True,
            "tier": lic.tier,
            "subject": lic.subject,
            "seats": lic.seats,
            "expires_at": lic.expires_at
        })
    except PermissionError:
        return jsonify({"active": False, "tier": "free"})

@app.route("/api/tools")
def list_tools():
    """List all available tools with tier requirements"""
    tools = [
        # Free tier
        {"name": "GParted", "cmd": "gparted", "tier": "free", "category": "Recovery"},
        {"name": "TestDisk", "cmd": "testdisk", "tier": "free", "category": "Recovery"},
        {"name": "SMART Check", "cmd": "gsmartcontrol", "tier": "free", "category": "Recovery"},
        {"name": "Boot Repair", "cmd": "boot-repair", "tier": "free", "category": "Recovery"},
        
        # Pro tier
        {"name": "Clonezilla", "cmd": "clonezilla", "tier": "pro", "category": "Recovery"},
        {"name": "Windows 11 Installer", "cmd": "phoenix-tool-win11", "tier": "pro", "category": "OS Installer"},
        {"name": "Ubuntu Installer", "cmd": "phoenix-tool-ubuntu", "tier": "pro", "category": "OS Installer"},
        {"name": "macOS Installer", "cmd": "phoenix-tool-macos", "tier": "pro", "category": "OS Installer"},
        {"name": "Chrome OS Flex", "cmd": "phoenix-tool-chromeos", "tier": "pro", "category": "OS Installer"},
        {"name": "Manjaro", "cmd": "phoenix-tool-manjaro", "tier": "pro", "category": "OS Installer"},
        {"name": "Kali Linux", "cmd": "phoenix-tool-kali", "tier": "pro", "category": "OS Installer"},
        {"name": "Tails OS", "cmd": "phoenix-tool-tails", "tier": "pro", "category": "OS Installer"},
        {"name": "OCLP Patcher", "cmd": "oclp", "tier": "pro", "category": "Mac Tools"},
        {"name": "Kext Injection", "cmd": "phoenix-tool-kext", "tier": "pro", "category": "Mac Tools"},
        {"name": "Boot Camp Drivers", "cmd": "phoenix-tool-bootcamp", "tier": "pro", "category": "Mac Tools"},
        
        # Enterprise tier
        {"name": "Bulk Operations", "cmd": "phoenix-tool-bulk", "tier": "enterprise", "category": "Advanced"},
        {"name": "Audit Export", "cmd": "phoenix-tool-audit-export", "tier": "enterprise", "category": "Advanced"},
        {"name": "Terminal", "cmd": "x-terminal-emulator", "tier": "free", "category": "Advanced"},
        {"name": "Network Tools", "cmd": "phoenix-tool-network", "tier": "free", "category": "Advanced"},
        {"name": "Memtest", "cmd": "memtester 512M", "tier": "free", "category": "Advanced"},
    ]
    return jsonify(tools)

@app.route("/api/run/<tool>", methods=["POST"])
def run_tool(tool: str):
    """Launch a tool command (canonical enforcement)"""
    token = get_license_token()
    
    # Map tool to feature name
    feature_map = {
        "clonezilla": "clonezilla",
        "gparted": "gparted",
        "testdisk": "testdisk",
        "boot-repair": "boot_repair",
        "gsmartcontrol": "smart_check",
        "phoenix-tool-bulk": "bulk_ops",
        "phoenix-tool-audit-export": "audit_export"
    }
    
    feature = feature_map.get(tool, tool)
    
    try:
        # Canonical authorization
        lic = core.authorize(token, feature, actor=request.remote_addr or "unknown")
        
        # Get command
        cmd = request.json.get("cmd") if request.is_json else tool
        
        # Launch asynchronously
        threading.Thread(target=run_command, args=(cmd, feature), daemon=True).start()
        
        return jsonify({
            "status": "launching",
            "cmd": cmd,
            "tier": lic.tier
        })
    except PermissionError as e:
        return jsonify({
            "error": "license_required",
            "message": str(e),
            "tier_required": "pro" if feature not in ["gparted", "testdisk", "smart_check"] else "free"
        }), 402

@app.route("/api/billing/checkout", methods=["POST"])
def create_checkout():
    """Create Stripe checkout session"""
    import stripe
    
    stripe.api_key = os.environ.get("STRIPE_SECRET", "")
    if not stripe.api_key:
        return jsonify({"error": "Stripe not configured"}), 500
    
    body = request.get_json(force=True)
    plan = body.get("plan", "pro_month")
    email = body.get("email")
    
    PRICES = {
        "pro_month": os.environ.get("STRIPE_PRICE_PRO", ""),
        "enterprise_month": os.environ.get("STRIPE_PRICE_ENTERPRISE", "")
    }
    
    price_id = PRICES.get(plan)
    if not price_id:
        return jsonify({"error": "Invalid plan"}), 400
    
    try:
        session = stripe.checkout.Session.create(
            mode="subscription",
            line_items=[{"price": price_id, "quantity": 1}],
            customer_email=email,
            success_url=f'{os.environ.get("APP_BASE_URL", "http://localhost:8000")}/#/billing/success?session={{CHECKOUT_SESSION_ID}}',
            cancel_url=f'{os.environ.get("APP_BASE_URL", "http://localhost:8000")}/#/billing/cancel'
        )
        return jsonify({"url": session.url})
    except Exception as e:
        logging.error(f"Stripe error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/billing/webhook", methods=["POST"])
def stripe_webhook():
    """Handle Stripe webhook events"""
    import stripe
    import time
    from core.license.sign import sign_license
    from core.license.types import License
    import uuid
    
    stripe.api_key = os.environ.get("STRIPE_SECRET", "")
    webhook_secret = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
    
    sig = request.headers.get("Stripe-Signature")
    try:
        event = stripe.Webhook.construct_event(
            request.data, sig, webhook_secret
        )
    except Exception as e:
        return str(e), 400
    
    if event["type"] in ("checkout.session.completed", "customer.subscription.updated"):
        obj = event["data"]["object"]
        customer = obj.get("customer_details", {}).get("email") or obj.get("customer_email")
        tier = "pro" if "pro" in str(obj).lower() else "enterprise"
        
        # Issue license
        lic = License(
            license_id=f"lic-{uuid.uuid4().hex[:12]}",
            subject=customer,
            tier=tier,
            seats=5 if tier == "pro" else 1000,
            expires_at=int(time.time()) + (365 * 24 * 3600),  # 1 year
            issuer_id="issuer-2026-01",
            env="PROD"
        )
        
        key = bytes.fromhex(LICENSE_KEY) if len(LICENSE_KEY) == 64 else LICENSE_KEY.encode()
        token = sign_license(lic, key)
        
        # Store license
        licenses_dir = PHOENIX_ROOT / "licenses"
        licenses_dir.mkdir(parents=True, exist_ok=True)
        (licenses_dir / f"{customer}.lic").write_text(token)
        
        logging.info(f"Issued license to {customer} tier={tier}")
    
    return "", 200

@app.route("/api/audit/export")
def audit_export():
    """Export audit log (Enterprise only)"""
    token = get_license_token()
    
    try:
        lic = core.authorize(token, "audit_export", actor=request.remote_addr or "unknown")
        
        if pathlib.Path(AUDIT_PATH).exists():
            seal_hash = seal(AUDIT_PATH, f"{AUDIT_PATH}.seal")
            return jsonify({
                "status": "ok",
                "seal_hash": seal_hash,
                "log_path": AUDIT_PATH
            })
        else:
            return jsonify({"status": "no_log"})
    except PermissionError:
        return jsonify({"error": "enterprise_required"}), 402

@app.route("/api/logs")
def logs():
    """Return last 200 lines of API log"""
    if not os.path.exists(LOG_PATH):
        return jsonify({"logs": "No logs yet."})
    with open(LOG_PATH, "r") as f:
        lines = f.readlines()[-200:]
    return jsonify({"logs": "".join(lines)})

# -------------------------------------------------------------
# FRONT-END SERVING
# -------------------------------------------------------------

@app.route("/")
def serve_index():
    """Serve index.html from dist/"""
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def serve_static(path):
    """Serve other static assets"""
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

# -------------------------------------------------------------
# ENTRY POINT
# -------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"[Phoenix] Flask API running on port {port} …")
    print(f"[Phoenix] Canonical core initialized")
    print(f"[Phoenix] Audit logging: {AUDIT_PATH}")
    app.run(host="0.0.0.0", port=port)
