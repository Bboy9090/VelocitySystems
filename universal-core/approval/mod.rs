// Universal Core: Approval Module
// Doctrine-agnostic approval system

pub mod request;
pub mod resolution;

pub use request::{ApprovalRequest, ApprovalState};
pub use resolution::{ApprovalRegistry, ApprovalResolution};
