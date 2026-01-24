// Prometheus Registry Service
// Immutable prompt storage with versioning and canon locks

use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::time::{SystemTime, UNIX_EPOCH};
use crate::universal_core::prometheus::PromptSchema;
use crate::universal_core::audit::AuditLog;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RegistryEntry {
    pub prompt_id: String,
    pub version: String,
    pub schema: PromptSchema,
    pub hash: String,
    pub created_at: u128,
    pub created_by: String,
    pub lock_status: String,
    pub changelog: Vec<ChangelogEntry>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ChangelogEntry {
    pub version: String,
    pub changed_at: u128,
    pub changed_by: String,
    pub changes: String,
    pub reason: String,
}

pub struct PrometheusRegistry {
    entries: HashMap<String, RegistryEntry>,
    audit_log: AuditLog,
}

impl PrometheusRegistry {
    pub fn new(audit_log: AuditLog) -> Self {
        Self {
            entries: HashMap::new(),
            audit_log,
        }
    }

    /// Register a new prompt schema
    pub fn register(
        &mut self,
        schema: PromptSchema,
        created_by: String,
    ) -> Result<String, String> {
        let prompt_id = schema.prompt_id.clone();
        let version = schema.version.clone();
        
        // Check if already exists
        if self.entries.contains_key(&prompt_id) {
            return Err("Prompt already registered. Use update() for new versions.".to_string());
        }

        // Compute hash
        let hash = crate::universal_core::prometheus::PromptLoader::compute_hash(&schema);

        // Create entry
        let entry = RegistryEntry {
            prompt_id: prompt_id.clone(),
            version: version.clone(),
            schema,
            hash: hash.clone(),
            created_at: SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .unwrap()
                .as_nanos(),
            created_by: created_by.clone(),
            lock_status: "DRAFT".to_string(),
            changelog: vec![ChangelogEntry {
                version: version.clone(),
                changed_at: SystemTime::now()
                    .duration_since(UNIX_EPOCH)
                    .unwrap()
                    .as_nanos(),
                changed_by: created_by.clone(),
                changes: "Initial registration".to_string(),
                reason: "New prompt schema".to_string(),
            }],
        };

        // Log registration
        self.audit_log.append(
            created_by,
            "prometheus:register".to_string(),
            prompt_id.clone(),
            "success".to_string(),
            serde_json::json!({
                "version": version,
                "hash": hash,
                "doctrine": entry.schema.doctrine,
            }),
            entry.schema.doctrine.clone(),
        );

        self.entries.insert(prompt_id.clone(), entry);
        Ok(prompt_id)
    }

    /// Update prompt schema (new version)
    pub fn update(
        &mut self,
        prompt_id: &str,
        new_schema: PromptSchema,
        changed_by: String,
        reason: String,
    ) -> Result<String, String> {
        let entry = self.entries.get_mut(prompt_id)
            .ok_or("Prompt not found")?;

        // Check lock status
        if entry.lock_status == "CANON" {
            return Err("Cannot update canon-locked prompt".to_string());
        }

        // Compute new hash
        let new_hash = crate::universal_core::prometheus::PromptLoader::compute_hash(&new_schema);

        // Add changelog entry
        entry.changelog.push(ChangelogEntry {
            version: new_schema.version.clone(),
            changed_at: SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .unwrap()
                .as_nanos(),
            changed_by: changed_by.clone(),
            changes: format!("Updated from {} to {}", entry.version, new_schema.version),
            reason,
        });

        // Update entry
        entry.version = new_schema.version.clone();
        entry.schema = new_schema;
        entry.hash = new_hash.clone();

        // Log update
        self.audit_log.append(
            changed_by,
            "prometheus:update".to_string(),
            prompt_id.to_string(),
            "success".to_string(),
            serde_json::json!({
                "version": entry.version,
                "hash": new_hash,
            }),
            entry.schema.doctrine.clone(),
        );

        Ok(entry.version.clone())
    }

    /// Lock prompt as canon
    pub fn lock_canon(
        &mut self,
        prompt_id: &str,
        locked_by: String,
    ) -> Result<(), String> {
        let entry = self.entries.get_mut(prompt_id)
            .ok_or("Prompt not found")?;

        entry.lock_status = "CANON".to_string();

        // Log canon lock
        self.audit_log.append(
            locked_by,
            "prometheus:lock_canon".to_string(),
            prompt_id.to_string(),
            "success".to_string(),
            serde_json::json!({
                "version": entry.version,
                "hash": entry.hash,
            }),
            entry.schema.doctrine.clone(),
        );

        Ok(())
    }

    /// Get prompt by ID and version
    pub fn get(&self, prompt_id: &str, version: Option<&str>) -> Option<&RegistryEntry> {
        let entry = self.entries.get(prompt_id)?;
        
        if let Some(version) = version {
            if entry.version != version {
                return None;
            }
        }
        
        Some(entry)
    }

    /// List all prompts for a doctrine
    pub fn list_by_doctrine(&self, doctrine: &str) -> Vec<&RegistryEntry> {
        self.entries
            .values()
            .filter(|e| e.schema.doctrine == doctrine)
            .collect()
    }

    /// Verify prompt integrity
    pub fn verify(&self, prompt_id: &str) -> Result<bool, String> {
        let entry = self.entries.get(prompt_id)
            .ok_or("Prompt not found")?;
        
        let computed_hash = crate::universal_core::prometheus::PromptLoader::compute_hash(&entry.schema);
        Ok(computed_hash == entry.hash)
    }
}
