// Universal Core Library
// The enterprise-grade foundation that powers both Phoenix Forge and Velocity Systems
// This core always records reality, regardless of doctrine

pub mod audit;
pub mod policy;
pub mod authority;
pub mod approval;
pub mod export;
pub mod prometheus;
pub mod kernel;

pub use kernel::{Kernel, ExecutionResult as KernelExecutionResult};
pub use audit::{AuditLog, AuditRecord, VerificationResult};
pub use policy::{PolicyEngine, PolicyDecision, Intent, DecisionResult};
pub use authority::{CapabilityRegistry, Capability, ExpiryManager};
pub use approval::{ApprovalRegistry, ApprovalRequest, ApprovalState};
pub use export::{EvidenceBundle, EvidenceExporter, BundleManager};
pub use prometheus::{
    PromptSchema,
    PromptLoader,
    PrometheusExecutor,
    ExecutionResult as PrometheusExecutionResult,
    SchemaValidator,
    CritiqueEngine,
};
