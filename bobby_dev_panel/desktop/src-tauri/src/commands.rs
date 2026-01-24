use serde::{Deserialize, Serialize};
use std::process::Command;
use crate::python;

#[derive(Debug, Serialize, Deserialize)]
pub struct DeviceInfo {
    pub platform: String,
    pub serial: String,
    pub model: String,
    pub status: String,
}

#[tauri::command]
pub fn check_device() -> Result<bool, String> {
    // Check Android
    let android_output = Command::new("adb")
        .arg("devices")
        .output();
    
    if let Ok(output) = android_output {
        let stdout = String::from_utf8_lossy(&output.stdout);
        let lines: Vec<&str> = stdout.lines().collect();
        for line in lines {
            if line.contains("device") && !line.starts_with("List") {
                return Ok(true);
            }
        }
    }
    
    // Check iOS
    let ios_output = Command::new("idevice_id")
        .arg("-l")
        .output();
    
    if let Ok(output) = ios_output {
        let stdout = String::from_utf8_lossy(&output.stdout);
        if !stdout.trim().is_empty() {
            return Ok(true);
        }
    }
    
    Ok(false)
}

#[tauri::command]
pub fn get_devices() -> Result<Vec<DeviceInfo>, String> {
    let mut devices = Vec::new();
    
    // Get Android devices
    let android_output = Command::new("adb")
        .arg("devices")
        .arg("-l")
        .output()
        .map_err(|e| format!("ADB error: {}", e))?;
    
    let stdout = String::from_utf8_lossy(&android_output.stdout);
    for line in stdout.lines().skip(1) {
        if line.contains("device") {
            let parts: Vec<&str> = line.split_whitespace().collect();
            if parts.len() >= 2 {
                let serial = parts[0].to_string();
                // Get model
                let model_output = Command::new("adb")
                    .arg("-s")
                    .arg(&serial)
                    .arg("shell")
                    .arg("getprop")
                    .arg("ro.product.model")
                    .output();
                
                let model = if let Ok(output) = model_output {
                    String::from_utf8_lossy(&output.stdout).trim().to_string()
                } else {
                    "Unknown".to_string()
                };
                
                devices.push(DeviceInfo {
                    platform: "android".to_string(),
                    serial,
                    model,
                    status: "connected".to_string(),
                });
            }
        }
    }
    
    // Get iOS devices
    let ios_output = Command::new("idevice_id")
        .arg("-l")
        .output();
    
    if let Ok(output) = ios_output {
        let stdout = String::from_utf8_lossy(&output.stdout);
        for udid in stdout.lines() {
            let udid = udid.trim();
            if !udid.is_empty() {
                // Get model
                let model_output = Command::new("ideviceinfo")
                    .arg("-u")
                    .arg(udid)
                    .arg("-k")
                    .arg("ProductType")
                    .output();
                
                let model = if let Ok(output) = model_output {
                    String::from_utf8_lossy(&output.stdout).trim().to_string()
                } else {
                    "Unknown".to_string()
                };
                
                devices.push(DeviceInfo {
                    platform: "ios".to_string(),
                    serial: udid.to_string(),
                    model,
                    status: "connected".to_string(),
                });
            }
        }
    }
    
    Ok(devices)
}

#[tauri::command]
pub fn get_platform() -> Result<String, String> {
    if check_device()? {
        // Check which platform
        let android_output = Command::new("adb")
            .arg("devices")
            .output();
        
        if let Ok(output) = android_output {
            let stdout = String::from_utf8_lossy(&output.stdout);
            if stdout.contains("device") {
                return Ok("android".to_string());
            }
        }
        
        let ios_output = Command::new("idevice_id")
            .arg("-l")
            .output();
        
        if let Ok(output) = ios_output {
            let stdout = String::from_utf8_lossy(&output.stdout);
            if !stdout.trim().is_empty() {
                return Ok("ios".to_string());
            }
        }
    }
    
    Ok("unknown".to_string())
}

#[tauri::command]
pub fn collect_dossier(device_serial: Option<String>) -> Result<serde_json::Value, String> {
    let mut args = Vec::new();
    if let Some(serial) = device_serial {
        args.push(serial);
    }
    
    python::run_python_module("dossier", "collect_dossier", args)
        .and_then(|output| {
            serde_json::from_str(&output.trim())
                .map_err(|e| format!("Failed to parse JSON: {} | Output: {}", e, output))
        })
}

#[tauri::command]
pub fn generate_bench_summary(device_serial: Option<String>) -> Result<serde_json::Value, String> {
    let mut args = Vec::new();
    if let Some(serial) = device_serial {
        args.push(serial);
    }
    
    python::run_python_module("report", "generate_bench_summary", args)
        .and_then(|output| {
            serde_json::from_str(&output.trim())
                .map_err(|e| format!("Failed to parse JSON: {} | Output: {}", e, output))
        })
}

#[tauri::command]
pub fn run_intake(output_file: Option<String>) -> Result<serde_json::Value, String> {
    let mut args = Vec::new();
    if let Some(file) = output_file {
        args.push(file);
    }
    
    python::run_python_module("intake", "full_intake", args)
        .and_then(|output| {
            serde_json::from_str(&output.trim())
                .map_err(|e| format!("Failed to parse JSON: {} | Output: {}", e, output))
        })
}

#[tauri::command]
pub fn get_history(device_serial: Option<String>, limit: Option<u32>) -> Result<serde_json::Value, String> {
    let mut args = Vec::new();
    if let Some(serial) = device_serial {
        args.push(serial);
    }
    args.push(limit.unwrap_or(100).to_string());
    
    python::run_python_module("history", "get_snapshots", args)
        .and_then(|output| {
            serde_json::from_str(&output.trim())
                .map_err(|e| format!("Failed to parse JSON: {} | Output: {}", e, output))
        })
}

#[tauri::command]
pub fn save_snapshot(device_serial: Option<String>) -> Result<serde_json::Value, String> {
    let mut args = Vec::new();
    if let Some(serial) = device_serial {
        args.push(serial);
    }
    
    python::run_python_module("history", "save_snapshot", args)
        .and_then(|output| {
            serde_json::from_str(&output.trim())
                .map_err(|e| format!("Failed to parse JSON: {} | Output: {}", e, output))
        })
}

#[tauri::command]
pub fn get_trends(device_serial: String, metric: String, days: u32) -> Result<serde_json::Value, String> {
    python::run_python_module(
        "history",
        "get_trends",
        vec![device_serial, metric, days.to_string()],
    )
    .and_then(|output| {
        serde_json::from_str(&output.trim())
            .map_err(|e| format!("Failed to parse JSON: {} | Output: {}", e, output))
    })
}

#[tauri::command]
pub fn verify_evidence() -> Result<serde_json::Value, String> {
    python::run_python_module("evidence", "verify_chain", vec![])
        .and_then(|output| {
            serde_json::from_str(&output.trim())
                .map_err(|e| format!("Failed to parse JSON: {} | Output: {}", e, output))
        })
}

#[tauri::command]
pub fn add_evidence(event_type: String, description: String, data: serde_json::Value) -> Result<serde_json::Value, String> {
    let data_str = serde_json::to_string(&data)
        .map_err(|e| format!("Failed to serialize data: {}", e))?;
    
    python::run_python_module(
        "evidence",
        "add_evidence",
        vec![event_type, description, data_str],
    )
    .and_then(|output| {
        serde_json::from_str(&output.trim())
            .map_err(|e| format!("Failed to parse JSON: {} | Output: {}", e, output))
    })
}

#[tauri::command]
pub fn export_html(summary: serde_json::Value, output_file: String) -> Result<bool, String> {
    let summary_str = serde_json::to_string(&summary)
        .map_err(|e| format!("Failed to serialize: {}", e))?;
    
    python::run_python_module(
        "export",
        "export_html",
        vec![summary_str, output_file],
    )
    .map(|_| true)
}

#[tauri::command]
pub fn export_csv(summary: serde_json::Value, output_file: String) -> Result<bool, String> {
    let summary_str = serde_json::to_string(&summary)
        .map_err(|e| format!("Failed to serialize: {}", e))?;
    
    python::run_python_module(
        "export",
        "export_csv",
        vec![summary_str, output_file],
    )
    .map(|_| true)
}

#[tauri::command]
pub fn start_monitor(interval: f64) -> Result<bool, String> {
    python::run_python_module(
        "monitor",
        "start_monitor",
        vec![interval.to_string()],
    )
    .map(|_| true)
}

#[tauri::command]
pub fn stop_monitor() -> Result<bool, String> {
    python::run_python_module("monitor", "stop_monitor", vec![])
        .map(|_| true)
}

#[tauri::command]
pub fn get_recommendations() -> Result<serde_json::Value, String> {
    python::run_python_module("optimize", "generate_recommendations", vec![])
        .and_then(|output| {
            serde_json::from_str(&output.trim())
                .map_err(|e| format!("Failed to parse JSON: {} | Output: {}", e, output))
        })
}

#[tauri::command]
pub fn predict_failure(device_serial: String, days: u32) -> Result<serde_json::Value, String> {
    python::run_python_module(
        "ai_engine",
        "predict_failure",
        vec![device_serial, days.to_string()],
    )
    .and_then(|output| {
        serde_json::from_str(&output.trim())
            .map_err(|e| format!("Failed to parse JSON: {} | Output: {}", e, output))
    })
}

#[tauri::command]
pub fn detect_anomalies(device_serial: String) -> Result<serde_json::Value, String> {
    python::run_python_module("ai_engine", "detect_anomalies", vec![device_serial])
        .and_then(|output| {
            serde_json::from_str(&output.trim())
                .map_err(|e| format!("Failed to parse JSON: {} | Output: {}", e, output))
        })
}

#[tauri::command]
pub fn fleet_dashboard() -> Result<serde_json::Value, String> {
    python::run_python_module("fleet", "fleet_dashboard", vec![])
        .and_then(|output| {
            serde_json::from_str(&output.trim())
                .map_err(|e| format!("Failed to parse JSON: {} | Output: {}", e, output))
        })
}

#[tauri::command]
pub fn forensics_scan() -> Result<serde_json::Value, String> {
    python::run_python_module("forensics", "full_forensics_scan", vec![])
        .and_then(|output| {
            serde_json::from_str(&output.trim())
                .map_err(|e| format!("Failed to parse JSON: {} | Output: {}", e, output))
        })
}
