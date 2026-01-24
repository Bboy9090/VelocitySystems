"""
Historical Data Tracking - Store and compare device health over time.
Aligned with Forge Doctrine: Evidence Over Assumption
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from .core import log
from .report import generate_bench_summary


class DeviceHistory:
    """Manages historical device data in SQLite database."""
    
    def __init__(self, db_path: str = "bobby_history.db"):
        """
        Initialize history database.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Device snapshots table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                device_serial TEXT,
                device_model TEXT,
                snapshot_data TEXT NOT NULL,
                health_score_overall INTEGER,
                battery_health_percent INTEGER,
                performance_io_grade TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create indexes
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_serial_timestamp 
            ON snapshots(device_serial, timestamp)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_timestamp 
            ON snapshots(timestamp)
        """)
        
        conn.commit()
        conn.close()
        log(f"History database initialized: {self.db_path}")
    
    def save_snapshot(self, device_serial: Optional[str] = None, 
                     device_model: Optional[str] = None) -> int:
        """
        Save current device snapshot.
        
        Args:
            device_serial: Device serial number
            device_model: Device model
            
        Returns:
            Snapshot ID
        """
        summary = generate_bench_summary()
        timestamp = summary.get("timestamp", datetime.now().isoformat())
        
        # Extract key metrics
        health_score = summary.get("health_score", {}).get("overall")
        battery_health = summary.get("battery_health", {}).get("percent_estimate")
        io_grade = summary.get("performance", {}).get("io_grade")
        
        # Get device info if not provided
        if not device_serial:
            device_serial = summary.get("device", {}).get("serial")
        if not device_model:
            device_model = summary.get("device", {}).get("model")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO snapshots 
            (timestamp, device_serial, device_model, snapshot_data, 
             health_score_overall, battery_health_percent, performance_io_grade)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            timestamp,
            device_serial,
            device_model,
            json.dumps(summary),
            health_score,
            battery_health,
            io_grade
        ))
        
        snapshot_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        log(f"Snapshot saved: ID {snapshot_id} at {timestamp}")
        return snapshot_id
    
    def get_snapshots(self, device_serial: Optional[str] = None,
                     limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get historical snapshots.
        
        Args:
            device_serial: Filter by device serial (optional)
            limit: Maximum number of snapshots to return
            
        Returns:
            List of snapshot dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if device_serial:
            cursor.execute("""
                SELECT * FROM snapshots 
                WHERE device_serial = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (device_serial, limit))
        else:
            cursor.execute("""
                SELECT * FROM snapshots 
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        snapshots = []
        for row in rows:
            snapshot = {
                "id": row["id"],
                "timestamp": row["timestamp"],
                "device_serial": row["device_serial"],
                "device_model": row["device_model"],
                "health_score_overall": row["health_score_overall"],
                "battery_health_percent": row["battery_health_percent"],
                "performance_io_grade": row["performance_io_grade"],
                "snapshot_data": json.loads(row["snapshot_data"])
            }
            snapshots.append(snapshot)
        
        return snapshots
    
    def get_trends(self, device_serial: str, metric: str = "health_score_overall",
                   days: int = 30) -> List[Dict[str, Any]]:
        """
        Get trend data for a specific metric.
        
        Args:
            device_serial: Device serial number
            metric: Metric to track (health_score_overall, battery_health_percent, etc.)
            days: Number of days to look back
            
        Returns:
            List of timestamp/value pairs
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(f"""
            SELECT timestamp, {metric} 
            FROM snapshots 
            WHERE device_serial = ? 
            AND timestamp >= datetime('now', '-{days} days')
            ORDER BY timestamp ASC
        """, (device_serial,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [{"timestamp": row[0], "value": row[1]} for row in rows]
    
    def compare_snapshots(self, snapshot_id1: int, snapshot_id2: int) -> Dict[str, Any]:
        """
        Compare two snapshots.
        
        Args:
            snapshot_id1: First snapshot ID
            snapshot_id2: Second snapshot ID
            
        Returns:
            Comparison dictionary with differences
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT snapshot_data FROM snapshots WHERE id = ?", (snapshot_id1,))
        row1 = cursor.fetchone()
        
        cursor.execute("SELECT snapshot_data FROM snapshots WHERE id = ?", (snapshot_id2,))
        row2 = cursor.fetchone()
        
        conn.close()
        
        if not row1 or not row2:
            return {"error": "One or both snapshots not found"}
        
        snap1 = json.loads(row1[0])
        snap2 = json.loads(row2[0])
        
        comparison = {
            "snapshot1_id": snapshot_id1,
            "snapshot2_id": snapshot_id2,
            "timestamp1": snap1.get("timestamp"),
            "timestamp2": snap2.get("timestamp"),
            "differences": {}
        }
        
        # Compare key metrics
        metrics = [
            ("health_score", "overall"),
            ("battery_health", "percent_estimate"),
            ("performance", "avg_mbps"),
        ]
        
        for section, key in metrics:
            val1 = snap1.get(section, {}).get(key)
            val2 = snap2.get(section, {}).get(key)
            
            if val1 is not None and val2 is not None:
                diff = val2 - val1
                comparison["differences"][f"{section}.{key}"] = {
                    "before": val1,
                    "after": val2,
                    "change": diff,
                    "percent_change": (diff / val1 * 100) if val1 != 0 else 0
                }
        
        return comparison


def history_menu():
    """Interactive menu for history tools."""
    history = DeviceHistory()
    
    while True:
        print("\n=== Device History ===")
        print("1. Save Current Snapshot")
        print("2. View Recent Snapshots")
        print("3. Get Trends (Health Score)")
        print("4. Get Trends (Battery Health)")
        print("5. Compare Snapshots")
        print("0. Back")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            snapshot_id = history.save_snapshot()
            print(f"\nSnapshot saved: ID {snapshot_id}")
        elif choice == "2":
            serial = input("Device serial (optional, press Enter for all): ").strip() or None
            snapshots = history.get_snapshots(device_serial=serial, limit=10)
            print(f"\nFound {len(snapshots)} snapshots:")
            for snap in snapshots:
                print(f"  ID {snap['id']}: {snap['timestamp']} - Health: {snap['health_score_overall']}")
        elif choice == "3":
            serial = input("Device serial: ").strip()
            trends = history.get_trends(serial, "health_score_overall", 30)
            print(f"\nHealth Score Trends (last 30 days):")
            for trend in trends:
                print(f"  {trend['timestamp']}: {trend['value']}")
        elif choice == "4":
            serial = input("Device serial: ").strip()
            trends = history.get_trends(serial, "battery_health_percent", 30)
            print(f"\nBattery Health Trends (last 30 days):")
            for trend in trends:
                print(f"  {trend['timestamp']}: {trend['value']}%")
        elif choice == "5":
            id1 = int(input("First snapshot ID: ").strip())
            id2 = int(input("Second snapshot ID: ").strip())
            comparison = history.compare_snapshots(id1, id2)
            print(f"\nComparison: {comparison}")
        elif choice == "0":
            break
        else:
            print("Invalid choice")
