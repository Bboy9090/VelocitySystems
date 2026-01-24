import { useState, useEffect } from "react";
import { invoke } from "@tauri-apps/api/tauri";
import { RefreshCw, Smartphone, Tablet } from "lucide-react";
import "./DeviceList.css";

interface Device {
  platform: string;
  serial: string;
  model: string;
  status: string;
}

interface DeviceListProps {
  devices: Device[];
  selectedDevice: Device | null;
  onSelectDevice: (device: Device) => void;
  onRefresh: () => void;
}

export default function DeviceList({ devices, selectedDevice, onSelectDevice, onRefresh }: DeviceListProps) {
  const [isRefreshing, setIsRefreshing] = useState(false);

  const handleRefresh = async () => {
    setIsRefreshing(true);
    await onRefresh();
    setTimeout(() => setIsRefreshing(false), 500);
  };

  return (
    <div className="device-list">
      <div className="device-list-header">
        <h2>Connected Devices</h2>
        <button 
          className="btn btn-primary"
          onClick={handleRefresh}
          disabled={isRefreshing}
        >
          <RefreshCw className={isRefreshing ? "spinning" : ""} size={16} />
          Refresh
        </button>
      </div>

      {devices.length === 0 ? (
        <div className="empty-state">
          <Smartphone size={48} />
          <p>No devices connected</p>
          <p className="empty-hint">Connect an Android device (USB debugging) or iOS device</p>
        </div>
      ) : (
        <div className="device-grid">
          {devices.map((device) => (
            <div
              key={device.serial}
              className={`device-card ${selectedDevice?.serial === device.serial ? "selected" : ""}`}
              onClick={() => onSelectDevice(device)}
            >
              <div className="device-icon">
                {device.platform === "ios" ? <Tablet size={32} /> : <Smartphone size={32} />}
              </div>
              <div className="device-info">
                <div className="device-model">{device.model}</div>
                <div className="device-platform">{device.platform.toUpperCase()}</div>
                <div className="device-serial">{device.serial.substring(0, 20)}...</div>
              </div>
              <div className={`device-status ${device.status}`}>
                {device.status}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
