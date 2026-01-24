# Quick Reference: What Works on Real Devices

## ✅ WORKS 100% (Tested/Real ADB Commands)

| Module | Feature | Works On | Notes |
|--------|---------|----------|-------|
| **core.py** | Device check, model, serial | All Android | Real ADB commands |
| **dossier.py** | Device info, battery data | All Android 4.0+ | Real `getprop`, `dumpsys battery` |
| **forbidden.py** | Security info, SELinux | Android 6.0+ | Some features need 8.0+ |
| **warhammer.py** | Debloat packages | All Android | May need root for some apps |
| **logs_evidence.py** | Package list, logcat | All Android | Real commands |
| **report.py** | Battery health calc | All Android | Approximation (not exact) |
| **history.py** | SQLite database | All platforms | Pure Python |
| **evidence.py** | Hash verification | All platforms | Pure Python |
| **export.py** | HTML/CSV/JSON | All platforms | Pure Python |
| **optimize.py** | Recommendations | All Android | Based on real data |

## ⚠️ WORKS BUT SIMPLIFIED (Real Commands, Basic Logic)

| Module | Feature | Works On | Problem |
|--------|---------|----------|---------|
| **dark_lab.py** | I/O test | Most Android | `oflag=direct` may fail |
| **dark_lab.py** | Thermal monitor | Most Android | Device-dependent paths |
| **dark_lab.py** | CPU stress | All Android | **INEFFECTIVE** - just loops |
| **sensors.py** | Sensor detection | All Android | **FAKE** - just checks "unknown" |
| **monitor.py** | CPU usage | All Android | Basic parsing, not accurate % |
| **forensics.py** | Threat detection | All Android | **BASIC** - keyword matching only |

## ❌ PLACEHOLDER/SIMULATION (Not Real)

| Module | Feature | Reality |
|--------|---------|---------|
| **ai_engine.py** | "AI" predictions | **NOT AI** - just statistics/math |
| **ai_engine.py** | Failure prediction | Linear extrapolation, not ML |
| **forensics.py** | Malware detection | Keyword matching, not real scanning |

## Device-Specific Compatibility

### Samsung S22+ / Samsung Devices
- ✅ Works: Dossier, Report, Forbidden, Logs
- ⚠️ Partial: Warhammer (some apps protected), Dark Lab I/O
- ❌ Issues: System apps need root to disable

### Motorola G Play 2023 / Motorola Devices  
- ✅ Works: Dossier, Report, Forbidden, Bootloader Helper
- ⚠️ Partial: Warhammer (Motorola restrictions)
- ❌ Issues: Very strict debloat restrictions

### Generic Android Devices
- ✅ Works: Most modules
- ⚠️ Partial: OEM-specific variations
- ❌ Issues: Some props hidden by OEMs

### iOS Devices (iPhone 15, etc.)
- ❌ **DOES NOT WORK** - Android-only tool
- Would need libimobiledevice for iOS

## What to Actually Use

### ✅ Safe to Use (Real Functionality)
1. **Dossier** - Get device info
2. **Report** - Battery health (approximation)
3. **Forbidden** - Security state
4. **Warhammer** - Debloat (with limitations)
5. **History** - Track device over time
6. **Evidence** - Immutable logs
7. **Export** - Generate reports

### ⚠️ Use with Caution (Simplified)
1. **Dark Lab I/O Test** - Works but may fail on some devices
2. **Monitor** - Real data but basic parsing
3. **Sensors** - Real data, fake dead detection

### ❌ Don't Rely On (Placeholder)
1. **AI Engine** - It's statistics, not AI
2. **CPU Stress Test** - Ineffective
3. **Sensor Dead Detection** - Fake logic
4. **Forensics Threat Detection** - Basic keyword matching

## Bottom Line

**70% real and functional**  
**20% simplified but works**  
**10% placeholder/simulation**

**Core features (dossier, battery health, security, debloat) are 100% real and work on actual Android devices.**

**"Revolutionary" features are mostly statistical analysis, not actual AI/ML.**
