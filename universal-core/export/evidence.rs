// Universal Core: Evidence Export
// Creates legal-grade evidence bundles regardless of doctrine

use serde::{Deserialize, Serialize};
use crate::audit::{AuditRecord, AuditLog};
use crate::authority::Capability;
use crate::approval::ApprovalRequest;
use crate::policy::PolicyRule;
use uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EvidenceBundle {
    pub id: String,
    pub created_at: u128,
    pub merkle_root: String,
    pub audit_records: Vec<AuditRecord>,
    pub capabilities: Vec<Capability>,
    pub approvals: Vec<ApprovalRequest>,
    pub policies: Vec<PolicyRule>,
    pub integrity_verified: bool,
    pub metadata: std::collections::HashMap<String, String>,
}

pub struct EvidenceExporter;

impl EvidenceExporter {
    /// Create a complete evidence bundle from system state
    pub fn export(
        audit_log: &AuditLog,
        capabilities: Vec<Capability>,
        approvals: Vec<ApprovalRequest>,
        policies: Vec<PolicyRule>,
        metadata: std::collections::HashMap<String, String>,
    ) -> EvidenceBundle {
        let records = audit_log.all_records();
        let merkle_root = Self::compute_merkle_root(records);

        let bundle = EvidenceBundle {
            id: uuid::Uuid::new_v4().to_string(),
            created_at: std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap()
                .as_nanos(),
            merkle_root,
            audit_records: records.to_vec(),
            capabilities,
            approvals,
            policies,
            integrity_verified: audit_log.verify_chain(),
            metadata,
        };

        bundle
    }

    /// Compute Merkle root for evidence integrity
    fn compute_merkle_root(records: &[AuditRecord]) -> String {
        use sha2::{Sha256, Digest};
        
        if records.is_empty() {
            return "empty".to_string();
        }

        let mut hashes: Vec<String> = records.iter().map(|r| r.hash.clone()).collect();

        while hashes.len() > 1 {
            let mut next_level = Vec::new();
            for chunk in hashes.chunks(2) {
                let mut hasher = Sha256::new();
                hasher.update(chunk[0].as_bytes());
                if chunk.len() > 1 {
                    hasher.update(chunk[1].as_bytes());
                } else {
                    hasher.update(chunk[0].as_bytes());
                }
                next_level.push(format!("{:x}", hasher.finalize()));
            }
            hashes = next_level;
        }

        hashes.first().cloned().unwrap_or_else(|| "empty".to_string())
    }

    /// Export bundle to JSON (for legal/regulatory purposes)
    pub fn to_json(bundle: &EvidenceBundle) -> Result<String, serde_json::Error> {
        serde_json::to_string_pretty(bundle)
    }

    /// Verify bundle integrity
    pub fn verify(bundle: &EvidenceBundle) -> bool {
        if !bundle.integrity_verified {
            return false;
        }

        let computed_root = Self::compute_merkle_root(&bundle.audit_records);
        computed_root == bundle.merkle_root
    }
}
