// Velocity Systems Doctrine: Risk Model
// Assumes good intent, good memory, good behavior

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RiskAssessment {
    pub action: String,
    pub risk_level: RiskLevel,
    pub assumptions: Vec<RiskAssumption>,
    pub mitigation_required: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum RiskLevel {
    Low,
    Medium,
    High,
    Extreme,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum RiskAssumption {
    GoodIntent,
    GoodMemory,
    GoodBehavior,
    SkilledOperators,
    HighTrust,
}

pub struct VelocityRiskModel;

impl VelocityRiskModel {
    /// Assess risk for an action (Velocity assumes best case)
    pub fn assess(action: &str) -> RiskAssessment {
        let risk_level = Self::classify_risk(action);
        let assumptions = Self::get_assumptions(action);
        // Only require mitigation for truly catastrophic actions
        let mitigation_required = risk_level == RiskLevel::Extreme;

        RiskAssessment {
            action: action.to_string(),
            risk_level,
            assumptions,
            mitigation_required,
        }
    }

    fn classify_risk(action: &str) -> RiskLevel {
        if action.contains("catastrophic") {
            RiskLevel::Extreme
        } else {
            RiskLevel::Low // Velocity assumes low risk by default
        }
    }

    fn get_assumptions(action: &str) -> Vec<RiskAssumption> {
        vec![
            RiskAssumption::GoodIntent,
            RiskAssumption::GoodMemory,
            RiskAssumption::GoodBehavior,
            RiskAssumption::SkilledOperators,
            RiskAssumption::HighTrust,
        ]
    }
}
