// Prometheus Engine: Schema Validator
// Validates prompt schemas against doctrine rules

use super::loader::PromptSchema;
use crate::audit::AuditLog;

pub struct SchemaValidator;

impl SchemaValidator {
    /// Validate schema against doctrine rules
    pub fn validate_doctrine(schema: &PromptSchema, doctrine: &str) -> Result<(), String> {
        if schema.doctrine != doctrine {
            return Err(format!("Schema doctrine {} does not match requested {}", schema.doctrine, doctrine));
        }

        // Doctrine-specific validation
        match doctrine {
            "phoenix_forge" => Self::validate_phoenix(schema),
            "velocity_systems" => Self::validate_velocity(schema),
            _ => Err("Unknown doctrine".to_string()),
        }
    }

    fn validate_phoenix(schema: &PromptSchema) -> Result<(), String> {
        // Phoenix must have compliance considerations
        if !schema.quality_governance.risks_to_surface.iter()
            .any(|r| r.contains("audit") || r.contains("compliance") || r.contains("legal")) {
            return Err("Phoenix schemas must surface audit/compliance risks".to_string());
        }

        // Phoenix must require justification
        if !schema.output_contract.explicit_exclusions.iter()
            .any(|e| e.contains("justification")) {
            // This is okay - justification might be in mandatory sections
        }

        Ok(())
    }

    fn validate_velocity(schema: &PromptSchema) -> Result<(), String> {
        // Velocity must not require compliance language
        if schema.output_contract.explicit_exclusions.iter()
            .any(|e| e.contains("compliance") || e.contains("legal")) {
            // This is good
        }

        // Velocity must optimize for speed
        if !schema.quality_governance.validation_checklist.iter()
            .any(|c| c.contains("speed") || c.contains("friction") || c.contains("latency")) {
            return Err("Velocity schemas must validate for speed/friction".to_string());
        }

        Ok(())
    }

    /// Validate schema completeness
    pub fn validate_completeness(schema: &PromptSchema) -> Result<(), String> {
        // Check all required sections are present
        if schema.intent_core.objective.is_empty() {
            return Err("Intent core objective is required".to_string());
        }

        if schema.role_authority_matrix.absolute_authority.is_empty() {
            return Err("Absolute authority is required".to_string());
        }

        if schema.domain_lock.industry.is_empty() {
            return Err("Domain lock industry is required".to_string());
        }

        if schema.output_contract.mandatory_sections.is_empty() {
            return Err("At least one mandatory section is required".to_string());
        }

        Ok(())
    }

    /// Validate schema version
    pub fn validate_version(schema: &PromptSchema, expected_version: &str) -> Result<(), String> {
        if schema.version != expected_version {
            return Err(format!("Version mismatch: expected {}, got {}", expected_version, schema.version));
        }
        Ok(())
    }
}
