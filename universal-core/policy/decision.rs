// Universal Core: Policy Decision Logic
// Handles decision outcomes and their implications

use super::engine::{PolicyDecision, PolicyContext};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DecisionResult {
    pub decision: PolicyDecision,
    pub context: PolicyContext,
    pub rule_id: Option<String>,
    pub requires_approval: bool,
    pub requires_dual_approval: bool,
    pub can_proceed: bool,
    pub reason: String,
}

impl DecisionResult {
    pub fn from_decision(decision: PolicyDecision, context: PolicyContext, rule_id: Option<String>) -> Self {
        let requires_approval = matches!(
            decision,
            PolicyDecision::AllowWithApproval | PolicyDecision::RequireDualApproval
        );
        let requires_dual_approval = matches!(decision, PolicyDecision::RequireDualApproval);
        let can_proceed = matches!(
            decision,
            PolicyDecision::Allow | PolicyDecision::AllowWithApproval | PolicyDecision::RequireDualApproval
        );

        let reason = match decision {
            PolicyDecision::Allow => "Action allowed by policy".to_string(),
            PolicyDecision::Deny => "Action denied by policy".to_string(),
            PolicyDecision::AllowWithApproval => "Action requires approval".to_string(),
            PolicyDecision::RequireDualApproval => "Action requires dual approval".to_string(),
            PolicyDecision::Escalate => "Action requires escalation".to_string(),
        };

        Self {
            decision,
            context,
            rule_id,
            requires_approval,
            requires_dual_approval,
            can_proceed,
            reason,
        }
    }

    /// Check if this decision should be logged (always true for core)
    pub fn should_log(&self) -> bool {
        true // Core always logs
    }

    /// Check if this decision should be surfaced to user (doctrine-dependent)
    pub fn should_surface(&self) -> bool {
        // Doctrine layer controls this
        matches!(
            self.decision,
            PolicyDecision::Deny | PolicyDecision::RequireDualApproval | PolicyDecision::Escalate
        )
    }
}
