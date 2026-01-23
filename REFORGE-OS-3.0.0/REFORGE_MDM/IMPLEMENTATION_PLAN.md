# REFORGE MDM - Implementation Plan

## What Exists (Reuse)

### ✅ Phoenix Key Infrastructure
- **Licensing system** → Perfect for Enterprise MDM tier
- **Audit logging** → Required for compliance
- **API framework** → Extend for MDM endpoints
- **CLI tool** → Add MDM commands

### ✅ What We Built
- Canonical core (`/core`)
- Enterprise API structure
- License enforcement
- Audit trails

---

## What Needs to Be Built

### 1. Apple MDM Integration

**Required:**
- Apple Business Manager (ABM) API integration
- Device Enrollment Program (DEP) enrollment
- MDM server setup (or use existing MDM provider API)
- Supervision profile generation/signing

**Implementation:**
```python
# REFORGE_MDM/mdm/apple/dep.py
class AppleDEP:
    def enroll_device(self, serial: str) -> bool:
        # DEP enrollment via ABM API
        pass
    
    def push_supervision(self, device_id: str) -> bool:
        # Push supervision profile
        pass
```

**Tools to Integrate:**
- `profiles` command (macOS)
- Apple Configurator 2 (for supervision)
- ABM API client

---

### 2. Windows Mass Deployment

**Required:**
- Windows Autopilot integration
- Domain join automation
- Group Policy push
- WDS/MDT integration

**Implementation:**
```python
# REFORGE_MDM/mdm/windows/deploy.py
class WindowsDeploy:
    def deploy_os(self, device: str, image: str) -> bool:
        # Deploy Windows image
        pass
    
    def domain_join(self, device: str, domain: str) -> bool:
        # Auto domain join
        pass
```

**Tools to Integrate:**
- PowerShell DSC
- Windows Deployment Services (WDS)
- Intune Graph API (optional)

---

### 3. Android Enterprise Enrollment

**Required:**
- Android Enterprise (EMM) setup
- Device Policy Controller (DPC)
- Managed Google Play integration
- QR code enrollment

**Implementation:**
```python
# REFORGE_MDM/mdm/android/enroll.py
class AndroidEnroll:
    def enterprise_enroll(self, device: str) -> bool:
        # Android Enterprise enrollment
        pass
    
    def push_policy(self, device_id: str, policy: dict) -> bool:
        # Push EMM policy
        pass
```

**Tools to Integrate:**
- `adb` (Android Debug Bridge)
- Google Play EMM API
- DPC app

---

### 4. Unified Dashboard

**Required:**
- Fleet view (500-1000 devices)
- Real-time status
- Bulk operations
- Policy management

**Implementation:**
```typescript
// REFORGE_MDM/dashboard/FleetView.tsx
- Device grid/list view
- Filter by platform/status
- Bulk select
- One-click actions
- Progress tracking
```

---

### 5. Mass Deployment Engine

**Required:**
- Parallel deployment (batches)
- Progress tracking
- Error handling
- Rollback capability

**Implementation:**
```python
# REFORGE_MDM/deployment/mass_deploy.py
class MassDeploy:
    def deploy_to_fleet(self, devices: List[str], os: str) -> Job:
        # Parallel deployment with batching
        pass
    
    def track_progress(self, job_id: str) -> Status:
        # Real-time progress
        pass
```

---

## Integration with Phoenix Key

### Reuse Licensing

```python
# REFORGE_MDM/api/mdm_api.py
from phoenix_key.core.core import get_core

@app.route("/api/mdm/deploy", methods=["POST"])
def deploy_fleet():
    # Check Enterprise license
    core = get_core()
    lic = core.authorize(token, "mass_deploy", actor=user)
    
    # Deploy...
```

### Reuse Audit

```python
# Every MDM action is audited
core.authorize(token, "mdm_enroll", actor=user)
# Automatically logged in audit trail
```

---

## Quick Start (MVP)

### Week 1: Apple MDM
- [ ] ABM API integration
- [ ] DEP enrollment
- [ ] Supervision profile push
- [ ] Test with 10 devices

### Week 2: Windows Deployment
- [ ] Autopilot integration
- [ ] Domain join automation
- [ ] Test with 10 devices

### Week 3: Android Enterprise
- [ ] EMM enrollment
- [ ] Policy push
- [ ] Test with 10 devices

### Week 4: Unified Dashboard
- [ ] Fleet view
- [ ] Bulk operations
- [ ] Test with 100 devices

### Week 5: Mass Deployment
- [ ] Parallel deployment
- [ ] Progress tracking
- [ ] Test with 500 devices

---

## Technical Stack

### Backend
- **Python** (FastAPI or Flask)
- **Phoenix Key core** (reuse)
- **Platform APIs:**
  - Apple Business Manager API
  - Microsoft Graph API (Intune)
  - Google Play EMM API

### Frontend
- **React** (reuse existing UI)
- **Fleet dashboard**
- **Real-time updates** (WebSocket)

### Infrastructure
- **MDM Server** (or integrate with existing)
- **Device discovery** (network scanning)
- **Deployment queue** (Celery or similar)

---

## Cost Considerations

### Apple MDM
- **ABM account:** Free
- **MDM server:** Self-hosted or provider ($X/month)
- **VPP:** Free (volume app purchases)

### Windows
- **Intune:** $X/device/month (or use Group Policy)
- **Autopilot:** Free (with Intune)

### Android
- **Google Workspace:** $X/user/month (or use standalone EMM)

**Your Advantage:**
- Unified platform = lower total cost
- Self-hosted option = more control

---

## Go-to-Market

### Target Customers

1. **Schools** (K-12, Universities)
   - 500-1000 student devices
   - Mixed platforms (iPads, Chromebooks, Macs)
   - Budget-conscious

2. **Businesses** (SMB to Enterprise)
   - Fleet management
   - BYOD + corporate devices
   - Compliance requirements

3. **MSPs** (Managed Service Providers)
   - Multi-tenant
   - White-label option
   - Recurring revenue

### Pricing

**Per-Device:**
- $5-10/device/year

**Unlimited:**
- $500-1000/month (unlimited devices)

**Uses Phoenix Key Enterprise licensing!**

---

**This is the pivot. This is the real product.**
