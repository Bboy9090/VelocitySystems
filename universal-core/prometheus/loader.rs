// Prometheus Engine: Prompt Loader
// Loads and validates doctrine-locked prompt schemas

use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use sha2::{Sha256, Digest};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PromptSchema {
    pub prompt_id: String,
    pub version: String,
    pub lock_status: String, // "CANON" | "DRAFT" | "LOCKED"
    pub authorized_use_scope: Vec<String>,
    pub doctrine: String, // "phoenix_forge" | "velocity_systems"
    
    pub intent_core: IntentCore,
    pub role_authority_matrix: RoleAuthorityMatrix,
    pub domain_lock: DomainLock,
    pub output_contract: OutputContract,
    pub quality_governance: QualityGovernance,
    pub iteration_engine: IterationEngine,
    pub active_libraries: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct IntentCore {
    pub objective: String,
    pub stakes_if_failure: String,
    pub definition_of_success: String,
    pub decision_authority: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RoleAuthorityMatrix {
    pub absolute_authority: String,
    pub support_roles: Vec<String>,
    pub explicit_exclusions: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DomainLock {
    pub industry: String,
    pub system_maturity: String,
    pub hard_constraints: Vec<String>,
    pub time_horizon: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OutputContract {
    pub deliverable_type: Vec<String>,
    pub required_format: String,
    pub mandatory_sections: Vec<String>,
    pub length_bounds: LengthBounds,
    pub explicit_exclusions: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LengthBounds {
    pub min: String,
    pub max: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct QualityGovernance {
    pub assumptions: Vec<String>,
    pub risks_to_surface: Vec<String>,
    pub failure_modes_to_avoid: Vec<String>,
    pub validation_checklist: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct IterationEngine {
    pub auto_critique: bool,
    pub rewrite_rules: Vec<String>,
    pub final_output_only: bool,
}

pub struct PromptLoader;

impl PromptLoader {
    /// Load prompt schema from JSON
    pub fn load(json: &str) -> Result<PromptSchema, String> {
        let schema: PromptSchema = serde_json::from_str(json)
            .map_err(|e| format!("Failed to parse prompt schema: {}", e))?;
        
        Self::validate(&schema)?;
        Ok(schema)
    }

    /// Validate schema structure and constraints
    fn validate(schema: &PromptSchema) -> Result<(), String> {
        // Validate lock status
        if schema.lock_status != "CANON" && schema.lock_status != "DRAFT" && schema.lock_status != "LOCKED" {
            return Err("Invalid lock_status".to_string());
        }

        // Validate doctrine
        if schema.doctrine != "phoenix_forge" && schema.doctrine != "velocity_systems" {
            return Err("Invalid doctrine".to_string());
        }

        // Validate required fields
        if schema.intent_core.objective.is_empty() {
            return Err("Intent core objective is required".to_string());
        }

        if schema.role_authority_matrix.absolute_authority.is_empty() {
            return Err("Absolute authority is required".to_string());
        }

        Ok(())
    }

    /// Compute schema hash for versioning
    pub fn compute_hash(schema: &PromptSchema) -> String {
        let json = serde_json::to_string(schema).unwrap();
        let mut hasher = Sha256::new();
        hasher.update(json.as_bytes());
        format!("{:x}", hasher.finalize())
    }

    /// Verify schema is canon-locked
    pub fn is_canon(schema: &PromptSchema) -> bool {
        schema.lock_status == "CANON"
    }

    /// Check if schema is authorized for use
    pub fn is_authorized(schema: &PromptSchema, context: &str) -> bool {
        schema.authorized_use_scope.iter().any(|scope| {
            context.contains(scope) || scope == "*"
        })
    }
}
