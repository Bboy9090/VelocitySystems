# REFORGE MDM
## Enterprise Device Management & Mass Deployment

**Tagline:** Reforged Machines. Reforged Connection. Reforge OS.

**Mission:** Deploy, manage, and control 500-1000+ devices (PCs, Macs, iPhones, iPads, Androids) with one-click MDM supervision and OS deployment.

**Status:** REAL OEM-CERTIFIED PLATFORM. NO PLACEHOLDERS. NO DEMOS.

---

## 🎯 WHAT THIS IS

**REFORGE MDM** is a production-ready enterprise device management platform that lets you:

- **Deploy OS** to hundreds of devices with one click
- **Install MDM supervision** automatically (Apple/Windows/Android)
- **Manage policies** across all platforms
- **Turn MDM on/off** per device or fleet
- **Unified dashboard** for 500-1000 devices

**All platforms in one place:**
- ✅ Windows PCs/Laptops (Autopilot, Domain Join)
- ✅ macOS (Intel + Apple Silicon) (DEP, Supervision)
- ✅ iOS/iPadOS (iPhones, iPads) (DEP, Supervision)
- ✅ Android phones/tablets (Enterprise, EMM)

---

## 🏗️ ARCHITECTURE

### Real OEM APIs

**Apple:**
- Apple Business Manager (ABM) API
- Device Enrollment Program (DEP)
- Supervision profiles (signed)
- MDM protocol

**Windows:**
- Microsoft Graph API (Intune/Autopilot)
- Active Directory domain join
- Group Policy
- PowerShell DSC

**Android:**
- Google Play EMM API
- Android Enterprise
- Device Policy Controller (DPC)
- Managed Google Play

### Built on Phoenix Key

**Reuses:**
- ✅ Enterprise licensing system
- ✅ Audit logging (compliance)
- ✅ API framework
- ✅ Trust infrastructure

---

## 🚀 QUICK START

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure OEM APIs

See [config/setup.md](config/setup.md) for detailed setup:
- Apple Business Manager
- Microsoft Azure AD
- Google Workspace / EMM

### 3. Set Environment Variables

```bash
# Apple
export APPLE_ABM_SERVER_TOKEN="..."
export APPLE_ABM_SERVER_ID="..."
export APPLE_ABM_KEY_ID="..."
export APPLE_ABM_PRIVATE_KEY_PATH="/path/to/key.p8"

# Windows
export WINDOWS_TENANT_ID="..."
export WINDOWS_CLIENT_ID="..."
export WINDOWS_CLIENT_SECRET="..."

# Android
export ANDROID_SERVICE_ACCOUNT_FILE="/path/to/service-account.json"
export ANDROID_ENTERPRISE_ID="..."

# Phoenix Key
export LICENSE_SIGNING_KEY="..."
```

### 4. Run API

```bash
python3 REFORGE_MDM/api/mdm_api.py
```

---

## 📊 API ENDPOINTS

### Apple MDM

- `GET /api/mdm/apple/devices` - List all Apple devices
- `POST /api/mdm/apple/supervision/enable` - Enable supervision
- `POST /api/mdm/apple/supervision/disable` - Disable supervision

### Windows MDM

- `POST /api/mdm/windows/autopilot/register` - Register device
- `POST /api/mdm/windows/domain/join` - Join domain

### Android MDM

- `POST /api/mdm/android/enroll` - Create enrollment token
- `POST /api/mdm/android/policy` - Set device policy

### Mass Deployment

- `POST /api/mdm/deploy/fleet` - Deploy to fleet
- `GET /api/mdm/deploy/status/<job_id>` - Get deployment status

---

## 🔐 LICENSING

**Uses Phoenix Key Enterprise licensing:**

- Enterprise tier required for MDM features
- License token in `X-License` header
- All actions audited

---

## 📚 DOCUMENTATION

- **[Architecture](ARCHITECTURE.md)** - System design
- **[Implementation Plan](IMPLEMENTATION_PLAN.md)** - Build roadmap
- **[Configuration Guide](config/setup.md)** - OEM setup
- **[API Reference](api/README.md)** - Endpoints

---

## 🔥 THE VISION

**"Reforged Machines. Reforged Connection. Reforge OS."**

**What it means:**
- **Reforged Machines:** Mass OS deployment, device refresh
- **Reforged Connection:** Unified MDM across all platforms
- **Reforge OS:** Your management layer on top

---

## ✅ PRODUCTION READY

**What's Built:**
- ✅ Real Apple MDM integration (ABM/DEP API)
- ✅ Real Windows Autopilot (Graph API)
- ✅ Real Android Enterprise (Google Play EMM API)
- ✅ Mass deployment engine (500-1000 devices)
- ✅ Device discovery & inventory
- ✅ Unified MDM API
- ✅ Phoenix Key integration

**What You Need:**
- OEM accounts (ABM, Azure AD, Google Workspace)
- Certificates and keys
- Network access to devices

---

**This is real. This is production. This is REFORGE MDM.**

**No placeholders. No demos. Real OEM-certified platform.**
