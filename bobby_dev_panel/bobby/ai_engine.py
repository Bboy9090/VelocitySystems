"""
AI/ML Engine - Predictive analytics, anomaly detection, automated diagnosis.
Revolutionary feature: Beyond world-class intelligence.
"""

import json
import statistics
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from .core import log
from .history import DeviceHistory
from .report import generate_bench_summary


class AIEngine:
    """AI-powered predictive analytics and anomaly detection."""
    
    def __init__(self, history: Optional[DeviceHistory] = None):
        """
        Initialize AI engine.
        
        Args:
            history: DeviceHistory instance for trend analysis
        """
        self.history = history or DeviceHistory()
    
    def predict_failure(self, device_serial: str, days_ahead: int = 30) -> Dict[str, Any]:
        """
        Predict device failure probability based on historical trends.
        
        Args:
            device_serial: Device serial number
            days_ahead: Days to predict ahead
            
        Returns:
            Prediction dictionary with failure probability and factors
        """
        trends = self.history.get_trends(device_serial, "health_score_overall", days=90)
        
        if len(trends) < 3:
            return {
                "prediction": "INSUFFICIENT_DATA",
                "message": "Need at least 3 data points for prediction",
                "confidence": 0
            }
        
        # Extract values
        values = [t["value"] for t in trends if t["value"] is not None]
        
        if not values:
            return {
                "prediction": "NO_DATA",
                "message": "No historical data available",
                "confidence": 0
            }
        
        # Calculate trend
        recent = values[-7:] if len(values) >= 7 else values
        older = values[:-7] if len(values) > 7 else []
        
        recent_avg = statistics.mean(recent) if recent else 0
        older_avg = statistics.mean(older) if older else recent_avg
        
        # Trend analysis
        decline_rate = older_avg - recent_avg
        decline_percent = (decline_rate / older_avg * 100) if older_avg > 0 else 0
        
        # Predict future value
        predicted_value = recent_avg - (decline_rate * (days_ahead / 30))
        predicted_value = max(0, min(100, predicted_value))
        
        # Calculate failure probability
        if predicted_value < 40:
            failure_prob = 0.8
            risk = "CRITICAL"
        elif predicted_value < 60:
            failure_prob = 0.5
            risk = "HIGH"
        elif predicted_value < 75:
            failure_prob = 0.3
            risk = "MODERATE"
        else:
            failure_prob = 0.1
            risk = "LOW"
        
        # Confidence based on data points
        confidence = min(0.95, 0.5 + (len(values) * 0.05))
        
        return {
            "prediction": "FAILURE_RISK",
            "risk_level": risk,
            "failure_probability": round(failure_prob, 2),
            "predicted_health_score": round(predicted_value, 1),
            "current_health_score": round(recent_avg, 1),
            "decline_rate": round(decline_rate, 2),
            "decline_percent": round(decline_percent, 1),
            "days_ahead": days_ahead,
            "confidence": round(confidence, 2),
            "data_points": len(values),
            "recommendation": self._get_failure_recommendation(risk, predicted_value)
        }
    
    def _get_failure_recommendation(self, risk: str, predicted_score: float) -> str:
        """Get recommendation based on risk level."""
        if risk == "CRITICAL":
            return "Immediate action required. Device likely to fail within 30 days. Backup data and prepare for replacement."
        elif risk == "HIGH":
            return "High risk of failure. Monitor closely, optimize device, consider preventive maintenance."
        elif risk == "MODERATE":
            return "Moderate risk. Continue monitoring, address performance issues proactively."
        else:
            return "Low risk. Device appears stable. Continue regular monitoring."
    
    def detect_anomalies(self, device_serial: str) -> List[Dict[str, Any]]:
        """
        Detect anomalies in device behavior.
        
        Args:
            device_serial: Device serial number
            
        Returns:
            List of detected anomalies
        """
        anomalies = []
        trends = self.history.get_trends(device_serial, "health_score_overall", days=30)
        
        if len(trends) < 5:
            return [{
                "type": "INSUFFICIENT_DATA",
                "severity": "INFO",
                "message": "Need more data points for anomaly detection"
            }]
        
        values = [t["value"] for t in trends if t["value"] is not None]
        
        if not values:
            return []
        
        # Statistical analysis
        mean = statistics.mean(values)
        stdev = statistics.stdev(values) if len(values) > 1 else 0
        
        # Detect sudden drops
        for i in range(1, len(values)):
            change = values[i-1] - values[i]
            if change > (mean * 0.2):  # 20% drop
                anomalies.append({
                    "type": "SUDDEN_DROP",
                    "severity": "HIGH",
                    "timestamp": trends[i]["timestamp"],
                    "value_before": values[i-1],
                    "value_after": values[i],
                    "drop_percent": round((change / values[i-1]) * 100, 1),
                    "message": f"Sudden health score drop of {round(change, 1)} points"
                })
        
        # Detect outliers (3 sigma rule)
        for i, value in enumerate(values):
            if stdev > 0:
                z_score = abs((value - mean) / stdev)
                if z_score > 3:
                    anomalies.append({
                        "type": "OUTLIER",
                        "severity": "MEDIUM",
                        "timestamp": trends[i]["timestamp"],
                        "value": value,
                        "z_score": round(z_score, 2),
                        "message": f"Unusual health score value: {value} (expected: {round(mean, 1)} ± {round(stdev, 1)})"
                    })
        
        # Detect rapid decline
        if len(values) >= 7:
            recent_avg = statistics.mean(values[-7:])
            older_avg = statistics.mean(values[:-7]) if len(values) > 7 else recent_avg
            decline = older_avg - recent_avg
            
            if decline > 15:  # 15 point decline
                anomalies.append({
                    "type": "RAPID_DECLINE",
                    "severity": "HIGH",
                    "decline_points": round(decline, 1),
                    "period_days": 7,
                    "message": f"Rapid health decline: {round(decline, 1)} points in 7 days"
                })
        
        return anomalies
    
    def diagnose_issues(self) -> Dict[str, Any]:
        """
        Automated diagnosis based on current device state.
        
        Returns:
            Diagnosis dictionary with identified issues and root causes
        """
        summary = generate_bench_summary()
        issues = []
        root_causes = []
        
        # Battery analysis
        battery_health = summary.get("battery_health", {})
        battery_percent = battery_health.get("percent_estimate")
        
        if battery_percent and battery_percent < 70:
            issues.append({
                "category": "battery",
                "severity": "HIGH",
                "symptom": f"Battery health at {battery_percent}%",
                "root_cause": "Battery degradation",
                "confidence": 0.9
            })
            root_causes.append("Battery degradation likely due to age and usage patterns")
        
        # Performance analysis
        performance = summary.get("performance", {})
        io_grade = performance.get("io_grade")
        
        if io_grade == "DEGRADED":
            issues.append({
                "category": "storage",
                "severity": "HIGH",
                "symptom": "Storage I/O performance degraded",
                "root_cause": "Storage wear or fragmentation",
                "confidence": 0.85
            })
            root_causes.append("Storage performance degradation indicates hardware wear or software issues")
        
        # Security analysis
        security = summary.get("security", {})
        verified_boot = security.get("verified_boot_state", "").lower()
        
        if verified_boot != "green":
            issues.append({
                "category": "security",
                "severity": "CRITICAL",
                "symptom": f"Verified boot state: {verified_boot}",
                "root_cause": "Boot integrity compromised",
                "confidence": 0.95
            })
            root_causes.append("Boot integrity issue - device may be compromised")
        
        # Sensor analysis
        sensors = summary.get("sensors", {})
        dead_count = sensors.get("dead_count", 0)
        
        if dead_count > 3:
            issues.append({
                "category": "hardware",
                "severity": "MEDIUM",
                "symptom": f"{dead_count} dead sensors",
                "root_cause": "Hardware failure or driver issues",
                "confidence": 0.7
            })
            root_causes.append("Multiple sensor failures suggest hardware or driver problems")
        
        # Overall diagnosis
        health_score = summary.get("health_score", {}).get("overall", 100)
        
        diagnosis = {
            "timestamp": datetime.now().isoformat(),
            "overall_health": health_score,
            "issues_found": len(issues),
            "issues": issues,
            "root_causes": root_causes,
            "diagnosis_confidence": round(statistics.mean([i["confidence"] for i in issues]) if issues else 0, 2),
            "recommended_actions": self._get_diagnosis_actions(issues)
        }
        
        return diagnosis
    
    def _get_diagnosis_actions(self, issues: List[Dict[str, Any]]) -> List[str]:
        """Get recommended actions based on diagnosed issues."""
        actions = []
        
        for issue in issues:
            if issue["category"] == "battery":
                actions.append("Replace battery or optimize charging habits")
            elif issue["category"] == "storage":
                actions.append("Run storage optimization or consider replacement")
            elif issue["category"] == "security":
                actions.append("Investigate boot integrity, consider reflashing firmware")
            elif issue["category"] == "hardware":
                actions.append("Hardware inspection and potential repair")
        
        return list(set(actions))  # Remove duplicates
    
    def generate_insights(self, device_serial: str) -> Dict[str, Any]:
        """
        Generate AI-powered insights about device.
        
        Args:
            device_serial: Device serial number
            
        Returns:
            Insights dictionary
        """
        summary = generate_bench_summary()
        prediction = self.predict_failure(device_serial)
        anomalies = self.detect_anomalies(device_serial)
        diagnosis = self.diagnose_issues()
        
        insights = {
            "timestamp": datetime.now().isoformat(),
            "device_serial": device_serial,
            "current_state": {
                "health_score": summary.get("health_score", {}).get("overall"),
                "battery_health": summary.get("battery_health", {}).get("percent_estimate"),
                "performance_grade": summary.get("performance", {}).get("io_grade")
            },
            "predictions": prediction,
            "anomalies": anomalies,
            "diagnosis": diagnosis,
            "key_insights": self._generate_key_insights(prediction, anomalies, diagnosis)
        }
        
        return insights
    
    def _generate_key_insights(self, prediction: Dict, anomalies: List, diagnosis: Dict) -> List[str]:
        """Generate key insights summary."""
        insights = []
        
        if prediction.get("risk_level") in ["CRITICAL", "HIGH"]:
            insights.append(f"⚠️ High failure risk detected: {prediction.get('failure_probability', 0)*100}% probability")
        
        if anomalies:
            critical_anomalies = [a for a in anomalies if a.get("severity") == "HIGH"]
            if critical_anomalies:
                insights.append(f"🚨 {len(critical_anomalies)} critical anomalies detected")
        
        if diagnosis.get("issues_found", 0) > 0:
            insights.append(f"🔍 {diagnosis.get('issues_found')} issues diagnosed with {diagnosis.get('diagnosis_confidence', 0)*100}% confidence")
        
        return insights


def ai_menu():
    """Interactive menu for AI engine."""
    ai = AIEngine()
    
    while True:
        print("\n=== AI Engine - Predictive Analytics ===")
        print("1. Predict Failure Risk (30 days)")
        print("2. Detect Anomalies")
        print("3. Automated Diagnosis")
        print("4. Generate Complete Insights")
        print("0. Back")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            from .core import get_serial
            serial = get_serial() or input("Device serial: ").strip()
            if serial:
                prediction = ai.predict_failure(serial)
                print(f"\nPrediction: {json.dumps(prediction, indent=2)}")
        elif choice == "2":
            from .core import get_serial
            serial = get_serial() or input("Device serial: ").strip()
            if serial:
                anomalies = ai.detect_anomalies(serial)
                print(f"\nAnomalies: {json.dumps(anomalies, indent=2)}")
        elif choice == "3":
            diagnosis = ai.diagnose_issues()
            print(f"\nDiagnosis: {json.dumps(diagnosis, indent=2)}")
        elif choice == "4":
            from .core import get_serial
            serial = get_serial() or input("Device serial: ").strip()
            if serial:
                insights = ai.generate_insights(serial)
                print(f"\nInsights: {json.dumps(insights, indent=2)}")
        elif choice == "0":
            break
        else:
            print("Invalid choice")
