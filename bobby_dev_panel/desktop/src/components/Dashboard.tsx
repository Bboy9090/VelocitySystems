import { useState, useEffect } from "react";
import { invoke } from "@tauri-apps/api/tauri";
import { Battery, Shield, Activity, AlertTriangle, TrendingUp } from "lucide-react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from "recharts";
import "./Dashboard.css";

interface Device {
  platform: string;
  serial: string;
  model: string;
  status: string;
}

interface DashboardProps {
  device: Device | null;
  isConnected: boolean;
}

interface BenchSummary {
  device?: {
    model?: string;
    platform?: string;
  };
  battery_health?: {
    percent_estimate?: number;
    condition?: string;
  };
  health_score?: {
    overall?: number;
    battery?: number;
    security?: number;
    performance?: number;
    sensors?: number;
  };
  performance?: {
    io_grade?: string;
    avg_mbps?: number;
  };
  sensors?: {
    health_status?: string;
    dead_count?: number;
  };
}

export default function Dashboard({ device, isConnected }: DashboardProps) {
  const [summary, setSummary] = useState<BenchSummary | null>(null);
  const [loading, setLoading] = useState(false);
  const [trends, setTrends] = useState<any[]>([]);

  useEffect(() => {
    if (device && isConnected) {
      loadSummary();
      loadTrends();
    }
  }, [device, isConnected]);

  const loadSummary = async () => {
    if (!device) return;
    
    setLoading(true);
    try {
      const result = await invoke<BenchSummary>("generate_bench_summary", {
        deviceSerial: device.serial,
      });
      setSummary(result);
    } catch (error) {
      console.error("Error loading summary:", error);
    } finally {
      setLoading(false);
    }
  };

  const loadTrends = async () => {
    if (!device) return;
    
    try {
      const result = await invoke<any[]>("get_trends", {
        deviceSerial: device.serial,
        metric: "health_score_overall",
        days: 30,
      });
      setTrends(result || []);
    } catch (error) {
      console.error("Error loading trends:", error);
    }
  };

  if (!device) {
    return (
      <div className="dashboard-empty">
        <p>Select a device to view dashboard</p>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner" />
        <p>Loading device data...</p>
      </div>
    );
  }

  const healthScore = summary?.health_score?.overall || 0;
  const batteryHealth = summary?.battery_health?.percent_estimate || 0;
  const performanceGrade = summary?.performance?.io_grade || "N/A";

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Device Dashboard</h1>
        <div className="device-badge">
          <span>{device.model}</span>
          <span className="platform-badge">{device.platform.toUpperCase()}</span>
        </div>
      </div>

      {/* Health Score Card */}
      <div className="health-score-card">
        <div className="health-score-main">
          <div className="health-score-value">{healthScore}</div>
          <div className="health-score-label">Overall Health Score</div>
        </div>
        <div className="health-score-breakdown">
          <div className="score-item">
            <Battery size={20} />
            <span>Battery: {summary?.health_score?.battery || 0}</span>
          </div>
          <div className="score-item">
            <Shield size={20} />
            <span>Security: {summary?.health_score?.security || 0}</span>
          </div>
          <div className="score-item">
            <Activity size={20} />
            <span>Performance: {summary?.health_score?.performance || 0}</span>
          </div>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-header">
            <Battery className="metric-icon" />
            <span>Battery Health</span>
          </div>
          <div className="metric-value-large">{batteryHealth}%</div>
          <div className="metric-subvalue">
            {summary?.battery_health?.condition || "Unknown"}
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-header">
            <Activity className="metric-icon" />
            <span>Performance</span>
          </div>
          <div className="metric-value-large">{performanceGrade}</div>
          <div className="metric-subvalue">
            {summary?.performance?.avg_mbps 
              ? `${summary.performance.avg_mbps} MB/s` 
              : "N/A"}
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-header">
            <Shield className="metric-icon" />
            <span>Security</span>
          </div>
          <div className="metric-value-large">
            {summary?.health_score?.security || 0}
          </div>
          <div className="metric-subvalue">Score</div>
        </div>

        <div className="metric-card">
          <div className="metric-header">
            <AlertTriangle className="metric-icon" />
            <span>Sensors</span>
          </div>
          <div className="metric-value-large">
            {summary?.sensors?.health_status || "Unknown"}
          </div>
          <div className="metric-subvalue">
            {summary?.sensors?.dead_count || 0} dead
          </div>
        </div>
      </div>

      {/* Trends Chart */}
      {trends.length > 0 && (
        <div className="card">
          <div className="card-header">
            <TrendingUp className="card-icon" />
            <span className="card-title">Health Score Trend (30 days)</span>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={trends}>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" />
              <XAxis 
                dataKey="timestamp" 
                stroke="#888"
                tick={{ fill: "#888" }}
              />
              <YAxis 
                stroke="#888"
                tick={{ fill: "#888" }}
                domain={[0, 100]}
              />
              <Tooltip 
                contentStyle={{
                  background: "#1a1a1a",
                  border: "1px solid #333",
                  borderRadius: "6px",
                }}
              />
              <Line 
                type="monotone" 
                dataKey="value" 
                stroke="#00ff88" 
                strokeWidth={2}
                dot={{ fill: "#00ff88", r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Recommendations */}
      <div className="card">
        <div className="card-header">
          <AlertTriangle className="card-icon" />
          <span className="card-title">Recommendations</span>
        </div>
        <div className="recommendations-list">
          {healthScore < 70 && (
            <div className="recommendation-item warning">
              <AlertTriangle size={16} />
              <span>Overall health score is below optimal. Review device status.</span>
            </div>
          )}
          {batteryHealth < 70 && (
            <div className="recommendation-item warning">
              <Battery size={16} />
              <span>Battery health is degrading. Consider battery replacement.</span>
            </div>
          )}
          {performanceGrade === "DEGRADED" && (
            <div className="recommendation-item error">
              <Activity size={16} />
              <span>Storage performance is degraded. Check storage health.</span>
            </div>
          )}
          {(!summary || healthScore >= 80) && (
            <div className="recommendation-item success">
              <span>Device is in good condition. Continue regular monitoring.</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
