// Universal Core: Export Module
// Doctrine-agnostic evidence export

pub mod evidence;
pub mod bundle;

pub use evidence::{EvidenceBundle, EvidenceExporter};
pub use bundle::BundleManager;
