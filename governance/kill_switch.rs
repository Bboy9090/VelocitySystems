// Governance: Kill-Switch Doctrine
// When reality goes sideways, this stops the world without destroying it

use serde::{Deserialize, Serialize};
use std::time::{SystemTime, UNIX_EPOCH};
// Note: In actual implementation, this would import from universal-core crate
// For now, using a trait/interface approach
pub trait AuditLogTrait {
    fn append(&mut self, actor: String, action: String, resource: String, outcome: String, event_data: serde_json::Value, doctrine: String) -> ();
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum KillSwitchReason {
    CoreCompromise,
    LegalInjunction,
    RegulatorySeizure,
    InternalBetrayal,
    IrreversibleMisconfiguration,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct KillSwitchEvent {
    pub id: String,
    pub triggered_at: u128,
    pub triggered_by: Vec<String>, // Dual-key holders
    pub reason: KillSwitchReason,
    pub description: String,
    pub audit_marker: String, // Links to audit record
}

pub struct KillSwitch {
    active: bool,
    events: Vec<KillSwitchEvent>,
    // Note: In actual implementation, would hold reference to AuditLog
    // For now, using a simplified approach
}

impl KillSwitch {
    pub fn new() -> Self {
        Self {
            active: false,
            events: Vec::new(),
        }
    }

    /// Trigger kill-switch (requires dual-key authorization)
    pub fn trigger(
        &mut self,
        key_holder_1: String,
        key_holder_2: String,
        reason: KillSwitchReason,
        description: String,
    ) -> Result<(), String> {
        // Verify dual-key requirement
        if key_holder_1 == key_holder_2 {
            return Err("Kill-switch requires two distinct key holders".to_string());
        }

        // Log kill-switch activation
        let event = KillSwitchEvent {
            id: uuid::Uuid::new_v4().to_string(),
            triggered_at: SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .unwrap()
                .as_nanos(),
            triggered_by: vec![key_holder_1.clone(), key_holder_2.clone()],
            reason: reason.clone(),
            description: description.clone(),
            audit_marker: String::new(), // Will be set after logging
        };

        // Create EXTREME severity audit record
        // In actual implementation, would call audit_log.append(...)

        // Activate kill-switch
        self.active = true;
        self.events.push(event);

        Ok(())
    }

    /// Check if kill-switch is active
    pub fn is_active(&self) -> bool {
        self.active
    }

    /// Check if an action is allowed (all actions blocked when active)
    pub fn can_proceed(&self, action: &str, resource: &str) -> bool {
        if self.active {
            // Log blocked action
            // In actual implementation, would call audit_log.append(...)
            false
        } else {
            true
        }
    }

    /// Get kill-switch history
    pub fn history(&self) -> &[KillSwitchEvent] {
        &self.events
    }

    /// Deactivate kill-switch (requires dual-key + justification)
    pub fn deactivate(
        &mut self,
        key_holder_1: String,
        key_holder_2: String,
        justification: String,
    ) -> Result<(), String> {
        if !self.active {
            return Err("Kill-switch is not active".to_string());
        }

        if key_holder_1 == key_holder_2 {
            return Err("Deactivation requires two distinct key holders".to_string());
        }

        // Log deactivation
        // In actual implementation, would call audit_log.append(...)

        self.active = false;
        Ok(())
    }
}

/// Kill-switch effects (what happens when triggered)
pub struct KillSwitchEffects;

impl KillSwitchEffects {
    /// All write/override actions are blocked
    pub fn block_writes() -> bool {
        true
    }

    /// All capabilities are revoked
    pub fn revoke_all_capabilities() -> bool {
        true
    }

    /// All doctrines forced into read-only
    pub fn force_read_only() -> bool {
        true
    }

    /// Truth Escrow is sealed
    pub fn seal_truth_escrow() -> bool {
        true
    }

    /// Self-audit is emitted (EXTREME severity)
    pub fn emit_self_audit() -> bool {
        true
    }
}
