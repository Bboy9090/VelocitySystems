import { useState } from "react";
import { invoke } from "@tauri-apps/api/core";

type TabType = "dashboard" | "analysis" | "metrics";

function App() {
  const [activeTab, setActiveTab] = useState<TabType>("dashboard");
  const [deviceInfo, setDeviceInfo] = useState("");
  const [analysisResult, setAnalysisResult] = useState("");
  const [metrics, setMetrics] = useState("");

  async function runAnalysis() {
    try {
      const result = await invoke<string>("analyze_device", {
        deviceInfo,
        actor: "user",
      });
      setAnalysisResult(result);
    } catch (error) {
      console.error("Analysis failed:", error);
      setAnalysisResult("Analysis failed - backend not available");
    }
  }

  async function loadMetrics() {
    try {
      const result = await invoke<string>("get_ops_metrics");
      setMetrics(result);
    } catch (error) {
      console.error("Metrics load failed:", error);
      setMetrics("Metrics load failed - backend not available");
    }
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <header className="bg-gray-800 p-4">
        <h1 className="text-2xl font-bold text-center">REFORGE OS - Professional Repair Platform</h1>
        <p className="text-center text-gray-400 mt-2">
          Compliance-First Device Analysis & Repair Intelligence
        </p>
      </header>

      <nav className="bg-gray-800 border-b border-gray-700">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex space-x-8">
            <button
              onClick={() => setActiveTab("dashboard")}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === "dashboard"
                  ? "border-blue-500 text-blue-400"
                  : "border-transparent text-gray-400 hover:text-gray-300"
              }`}
            >
              Dashboard
            </button>
            <button
              onClick={() => setActiveTab("analysis")}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === "analysis"
                  ? "border-blue-500 text-blue-400"
                  : "border-transparent text-gray-400 hover:text-gray-300"
              }`}
            >
              Device Analysis
            </button>
            <button
              onClick={() => setActiveTab("metrics")}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === "metrics"
                  ? "border-blue-500 text-blue-400"
                  : "border-transparent text-gray-400 hover:text-gray-300"
              }`}
            >
              Operations Metrics
            </button>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-6 px-4">
        {activeTab === "dashboard" && (
          <div className="space-y-6">
            <div className="bg-gray-800 rounded-lg p-6">
              <h2 className="text-xl font-semibold mb-4">Welcome to REFORGE OS</h2>
              <p className="text-gray-300 mb-4">
                Professional repair platform with compliance-first device analysis,
                ownership verification, legal classification, and authority routing.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-gray-700 p-4 rounded">
                  <h3 className="font-medium text-blue-400">Hardware Suite</h3>
                  <p className="text-sm text-gray-300">ForgeCore Diagnostic Bridge + Thermal Platform</p>
                </div>
                <div className="bg-gray-700 p-4 rounded">
                  <h3 className="font-medium text-blue-400">Software Stack</h3>
                  <p className="text-sm text-gray-300">Rust services + React UI + Postgres DB</p>
                </div>
                <div className="bg-gray-700 p-4 rounded">
                  <h3 className="font-medium text-blue-400">Compliance</h3>
                  <p className="text-sm text-gray-300">Audit trails + Legal routing + No execution</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === "analysis" && (
          <div className="space-y-6">
            <div className="bg-gray-800 rounded-lg p-6">
              <h2 className="text-xl font-semibold mb-4">Device Analysis</h2>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Device Information</label>
                  <textarea
                    value={deviceInfo}
                    onChange={(e) => setDeviceInfo(e.target.value)}
                    className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white"
                    rows={3}
                    placeholder="Enter device details (e.g., iPhone 13 Pro - Clean device)"
                  />
                </div>
                <button
                  onClick={runAnalysis}
                  className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded font-medium"
                >
                  Analyze Device
                </button>
              </div>
            </div>

            {analysisResult && (
              <div className="bg-gray-800 rounded-lg p-6">
                <h3 className="text-lg font-semibold mb-4">Analysis Results</h3>
                <pre className="bg-gray-900 p-4 rounded text-sm overflow-auto">
                  {analysisResult}
                </pre>
              </div>
            )}
          </div>
        )}

        {activeTab === "metrics" && (
          <div className="space-y-6">
            <div className="bg-gray-800 rounded-lg p-6">
              <h2 className="text-xl font-semibold mb-4">Operations Control Tower</h2>
              <button
                onClick={loadMetrics}
                className="bg-green-600 hover:bg-green-700 px-4 py-2 rounded font-medium"
              >
                Load Metrics
              </button>
            </div>

            {metrics && (
              <div className="bg-gray-800 rounded-lg p-6">
                <h3 className="text-lg font-semibold mb-4">Current Metrics</h3>
                <pre className="bg-gray-900 p-4 rounded text-sm">
                  {metrics}
                </pre>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
