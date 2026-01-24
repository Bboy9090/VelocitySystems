// Universal Core: Audit Module
// Doctrine-agnostic audit system that always records reality

pub mod append;
pub mod verify;
pub mod merkle;

pub use append::{AuditRecord, AuditLog};
pub use verify::{verify_chain, verify_record, verify_range, verify_merkle, VerificationResult};
pub use merkle::{MerkleTree, MerkleNode};
