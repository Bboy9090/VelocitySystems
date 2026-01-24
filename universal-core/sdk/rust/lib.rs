// Universal Core: Rust SDK
// Provides idiomatic Rust bindings to the Universal Core

pub use universal_core::*;

/// Rust SDK wrapper for easier integration
pub struct UniversalSDK {
    kernel: Kernel,
}

impl UniversalSDK {
    pub fn new(doctrine: String, default_ttl: Option<std::time::Duration>) -> Self {
        Self {
            kernel: Kernel::new(doctrine, default_ttl),
        }
    }

    pub fn kernel(&self) -> &Kernel {
        &self.kernel
    }

    pub fn kernel_mut(&mut self) -> &mut Kernel {
        &mut self.kernel
    }
}
