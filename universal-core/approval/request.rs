// Universal Core: Approval Request System
// Handles approval workflows regardless of doctrine

use serde::{Deserialize, Serialize};
use std::time::{SystemTime, UNIX_EPOCH};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum ApprovalState {
    Pending,
    Approved,
    Denied,
    Expired,
    Cancelled,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ApprovalRequest {
    pub id: String,
    pub intent_id: String, // Links to original intent
    pub actor: String,
    pub action: String,
    pub resource: String,
    pub justification: Option<String>,
    pub state: ApprovalState,
    pub created_at: u128,
    pub expires_at: Option<u128>,
    pub approved_by: Vec<String>, // For dual approval
    pub denied_by: Option<String>,
    pub metadata: std::collections::HashMap<String, String>,
}

impl ApprovalRequest {
    pub fn new(
        id: String,
        intent_id: String,
        actor: String,
        action: String,
        resource: String,
        justification: Option<String>,
        expires_at: Option<u128>,
    ) -> Self {
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_nanos();

        Self {
            id,
            intent_id,
            actor,
            action,
            resource,
            justification,
            state: ApprovalState::Pending,
            created_at: now,
            expires_at,
            approved_by: Vec::new(),
            denied_by: None,
            metadata: std::collections::HashMap::new(),
        }
    }

    /// Approve this request
    pub fn approve(&mut self, approver: String, requires_dual: bool) -> Result<(), String> {
        if self.state != ApprovalState::Pending {
            return Err("Request is not pending".to_string());
        }

        if self.is_expired() {
            self.state = ApprovalState::Expired;
            return Err("Request has expired".to_string());
        }

        self.approved_by.push(approver);

        if requires_dual {
            if self.approved_by.len() >= 2 {
                self.state = ApprovalState::Approved;
            }
            // Still pending if only one approval
        } else {
            self.state = ApprovalState::Approved;
        }

        Ok(())
    }

    /// Deny this request
    pub fn deny(&mut self, denier: String, reason: Option<String>) -> Result<(), String> {
        if self.state != ApprovalState::Pending {
            return Err("Request is not pending".to_string());
        }

        self.state = ApprovalState::Denied;
        self.denied_by = Some(denier);
        if let Some(reason) = reason {
            self.metadata.insert("denial_reason".to_string(), reason);
        }

        Ok(())
    }

    /// Check if request is expired
    pub fn is_expired(&self) -> bool {
        if let Some(expires_at) = self.expires_at {
            let now = SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .unwrap()
                .as_nanos();
            return now > expires_at;
        }
        false
    }

    /// Check if request is approved
    pub fn is_approved(&self) -> bool {
        self.state == ApprovalState::Approved
    }
}
