// Phoenix Forge Doctrine: Risk Model
// Assumes reality, stress, and human error

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
    HumanError,
    Stress,
    Reality,
    TimePressure,
    Misconfiguration,
}

pub struct PhoenixRiskModel;

impl PhoenixRiskModel {
    /// Assess risk for an action (Phoenix assumes worst case)
    pub fn assess(action: &str) -> RiskAssessment {
        let risk_level = Self::classify_risk(action);
        let assumptions = Self::get_assumptions(action);
        let mitigation_required = risk_level == RiskLevel::High || risk_level == RiskLevel::Extreme;

        RiskAssessment {
            action: action.to_string(),
            risk_level,
            assumptions,
            mitigation_required,
        }
    }

    fn classify_risk(action: &str) -> RiskLevel {
        if action.contains("delete") || action.contains("admin") || action.contains("export") {
            RiskLevel::Extreme
        } else if action.contains("modify") || action.contains("update") {
            RiskLevel::High
        } else if action.contains("read") || action.contains("view") {
            RiskLevel::Low
        } else {
            RiskLevel::Medium
        }
    }

    fn get_assumptions(action: &str) -> Vec<RiskAssumption> {
        let mut assumptions = vec![
            RiskAssumption::HumanError,
            RiskAssumption::Reality,
        ];

        if action.contains("delete") || action.contains("admin") {
            assumptions.push(RiskAssumption::Stress);
            assumptions.push(RiskAssumption::TimePressure);
        }

        assumptions
    }
}
