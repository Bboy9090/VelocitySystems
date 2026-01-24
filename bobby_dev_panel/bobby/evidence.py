"""
Evidence System - Immutable logs with hash verification.
Aligned with Forge Doctrine: Evidence Over Assumption, Transparency Over Convenience
"""

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from .core import log


class EvidenceChain:
    """Immutable evidence chain with hash verification."""
    
    def __init__(self, evidence_dir: str = "evidence"):
        """
        Initialize evidence system.
        
        Args:
            evidence_dir: Directory to store evidence files
        """
        self.evidence_dir = Path(evidence_dir)
        self.evidence_dir.mkdir(exist_ok=True)
        self.chain_file = self.evidence_dir / "chain.json"
        self._init_chain()
    
    def _init_chain(self):
        """Initialize evidence chain if it doesn't exist."""
        if not self.chain_file.exists():
            chain = {
                "created_at": datetime.now().isoformat(),
                "entries": [],
                "last_hash": None
            }
            self._write_chain(chain)
    
    def _read_chain(self) -> Dict[str, Any]:
        """Read evidence chain from file."""
        with open(self.chain_file, "r") as f:
            return json.load(f)
    
    def _write_chain(self, chain: Dict[str, Any]):
        """Write evidence chain to file."""
        with open(self.chain_file, "w") as f:
            json.dump(chain, f, indent=2)
    
    def _hash_data(self, data: str) -> str:
        """Generate SHA256 hash of data."""
        return hashlib.sha256(data.encode()).hexdigest()
    
    def add_evidence(self, event_type: str, data: Dict[str, Any],
                    description: str = "") -> str:
        """
        Add evidence entry to chain.
        
        Args:
            event_type: Type of event (e.g., "intake", "bench_summary", "debloat")
            data: Event data dictionary
            description: Human-readable description
            
        Returns:
            Evidence entry ID (hash)
        """
        chain = self._read_chain()
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "description": description,
            "data": data,
            "previous_hash": chain.get("last_hash")
        }
        
        # Generate hash of entry
        entry_str = json.dumps(entry, sort_keys=True)
        entry_hash = self._hash_data(entry_str)
        entry["hash"] = entry_hash
        
        # Add to chain
        chain["entries"].append(entry)
        chain["last_hash"] = entry_hash
        chain["last_updated"] = datetime.now().isoformat()
        
        self._write_chain(chain)
        
        # Save individual evidence file
        evidence_file = self.evidence_dir / f"{entry_hash}.json"
        with open(evidence_file, "w") as f:
            json.dump(entry, f, indent=2)
        
        log(f"Evidence added: {entry_hash[:16]}... ({event_type})")
        return entry_hash
    
    def verify_chain(self) -> Dict[str, Any]:
        """
        Verify integrity of evidence chain.
        
        Returns:
            Verification result dictionary
        """
        chain = self._read_chain()
        entries = chain.get("entries", [])
        
        if not entries:
            return {
                "valid": True,
                "message": "Chain is empty (no entries yet)",
                "entry_count": 0
            }
        
        errors = []
        previous_hash = None
        
        for i, entry in enumerate(entries):
            # Verify previous hash link
            if entry.get("previous_hash") != previous_hash:
                errors.append(f"Entry {i}: Previous hash mismatch")
            
            # Verify entry hash
            entry_copy = entry.copy()
            entry_hash = entry_copy.pop("hash")
            entry_str = json.dumps(entry_copy, sort_keys=True)
            computed_hash = self._hash_data(entry_str)
            
            if entry_hash != computed_hash:
                errors.append(f"Entry {i}: Hash verification failed")
            
            previous_hash = entry_hash
        
        # Verify last hash matches
        if chain.get("last_hash") != previous_hash:
            errors.append("Last hash mismatch")
        
        return {
            "valid": len(errors) == 0,
            "entry_count": len(entries),
            "errors": errors,
            "last_hash": chain.get("last_hash")
        }
    
    def get_evidence(self, entry_hash: Optional[str] = None,
                    event_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get evidence entries.
        
        Args:
            entry_hash: Specific entry hash (optional)
            event_type: Filter by event type (optional)
            
        Returns:
            List of evidence entries
        """
        chain = self._read_chain()
        entries = chain.get("entries", [])
        
        if entry_hash:
            entries = [e for e in entries if e.get("hash") == entry_hash]
        
        if event_type:
            entries = [e for e in entries if e.get("event_type") == event_type]
        
        return entries
    
    def export_bundle(self, output_file: str) -> str:
        """
        Export evidence bundle (all entries + verification).
        
        Args:
            output_file: Output file path
            
        Returns:
            Bundle hash
        """
        chain = self._read_chain()
        verification = self.verify_chain()
        
        bundle = {
            "exported_at": datetime.now().isoformat(),
            "chain": chain,
            "verification": verification
        }
        
        bundle_str = json.dumps(bundle, indent=2)
        bundle_hash = self._hash_data(bundle_str)
        
        with open(output_file, "w") as f:
            f.write(bundle_str)
        
        log(f"Evidence bundle exported: {output_file} (hash: {bundle_hash[:16]}...)")
        return bundle_hash


def evidence_menu():
    """Interactive menu for evidence tools."""
    evidence = EvidenceChain()
    
    while True:
        print("\n=== Evidence System ===")
        print("1. Add Evidence Entry")
        print("2. Verify Chain")
        print("3. View Evidence")
        print("4. Export Bundle")
        print("0. Back")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            event_type = input("Event type: ").strip()
            description = input("Description: ").strip()
            data_str = input("Data (JSON, or press Enter for empty): ").strip()
            data = json.loads(data_str) if data_str else {}
            entry_hash = evidence.add_evidence(event_type, data, description)
            print(f"\nEvidence added: {entry_hash}")
        elif choice == "2":
            result = evidence.verify_chain()
            print(f"\nVerification: {result}")
        elif choice == "3":
            event_type = input("Event type filter (optional): ").strip() or None
            entries = evidence.get_evidence(event_type=event_type)
            print(f"\nFound {len(entries)} entries:")
            for entry in entries[-10:]:  # Last 10
                print(f"  {entry['hash'][:16]}... - {entry['event_type']} - {entry['timestamp']}")
        elif choice == "4":
            output_file = input("Output file: ").strip() or "evidence_bundle.json"
            bundle_hash = evidence.export_bundle(output_file)
            print(f"\nBundle exported: {output_file}")
        elif choice == "0":
            break
        else:
            print("Invalid choice")
