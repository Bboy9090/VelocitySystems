import { Wifi, WifiOff } from "lucide-react";
import "./StatusBar.css";

interface StatusBarProps {
  isConnected: boolean;
  deviceCount: number;
  selectedDevice: { platform: string; model: string; serial: string } | null;
}

export default function StatusBar({ isConnected, deviceCount, selectedDevice }: StatusBarProps) {
  return (
    <div className="status-bar">
      <div className="status-left">
        <div className={`status-item ${isConnected ? "connected" : "disconnected"}`}>
          {isConnected ? <Wifi size={16} /> : <WifiOff size={16} />}
          <span>{isConnected ? "Connected" : "Disconnected"}</span>
        </div>
        {selectedDevice && (
          <div className="status-item">
            <span className="status-label">Device:</span>
            <span className="status-value">{selectedDevice.model}</span>
            <span className="status-badge">{selectedDevice.platform.toUpperCase()}</span>
          </div>
        )}
      </div>
      <div className="status-right">
        <div className="status-item">
          <span className="status-label">Devices:</span>
          <span className="status-value">{deviceCount}</span>
        </div>
      </div>
    </div>
  );
}
