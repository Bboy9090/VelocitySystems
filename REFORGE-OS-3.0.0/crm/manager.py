"""CRM manager - customers and devices."""
import os
import json
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional


BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "storage", "crm")
os.makedirs(BASE_DIR, exist_ok=True)

CUSTOMERS_FILE = os.path.join(BASE_DIR, "customers.json")
DEVICES_FILE = os.path.join(BASE_DIR, "devices.json")


def _load_customers() -> Dict[str, Any]:
    """Load customers."""
    if not os.path.exists(CUSTOMERS_FILE):
        return {}
    try:
        with open(CUSTOMERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def _save_customers(data: Dict[str, Any]) -> None:
    """Save customers."""
    with open(CUSTOMERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _load_devices() -> Dict[str, Any]:
    """Load devices."""
    if not os.path.exists(DEVICES_FILE):
        return {}
    try:
        with open(DEVICES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def _save_devices(data: Dict[str, Any]) -> None:
    """Save devices."""
    with open(DEVICES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def add_customer(name: str, phone: str = "", email: str = "") -> str:
    """Add a customer."""
    customers = _load_customers()
    customer_id = str(uuid.uuid4())
    
    customer = {
        "id": customer_id,
        "name": name,
        "phone": phone,
        "email": email,
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    
    customers[customer_id] = customer
    _save_customers(customers)
    return customer_id


def list_customers() -> List[Dict[str, Any]]:
    """List all customers."""
    customers = _load_customers()
    return list(customers.values())


def add_device(
    customer_id: str,
    label: str,
    serial: str = "",
    notes: str = "",
    platform: str = "android",
    status: str = "active"
) -> str:
    """Add a device to a customer."""
    devices = _load_devices()
    device_id = str(uuid.uuid4())
    
    device = {
        "id": device_id,
        "customer_id": customer_id,
        "label": label,
        "serial": serial,
        "notes": notes,
        "platform": platform,
        "status": status,
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    
    devices[device_id] = device
    _save_devices(devices)
    return device_id


def list_devices(customer_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """List devices, optionally filtered by customer."""
    devices = _load_devices()
    device_list = list(devices.values())
    
    if customer_id:
        device_list = [d for d in device_list if d.get("customer_id") == customer_id]
    
    return device_list
