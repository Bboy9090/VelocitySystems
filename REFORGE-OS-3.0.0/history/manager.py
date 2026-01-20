"""History manager - case files and master tickets."""
import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional


BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "storage", "history")
os.makedirs(BASE_DIR, exist_ok=True)

MASTER_FILE = os.path.join(BASE_DIR, "master_tickets.json")


def _load_master_tickets() -> Dict[str, Any]:
    """Load master tickets."""
    if not os.path.exists(MASTER_FILE):
        return {}
    try:
        with open(MASTER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def _save_master_tickets(data: Dict[str, Any]) -> None:
    """Save master tickets."""
    with open(MASTER_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def save_case(ticket_id: str, payload: Dict[str, Any]) -> None:
    """Save a case file."""
    case_file = os.path.join(BASE_DIR, f"{ticket_id}.json")
    payload["saved_at"] = datetime.utcnow().isoformat() + "Z"
    with open(case_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def load_case(ticket_id: str) -> Optional[Dict[str, Any]]:
    """Load a case file."""
    case_file = os.path.join(BASE_DIR, f"{ticket_id}.json")
    if not os.path.exists(case_file):
        return None
    try:
        with open(case_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None


def list_cases() -> List[str]:
    """List all case IDs."""
    cases = []
    for filename in os.listdir(BASE_DIR):
        if filename.endswith(".json") and filename != "master_tickets.json":
            cases.append(filename[:-5])
    return sorted(cases)


def create_master_ticket(label: str, description: str = "", initial_cases: List[str] = None) -> Dict[str, Any]:
    """Create a master ticket."""
    masters = _load_master_tickets()
    master_id = f"MASTER-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"
    
    master = {
        "id": master_id,
        "label": label,
        "description": description,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "cases": initial_cases or []
    }
    
    masters[master_id] = master
    _save_master_tickets(masters)
    return master


def list_master_tickets() -> List[Dict[str, Any]]:
    """List all master tickets."""
    masters = _load_master_tickets()
    return list(masters.values())


def attach_case_to_master(master_id: str, case_id: str) -> Dict[str, Any]:
    """Attach a case to a master ticket."""
    masters = _load_master_tickets()
    if master_id not in masters:
        raise ValueError(f"Master ticket not found: {master_id}")
    
    master = masters[master_id]
    if case_id not in master["cases"]:
        master["cases"].append(case_id)
        _save_master_tickets(masters)
    
    return master


def save_devmode_run(profile: Dict[str, Any], module: str, output: str) -> str:
    """Save a DevMode run as a case."""
    ticket_id = f"DEVMODE-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"
    payload = {
        "ticket_id": ticket_id,
        "type": "devmode",
        "profile": profile,
        "module": module,
        "output": output,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    save_case(ticket_id, payload)
    return ticket_id


def save_diagnostic_run(device_info: Dict[str, Any], results: Dict[str, Any]) -> str:
    """Save a diagnostic run as a case."""
    ticket_id = f"DIAG-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"
    payload = {
        "ticket_id": ticket_id,
        "type": "diagnostic",
        "device": device_info,
        "results": results,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    save_case(ticket_id, payload)
    return ticket_id
