
# REFORGE OS - Python Backend Modules

This document describes the Python backend modules that power the REFORGE OS platform.

## Module Structure

### BootForge (`bootforge/`)
Safe drive imaging and verification tool.

**Modules:**
- `core.py` - Core utilities and logging
- `drives.py` - Drive detection and probing (macOS, Linux, Windows)
- `imager.py` - Image writing and hash verification

**CLI:** `bootforge_cli.py`

**Usage:**
```bash
python bootforge_cli.py list --json
python bootforge_cli.py probe /dev/disk0
python bootforge_cli.py write image.img /dev/disk0 --verify
```

### Phoenix Key (`phoenix/`)
OS recipe management and deployment.

**Modules:**
- `registry.py` - OS recipe registry
- `router.py` - OS deployment router
- `verifier.py` - Recipe verification and validation
- `device_info.py` - Device information gathering

**Recipes:** `phoenix/recipes/*.json`

**CLI:** `phoenix_api_cli.py`

**Usage:**
```bash
python phoenix_api_cli.py list --json
python phoenix_api_cli.py get ubuntu_server_22.04
python phoenix_api_cli.py deploy ubuntu_server_22.04 /dev/disk0
```

### Bobby Dev Mode (`bobby_dev_mode/`)
Android device diagnostics and debloat tool.

**Modules:**
- `adb_utils.py` - ADB/Fastboot utilities
- `modules/dossier.py` - Device information collection
- `modules/warhammer.py` - Safe package removal (debloat)
- `modules/darklab.py` - Performance and thermal testing
- `modules/forbidden.py` - Security and encryption analysis
- `modules/fastboot_arsenal.py` - Fastboot/flash guidance
- `modules/recovery_ops.py` - Recovery mode guidance

**Profiles:** `bobby_dev_mode/profiles/*.json`

**CLI:** `bobby_dev_mode/cli.py` and `bobby_dev_mode/api_cli.py`

**Usage:**
```bash
python bobby_dev_mode/cli.py --profile moto_g_play_23 --module dossier
python bobby_dev_mode/api_cli.py list-profiles
python bobby_dev_mode/api_cli.py run moto_g_play_23 dossier
```

### History (`history/`)
Case file and master ticket management.

**Modules:**
- `manager.py` - Case files, master tickets, DevMode run saving

**Storage:** `storage/history/`

**Usage:**
```python
from history.manager import save_case, load_case, list_cases, create_master_ticket
```

### CRM (`crm/`)
Customer and device management.

**Modules:**
- `manager.py` - Customers and devices

**Storage:** `storage/crm/`

**Usage:**
```python
from crm.manager import add_customer, list_customers, add_device, list_devices
```

### Reports (`reports/`)
PDF export and case reports.

**Modules:**
- `pdf_export.py` - PDF export (with HTML fallback)

**Storage:** `storage/exports/pdf/` and `storage/exports/html/`

**Usage:**
```python
from reports.pdf_export import export_case_pdf
filepath = export_case_pdf(ticket_id, case_data)
```

## Integration with Tauri

The Tauri backend (`apps/workshop-ui/src-tauri/src/main.rs`) provides Rust commands that call the Python modules via subprocess:

- `list_drives()` → `bootforge_cli.py list --json`
- `list_os_recipes()` → `phoenix_api_cli.py list --json`
- `devmode_list_profiles()` → `bobby_dev_mode/api_cli.py list-profiles`
- `devmode_run_module()` → `bobby_dev_mode/api_cli.py run <profile> <module>`

## Requirements

- Python 3.8+
- ADB (for Bobby Dev Mode)
- `reportlab` (optional, for PDF export)
- `smartctl` (optional, for SMART health checks)

## Storage Structure

```
storage/
├── history/          # Case files and master tickets
├── crm/             # Customers and devices
└── exports/
    ├── pdf/         # PDF reports
    └── html/        # HTML reports (fallback)

logs/
└── bootforge.log    # BootForge operation logs
```

## Notes

- All Python modules are designed to be called from Tauri backend
- JSON is used for data exchange between Python and Rust
- Storage uses JSON files for simplicity (can be migrated to database later)
- Profile and recipe files are in JSON format for easy editing
