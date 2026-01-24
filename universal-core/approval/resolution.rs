// Universal Core: Approval Resolution
// Resolves approval requests and links to execution

use super::request::{ApprovalRequest, ApprovalState};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ApprovalResolution {
    pub request_id: String,
    pub final_state: ApprovalState,
    pub resolved_at: u128,
    pub approvers: Vec<String>,
    pub execution_id: Option<String>, // Links to actual execution if approved
}

pub struct ApprovalRegistry {
    requests: std::collections::HashMap<String, ApprovalRequest>,
}

impl ApprovalRegistry {
    pub fn new() -> Self {
        Self {
            requests: std::collections::HashMap::new(),
        }
    }

    /// Create a new approval request
    pub fn create(&mut self, request: ApprovalRequest) {
        self.requests.insert(request.id.clone(), request);
    }

    /// Get a request by ID
    pub fn get(&self, id: &str) -> Option<&ApprovalRequest> {
        self.requests.get(id)
    }

    /// Get a mutable request by ID
    pub fn get_mut(&mut self, id: &str) -> Option<&mut ApprovalRequest> {
        self.requests.get_mut(id)
    }

    /// Get all pending requests
    pub fn pending(&self) -> Vec<&ApprovalRequest> {
        self.requests
            .values()
            .filter(|r| r.state == ApprovalState::Pending)
            .collect()
    }

    /// Get all requests for an actor
    pub fn actor_requests(&self, actor: &str) -> Vec<&ApprovalRequest> {
        self.requests
            .values()
            .filter(|r| r.actor == actor)
            .collect()
    }

    /// Expire old requests
    pub fn expire_old(&mut self) {
        for request in self.requests.values_mut() {
            if request.state == ApprovalState::Pending && request.is_expired() {
                request.state = ApprovalState::Expired;
            }
        }
    }

    /// Get all requests (for export/audit)
    pub fn all_requests(&self) -> Vec<&ApprovalRequest> {
        self.requests.values().collect()
    }
}

impl Default for ApprovalRegistry {
    fn default() -> Self {
        Self::new()
    }
}
