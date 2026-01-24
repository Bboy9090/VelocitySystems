// Universal Core: Policy Module
// Doctrine-agnostic policy evaluation

pub mod engine;
pub mod decision;
pub mod intent;

pub use engine::{PolicyEngine, PolicyRule, PolicyDecision, PolicyContext};
pub use decision::DecisionResult;
pub use intent::{Intent, Urgency};
