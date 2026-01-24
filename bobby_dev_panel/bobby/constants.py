"""
Constants and configuration for Bobby Dev Panel.
"""

# Version
VERSION = "1.0.0"

# Default values
DEFAULT_IO_TEST_SIZE_MB = 50
DEFAULT_STRESS_TEST_DURATION_SEC = 10
DEFAULT_THERMAL_MONITOR_DURATION_SEC = 30

# Health score weights
HEALTH_SCORE_WEIGHTS = {
    "battery": 0.35,
    "security": 0.30,
    "performance": 0.20,
    "sensors": 0.15,
}

# Battery health thresholds
BATTERY_HEALTH_THRESHOLDS = {
    "EXCELLENT": 90,
    "GOOD": 80,
    "FAIR": 70,
    "WEAK": 60,
    "POOR": 0,
}

# Cycle count hints
CYCLE_HINT_THRESHOLDS = {
    "VERY_HIGH": 800,
    "HIGH": 500,
    "MODERATE": 300,
    "LOW": 0,
}

# I/O performance grades
IO_GRADE_THRESHOLDS = {
    "FAST": 50,  # MB/s
    "OK": 20,    # MB/s
    "DEGRADED": 0,  # MB/s
}

# Sensor health thresholds
SENSOR_HEALTH_THRESHOLDS = {
    "EXCELLENT": 0,   # dead sensors
    "GOOD": 2,        # dead sensors
    "FAIR": 5,        # dead sensors
    "POOR": 999,      # dead sensors
}
