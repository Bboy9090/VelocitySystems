// Universal Core: Capability Lifecycle
// Manages authority grants regardless of doctrine

use serde::{Deserialize, Serialize};
use std::time::{SystemTime, UNIX_EPOCH};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum CapabilityState {
    Active,
    Expired,
    Revoked,
    Suspended,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Capability {
    pub id: String,
    pub actor: String,
    pub action: String,
    pub resource: String,
    pub granted_at: u128, // Unix timestamp (nanoseconds)
    pub expires_at: Option<u128>, // None = never expires (doctrine-dependent)
    pub revoked_at: Option<u128>,
    pub state: CapabilityState,
    pub granted_by: String,
    pub justification: Option<String>,
    pub metadata: std::collections::HashMap<String, String>,
}

impl Capability {
    pub fn new(
        id: String,
        actor: String,
        action: String,
        resource: String,
        granted_by: String,
        expires_at: Option<u128>,
    ) -> Self {
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_nanos();

        Self {
            id,
            actor,
            action,
            resource,
            granted_at: now,
            expires_at,
            revoked_at: None,
            state: CapabilityState::Active,
            granted_by,
            justification: None,
            metadata: std::collections::HashMap::new(),
        }
    }

    /// Check if capability is currently valid
    pub fn is_valid(&self) -> bool {
        if self.state != CapabilityState::Active {
            return false;
        }

        if let Some(expires_at) = self.expires_at {
            let now = SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .unwrap()
                .as_nanos();
            if now > expires_at {
                return false;
            }
        }

        true
    }

    /// Check if capability matches action and resource
    pub fn matches(&self, action: &str, resource: &str) -> bool {
        self.action == action && self.resource == resource
    }

    /// Revoke this capability
    pub fn revoke(&mut self, revoked_by: String) {
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_nanos();
        self.revoked_at = Some(now);
        self.state = CapabilityState::Revoked;
        self.metadata.insert("revoked_by".to_string(), revoked_by);
    }

    /// Expire this capability (time-based)
    pub fn expire(&mut self) {
        self.state = CapabilityState::Expired;
    }

    /// Update expiry time
    pub fn set_expiry(&mut self, expires_at: Option<u128>) {
        self.expires_at = expires_at;
    }
}

pub struct CapabilityRegistry {
    capabilities: std::collections::HashMap<String, Capability>,
}

impl CapabilityRegistry {
    pub fn new() -> Self {
        Self {
            capabilities: std::collections::HashMap::new(),
        }
    }

    /// Grant a new capability
    pub fn grant(&mut self, capability: Capability) {
        self.capabilities.insert(capability.id.clone(), capability);
    }

    /// Revoke a capability
    pub fn revoke(&mut self, id: &str, revoked_by: String) -> bool {
        if let Some(cap) = self.capabilities.get_mut(id) {
            cap.revoke(revoked_by);
            true
        } else {
            false
        }
    }

    /// Check if actor has valid capability for action/resource
    pub fn has_capability(&self, actor: &str, action: &str, resource: &str) -> bool {
        self.capabilities
            .values()
            .any(|cap| {
                cap.actor == actor
                    && cap.matches(action, resource)
                    && cap.is_valid()
            })
    }

    /// Get all capabilities for an actor
    pub fn actor_capabilities(&self, actor: &str) -> Vec<&Capability> {
        self.capabilities
            .values()
            .filter(|cap| cap.actor == actor)
            .collect()
    }

    /// Get all active capabilities
    pub fn active_capabilities(&self) -> Vec<&Capability> {
        self.capabilities
            .values()
            .filter(|cap| cap.is_valid())
            .collect()
    }

    /// Expire capabilities that have passed their expiry time
    pub fn expire_old(&mut self) {
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_nanos();

        for cap in self.capabilities.values_mut() {
            if cap.state == CapabilityState::Active {
                if let Some(expires_at) = cap.expires_at {
                    if now > expires_at {
                        cap.expire();
                    }
                }
            }
        }
    }

    /// Get all capabilities (for export/audit)
    pub fn all_capabilities(&self) -> Vec<&Capability> {
        self.capabilities.values().collect()
    }
}

impl Default for CapabilityRegistry {
    fn default() -> Self {
        Self::new()
    }
}
