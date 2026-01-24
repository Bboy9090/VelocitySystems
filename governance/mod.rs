// Governance Module
// Internal controls that maintain integrity across doctrines

pub mod internal_charter;
pub mod kill_switch;
pub mod truth_escrow;

pub use kill_switch::{KillSwitch, KillSwitchReason, KillSwitchEffects};
pub use truth_escrow::{TruthEscrowManager, EscrowAccessReason, EscrowStatus};
