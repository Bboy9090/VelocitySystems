# REFORGE OS — Manufacturing Procurement Guide

**Green-Lit Components for Production**

This guide provides procurement information for REFORGE OS hardware manufacturing.

---

## Approved Vendors

### Electronics Components

#### MCU (STM32G431KBU6)

- **Primary Vendor**: STMicroelectronics
- **Distributors**: Digikey, Mouser, Arrow
- **MOQ**: 100 units
- **Lead Time**: 8-12 weeks
- **Alternative**: STM32H5 series (if G4 unavailable)

#### Secure Element (ATECC608B)

- **Primary Vendor**: Microchip
- **Distributors**: Digikey, Mouser
- **MOQ**: 250 units
- **Lead Time**: 12-16 weeks
- **Provisioning**: Microchip secure provisioning service required

#### USB-C PD Controller (TPS6598x)

- **Primary Vendor**: Texas Instruments
- **Distributors**: Digikey, Mouser, TI Direct
- **MOQ**: 250 units
- **Lead Time**: 8-12 weeks

#### USB Hub IC (USB5744)

- **Primary Vendor**: Microchip
- **Distributors**: Digikey, Mouser
- **MOQ**: 100 units
- **Lead Time**: 8-10 weeks

---

## Manufacturing Partners

### PCB Fabrication

#### JLCPCB (Prototyping + Low-Mid Volume)

- **Location**: China
- **Capacity**: 1-10k units
- **Capabilities**: 4-layer FR-4, SMT assembly
- **Lead Time**: 2-3 weeks
- **Certifications**: ISO 9001

#### PCBWay (Mid-Volume)

- **Location**: China
- **Capacity**: 1-50k units
- **Capabilities**: 4-layer FR-4, SMT assembly
- **Lead Time**: 2-4 weeks
- **Certifications**: ISO 9001

#### Seeed Studio Fusion (Scalable Production)

- **Location**: China
- **Capacity**: 10k-100k+ units
- **Capabilities**: Full turnkey, ISO-certified
- **Lead Time**: 4-8 weeks
- **Certifications**: ISO 9001, ISO 14001

---

### CNC & Enclosures

#### Dongguan CNC Shops

- **Specialization**: Precision aluminum machining
- **Lead Time**: 3-4 weeks
- **MOQ**: 100 units
- **Finish Options**: Anodized black, clear, custom colors

#### Shenzhen Rapid Direct

- **Specialization**: Rapid prototyping + production
- **Lead Time**: 2-3 weeks (prototype), 4-6 weeks (production)
- **MOQ**: 50 units (prototype), 500 units (production)

---

### Assembly (EMS)

#### ISO-9001 Tier-2 EMS Providers

**Requirements**:
- ISO 9001 certification
- Secure element provisioning capability
- Manual QA lines
- Calibration equipment
- Audit trail capability

**Recommended Regions**:
- Shenzhen, China (cost-effective)
- Taiwan (quality + cost balance)
- Mexico (near-shore for US)
- Eastern Europe (near-shore for EU)

---

## Procurement Phases

### Phase 1: Prototype (EVT)

**Quantity**: 50 units

**Procurement**:
- Components: Digikey/Mouser (no MOQ concerns)
- PCB: JLCPCB (prototype service)
- Assembly: Manual (internal or small EMS)
- Enclosure: 3D printed or small-batch CNC

**Timeline**: 4-6 weeks

---

### Phase 2: Pilot (DVT)

**Quantity**: 250 units

**Procurement**:
- Components: Distributors (meet MOQ)
- PCB: PCBWay (mid-volume)
- Assembly: Small EMS (ISO-certified)
- Enclosure: Small-batch CNC (Dongguan)

**Timeline**: 8-10 weeks

---

### Phase 3: Production (PVT)

**Quantity**: 1,000 units

**Procurement**:
- Components: Manufacturer direct (negotiate pricing)
- PCB: Seeed Studio Fusion or equivalent
- Assembly: Established EMS (full turnkey)
- Enclosure: Production CNC (Dongguan)

**Timeline**: 12-16 weeks

---

### Phase 4: Scale Production

**Quantity**: 10k-100k+ units

**Procurement**:
- Components: Manufacturer contracts
- PCB: High-volume fabricator
- Assembly: Tier-1 EMS (full automation)
- Enclosure: Production CNC (high-volume)

**Timeline**: 16-20 weeks (first batch)

---

## Component Substitution Guidelines

### Approved Substitutions

**MCU**: STM32G4 → STM32H5 (pin-compatible)
**Secure Element**: ATECC608B → ATECC608A (functionally equivalent)
**USB Hub**: USB5744 → USB5734 (if 5744 unavailable)

### Substitution Process

1. Engineering review
2. Compatibility testing
3. Compliance verification
4. BOM update
5. Documentation update

---

## Quality Requirements

### Component Quality

- **Grade**: Industrial/commercial (not consumer)
- **Temperature Range**: -40°C to 85°C (extended temp)
- **Reliability**: > 10,000 hours MTBF

### Manufacturing Quality

- **IPC-A-610**: Class 2 minimum (Class 3 for secure element)
- **Solder Quality**: Visual + X-ray inspection
- **Test Coverage**: 100% functional testing

---

## Cost Targets

### Volume Pricing Goals

| Quantity | Target COGS Reduction |
|----------|----------------------|
| 1k units | Baseline |
| 5k units | -10% |
| 10k units | -15% |
| 50k units | -25% |
| 100k+ units | -35% |

**Negotiation Strategy**: Manufacturer direct contracts at 10k+ volume

---

## Lead Time Planning

### Component Lead Times

- **Standard Components**: 8-12 weeks
- **Secure Element**: 12-16 weeks (provisioning)
- **Custom Components**: 16-20 weeks
- **Enclosures**: 4-6 weeks (CNC)

### Buffer Recommendations

- **Component Buffer**: +20% safety stock
- **Assembly Buffer**: +15% yield loss
- **Total Buffer**: Plan for 25-30% overhead

---

## Compliance Procurement

### Certifications Required

- **RoHS**: All components must be RoHS compliant
- **REACH**: EU compliance
- **Conflict Minerals**: Due diligence required
- **USB-IF**: USB components must be certified

### Documentation Required

- Component certificates of compliance
- Test reports
- Material declarations
- Country of origin documentation

---

## Supplier Qualification

### Required Criteria

- ISO 9001 certification (minimum)
- Quality audit
- Financial stability check
- Supply chain audit (for critical components)
- Conflict minerals compliance

### Evaluation Process

1. RFQ (Request for Quotation)
2. Supplier qualification audit
3. Sample evaluation
4. Contract negotiation
5. Quality agreement signing

---

## Risk Management

### Supply Chain Risks

- **Single Source**: Avoid for critical components
- **Geographic Concentration**: Diversify manufacturing
- **Component Obsolescence**: Monitor EOL notices
- **Price Volatility**: Lock pricing contracts

### Mitigation Strategies

- Approved alternate vendors
- Safety stock (critical components)
- Multiple manufacturing locations
- Long-term supply agreements

---

**Document Version**: 1.0  
**Status**: PROCUREMENT GUIDE FINAL  
**Last Updated**: Manufacturing Procurement