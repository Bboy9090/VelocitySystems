// Universal Core: Authority Module
// Doctrine-agnostic authority management

pub mod capability;
pub mod expiry;
pub mod revoke;

pub use capability::{Capability, CapabilityRegistry, CapabilityState};
pub use expiry::ExpiryManager;
pub use revoke::{RevocationManager, RevocationRequest};
