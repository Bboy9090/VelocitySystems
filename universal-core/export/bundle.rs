// Universal Core: Evidence Bundle Management
// Handles evidence bundle creation and verification

use super::evidence::{EvidenceBundle, EvidenceExporter};
use std::path::Path;
use std::fs;

pub struct BundleManager;

impl BundleManager {
    /// Save evidence bundle to file
    pub fn save(bundle: &EvidenceBundle, path: &Path) -> Result<(), String> {
        let json = EvidenceExporter::to_json(bundle)
            .map_err(|e| format!("Failed to serialize bundle: {}", e))?;
        
        fs::write(path, json)
            .map_err(|e| format!("Failed to write bundle: {}", e))?;
        
        Ok(())
    }

    /// Load evidence bundle from file
    pub fn load(path: &Path) -> Result<EvidenceBundle, String> {
        let json = fs::read_to_string(path)
            .map_err(|e| format!("Failed to read bundle: {}", e))?;
        
        let bundle: EvidenceBundle = serde_json::from_str(&json)
            .map_err(|e| format!("Failed to parse bundle: {}", e))?;
        
        if !EvidenceExporter::verify(&bundle) {
            return Err("Bundle integrity verification failed".to_string());
        }
        
        Ok(bundle)
    }

    /// Create timestamped bundle filename
    pub fn bundle_filename(prefix: &str) -> String {
        use std::time::{SystemTime, UNIX_EPOCH};
        let timestamp = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_secs();
        format!("{}_{}.evidence.json", prefix, timestamp)
    }
}
