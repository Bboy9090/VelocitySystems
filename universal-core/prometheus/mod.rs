// Prometheus Engine Module
// Doctrine-aware cognitive engine for structured prompt execution

pub mod loader;
pub mod validator;
pub mod executor;
pub mod critique;

pub use loader::{PromptSchema, PromptLoader, IntentCore, RoleAuthorityMatrix, DomainLock, OutputContract, QualityGovernance, IterationEngine};
pub use validator::SchemaValidator;
pub use executor::{PrometheusExecutor, ExecutionResult};
pub use critique::CritiqueEngine;
