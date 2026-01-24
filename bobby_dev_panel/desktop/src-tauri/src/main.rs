// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod commands;
mod python;

use tauri::Manager;

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            commands::check_device,
            commands::get_devices,
            commands::get_platform,
            commands::collect_dossier,
            commands::generate_bench_summary,
            commands::run_intake,
            commands::get_history,
            commands::save_snapshot,
            commands::get_trends,
            commands::verify_evidence,
            commands::add_evidence,
            commands::export_html,
            commands::export_csv,
            commands::start_monitor,
            commands::stop_monitor,
            commands::get_recommendations,
            commands::predict_failure,
            commands::detect_anomalies,
            commands::fleet_dashboard,
            commands::forensics_scan,
        ])
        .setup(|app| {
            // Initialize Python runtime check
            python::check_python_available();
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
