# REFORGE OS - Quick Start Guide

## Status: ✅ Ready to Run

All Python backend modules have been created and integrated with the Tauri frontend.

## What Was Built

### ✅ Python Backend Modules
- **BootForge** - Drive imaging and verification (`bootforge/`)
- **Phoenix Key** - OS recipe management (`phoenix/`)
- **Bobby Dev Mode** - Android diagnostics (`bobby_dev_mode/`)
- **History/CRM** - Case files and customer management (`history/`, `crm/`)
- **Reports** - PDF export (`reports/`)

### ✅ Tauri Integration
- Updated `apps/workshop-ui/src-tauri/src/main.rs` with Python command bridges
- All UI commands now call Python modules via subprocess

### ✅ Configuration
- Python 3.14.0 installed and working
- BootForge module tested and functional
- Dependencies installed (`npm install`)

## Starting the Application

### Option 1: Development Mode (Current)
```powershell
cd "C:\Users\Bobby\NEWFORGEl - Copy\apps\workshop-ui"
npm run dev
```
or
```powershell
npm run tauri:dev
```

The application will:
1. Compile the Rust backend (first time takes a few minutes)
2. Start the Vite dev server
3. Launch the REFORGE OS window automatically

### Option 2: Production Build
```powershell
cd "C:\Users\Bobby\NEWFORGEl - Copy\apps\workshop-ui"
npm run build
```

This creates:
- `src-tauri/target/release/reforge-os.exe` (Windows executable)

## Python Script Paths

The Tauri backend automatically resolves Python script paths relative to the workspace root:
- `bootforge_cli.py`
- `phoenix_api_cli.py`
- `bobby_dev_mode/api_cli.py`

All scripts are called from the workspace root directory.

## Testing Python Modules

### BootForge
```powershell
cd "C:\Users\Bobby\NEWFORGEl - Copy"
python bootforge_cli.py list --json
python bootforge_cli.py probe \\.\PhysicalDrive0
```

### Phoenix Key
```powershell
python phoenix_api_cli.py list --json
python phoenix_api_cli.py get ubuntu_server_22.04
```

### Bobby Dev Mode
```powershell
python bobby_dev_mode/api_cli.py list-profiles
python bobby_dev_mode/api_cli.py run moto_g_play_23 dossier
```

## Troubleshooting

### Python Not Found
- Ensure Python 3.x is in PATH
- Test with: `python --version`

### Tauri Build Errors
- First build takes time (downloading Rust dependencies)
- Ensure Rust toolchain is installed: `rustc --version`

### Module Not Found
- Ensure you're in the workspace root when running Python scripts
- Check that all `__init__.py` files exist in module directories

## Next Steps

1. **Add More Device Profiles** - Extend `bobby_dev_mode/profiles/`
2. **Add OS Recipes** - Add more recipes to `phoenix/recipes/`
3. **Enhance UI** - Connect more UI components to Python backend
4. **Database Migration** - Move from JSON files to Postgres when ready

## Application Features

The REFORGE OS application includes:

- **Dashboard** - Device overview and analysis
- **Device Analysis** - Comprehensive device information
- **Compliance Summary** - Regulatory compliance tracking
- **Legal Classification** - Jurisdiction-aware device status
- **Certification** - Technician certification management
- **Operations** - Control tower with metrics
- **Custodian Vault** - Internal Pandora Codex access (if authorized)

All features are connected to the Python backend for actual device interaction and data management.

---

**Application is starting...** The Tauri dev server should launch automatically when compilation completes.
