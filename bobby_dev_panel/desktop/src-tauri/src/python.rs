use std::process::Command;
use std::path::PathBuf;
use std::env;
use serde_json;

pub fn check_python_available() -> bool {
    let output = Command::new("python3")
        .arg("--version")
        .output();
    
    if output.is_err() {
        // Try python
        let output = Command::new("python")
            .arg("--version")
            .output();
        return output.is_ok();
    }
    
    true
}

pub fn get_python_command() -> String {
    // Try python3 first, then python
    let output = Command::new("python3")
        .arg("--version")
        .output();
    
    if output.is_ok() {
        return "python3".to_string();
    }
    
    "python".to_string()
}

pub fn get_bobby_module_path() -> PathBuf {
    // Try multiple paths in order of likelihood
    let mut paths_to_try = Vec::new();
    
    // 1. Parent directory of desktop folder (most common in development)
    if let Ok(current) = env::current_dir() {
        if let Some(parent) = current.parent() {
            paths_to_try.push(parent.join("bobby_dev_panel"));
        }
        // Also try current directory
        paths_to_try.push(current.join("bobby_dev_panel"));
    }
    
    // 2. Next to executable (production)
    if let Ok(exe) = env::current_exe() {
        if let Some(exe_dir) = exe.parent() {
            paths_to_try.push(exe_dir.join("bobby_dev_panel"));
            // Also try parent of exe dir
            if let Some(exe_parent) = exe_dir.parent() {
                paths_to_try.push(exe_parent.join("bobby_dev_panel"));
            }
        }
    }
    
    // 3. Absolute fallback
    paths_to_try.push(PathBuf::from("bobby_dev_panel"));
    
    // Check each path
    for path in &paths_to_try {
        if path.exists() && path.join("bobby").exists() {
            return path.clone();
        }
    }
    
    // Return first path as fallback (will be created/used)
    paths_to_try[0].clone()
}

pub fn run_python_module(module: &str, function: &str, args: Vec<String>) -> Result<String, String> {
    let python_cmd = get_python_command();
    let bobby_path = get_bobby_module_path();
    
    // Create a temporary Python script file for better reliability
    use std::fs::File;
    use std::io::Write;
    
    // Handle class-based modules that need instantiation
    let (module_name, class_name, method_name) = match (module, function) {
        ("history", "get_snapshots") => ("history", "DeviceHistory", "get_snapshots"),
        ("history", "save_snapshot") => ("history", "DeviceHistory", "save_snapshot"),
        ("history", "get_trends") => ("history", "DeviceHistory", "get_trends"),
        ("evidence", "verify_chain") => ("evidence", "EvidenceChain", "verify_chain"),
        ("evidence", "add_evidence") => ("evidence", "EvidenceChain", "add_evidence"),
        ("monitor", "start_monitor") => ("monitor", "DeviceMonitor", "start"),
        ("monitor", "stop_monitor") => ("monitor", "DeviceMonitor", "stop"),
        ("ai_engine", "predict_failure") => ("ai_engine", "AIEngine", "predict_failure"),
        ("ai_engine", "detect_anomalies") => ("ai_engine", "AIEngine", "detect_anomalies"),
        ("fleet", "fleet_dashboard") => ("fleet", "FleetManager", "fleet_dashboard"),
        ("forensics", "full_forensics_scan") => ("forensics", "ForensicsEngine", "full_forensics_scan"),
        _ => (module, "", function), // Regular function call
    };
    
    let is_class_method = !class_name.is_empty();
    
    let args_code = if args.is_empty() {
        "call_args = []".to_string()
    } else {
        let args_list = args.iter()
            .map(|a| format!(r#""{}""#, a.replace('"', r#"\""#).replace('\n', "\\n").replace('\r', "")))
            .collect::<Vec<_>>()
            .join(", ");
        format!("call_args = [{}]", args_list)
    };
    
    let call_code = if is_class_method {
        format!(
            r#"
    # Class-based module
    from bobby.{} import {}
    instance = {}()
    if call_args:
        result = instance.{}(*call_args)
    else:
        result = instance.{}()
"#,
            module_name, class_name, class_name, method_name, method_name
        )
    } else {
        format!(
            r#"
    # Function-based module
    from bobby.{} import {}
    if call_args:
        result = {}(*call_args)
    else:
        result = {}()
"#,
            module_name, function, function, function
        )
    };
    
    let script_content = format!(
        r#"
import sys
import os
import json

# Add bobby_dev_panel to path
bobby_path = r"{}"
if os.path.exists(bobby_path):
    sys.path.insert(0, bobby_path)
else:
    # Try parent directory
    parent_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "bobby_dev_panel")
    if os.path.exists(parent_path):
        sys.path.insert(0, parent_path)
    # Try current directory parent
    if os.path.exists(os.path.join("..", "bobby_dev_panel")):
        sys.path.insert(0, os.path.join("..", "bobby_dev_panel"))

try:
    {}
    
    # Serialize result
    if isinstance(result, dict):
        output = json.dumps(result, default=str)
    elif isinstance(result, (list, tuple)):
        output = json.dumps(list(result), default=str)
    else:
        output = json.dumps({{"result": result}}, default=str)
    
    print(output)
except Exception as e:
    import traceback
    error_output = json.dumps({{
        "error": str(e),
        "type": type(e).__name__,
        "traceback": traceback.format_exc()
    }})
    print(error_output, file=sys.stderr)
    sys.exit(1)
"#,
        bobby_path.to_str().unwrap_or("."),
        args_code,
        call_code
    );
    
    // Write to temporary file
    use std::time::{SystemTime, UNIX_EPOCH};
    let timestamp = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_nanos();
    let temp_file = std::env::temp_dir().join(format!("bobby_call_{}.py", timestamp));
    let mut file = File::create(&temp_file)
        .map_err(|e| format!("Failed to create temp file: {}", e))?;
    file.write_all(script_content.as_bytes())
        .map_err(|e| format!("Failed to write temp file: {}", e))?;
    drop(file);
    
    // Execute Python script
    let output = Command::new(&python_cmd)
        .arg(temp_file.to_str().unwrap())
        .output()
        .map_err(|e| format!("Failed to execute Python: {}", e))?;
    
    // Clean up temp file
    let _ = std::fs::remove_file(&temp_file);
    
    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);
    
    // Check for JSON error in stderr
    if let Ok(json_val) = serde_json::from_str::<serde_json::Value>(&stderr) {
        if let Some(error) = json_val.get("error") {
            return Err(format!("Python error: {}", error));
        }
    }
    
    if !output.status.success() {
        return Err(format!("Python command failed: {}", stderr));
    }
    
    Ok(stdout.trim().to_string())
}
