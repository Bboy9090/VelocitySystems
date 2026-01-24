# Complete Module Structure - Bobby Dev Panel

## All Modules & Components

### Core Modules

1. **`bobby/__init__.py`** - Package initialization
2. **`bobby/core.py`** - Core helper functions (ADB commands, logging, device checks)
3. **`bobby/constants.py`** - Constants and configuration values
4. **`bobby/main.py`** - Main interactive menu entry point
5. **`bobby/cli.py`** - CLI entry point with argument parsing
6. **`bobby/__main__.py`** - Module entry point (`python -m bobby`)

### Feature Modules

7. **`bobby/dossier.py`** - Device dossier collection (identity, build, hardware, battery)
8. **`bobby/warhammer.py`** - Debloat profiles and package management
9. **`bobby/dark_lab.py`** - Stress testing (CPU, thermal, storage I/O)
10. **`bobby/forbidden.py`** - Deep introspection (boot/security, SELinux, encryption, partitions)
11. **`bobby/logs_evidence.py`** - Log collection and package lists
12. **`bobby/bootloader_helper.py`** - Bootloader unlock assistance
13. **`bobby/intake.py`** - Full intake preset (all modules)
14. **`bobby/device_profile.py`** - Device detection and profile recommendations
15. **`bobby/report.py`** - Bench summary generation with health scores
16. **`bobby/sensors.py`** - Sensor health collection and assessment

### Supporting Files

17. **`setup.py`** - Package setup and installation
18. **`requirements.txt`** - Dependencies (all stdlib, no external deps)
19. **`validate.py`** - Module validation script
20. **`README.md`** - User documentation
21. **`LEGENDARY_UPGRADES.md`** - Legendary upgrades documentation

## Module Dependencies

```
main.py
├── core.py (base)
├── dossier.py → core.py
├── warhammer.py → core.py
├── dark_lab.py → core.py
├── forbidden.py → core.py
├── logs_evidence.py → core.py
├── bootloader_helper.py → core.py
├── device_profile.py → core.py
├── sensors.py → core.py
├── intake.py → core.py, dossier.py, forbidden.py, dark_lab.py, logs_evidence.py, report.py
└── report.py → core.py, dossier.py, forbidden.py, dark_lab.py, sensors.py

cli.py → main.py, core.py, report.py, intake.py
__main__.py → main.py
```

## Entry Points

1. **Interactive Mode** (default):
   ```bash
   python -m bobby
   python -m bobby.main
   bobby-dev-panel
   ```

2. **CLI Mode**:
   ```bash
   bobby-dev-panel --bench-summary
   bobby-dev-panel --intake -o output.json
   bobby-dev-panel --check-device
   ```

3. **Programmatic**:
   ```python
   from bobby.report import generate_bench_summary
   from bobby.intake import full_intake
   ```

## All Functions & Menus

### Core Functions
- `check_device()` - Check ADB device connection
- `run_cmd()` - Run shell commands
- `log()` - Logging utility
- `get_model()` - Get device model
- `get_serial()` - Get device serial

### Dossier Module
- `collect_dossier()` - Collect device dossier
- `dossier_menu()` - Interactive menu

### Warhammer Module
- `show_profiles()` - Show debloat profiles
- `preview_profile()` - Preview profile packages
- `apply_profile()` - Apply debloat profile
- `warhammer_menu()` - Interactive menu

### Dark Lab Module
- `cpu_stress_test()` - CPU stress test
- `thermal_monitor()` - Thermal monitoring
- `storage_io_test()` - Storage I/O test
- `io_latency_test()` - Quick I/O latency test
- `snapshot_top_mem()` - Memory snapshot
- `darklab_menu()` - Interactive menu

### Forbidden Module
- `show_boot_security()` - Boot/security info
- `show_selinux()` - SELinux info
- `show_encryption()` - Encryption info
- `show_partitions()` - Partition info
- `show_battery()` - Battery info
- `forbidden_full_scan()` - Full forbidden scan
- `forbidden_menu()` - Interactive menu

### Logs & Evidence Module
- `collect_basic_logs()` - Collect logs and packages

### Bootloader Helper Module
- `motorola_unlock_helper()` - Motorola unlock helper
- `bootloader_menu()` - Interactive menu

### Intake Module
- `full_intake()` - Full intake preset
- `intake_menu()` - Interactive menu

### Device Profile Module
- `detect_device_profile()` - Detect device and recommend profile

### Report Module
- `_get_battery_snapshot()` - Get battery snapshot
- `_estimate_battery_health()` - Estimate battery health
- `_compute_health_score()` - Compute health scores
- `generate_bench_summary()` - Generate full bench summary
- `report_menu()` - Interactive menu

### Sensors Module
- `collect_sensor_data()` - Collect sensor data
- `get_sensor_health_summary()` - Get sensor health summary

## Validation

Run validation script:
```bash
python validate.py
```

This checks:
- All modules can be imported
- Key functions exist
- Module structure is correct

## Status: ✅ COMPLETE

All modules, functions, menus, and entry points are implemented and connected.
