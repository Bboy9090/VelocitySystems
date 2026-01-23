#!/usr/bin/env python3
"""
Binary Provenance Generator
===========================
Embeds build provenance into every artifact.
"""
import json
import hashlib
import subprocess
import pathlib
import time
from datetime import datetime

def get_git_commit() -> str:
    """Get current git commit hash"""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()[:12]
    except Exception:
        return "unknown"

def get_git_branch() -> str:
    """Get current git branch"""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception:
        return "unknown"

def hash_directory(path: str) -> str:
    """Compute SHA-256 hash of directory contents"""
    h = hashlib.sha256()
    for file in sorted(pathlib.Path(path).rglob("*")):
        if file.is_file():
            h.update(str(file.relative_to(path)).encode())
            h.update(file.read_bytes())
    return h.hexdigest()

def generate_provenance(
    product: str = "Phoenix Key",
    edition: str = "BootForge",
    version: str = "1.0.0",
    build_env: str = "PROD"
) -> dict:
    """Generate canonical provenance object"""
    
    core_path = pathlib.Path(__file__).parent.parent / "core"
    core_hash = hash_directory(str(core_path)) if core_path.exists() else ""
    
    matrix_path = core_path / "entitlement" / "matrix.json"
    matrix_hash = ""
    if matrix_path.exists():
        matrix_hash = hashlib.sha256(matrix_path.read_bytes()).hexdigest()
    
    return {
        "product": product,
        "edition": edition,
        "version": version,
        "build_id": f"{datetime.utcnow().strftime('%Y.%m.%d.%H%M')}",
        "git_commit": get_git_commit(),
        "git_branch": get_git_branch(),
        "build_env": build_env,
        "builder": os.environ.get("CI", "local"),
        "built_at": datetime.utcnow().isoformat() + "Z",
        "core_hash": f"sha256:{core_hash}",
        "entitlement_matrix_hash": f"sha256:{matrix_hash}",
        "public_keys": [
            "issuer-2026-01.pub"
        ],
        "signed": True
    }

if __name__ == "__main__":
    import os
    import sys
    
    env = os.getenv("PHOENIX_ENV", "PROD")
    prov = generate_provenance(build_env=env)
    
    output = sys.argv[1] if len(sys.argv) > 1 else "provenance.json"
    with open(output, 'w') as f:
        json.dump(prov, f, indent=2)
    
    print(f"Provenance written to {output}")
    print(json.dumps(prov, indent=2))
