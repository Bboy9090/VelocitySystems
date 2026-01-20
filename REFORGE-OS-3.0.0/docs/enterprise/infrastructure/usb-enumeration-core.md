# REFORGE OS — USB Enumeration Core

**Source**: BootForge USB Library

**Status**: INTEGRATED INTO REFORGE OS

---

## Overview

The USB enumeration core is the foundation of REFORGE OS device detection capabilities. It provides cross-platform USB device enumeration and information gathering.

---

## Core Capabilities

### Device Enumeration

- **Cross-platform**: Windows, macOS, Linux
- **Protocol**: libusb 1.0 (via rusb)
- **Platform-specific enrichment**: 
  - Windows: SetupAPI (planned)
  - macOS: IOKit (planned)
  - Linux: sysfs paths

### Device Information

- Vendor ID / Product ID
- Manufacturer string
- Product name string
- Serial number
- USB class/subclass/protocol
- USB version
- Device version
- Bus number and device address
- Platform-specific paths

---

## Integration into REFORGE OS

### Service Integration

```
services/device-analysis/
├── enumeration/
│   ├── usb_core.rs          # BootForge USB integration
│   ├── platform_enrich.rs   # OS-specific enrichment
│   └── classification.rs    # Device type classification
```

### API Endpoints

- `GET /api/device/enumerate` — Enumerate all USB devices
- `GET /api/device/:id/info` — Get detailed device information
- `GET /api/device/:id/classify` — Classify device type (iOS/Android/Unknown)

---

## From BootForge USB Source

### Direct Integration

✅ **Source Code**:
- `src/enumerate/` — Enumeration modules
- `src/types.rs` — Device information structures
- `src/enumerate/libusb.rs` — Base enumeration
- `src/enumerate/windows.rs` — Windows enrichment (planned)
- `src/enumerate/linux.rs` — Linux enrichment
- `src/enumerate/macos.rs` — macOS enrichment (planned)

✅ **Structures**:
- `UsbDeviceInfo` — Device information structure
- `PlatformHint` — OS-specific paths
- `UsbBusType` — Bus type classification

---

## Compliance & Safety

### No Modification Capability

The USB enumeration core is **read-only**:
- ✅ Reads device descriptors
- ✅ Reads string descriptors
- ✅ Enumerates devices
- ❌ Does NOT modify devices
- ❌ Does NOT execute exploits
- ❌ Does NOT bypass security

---

## Platform Support Status

| Platform | Status | Implementation |
|----------|--------|----------------|
| Linux | ✅ Implemented | libusb + sysfs |
| Windows | 🚧 Planned | libusb + SetupAPI |
| macOS | 🚧 Planned | libusb + IOKit |

---

## Future Enhancements

- Hotplug monitoring (real-time device connect/disconnect)
- Driver information querying
- Interface enumeration
- Power management querying
- USB IDs database integration

---

**Document Version**: 1.0  
**Source**: BootForge USB  
**Status**: INTEGRATED