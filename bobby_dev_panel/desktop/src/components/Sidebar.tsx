import { Home, Smartphone, Activity, FileText, History, Shield, Settings, Zap } from "lucide-react";
import "./Sidebar.css";

interface SidebarProps {
  currentView: string;
  onViewChange: (view: string) => void;
  isConnected: boolean;
}

export default function Sidebar({ currentView, onViewChange, isConnected }: SidebarProps) {
  const menuItems = [
    { id: "dashboard", label: "Dashboard", icon: Home },
    { id: "devices", label: "Devices", icon: Smartphone },
    { id: "intake", label: "Intake", icon: FileText },
    { id: "history", label: "History", icon: History },
    { id: "monitor", label: "Monitor", icon: Activity },
    { id: "forensics", label: "Forensics", icon: Shield },
    { id: "ai", label: "AI Analytics", icon: Zap },
    { id: "settings", label: "Settings", icon: Settings },
  ];

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <div className="logo">
          <Zap className="logo-icon" />
          <span className="logo-text">Bobby Dev Panel</span>
        </div>
        <div className="subtitle">Pandora Codex</div>
      </div>

      <div className="connection-status">
        <div className={`status-dot ${isConnected ? "connected" : "disconnected"}`} />
        <span>{isConnected ? "Device Connected" : "No Device"}</span>
      </div>

      <nav className="sidebar-nav">
        {menuItems.map((item) => {
          const Icon = item.icon;
          return (
            <button
              key={item.id}
              className={`nav-item ${currentView === item.id ? "active" : ""}`}
              onClick={() => onViewChange(item.id)}
              disabled={!isConnected && item.id !== "devices" && item.id !== "settings"}
            >
              <Icon className="nav-icon" />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>

      <div className="sidebar-footer">
        <div className="version">v1.0.0</div>
        <div className="brand">Bobby's Workshop</div>
      </div>
    </div>
  );
}
