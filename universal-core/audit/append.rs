// Universal Core: Append-Only Audit Writer
// This module is doctrine-agnostic and always records reality.

use serde::{Deserialize, Serialize};
use sha2::{Sha256, Digest};
use std::time::{SystemTime, UNIX_EPOCH};

/// Immutable audit record that cannot be altered
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AuditRecord {
    /// Sequential index in the chain
    pub index: u64,
    /// Previous record's hash (forms chain)
    pub previous_hash: String,
    /// Current record's hash
    pub hash: String,
    /// Unix timestamp (nanoseconds)
    pub timestamp: u128,
    /// Actor who performed the action
    pub actor: String,
    /// Action performed
    pub action: String,
    /// Resource affected
    pub resource: String,
    /// Outcome (success/failure/denied)
    pub outcome: String,
    /// Raw event data (JSON)
    pub event_data: serde_json::Value,
    /// Doctrine context (phoenix_forge or velocity_systems)
    pub doctrine: String,
    /// Whether this was surfaced to user (doctrine-dependent)
    pub surfaced: bool,
}

impl AuditRecord {
    /// Create a new audit record and compute its hash
    pub fn new(
        index: u64,
        previous_hash: String,
        actor: String,
        action: String,
        resource: String,
        outcome: String,
        event_data: serde_json::Value,
        doctrine: String,
    ) -> Self {
        let timestamp = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_nanos();

        let mut record = Self {
            index,
            previous_hash,
            hash: String::new(), // Will compute
            timestamp,
            actor,
            action,
            resource,
            outcome,
            event_data,
            doctrine,
            surfaced: false, // Doctrine layer controls this
        };

        record.hash = record.compute_hash();
        record
    }

    /// Compute SHA-256 hash of this record
    fn compute_hash(&self) -> String {
        let mut hasher = Sha256::new();
        hasher.update(self.index.to_string().as_bytes());
        hasher.update(self.previous_hash.as_bytes());
        hasher.update(self.timestamp.to_string().as_bytes());
        hasher.update(self.actor.as_bytes());
        hasher.update(self.action.as_bytes());
        hasher.update(self.resource.as_bytes());
        hasher.update(self.outcome.as_bytes());
        hasher.update(serde_json::to_string(&self.event_data).unwrap().as_bytes());
        hasher.update(self.doctrine.as_bytes());
        
        format!("{:x}", hasher.finalize())
    }

    /// Verify this record's integrity
    pub fn verify(&self) -> bool {
        self.hash == self.compute_hash()
    }
}

/// Append-only audit log that maintains chain integrity
pub struct AuditLog {
    records: Vec<AuditRecord>,
    last_hash: String,
}

impl AuditLog {
    pub fn new() -> Self {
        Self {
            records: Vec::new(),
            last_hash: "genesis".to_string(),
        }
    }

    /// Append a new record to the chain
    /// This is the ONLY way to add records - no deletion, no modification
    pub fn append(
        &mut self,
        actor: String,
        action: String,
        resource: String,
        outcome: String,
        event_data: serde_json::Value,
        doctrine: String,
    ) -> AuditRecord {
        let index = self.records.len() as u64;
        let record = AuditRecord::new(
            index,
            self.last_hash.clone(),
            actor,
            action,
            resource,
            outcome,
            event_data,
            doctrine,
        );

        // Verify chain integrity before appending
        if !self.verify_chain() {
            panic!("Audit chain integrity violated - cannot append");
        }

        self.last_hash = record.hash.clone();
        self.records.push(record.clone());
        record
    }

    /// Verify entire chain integrity
    pub fn verify_chain(&self) -> bool {
        for (i, record) in self.records.iter().enumerate() {
            if !record.verify() {
                return false;
            }
            if i > 0 {
                let prev = &self.records[i - 1];
                if record.previous_hash != prev.hash {
                    return false;
                }
            } else {
                if record.previous_hash != "genesis" {
                    return false;
                }
            }
        }
        true
    }

    /// Get all records (immutable view)
    pub fn all_records(&self) -> &[AuditRecord] {
        &self.records
    }

    /// Get records for a specific doctrine
    pub fn by_doctrine(&self, doctrine: &str) -> Vec<&AuditRecord> {
        self.records
            .iter()
            .filter(|r| r.doctrine == doctrine)
            .collect()
    }

    /// Export for evidence bundle (doctrine-agnostic)
    pub fn export_evidence(&self) -> Vec<&AuditRecord> {
        self.records.iter().collect()
    }
}

impl Default for AuditLog {
    fn default() -> Self {
        Self::new()
    }
}
