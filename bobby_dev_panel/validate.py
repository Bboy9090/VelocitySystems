#!/usr/bin/env python3
"""
Validation script to check all modules are properly structured.
"""

import sys
import importlib
import pkgutil

def validate_imports():
    """Validate all modules can be imported."""
    print("Validating module imports...")
    
    modules_to_check = [
        "bobby.core",
        "bobby.dossier",
        "bobby.warhammer",
        "bobby.dark_lab",
        "bobby.forbidden",
        "bobby.logs_evidence",
        "bobby.bootloader_helper",
        "bobby.intake",
        "bobby.device_profile",
        "bobby.report",
        "bobby.sensors",
        "bobby.main",
        "bobby.cli",
        "bobby.constants",
    ]
    
    errors = []
    for module_name in modules_to_check:
        try:
            importlib.import_module(module_name)
            print(f"  ✓ {module_name}")
        except Exception as e:
            print(f"  ✗ {module_name}: {e}")
            errors.append((module_name, str(e)))
    
    if errors:
        print(f"\n{len(errors)} module(s) failed to import:")
        for module_name, error in errors:
            print(f"  - {module_name}: {error}")
        return False
    
    print(f"\n✓ All {len(modules_to_check)} modules imported successfully")
    return True


def validate_functions():
    """Validate key functions exist."""
    print("\nValidating key functions...")
    
    from bobby import core, report, intake, sensors
    
    functions_to_check = [
        (core, "check_device"),
        (core, "run_cmd"),
        (core, "log"),
        (report, "generate_bench_summary"),
        (report, "_estimate_battery_health"),
        (report, "_compute_health_score"),
        (intake, "full_intake"),
        (sensors, "collect_sensor_data"),
        (sensors, "get_sensor_health_summary"),
    ]
    
    errors = []
    for module, func_name in functions_to_check:
        if hasattr(module, func_name):
            print(f"  ✓ {module.__name__}.{func_name}")
        else:
            print(f"  ✗ {module.__name__}.{func_name} (missing)")
            errors.append(f"{module.__name__}.{func_name}")
    
    if errors:
        print(f"\n{len(errors)} function(s) missing:")
        for func in errors:
            print(f"  - {func}")
        return False
    
    print(f"\n✓ All {len(functions_to_check)} functions found")
    return True


def main():
    """Run all validation checks."""
    print("=" * 60)
    print("Bobby Dev Panel - Module Validation")
    print("=" * 60)
    
    import_ok = validate_imports()
    func_ok = validate_functions()
    
    print("\n" + "=" * 60)
    if import_ok and func_ok:
        print("✓ All validations passed!")
        sys.exit(0)
    else:
        print("✗ Some validations failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
