// ForgeWorks Core - Operations Dashboard
// Control Tower for platform monitoring

import React, { useEffect, useState } from 'react';

interface DashboardMetrics {
  active_units: number;
  audit_coverage_pct: number;
  compliance_escalations_30d: number;
  audit_entries_24h: number;
  integrity_violations: number;
  active_jurisdictions: number;
  timestamp: string;
}

interface RiskDistribution {
  risk_level: string;
  count: number;
  percentage: number;
}

export default function OpsDashboard() {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [riskDist, setRiskDist] = useState<RiskDistribution[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 60000); // Refresh every minute
    return () => clearInterval(interval);
  }, []);

  const fetchMetrics = async () => {
    try {
      // In production, fetch from API endpoint
      const response = await fetch('/api/metrics/dashboard');
      if (!response.ok) throw new Error('Failed to fetch metrics');
      const data = await response.json();
      setMetrics(data);
      setLoading(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
      setLoading(false);
    }
  };

  const getHealthStatus = () => {
    if (!metrics) return 'unknown';
    if (metrics.audit_coverage_pct < 100 || metrics.integrity_violations > 0) {
      return 'critical';
    }
    if (metrics.compliance_escalations_30d > 1000) {
      return 'warning';
    }
    return 'healthy';
  };

  const healthStatus = getHealthStatus();
  const healthColor = {
    healthy: 'text-green-600',
    warning: 'text-yellow-600',
    critical: 'text-red-600',
    unknown: 'text-gray-600',
  }[healthStatus];

  if (loading) {
    return (
      <div className="p-6">
        <h1 className="text-2xl font-bold mb-4">Operations Control Tower</h1>
        <p>Loading metrics...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6">
        <h1 className="text-2xl font-bold mb-4">Operations Control Tower</h1>
        <div className="bg-red-50 border border-red-200 rounded p-4">
          <p className="text-red-800">Error: {error}</p>
        </div>
      </div>
    );
  }

  return (
    <section className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold mb-2">Operations Control Tower</h1>
        <p className="text-gray-600">Real-time platform monitoring and metrics</p>
        <div className={`mt-2 text-sm font-semibold ${healthColor}`}>
          System Status: <span className="uppercase">{healthStatus}</span>
        </div>
      </div>

      {metrics && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
          <MetricCard
            title="Active Units"
            value={metrics.active_units.toLocaleString()}
            description="Unique devices (last 30 days)"
            status={metrics.active_units > 0 ? 'normal' : 'warning'}
          />
          <MetricCard
            title="Audit Coverage"
            value={`${metrics.audit_coverage_pct.toFixed(2)}%`}
            description="Operations with valid audit logs"
            status={metrics.audit_coverage_pct >= 100 ? 'normal' : 'critical'}
          />
          <MetricCard
            title="Compliance Escalations"
            value={metrics.compliance_escalations_30d.toLocaleString()}
            description="Last 30 days"
            status={metrics.compliance_escalations_30d < 1000 ? 'normal' : 'warning'}
          />
          <MetricCard
            title="Audit Entries (24h)"
            value={metrics.audit_entries_24h.toLocaleString()}
            description="Total audit log entries"
            status="normal"
          />
          <MetricCard
            title="Integrity Violations"
            value={metrics.integrity_violations.toString()}
            description="Hash chain breaks (must be 0)"
            status={metrics.integrity_violations === 0 ? 'normal' : 'critical'}
          />
          <MetricCard
            title="Active Jurisdictions"
            value={metrics.active_jurisdictions.toString()}
            description="Unique jurisdictions"
            status="normal"
          />
        </div>
      )}

      {healthStatus === 'critical' && (
        <div className="bg-red-50 border border-red-200 rounded p-4 mb-6">
          <h2 className="font-bold text-red-800 mb-2">⚠️ Critical Alert</h2>
          <ul className="list-disc list-inside text-red-700">
            {metrics && metrics.audit_coverage_pct < 100 && (
              <li>Audit coverage is below 100% - audit logging may be failing</li>
            )}
            {metrics && metrics.integrity_violations > 0 && (
              <li>Hash chain integrity violations detected - possible tampering</li>
            )}
          </ul>
          <p className="mt-2 text-sm text-red-600">
            <strong>Action Required:</strong> Freeze operations, export logs, contact compliance team.
          </p>
        </div>
      )}

      <div className="mt-6">
        <h2 className="text-xl font-bold mb-4">Risk Distribution (Last 30 Days)</h2>
        {riskDist.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Risk Level</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Count</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Percentage</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {riskDist.map((risk, idx) => (
                  <tr key={idx}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">{risk.risk_level}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">{risk.count}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">{risk.percentage.toFixed(2)}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="text-gray-500">No risk distribution data available</p>
        )}
      </div>

      {metrics && (
        <div className="mt-6 text-sm text-gray-500">
          Last updated: {new Date(metrics.timestamp).toLocaleString()}
        </div>
      )}
    </section>
  );
}

interface MetricCardProps {
  title: string;
  value: string;
  description: string;
  status: 'normal' | 'warning' | 'critical';
}

function MetricCard({ title, value, description, status }: MetricCardProps) {
  const statusColors = {
    normal: 'border-gray-200 bg-white',
    warning: 'border-yellow-300 bg-yellow-50',
    critical: 'border-red-300 bg-red-50',
  };

  return (
    <div className={`border rounded-lg p-4 ${statusColors[status]}`}>
      <h3 className="text-sm font-medium text-gray-600 mb-1">{title}</h3>
      <p className="text-2xl font-bold text-gray-900 mb-1">{value}</p>
      <p className="text-xs text-gray-500">{description}</p>
    </div>
  );
}
