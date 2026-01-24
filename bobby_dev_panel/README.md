# Bobby Dev Panel - Pandora Codex

Device diagnostics and control panel for Android devices.

## Features

### Core Modules

- **Dossier**: Device identity, build, hardware, battery info
- **Warhammer**: Debloat Android devices with preset profiles
- **Dark Lab**: Stress testing (CPU, thermal, storage I/O)
- **Forbidden**: Deep introspection (boot/security, SELinux, encryption, partitions, battery)
- **Logs & Evidence**: Collect basic logs and package lists
- **Bootloader Helper**: Assist with official bootloader unlock
- **Intake**: Full intake preset (all modules)
- **Report**: Bench summary JSON with battery health and health score

### Legendary Upgrades

- **Battery Health Estimation**: Estimates battery health percentage and condition
- **Health Score**: Overall health score (0-100) with sub-scores for battery, security, performance, sensors
- **Performance Block**: I/O latency test results integrated into bench summary
- **Sensor Health**: Sensor data collection and health assessment

### Ultra-Level Features

- **Historical Tracking**: SQLite database for device snapshots, trend analysis, snapshot comparison
- **Evidence System**: Immutable evidence chain with hash verification (Forge Doctrine aligned)
- **Export System**: HTML reports with visualizations, CSV exports, JSON exports
- **Real-time Monitoring**: Live streaming of device metrics (battery, CPU, memory, thermal)
- **Optimization Engine**: Intelligent recommendations based on device state
- **Auto Evidence**: Intake automatically creates evidence entries

## Usage

```bash
python -m bobby.main
```

Or:

```bash
cd bobby_dev_panel
python -m bobby.main
```

## Requirements

- Python 3.8+
- ADB (Android Debug Bridge) installed and in PATH
- Android device connected via USB with USB debugging enabled

## Module Structure

```
bobby/
├── __init__.py
├── __main__.py          # Module entry point
├── main.py              # Main interactive menu
├── cli.py               # CLI with arguments
├── constants.py         # Constants and config
├── core.py              # Core helper functions
├── dossier.py           # Device dossier collection
├── warhammer.py         # Debloat profiles
├── dark_lab.py          # Stress testing
├── forbidden.py         # Deep introspection
├── logs_evidence.py     # Log collection
├── bootloader_helper.py # Bootloader unlock helper
├── intake.py            # Full intake preset
├── report.py            # Bench summary generation
├── sensors.py           # Sensor health module
├── device_profile.py    # Device detection
├── history.py           # Historical data tracking (ULTRA)
├── evidence.py          # Immutable evidence chain (ULTRA)
├── export.py            # HTML/CSV export (ULTRA)
├── monitor.py           # Real-time monitoring (ULTRA)
└── optimize.py          # Optimization recommendations (ULTRA)
```

## Bench Summary JSON

The bench summary includes:

- `device`: Model, manufacturer, serial, Android version
- `battery_health`: Health percentage, condition, cycle count, cycle hint
- `security`: Verified boot state, VBMeta state, bootloader lock state
- `performance`: I/O grade, read/write speeds
- `sensors`: Sensor health status, dead count, total count
- `health_score`: Overall score and sub-scores (battery, security, performance, sensors)

## Documentation

- [Legendary Upgrades](LEGENDARY_UPGRADES.md) - Battery health, health scores, performance integration
- [Ultra Upgrades](ULTRA_UPGRADES.md) - Historical tracking, evidence system, monitoring, optimization
- [Complete Modules](COMPLETE_MODULES.md) - Full module structure and dependencies

## License

Part of Pandora Codex ecosystem. Aligned with Forge Doctrine principles.
