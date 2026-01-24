// Universal Core: Policy Evaluation Engine
// Doctrine-agnostic policy engine that evaluates intent against rules

use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum PolicyDecision {
    Allow,
    Deny,
    AllowWithApproval,
    RequireDualApproval,
    Escalate,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PolicyRule {
    pub id: String,
    pub name: String,
    pub action_pattern: String, // e.g., "user.*", "admin.delete"
    pub resource_pattern: String,
    pub decision: PolicyDecision,
    pub conditions: HashMap<String, String>, // Key-value conditions
    pub priority: u32, // Higher = evaluated first
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PolicyContext {
    pub actor: String,
    pub action: String,
    pub resource: String,
    pub actor_roles: Vec<String>,
    pub resource_tags: Vec<String>,
    pub metadata: HashMap<String, String>,
}

pub struct PolicyEngine {
    rules: Vec<PolicyRule>,
}

impl PolicyEngine {
    pub fn new() -> Self {
        Self {
            rules: Vec::new(),
        }
    }

    /// Load rules from doctrine configuration
    pub fn load_rules(&mut self, rules: Vec<PolicyRule>) {
        self.rules = rules;
        // Sort by priority (highest first)
        self.rules.sort_by(|a, b| b.priority.cmp(&a.priority));
    }

    /// Evaluate policy for a given context
    pub fn evaluate(&self, context: &PolicyContext) -> PolicyDecision {
        for rule in &self.rules {
            if self.matches(rule, context) {
                return rule.decision.clone();
            }
        }
        // Default deny if no rule matches
        PolicyDecision::Deny
    }

    /// Check if a rule matches the context
    fn matches(&self, rule: &PolicyRule, context: &PolicyContext) -> bool {
        // Check action pattern
        if !self.pattern_matches(&rule.action_pattern, &context.action) {
            return false;
        }

        // Check resource pattern
        if !self.pattern_matches(&rule.resource_pattern, &context.resource) {
            return false;
        }

        // Check conditions
        for (key, expected_value) in &rule.conditions {
            match key.as_str() {
                "role" => {
                    if !context.actor_roles.iter().any(|r| r == expected_value) {
                        return false;
                    }
                }
                "tag" => {
                    if !context.resource_tags.iter().any(|t| t == expected_value) {
                        return false;
                    }
                }
                _ => {
                    // Check metadata
                    if let Some(actual_value) = context.metadata.get(key) {
                        if actual_value != expected_value {
                            return false;
                        }
                    } else {
                        return false;
                    }
                }
            }
        }

        true
    }

    /// Simple pattern matching (supports * wildcard)
    fn pattern_matches(&self, pattern: &str, value: &str) -> bool {
        if pattern == "*" {
            return true;
        }
        if pattern == value {
            return true;
        }
        // Simple wildcard matching
        if pattern.ends_with(".*") {
            let prefix = &pattern[..pattern.len() - 2];
            return value.starts_with(prefix);
        }
        false
    }

    /// Get all rules (for export/audit)
    pub fn all_rules(&self) -> &[PolicyRule] {
        &self.rules
    }

    /// Get rules matching a pattern
    pub fn rules_for_action(&self, action: &str) -> Vec<&PolicyRule> {
        self.rules
            .iter()
            .filter(|r| self.pattern_matches(&r.action_pattern, action))
            .collect()
    }
}

impl Default for PolicyEngine {
    fn default() -> Self {
        Self::new()
    }
}
