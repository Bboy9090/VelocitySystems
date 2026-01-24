// Universal Core: Kernel
// The central integration point that binds all core systems together
// This is doctrine-agnostic and always records reality

use crate::audit::{AuditLog, AuditRecord};
use crate::policy::{PolicyEngine, Intent, DecisionResult, PolicyDecision};
use crate::authority::{CapabilityRegistry, ExpiryManager};
use crate::approval::{ApprovalRegistry, ApprovalRequest};
use crate::export::{EvidenceExporter, EvidenceBundle};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// Universal Kernel - the core that never lies
pub struct Kernel {
    audit_log: AuditLog,
    policy_engine: PolicyEngine,
    capability_registry: CapabilityRegistry,
    approval_registry: ApprovalRegistry,
    expiry_manager: ExpiryManager,
    doctrine: String, // "phoenix_forge" or "velocity_systems"
    truth_escrow_enabled: bool,
}

impl Kernel {
    /// Create a new kernel with a doctrine
    pub fn new(doctrine: String, default_ttl: Option<std::time::Duration>) -> Self {
        Self {
            audit_log: AuditLog::new(),
            policy_engine: PolicyEngine::new(),
            capability_registry: CapabilityRegistry::new(),
            approval_registry: ApprovalRegistry::new(),
            expiry_manager: ExpiryManager::new(default_ttl),
            doctrine: doctrine.clone(),
            truth_escrow_enabled: true, // Always enabled in core
        }
    }

    /// Load policy rules (from doctrine)
    pub fn load_policies(&mut self, rules: Vec<crate::policy::PolicyRule>) {
        self.policy_engine.load_rules(rules);
    }

    /// Execute an intent through the system
    pub fn execute_intent(
        &mut self,
        intent: Intent,
        actor_roles: Vec<String>,
        resource_tags: Vec<String>,
    ) -> ExecutionResult {
        // 1. Validate intent (doctrine may require justification)
        let require_justification = self.doctrine == "phoenix_forge";
        if let Err(e) = intent.validate(require_justification) {
            return ExecutionResult::denied(e);
        }

        // 2. Evaluate policy
        let context = intent.to_context(actor_roles, resource_tags);
        let decision = self.policy_engine.evaluate(&context);
        let decision_result = DecisionResult::from_decision(
            decision.clone(),
            context.clone(),
            None, // Rule ID would come from engine
        );

        // 3. Check capabilities
        let has_capability = self.capability_registry.has_capability(
            &intent.actor,
            &intent.action,
            &intent.resource,
        );

        // 4. Determine if approval is needed
        let needs_approval = decision_result.requires_approval
            || (self.doctrine == "phoenix_forge" && !has_capability);

        // 5. Log the intent evaluation (ALWAYS - core never lies)
        self.audit_log.append(
            intent.actor.clone(),
            format!("intent:evaluate:{}", intent.action),
            intent.resource.clone(),
            format!("decision:{:?}", decision),
            serde_json::json!({
                "intent_id": "temp", // Would be generated
                "needs_approval": needs_approval,
                "has_capability": has_capability,
            }),
            self.doctrine.clone(),
        );

        // 6. Handle approval requirement
        if needs_approval {
            if self.doctrine == "velocity_systems" {
                // Velocity: approvals are optional, proceed anyway
                return ExecutionResult::approved_with_warning(
                    "Proceeding without explicit approval (Velocity mode)".to_string(),
                );
            } else {
                // Phoenix: require approval
                let approval_id = uuid::Uuid::new_v4().to_string();
                let approval = ApprovalRequest::new(
                    approval_id.clone(),
                    "intent_id".to_string(), // Would link to actual intent
                    intent.actor.clone(),
                    intent.action.clone(),
                    intent.resource.clone(),
                    intent.justification.clone(),
                    None, // Expiry would be doctrine-dependent
                );
                self.approval_registry.create(approval);
                return ExecutionResult::requires_approval(approval_id);
            }
        }

        // 7. Execute (if allowed)
        if decision_result.can_proceed {
            ExecutionResult::allowed("Action executed".to_string())
        } else {
            ExecutionResult::denied(decision_result.reason)
        }
    }

    /// Grant a capability
    pub fn grant_capability(
        &mut self,
        actor: String,
        action: String,
        resource: String,
        granted_by: String,
        expires_at: Option<u128>,
    ) -> String {
        let id = uuid::Uuid::new_v4().to_string();
        let capability = crate::authority::Capability::new(
            id.clone(),
            actor.clone(),
            action.clone(),
            resource.clone(),
            granted_by.clone(),
            expires_at,
        );
        self.capability_registry.grant(capability);

        // Log capability grant (ALWAYS)
        self.audit_log.append(
            granted_by,
            "capability:grant".to_string(),
            format!("{}:{}", action, resource),
            "success".to_string(),
            serde_json::json!({
                "capability_id": id,
                "actor": actor,
            }),
            self.doctrine.clone(),
        );

        id
    }

    /// Export evidence bundle (for legal/regulatory purposes)
    pub fn export_evidence(&self, metadata: HashMap<String, String>) -> EvidenceBundle {
        EvidenceExporter::export(
            &self.audit_log,
            self.capability_registry.all_capabilities().iter().map(|c| (*c).clone()).collect(),
            self.approval_registry.all_requests().iter().map(|r| (*r).clone()).collect(),
            self.policy_engine.all_rules().iter().map(|r| (*r).clone()).collect(),
            metadata,
        )
    }

    /// Verify system integrity
    pub fn verify_integrity(&self) -> bool {
        self.audit_log.verify_chain()
    }

    /// Get audit log (read-only)
    pub fn audit_log(&self) -> &AuditLog {
        &self.audit_log
    }

    /// Process expiry (should be called periodically)
    pub fn process_expiry(&mut self) {
        self.expiry_manager.process_expiry(&mut self.capability_registry);
        self.approval_registry.expire_old();
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum ExecutionResult {
    Allowed(String),
    Denied(String),
    RequiresApproval(String), // Approval ID
    ApprovedWithWarning(String),
}

impl ExecutionResult {
    pub fn allowed(message: String) -> Self {
        Self::Allowed(message)
    }

    pub fn denied(reason: String) -> Self {
        Self::Denied(reason)
    }

    pub fn requires_approval(approval_id: String) -> Self {
        Self::RequiresApproval(approval_id)
    }

    pub fn approved_with_warning(message: String) -> Self {
        Self::ApprovedWithWarning(message)
    }
}
