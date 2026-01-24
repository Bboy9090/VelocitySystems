// Prometheus Engine: Critique System
// Provides adversarial review based on doctrine

use super::loader::PromptSchema;

pub struct CritiqueEngine;

impl CritiqueEngine {
    /// Run adversarial critique based on doctrine
    pub fn critique(output: &str, schema: &PromptSchema) -> Result<String, String> {
        match schema.doctrine.as_str() {
            "phoenix_forge" => Self::critique_phoenix(output, schema),
            "velocity_systems" => Self::critique_velocity(output, schema),
            _ => Err("Unknown doctrine".to_string()),
        }
    }

    fn critique_phoenix(output: &str, schema: &PromptSchema) -> Result<String, String> {
        let mut critiques = Vec::new();

        // Check for audit failure scenarios
        if !output.contains("audit") && !output.contains("evidence") {
            critiques.push("Does not address audit/evidence requirements");
        }

        // Check for authority ambiguity
        if !output.contains("authority") && !output.contains("approval") {
            critiques.push("Authority/approval not clearly defined");
        }

        // Check for risk surfacing
        let risks_mentioned = schema.quality_governance.risks_to_surface.iter()
            .any(|risk| output.to_lowercase().contains(&risk.to_lowercase()));
        if !risks_mentioned {
            critiques.push("Risks not adequately surfaced");
        }

        // Check for compliance language
        if !output.contains("compliance") && !output.contains("regulatory") {
            critiques.push("Compliance considerations may be missing");
        }

        if critiques.is_empty() {
            Ok("Phoenix critique passed: output addresses audit, authority, and compliance".to_string())
        } else {
            Ok(format!("Phoenix critique issues:\n{}", critiques.join("\n")))
        }
    }

    fn critique_velocity(output: &str, schema: &PromptSchema) -> Result<String, String> {
        let mut critiques = Vec::new();

        // Check for friction
        if output.contains("approval") || output.contains("justification") {
            critiques.push("Contains approval/justification language - may add friction");
        }

        // Check for compliance language (should be excluded)
        if output.contains("compliance") || output.contains("regulatory") {
            critiques.push("Contains compliance language - should be excluded for Velocity");
        }

        // Check for speed optimization
        if !output.contains("immediate") && !output.contains("instant") && !output.contains("fast") {
            critiques.push("Does not emphasize speed/immediacy");
        }

        // Check for ceremony
        if output.contains("review") || output.contains("approve") {
            critiques.push("May introduce ceremony - check for necessity");
        }

        if critiques.is_empty() {
            Ok("Velocity critique passed: output optimized for speed with minimal friction".to_string())
        } else {
            Ok(format!("Velocity critique issues:\n{}", critiques.join("\n")))
        }
    }
}
