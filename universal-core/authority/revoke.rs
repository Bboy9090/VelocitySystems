// Universal Core: Capability Revocation
// Handles revocation regardless of doctrine

use super::capability::{CapabilityRegistry, Capability};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RevocationRequest {
    pub capability_id: String,
    pub revoked_by: String,
    pub reason: Option<String>,
    pub immediate: bool,
}

pub struct RevocationManager {
    registry: CapabilityRegistry,
}

impl RevocationManager {
    pub fn new(registry: CapabilityRegistry) -> Self {
        Self { registry }
    }

    /// Revoke a capability
    pub fn revoke(&mut self, request: RevocationRequest) -> Result<(), String> {
        if self.registry.revoke(&request.capability_id, request.revoked_by.clone()) {
            Ok(())
        } else {
            Err(format!("Capability {} not found", request.capability_id))
        }
    }

    /// Bulk revoke capabilities matching criteria
    pub fn revoke_matching(
        &mut self,
        actor: Option<&str>,
        action: Option<&str>,
        resource: Option<&str>,
        revoked_by: String,
    ) -> usize {
        let mut count = 0;
        let capabilities: Vec<String> = self
            .registry
            .all_capabilities()
            .into_iter()
            .filter(|cap| {
                cap.is_valid()
                    && actor.map_or(true, |a| cap.actor == a)
                    && action.map_or(true, |a| cap.action == a)
                    && resource.map_or(true, |r| cap.resource == r)
            })
            .map(|cap| cap.id.clone())
            .collect();

        for id in capabilities {
            if self.registry.revoke(&id, revoked_by.clone()) {
                count += 1;
            }
        }

        count
    }

    /// Get revocation history (for audit)
    pub fn revocation_history(&self) -> Vec<&Capability> {
        self.registry
            .all_capabilities()
            .into_iter()
            .filter(|cap| cap.revoked_at.is_some())
            .collect()
    }
}
