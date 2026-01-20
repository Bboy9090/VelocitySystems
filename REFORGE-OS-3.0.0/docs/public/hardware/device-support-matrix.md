# REFORGE OS — Device Support Matrix

**Hardware + Infrastructure Focus**

This matrix defines device compatibility for REFORGE OS hardware components. **Analysis and diagnostics only** — no circumvention execution.

---

## Device Classification

REFORGE OS hardware supports device analysis and diagnostic capabilities across:

- **iOS Devices** (iPhone, iPad, Apple Watch)
- **Android Devices** (All major manufacturers)
- **USB-connected devices** (General enumeration)

**Note**: Support indicates diagnostic/analysis capability, not modification execution.

---

## iOS Device Support

### iPhone Support Matrix

| Device Range | Chipset | Diagnostic Support | Analysis Capabilities |
|--------------|---------|-------------------|----------------------|
| iPhone X & Older | A7 - A11 | ✅ Full | Battery, sensors, ports, charge negotiation |
| iPhone XR to 15 Pro | A12 - A17 | ✅ Full | Battery, sensors, ports, charge negotiation |
| iPhone 16 / 17 / 18 | A18 - A19 | ✅ Full | Battery, sensors, ports, charge negotiation |
| Legacy Devices (32-bit) | Early 64-bit | ✅ Limited | Basic diagnostics only |

### iPad Support Matrix

| Model Range | Chipset | Diagnostic Support | Notes |
|-------------|---------|-------------------|-------|
| iPad (Early models) | A4-A5 | ⚠️ Limited | Basic USB enumeration |
| iPad Air/Pro (2013-2017) | A7-A10X | ✅ Full | Full diagnostic suite |
| iPad (2018-2021) | A12-A14 | ✅ Full | Full diagnostic suite |
| iPad (2022+) | A15-A18 | ✅ Full | Full diagnostic suite |

### Apple Watch Support

| Model Range | Chipset | Diagnostic Support | Notes |
|-------------|---------|-------------------|-------|
| Apple Watch S0-S3 | S1-S3 | ⚠️ Limited | Specialized charger required |
| Apple Watch S4+ | S4-S10 | ⚠️ Limited | Specialized charger required |

---

## Android Device Support

### Manufacturer Support Matrix

#### Samsung Galaxy

| Model Series | Diagnostic Support | Analysis Capabilities |
|--------------|-------------------|----------------------|
| Galaxy S (S6-S24) | ✅ Full | Battery, sensors, ports, charge, USB enumeration |
| Galaxy Note (Note 5-Note 20) | ✅ Full | Battery, sensors, ports, charge, USB enumeration |
| Galaxy A Series | ✅ Full | Battery, sensors, ports, charge, USB enumeration |
| Galaxy Tab | ✅ Full | Battery, sensors, ports, charge, USB enumeration |

#### Google Pixel

| Model | Diagnostic Support | Analysis Capabilities |
|-------|-------------------|----------------------|
| Pixel 1-3 | ✅ Full | Battery, sensors, ports, charge, USB enumeration |
| Pixel 4-6 | ✅ Full | Battery, sensors, ports, charge, USB enumeration |
| Pixel 7+ | ✅ Full | Battery, sensors, ports, charge, USB enumeration |

#### Xiaomi

| Series | Diagnostic Support | Analysis Capabilities |
|--------|-------------------|----------------------|
| Redmi/Note Series | ✅ Full | Battery, sensors, ports, charge, USB enumeration |
| Mi Series | ✅ Full | Battery, sensors, ports, charge, USB enumeration |
| POCO Series | ✅ Full | Battery, sensors, ports, charge, USB enumeration |

#### OnePlus

| Series | Diagnostic Support | Analysis Capabilities |
|--------|-------------------|----------------------|
| OnePlus 1-7 | ✅ Full | Battery, sensors, ports, charge, USB enumeration |
| OnePlus 8+ | ✅ Full | Battery, sensors, ports, charge, USB enumeration |

#### Oppo/Vivo

| Series | Diagnostic Support | Analysis Capabilities |
|--------|-------------------|----------------------|
| Oppo/Vivo Devices | ✅ Full | Battery, sensors, ports, charge, USB enumeration |

#### Huawei

| Series | Diagnostic Support | Analysis Capabilities |
|--------|-------------------|----------------------|
| Pre-2019 Devices | ✅ Limited | Basic USB enumeration |
| Post-2019 Devices | ⚠️ Limited | Bootloader restrictions limit diagnostics |

---

## Diagnostic Capabilities (Hardware-Based)

### ForgeCore Diagnostic Bridge Capabilities

✅ **Supported Diagnostic Functions**:

- USB device enumeration
- Vendor/Product ID detection
- Device descriptor reading
- Power negotiation analysis (read-only)
- Charge current/voltage monitoring
- Port integrity testing
- Battery cycle count reading (via I2C/SMBus)
- Sensor presence detection
- USB protocol analysis (sniffing only)

❌ **NOT Supported** (By Design):

- Device modification
- Bootloader unlocking
- Firmware flashing
- Security bypass
- Lock removal
- Root/jailbreak execution

---

## Hardware Connection Methods

### USB Connections

| Connection Type | Devices | ForgeCore Support |
|----------------|---------|-------------------|
| USB-C | Modern Android, iPhone 15+ | ✅ Native |
| Lightning | iPhone (up to 14), iPad | ✅ Via adapter |
| Micro-USB | Legacy Android | ✅ Via adapter |
| USB-A | General USB devices | ✅ Native |

### Physical Connections

| Connection Type | Purpose | Hardware Required |
|----------------|---------|-------------------|
| USB-C Direct | Primary connection | ForgeCore |
| Adapter Chain | Legacy devices | Lightning/USB-C/Micro-USB adapters |
| JTAG (Optional) | Advanced diagnostics | Separate JTAG tools (not in core kit) |

---

## Platform Support

### Operating System Compatibility

| Platform | ForgeCore Support | Notes |
|----------|------------------|-------|
| **Windows** | ✅ Full | Windows 10/11 |
| **macOS** | ✅ Full | macOS 10.15+ |
| **Linux** | ✅ Full | Kernel 5.4+ |

### Driver Requirements

- **libusb**: Required (included with REFORGE OS software)
- **USB-C PD**: Native OS support
- **Secure Element**: Platform drivers included

---

## Diagnostic Report Generation

REFORGE OS hardware enables generation of:

- **Device Status Reports**: Security state, ownership indicators
- **Battery Health Reports**: Cycle count, capacity, authenticity
- **Port Integrity Reports**: USB port health, charge capability
- **Sensor Reports**: Present sensors, functionality checks
- **Compliance Reports**: Legal classification, risk assessment

**All reports are analysis-only. No device modification occurs.**

---

## Support Status Legend

- ✅ **Full Support**: Complete diagnostic capabilities, regular testing
- ⚠️ **Limited Support**: Basic diagnostics, some limitations
- ❌ **Not Supported**: Device incompatible or not testable

---

## Update Frequency

- **Device Database**: Updated continuously as new devices tested
- **Firmware Updates**: OTA updates for ForgeCore (security patches, new device support)
- **Driver Updates**: Included with platform software updates

---

**Document Version**: 1.0  
**Status**: PRODUCTION-READY  
**Last Updated**: Device Support Matrix Final