import { useState, useEffect } from "react";
import { invoke } from "@tauri-apps/api/tauri";
import Dashboard from "./components/Dashboard";
import DeviceList from "./components/DeviceList";
import Sidebar from "./components/Sidebar";
import StatusBar from "./components/StatusBar";
import "./styles/App.css";

interface Device {
  platform: string;
  serial: string;
  model: string;
  status: string;
}

function App() {
  const [devices, setDevices] = useState<Device[]>([]);
  const [selectedDevice, setSelectedDevice] = useState<Device | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [currentView, setCurrentView] = useState("dashboard");

  useEffect(() => {
    checkConnection();
    loadDevices();
    
    // Refresh devices every 5 seconds
    const interval = setInterval(() => {
      checkConnection();
      loadDevices();
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const checkConnection = async () => {
    try {
      const connected = await invoke<boolean>("check_device");
      setIsConnected(connected);
    } catch (error) {
      console.error("Error checking device:", error);
      setIsConnected(false);
    }
  };

  const loadDevices = async () => {
    try {
      const deviceList = await invoke<Device[]>("get_devices");
      setDevices(deviceList);
      
      // Auto-select first device if none selected
      if (!selectedDevice && deviceList.length > 0) {
        setSelectedDevice(deviceList[0]);
      }
    } catch (error) {
      console.error("Error loading devices:", error);
    }
  };

  return (
    <div className="app">
      <Sidebar 
        currentView={currentView} 
        onViewChange={setCurrentView}
        isConnected={isConnected}
      />
      <div className="main-content">
        <StatusBar 
          isConnected={isConnected}
          deviceCount={devices.length}
          selectedDevice={selectedDevice}
        />
        <div className="content-area">
          {currentView === "devices" && (
            <DeviceList 
              devices={devices}
              selectedDevice={selectedDevice}
              onSelectDevice={setSelectedDevice}
              onRefresh={loadDevices}
            />
          )}
          {currentView === "dashboard" && (
            <Dashboard 
              device={selectedDevice}
              isConnected={isConnected}
            />
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
