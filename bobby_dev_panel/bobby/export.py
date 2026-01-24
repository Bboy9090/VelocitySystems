"""
Export System - HTML reports, CSV exports, visualizations.
Aligned with Forge Doctrine: Transparency Over Convenience
"""

import json
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from .core import log
from .report import generate_bench_summary


def export_html(summary: Dict[str, Any], output_file: str):
    """
    Export bench summary as HTML report with visualizations.
    
    Args:
        summary: Bench summary dictionary
        output_file: Output HTML file path
    """
    health_score = summary.get("health_score", {})
    battery_health = summary.get("battery_health", {})
    performance = summary.get("performance", {})
    sensors = summary.get("sensors", {})
    device = summary.get("device", {})
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Device Bench Summary - {device.get('model', 'Unknown')}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #0a0a0a;
            color: #e0e0e0;
            padding: 20px;
            line-height: 1.6;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ color: #00ff88; margin-bottom: 10px; }}
        h2 {{ color: #00ccff; margin-top: 30px; margin-bottom: 15px; }}
        .header {{ background: #1a1a1a; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
        .card {{
            background: #1a1a1a;
            border: 1px solid #333;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }}
        .metric {{
            display: inline-block;
            margin: 10px 15px 10px 0;
            padding: 15px;
            background: #252525;
            border-radius: 6px;
            min-width: 150px;
        }}
        .metric-label {{ color: #888; font-size: 0.9em; }}
        .metric-value {{ color: #00ff88; font-size: 1.8em; font-weight: bold; }}
        .score-bar {{
            width: 100%;
            height: 30px;
            background: #252525;
            border-radius: 15px;
            overflow: hidden;
            margin: 10px 0;
        }}
        .score-fill {{
            height: 100%;
            background: linear-gradient(90deg, #00ff88, #00ccff);
            transition: width 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #000;
            font-weight: bold;
        }}
        .health-excellent {{ background: linear-gradient(90deg, #00ff88, #00cc88); }}
        .health-good {{ background: linear-gradient(90deg, #88ff00, #00ff88); }}
        .health-fair {{ background: linear-gradient(90deg, #ffaa00, #88ff00); }}
        .health-weak {{ background: linear-gradient(90deg, #ff6600, #ffaa00); }}
        .health-poor {{ background: linear-gradient(90deg, #ff0000, #ff6600); }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #333;
        }}
        th {{ color: #00ccff; background: #252525; }}
        .timestamp {{ color: #888; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔧 Device Bench Summary</h1>
            <div class="timestamp">Generated: {summary.get('timestamp', 'Unknown')}</div>
        </div>
        
        <div class="card">
            <h2>Device Information</h2>
            <div class="metric">
                <div class="metric-label">Model</div>
                <div class="metric-value">{device.get('model', 'Unknown')}</div>
            </div>
            <div class="metric">
                <div class="metric-label">Manufacturer</div>
                <div class="metric-value">{device.get('manufacturer', 'Unknown')}</div>
            </div>
            <div class="metric">
                <div class="metric-label">Android Version</div>
                <div class="metric-value">{device.get('android_version', 'Unknown')}</div>
            </div>
        </div>
        
        <div class="card">
            <h2>Overall Health Score</h2>
            <div class="score-bar">
                <div class="score-fill health-{'excellent' if health_score.get('overall', 0) >= 90 else 'good' if health_score.get('overall', 0) >= 80 else 'fair' if health_score.get('overall', 0) >= 70 else 'weak' if health_score.get('overall', 0) >= 60 else 'poor'}" 
                     style="width: {health_score.get('overall', 0)}%">
                    {health_score.get('overall', 0)}/100
                </div>
            </div>
            <table>
                <tr><th>Category</th><th>Score</th></tr>
                <tr><td>Battery</td><td>{health_score.get('battery', 0)}/100</td></tr>
                <tr><td>Security</td><td>{health_score.get('security', 0)}/100</td></tr>
                <tr><td>Performance</td><td>{health_score.get('performance', 0)}/100</td></tr>
                <tr><td>Sensors</td><td>{health_score.get('sensors', 0)}/100</td></tr>
            </table>
        </div>
        
        <div class="card">
            <h2>Battery Health</h2>
            <div class="metric">
                <div class="metric-label">Health</div>
                <div class="metric-value">{battery_health.get('percent_estimate', 'N/A')}%</div>
            </div>
            <div class="metric">
                <div class="metric-label">Condition</div>
                <div class="metric-value">{battery_health.get('condition', 'Unknown')}</div>
            </div>
            {f'<div class="metric"><div class="metric-label">Cycles</div><div class="metric-value">{battery_health.get("cycle_count", "N/A")}</div></div>' if battery_health.get('cycle_count') else ''}
        </div>
        
        <div class="card">
            <h2>Performance</h2>
            <div class="metric">
                <div class="metric-label">I/O Grade</div>
                <div class="metric-value">{performance.get('io_grade', 'Unknown')}</div>
            </div>
            <div class="metric">
                <div class="metric-label">Avg Speed</div>
                <div class="metric-value">{performance.get('avg_mbps', 'N/A')} MB/s</div>
            </div>
        </div>
        
        <div class="card">
            <h2>Sensors</h2>
            <div class="metric">
                <div class="metric-label">Health Status</div>
                <div class="metric-value">{sensors.get('health_status', 'Unknown')}</div>
            </div>
            <div class="metric">
                <div class="metric-label">Dead Sensors</div>
                <div class="metric-value">{sensors.get('dead_count', 0)}/{sensors.get('total_count', 0)}</div>
            </div>
        </div>
        
        <div class="card">
            <h2>Raw Data</h2>
            <pre style="background: #0a0a0a; padding: 15px; border-radius: 6px; overflow-x: auto;">{json.dumps(summary, indent=2)}</pre>
        </div>
    </div>
</body>
</html>"""
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    
    log(f"HTML report exported: {output_file}")


def export_csv(summary: Dict[str, Any], output_file: str):
    """
    Export bench summary as CSV.
    
    Args:
        summary: Bench summary dictionary
        output_file: Output CSV file path
    """
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        
        # Header
        writer.writerow(["Metric", "Value"])
        
        # Device info
        device = summary.get("device", {})
        writer.writerow(["Device Model", device.get("model", "")])
        writer.writerow(["Manufacturer", device.get("manufacturer", "")])
        writer.writerow(["Serial", device.get("serial", "")])
        writer.writerow(["Android Version", device.get("android_version", "")])
        
        writer.writerow([])  # Empty row
        
        # Health scores
        health_score = summary.get("health_score", {})
        writer.writerow(["Overall Health Score", health_score.get("overall", "")])
        writer.writerow(["Battery Score", health_score.get("battery", "")])
        writer.writerow(["Security Score", health_score.get("security", "")])
        writer.writerow(["Performance Score", health_score.get("performance", "")])
        writer.writerow(["Sensors Score", health_score.get("sensors", "")])
        
        writer.writerow([])  # Empty row
        
        # Battery health
        battery_health = summary.get("battery_health", {})
        writer.writerow(["Battery Health %", battery_health.get("percent_estimate", "")])
        writer.writerow(["Battery Condition", battery_health.get("condition", "")])
        writer.writerow(["Battery Cycles", battery_health.get("cycle_count", "")])
        
        writer.writerow([])  # Empty row
        
        # Performance
        performance = summary.get("performance", {})
        writer.writerow(["I/O Grade", performance.get("io_grade", "")])
        writer.writerow(["Avg MB/s", performance.get("avg_mbps", "")])
        
        writer.writerow([])  # Empty row
        
        # Sensors
        sensors = summary.get("sensors", {})
        writer.writerow(["Sensor Health", sensors.get("health_status", "")])
        writer.writerow(["Dead Sensors", sensors.get("dead_count", "")])
        writer.writerow(["Total Sensors", sensors.get("total_count", "")])
    
    log(f"CSV exported: {output_file}")


def export_menu():
    """Interactive menu for export tools."""
    while True:
        print("\n=== Export ===")
        print("1. Export HTML Report")
        print("2. Export CSV")
        print("3. Export JSON")
        print("0. Back")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            summary = generate_bench_summary()
            output_file = input("Output file (default: report.html): ").strip() or "report.html"
            export_html(summary, output_file)
            print(f"\nHTML report exported: {output_file}")
        elif choice == "2":
            summary = generate_bench_summary()
            output_file = input("Output file (default: report.csv): ").strip() or "report.csv"
            export_csv(summary, output_file)
            print(f"\nCSV exported: {output_file}")
        elif choice == "3":
            summary = generate_bench_summary()
            output_file = input("Output file (default: report.json): ").strip() or "report.json"
            with open(output_file, "w") as f:
                json.dump(summary, f, indent=2)
            print(f"\nJSON exported: {output_file}")
        elif choice == "0":
            break
        else:
            print("Invalid choice")
