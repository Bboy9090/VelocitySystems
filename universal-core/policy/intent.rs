// Universal Core: Intent Evaluation
// Captures and evaluates user intent before execution

use serde::{Deserialize, Serialize};
use super::engine::PolicyContext;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Intent {
    pub actor: String,
    pub action: String,
    pub resource: String,
    pub justification: Option<String>, // Doctrine may require this
    pub urgency: Urgency,
    pub metadata: std::collections::HashMap<String, String>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum Urgency {
    Normal,
    High,
    Emergency,
}

impl Intent {
    pub fn new(actor: String, action: String, resource: String) -> Self {
        Self {
            actor,
            action,
            resource,
            justification: None,
            urgency: Urgency::Normal,
            metadata: std::collections::HashMap::new(),
        }
    }

    pub fn with_justification(mut self, justification: String) -> Self {
        self.justification = Some(justification);
        self
    }

    pub fn with_urgency(mut self, urgency: Urgency) -> Self {
        self.urgency = urgency;
        self
    }

    pub fn to_context(&self, actor_roles: Vec<String>, resource_tags: Vec<String>) -> PolicyContext {
        PolicyContext {
            actor: self.actor.clone(),
            action: self.action.clone(),
            resource: self.resource.clone(),
            actor_roles,
            resource_tags,
            metadata: self.metadata.clone(),
        }
    }

    /// Validate intent completeness (doctrine-dependent requirements)
    pub fn validate(&self, require_justification: bool) -> Result<(), String> {
        if require_justification && self.justification.is_none() {
            return Err("Justification required but not provided".to_string());
        }
        Ok(())
    }
}
