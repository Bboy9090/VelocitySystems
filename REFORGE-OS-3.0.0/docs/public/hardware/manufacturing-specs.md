# REFORGE OS — Hardware Manufacturing Specifications

**Status: GREEN-LIT FOR PRODUCTION**

This document contains the complete manufacturing specifications for REFORGE OS hardware components. All components are **hardware + infrastructure only**. No software tactics. No circumvention. Safe to execute.

---

## 🧱 OVERVIEW — WHAT WE ARE BUILDING

### Physical Product Line: Workshop Forge™ Hardware Suite

Hardware acts as:
- **Diagnostic bridge** — device status evaluation
- **Trust anchor** — hardware identity & verification
- **Audit key** — immutable logging capability
- **Permission gate** — license tier enforcement

### Manufacturing Goal

- **60–65% gross margin** at scale
- **Scalable** from 1k → 100k units/year
- **ISO-friendly** — compliant manufacturing
- **Regulator-neutral** — no circumvention capability

---

## 1️⃣ FORGECORE DIAGNOSTIC BRIDGE (FLAGSHIP)

### Function

USB diagnostic dongle with:
- Hardware identity + secure element
- Power negotiation & signal analysis
- **NO device modification capability**

### Core Components (Green-Lit)

| Component | Vendor | Part Number | Notes |
|-----------|--------|-------------|-------|
| **MCU** | STMicroelectronics | STM32G4 / STM32H5 | Industrial grade, long-term supply |
| **Secure Element** | Microchip | ATECC608B | Hardware identity & signing |
| **USB-C PD Controller** | Texas Instruments | TPS6598x | PD sniffing, not injection |
| **USB Hub IC** | Microchip | USB5744 | Stable, widely certified |
| **Flash** | Winbond | W25Q | Firmware storage |
| **Crystal** | Epson / Abracon | Standard | Clock stability |
| **PCB** | - | 4-layer FR-4 | JLCPCB / PCBWay |
| **Housing** | - | CNC aluminum | Dongguan |

### Manufacturing

- **PCB**: 4-layer FR-4 (JLCPCB / PCBWay)
- **Assembly**: SMT + manual QA
- **Housing**: CNC aluminum (Dongguan)
- **Certifications**: USB-IF, FCC, CE

### Specifications

- **Power**: USB-C PD 3.1 compliant
- **Connectors**: USB-C + USB-A dual port
- **Secure Element**: Provisioned per unit
- **Firmware**: OTA update capable (read-only in field for security)

**🟢 Status: READY FOR PRODUCTION**

---

## 2️⃣ SMART THERMAL PLATFORM (HEAT MAT)

### Function

Digitally controlled heat surface for repair-safe temperature profiles. USB-controlled. **NO bypass functionality**.

### Components

| Component | Vendor | Part Number |
|-----------|--------|-------------|
| **Heating Element** | UL-rated | Kapton / Silicone mat |
| **Temp Sensors** | Texas Instruments | TMP117 |
| **MCU** | STMicroelectronics | STM32F0 |
| **Power Regulator** | Mean Well / TI | Standard |

### Manufacturing

- **Silicone molding**: Shenzhen
- **Calibration**: Per unit (required)
- **Firmware**: Locked (read-only in field)

### Specifications

- **Temperature Range**: 40°C - 120°C (safety-limited)
- **Control Zones**: Multi-zone (up to 4 zones)
- **Presets**: OLED, AMOLED, LCD profiles
- **Safety**: Auto shutoff, thermal cutoffs

**🟢 Status: READY FOR PRODUCTION**

---

## 3️⃣ PRECISION TOOL MATRIX (PRO KIT)

### Components

| Item | Manufacturer | Specifications |
|------|--------------|----------------|
| **Torque Drivers** | Wiha / Wera (OEM custom run) | Pentalobe, Tri-Point, Torx, Phillips |
| **Bits** | S2 steel | CNC ground, laser-etched |
| **Spudgers** | Carbon fiber reinforced | Nylon construction |
| **Suction Tools** | Industrial grade | Nitrile material |
| **ESD Mat** | 3M certified | Standard size |

### Manufacturing

- **Tool steel forging**: Taiwan
- **Laser-etched serials**: Per tool
- **NFC tag in handle**: Optional (for software tool detection)

### Specifications

- **Torque calibration**: ±5% accuracy
- **Bit hardness**: 60-62 HRC
- **ESD protection**: < 10^6 ohms

**🟢 Status: READY FOR PRODUCTION**

---

## 4️⃣ MICROSOLDERING EXPANSION BAY (ELITE)

### Components

| Component | Vendor | Notes |
|-----------|--------|-------|
| **Hot Air Station** | Quick / Atten OEM | Profile memory |
| **Iron** | JBC-compatible | Cartridge system |
| **Microscope Mount** | AmScope OEM | HDMI/USB support |
| **Board Clamp** | CNC aluminum | Alignment guides |

### Specifications

- **Hot Air Temperature**: 100°C - 450°C
- **Iron Temperature**: 150°C - 500°C
- **Profile Memory**: 20+ profiles
- **Microscope Support**: Up to 1000x magnification

**🟡 Status: OPTIONAL / ELITE SKU**

---

## 5️⃣ SCREW & PARTS INTELLIGENCE TRAYS

### Components

| Component | Vendor | Specifications |
|-----------|--------|----------------|
| **NFC Tags** | NXP | NTAG213 |
| **Tray Material** | Injection-molded ABS | Durable, ESD-safe |
| **Encoding** | Dual | QR + NFC |

### Function

- Position-aware screw mapping
- Part replacement verification
- Customer transparency (repair receipts)

**🟢 Status: READY FOR PRODUCTION**

---

## 6️⃣ PACKAGING (REGULATOR-SAFE)

### Requirements

- ❌ No "unlock" language
- ❌ No claims of bypass
- ✅ Focus on: Diagnostics, Compliance, Repair intelligence

### Vendors

- PakFactory
- Packlane
- Dongguan custom foam

### Design Principles

- Professional, workshop-grade aesthetic
- Clear regulatory compliance messaging
- Hardware-first positioning

---

## 7️⃣ MANUFACTURING PARTNERS (SHORTLIST)

### Electronics

- **JLCPCB** — prototyping + low-mid volume
- **PCBWay** — mid-volume
- **Seeed Studio Fusion** — scalable production

### CNC & Enclosures

- **Dongguan CNC shops** — precision metalwork
- **Shenzhen Rapid Direct** — rapid prototyping

### Assembly

- **ISO-9001 Tier-2 EMS** — preferred
- **Manual QA lines** — required for secure element provisioning

---

## 8️⃣ QA & SECURITY (MANDATORY)

### Per-Unit QA Checklist

- [ ] Secure element provisioning
- [ ] Firmware signature verification
- [ ] USB descriptor validation
- [ ] Thermal safety test
- [ ] Audit log handshake test
- [ ] Serial number assignment & database entry

### Anti-Tamper

- **Epoxy-sealed secure element** — physical protection
- **Firmware rollback prevention** — version control
- **Serial ↔ account binding** — license enforcement

---

## 9️⃣ COST & MSRP TARGETS (CONFIRMED)

| Product | COGS | MSRP | Margin |
|---------|------|------|--------|
| **ForgeCore** | $45–55 | $149 | ~65% |
| **Thermal Mat** | $40–50 | $179 | ~60% |
| **Tool Matrix** | $60–70 | $199 | ~60% |
| **Elite Kit** | $220–260 | $899 | ~60% |
| **Pro Kit** | $145–175 | $449 | ~60% |

---

## 🔟 MANUFACTURING PHASES (GREEN-LIT)

### Phase A — EVT (Engineering Validation)

- **Units**: 50
- **Purpose**: Internal testing
- **Timeline**: 30 days

### Phase B — DVT (Design Validation)

- **Units**: 250
- **Purpose**: Pilot shops
- **Timeline**: 60 days

### Phase C — PVT (Production Validation)

- **Units**: 1,000
- **Purpose**: Full QA + packaging
- **Timeline**: 90 days

---

## 🧠 FINAL VERDICT

**🟢 All components listed are**:

- ✅ Legal
- ✅ Non-circumventing
- ✅ Supply-chain stable
- ✅ Scalable
- ✅ Audit-friendly

**This list is safe to send to factories, investors, and compliance teams.**

---

**Document Version**: 1.0  
**Status**: GREEN-LIT  
**Last Updated**: Manufacturing Specifications Final