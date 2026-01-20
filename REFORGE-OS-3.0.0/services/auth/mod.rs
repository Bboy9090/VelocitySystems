// ForgeWorks Core - Authentication Module
// OIDC, SAML, and Role-Based Access Control

pub mod oidc;
pub mod saml;
pub mod roles;

pub use oidc::{Claims, Role, AuthError, validate_token, validate_token_and_roles};
pub use saml::{SamlAssertion, SamlAttributes, parse_assertion, map_saml_roles_to_forgeworks};
pub use roles::{AuthorizationContext, authorize_action, can_access_interpretive_mode};
