# Legendary Level Upgrades - Pandora Codex

## Overview

This document describes the "legendary level" upgrades implemented for the Bobby Dev Panel (Pandora Codex ecosystem).

## Implemented Upgrades

### 1. Battery Health Estimation (`report.py`)

**Function**: `_estimate_battery_health(batt: dict) -> dict`

- Estimates battery health percentage based on `charge_full` vs `charge_full_design`
- Calculates condition: EXCELLENT (≥90%), GOOD (≥80%), FAIR (≥70%), WEAK (≥60%), POOR (<60%)
- Tracks cycle count and provides cycle hints: LOW, MODERATE, HIGH, VERY_HIGH
- Includes current level percentage and temperature if available

**Output**:
```json
{
  "percent_estimate": 85,
  "condition": "GOOD",
  "cycle_count": 250,
  "cycle_hint": "MODERATE",
  "current_level_percent": 75,
  "temperature_c": 28.5
}
```

### 2. Health Score Computation (`report.py`)

**Function**: `_compute_health_score(summary: dict) -> dict`

- Calculates overall health score (0-100) using weighted sub-scores
- Sub-scores:
  - **Battery** (35% weight): Based on battery health percentage
  - **Security** (30% weight): Based on verified boot state, VBMeta state, bootloader lock
  - **Performance** (20% weight): Based on I/O grade from Dark Lab tests
  - **Sensors** (15% weight): Based on dead sensor count

**Output**:
```json
{
  "overall": 82,
  "battery": 85,
  "security": 90,
  "performance": 80,
  "sensors": 75
}
```

### 3. Performance Block Integration (`report.py` + `dark_lab.py`)

**Function**: `io_latency_test() -> dict` (in `dark_lab.py`)

- Quick I/O latency test (50MB file)
- Measures read/write speeds in MB/s
- Grades performance: FAST (≥50 MB/s), OK (≥20 MB/s), DEGRADED (<20 MB/s)
- Integrated into bench summary `performance` block

**Output**:
```json
{
  "io_grade": "FAST",
  "avg_mbps": 65.5,
  "write_mbps": 70.2,
  "read_mbps": 60.8
}
```

### 4. Sensor Health Module (`sensors.py`)

**Function**: `collect_sensor_data() -> dict` and `get_sensor_health_summary() -> dict`

- Collects sensor information from device
- Detects dead/inactive sensors
- Provides health status: EXCELLENT, GOOD, FAIR, POOR
- Integrated into bench summary `sensors` block

**Output**:
```json
{
  "dead_count": 0,
  "total_count": 15,
  "health_status": "EXCELLENT"
}
```

### 5. Enhanced Bench Summary (`report.py`)

**Function**: `generate_bench_summary() -> dict`

The bench summary now includes:

- **Device Info**: Model, manufacturer, serial, Android version
- **Battery Health**: Health percentage, condition, cycle count, cycle hint
- **Security**: Verified boot state, VBMeta state, bootloader lock state
- **Performance**: I/O grade, read/write speeds (from Dark Lab)
- **Sensors**: Sensor health status, dead count, total count
- **Health Score**: Overall score and sub-scores (battery, security, performance, sensors)

**Full Example**:
```json
{
  "timestamp": "2024-01-15T10:30:00",
  "device": {
    "model": "SM-S906B",
    "manufacturer": "samsung",
    "serial": "R58M123456",
    "android_version": "13"
  },
  "battery_health": {
    "percent_estimate": 85,
    "condition": "GOOD",
    "cycle_count": 250,
    "cycle_hint": "MODERATE"
  },
  "security": {
    "verified_boot_state": "green",
    "vbmeta_device_state": "locked",
    "bootloader_locked": "1"
  },
  "performance": {
    "io_grade": "FAST",
    "avg_mbps": 65.5,
    "write_mbps": 70.2,
    "read_mbps": 60.8
  },
  "sensors": {
    "dead_count": 0,
    "total_count": 15,
    "health_status": "EXCELLENT"
  },
  "health_score": {
    "overall": 82,
    "battery": 85,
    "security": 90,
    "performance": 80,
    "sensors": 75
  }
}
```

### 6. Intake Integration (`intake.py`)

The `full_intake()` function now calls `generate_bench_summary()` at the end, ensuring all legendary upgrades are included in the intake data.

## Usage

### Generate Bench Summary

```python
from bobby.report import generate_bench_summary

summary = generate_bench_summary()
print(summary)
```

### Run Full Intake

```python
from bobby.intake import full_intake

intake_data = full_intake(output_file="intake_report.json")
```

### CLI Usage

```bash
python -m bobby.main
# Then select option 8: Report (Bench Summary)
```

## Next Steps (Future Legendary Upgrades)

1. **BootForge Integration**: Add drive probe for SMART/health data and safe write speed suggestions
2. **Enhanced Sensor Testing**: More sophisticated sensor health detection
3. **Thermal Profiling**: Long-term thermal trend analysis
4. **Battery Degradation Tracking**: Historical battery health tracking
5. **Performance Benchmarking**: Extended performance test suite

## Notes

- All health scores are calculated in real-time from device data
- Battery health estimation uses `charge_full` / `charge_full_design` ratio
- Performance grading is based on I/O latency test results
- Sensor health is assessed from `dumpsys sensorservice` output
- Security score considers verified boot, VBMeta, and bootloader lock state
