// Universal Core: Hash-Chain Verification
// Verifies integrity of audit chains regardless of doctrine

use super::append::{AuditRecord, AuditLog};
use serde::Serialize;
use sha2::{Sha256, Digest};

/// Verification result
#[derive(Debug, Clone, Serialize)]
pub struct VerificationResult {
    pub valid: bool,
    pub chain_length: usize,
    pub first_violation: Option<usize>,
    pub merkle_root: Option<String>,
    pub integrity_score: f64,
}

/// Verify a single record's hash
pub fn verify_record(record: &AuditRecord) -> bool {
    record.verify()
}

/// Verify entire audit chain integrity
pub fn verify_chain(log: &AuditLog) -> VerificationResult {
    let records = log.all_records();
    let mut first_violation = None;
    let mut valid_count = 0;

    for (i, record) in records.iter().enumerate() {
        if !record.verify() {
            if first_violation.is_none() {
                first_violation = Some(i);
            }
        } else {
            valid_count += 1;
        }

        // Verify chain linkage
        if i > 0 {
            let prev = &records[i - 1];
            if record.previous_hash != prev.hash {
                if first_violation.is_none() {
                    first_violation = Some(i);
                }
            }
        } else {
            if record.previous_hash != "genesis" {
                if first_violation.is_none() {
                    first_violation = Some(0);
                }
            }
        }
    }

    let integrity_score = if records.is_empty() {
        1.0
    } else {
        valid_count as f64 / records.len() as f64
    };

    VerificationResult {
        valid: first_violation.is_none(),
        chain_length: records.len(),
        first_violation,
        merkle_root: compute_merkle_root(records),
        integrity_score,
    }
}

/// Compute Merkle root for evidence purposes
fn compute_merkle_root(records: &[AuditRecord]) -> Option<String> {
    if records.is_empty() {
        return None;
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
                // Odd number - duplicate last hash
                hasher.update(chunk[0].as_bytes());
            }
            next_level.push(format!("{:x}", hasher.finalize()));
        }
        hashes = next_level;
    }

    hashes.first().cloned()
}

/// Verify specific record range
pub fn verify_range(log: &AuditLog, start: usize, end: usize) -> VerificationResult {
    let records = log.all_records();
    if end > records.len() {
        return VerificationResult {
            valid: false,
            chain_length: 0,
            first_violation: Some(start),
            merkle_root: None,
            integrity_score: 0.0,
        };
    }

    let range_records: Vec<&AuditRecord> = records[start..end].iter().collect();
    let mut first_violation = None;
    let mut valid_count = 0;

    for (i, record) in range_records.iter().enumerate() {
        if !record.verify() {
            if first_violation.is_none() {
                first_violation = Some(start + i);
            }
        } else {
            valid_count += 1;
        }
    }

    VerificationResult {
        valid: first_violation.is_none(),
        chain_length: range_records.len(),
        first_violation,
        merkle_root: compute_merkle_root(&range_records.iter().map(|r| (*r).clone()).collect::<Vec<_>>()),
        integrity_score: if range_records.is_empty() {
            1.0
        } else {
            valid_count as f64 / range_records.len() as f64
        },
    }
}

/// Verify records match expected Merkle root
pub fn verify_merkle(records: &[AuditRecord], expected_root: &str) -> bool {
    if let Some(root) = compute_merkle_root(records) {
        root == expected_root
    } else {
        false
    }
}
