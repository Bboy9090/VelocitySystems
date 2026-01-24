// Universal Core: Capability Expiry Management
// Handles time-based expiry regardless of doctrine defaults

use super::capability::CapabilityRegistry;
use std::time::{SystemTime, UNIX_EPOCH, Duration};

pub struct ExpiryManager {
    default_ttl: Option<Duration>, // Doctrine sets this
}

impl ExpiryManager {
    pub fn new(default_ttl: Option<Duration>) -> Self {
        Self { default_ttl }
    }

    /// Calculate expiry time from now
    pub fn calculate_expiry(&self, custom_ttl: Option<Duration>) -> Option<u128> {
        let ttl = custom_ttl.or(self.default_ttl)?;
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap();
        let expires = now + ttl;
        Some(expires.as_nanos() as u128)
    }

    /// Check if expiry should be enforced (doctrine-dependent)
    pub fn should_enforce_expiry(&self) -> bool {
        self.default_ttl.is_some()
    }

    /// Process expiry for all capabilities in registry
    pub fn process_expiry(&self, registry: &mut CapabilityRegistry) {
        registry.expire_old();
    }
}
