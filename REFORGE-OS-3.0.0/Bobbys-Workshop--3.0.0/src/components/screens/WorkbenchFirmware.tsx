/**
 * WorkbenchFirmware
 * Firmware library, search, and download - truth-first, no placeholder data
 */

import React, { useState, useEffect } from 'react';
import { Search, Download, Package } from 'lucide-react';
import { getAPIUrl } from '@/lib/apiConfig';
import { useApp } from '@/lib/app-context';
import { toast } from 'sonner';

function FirmwareDownloadButton({ firmware }: { firmware: FirmwareEntry }) {
  const [loading, setLoading] = useState(false);
  const handleDownload = async () => {
    const url = firmware.downloadUrl;
    if (!url) {
      toast.error('No download URL for this firmware');
      return;
    }
    setLoading(true);
    try {
      const res = await fetch(getAPIUrl('/api/firmware/download'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ downloadUrl: url, firmwareId: firmware.id }),
      });
      const data = await res.json().catch(() => ({}));
      if (res.ok && data?.downloadId) {
        toast.success('Download started');
      } else {
        toast.error(data?.message ?? 'Download failed');
      }
    } catch {
      toast.error('Download failed');
    } finally {
      setLoading(false);
    }
  };
  return (
    <button
      onClick={handleDownload}
      disabled={loading || !firmware.downloadUrl}
      className="w-full px-3 py-2 rounded-md border border-panel bg-basement-concrete text-ink-primary text-sm font-mono hover:border-spray-cyan hover:glow-cyan transition-all motion-snap flex items-center justify-center gap-2 disabled:opacity-50"
    >
      <Download className="w-4 h-4" />
      {loading ? 'Starting...' : 'Download'}
    </button>
  );
}

interface FirmwareEntry {
  id?: string;
  brand?: string;
  model?: string;
  version?: string;
  downloadUrl?: string;
  size?: string;
  [key: string]: unknown;
}

function flattenFirmware(data: { brands?: Array<{ brand: string; devices?: Array<{ model?: string; firmwares?: Array<Record<string, unknown>> }> }> }): FirmwareEntry[] {
  const out: FirmwareEntry[] = [];
  for (const b of data.brands ?? []) {
    for (const d of b.devices ?? []) {
      for (const f of d.firmwares ?? []) {
        out.push({ brand: b.brand, model: d.model, ...f } as FirmwareEntry);
      }
    }
  }
  return out;
}

export function WorkbenchFirmware() {
  const [searchQuery, setSearchQuery] = useState('');
  const [firmware, setFirmware] = useState<FirmwareEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { backendAvailable } = useApp();

  useEffect(() => {
    if (!backendAvailable) {
      setFirmware([]);
      setLoading(false);
      return;
    }
    let cancelled = false;
    setLoading(true);
    setError(null);
    fetch(getAPIUrl('/api/firmware/database'))
      .then((r) => (r.ok ? r.json() : Promise.reject(new Error(`HTTP ${r.status}`))))
      .then((data) => {
        if (cancelled) return;
        const raw = data?.data ?? data;
        setFirmware(Array.isArray(raw) ? raw : flattenFirmware(raw ?? {}));
      })
      .catch((err) => {
        if (!cancelled) setError(err?.message ?? 'Failed to load firmware');
        setFirmware([]);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => { cancelled = true; };
  }, [backendAvailable]);

  const filtered = firmware.filter(
    (f) =>
      !searchQuery ||
      [f.brand, f.model, f.version].some(
        (v) => typeof v === 'string' && v.toLowerCase().includes(searchQuery.toLowerCase())
      )
  );

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-ink-primary font-mono mb-2">
          Firmware
        </h1>
        <p className="text-sm text-ink-muted">
          Firmware library, search, and download
        </p>
      </div>

      <div className="relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-ink-muted" />
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search firmware by brand, model, version..."
          className="w-full pl-10 pr-4 py-3 rounded-lg bg-workbench-steel border border-panel text-ink-primary text-sm font-mono placeholder:text-ink-muted focus:outline-none focus:border-spray-cyan focus:glow-cyan transition-all motion-snap"
        />
      </div>

      {loading && (
        <p className="text-sm text-ink-muted">Loading firmware...</p>
      )}
      {error && (
        <p className="text-sm text-red-400"> {error}</p>
      )}
      {!loading && !error && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.length === 0 ? (
            <p className="text-sm text-ink-muted col-span-full">No firmware found. Connect backend and add firmware to the database.</p>
          ) : (
            filtered.map((f, i) => (
              <div
                key={f.id ?? i}
                className="p-4 rounded-lg border border-panel bg-workbench-steel"
              >
                <div className="flex items-center gap-3 mb-3">
                  <Package className="w-5 h-5 text-spray-cyan" />
                  <div>
                    <h3 className="text-sm font-mono font-bold text-ink-primary">
                      {[f.brand, f.model, f.version].filter(Boolean).join(' ') || 'Firmware'}
                    </h3>
                    <p className="text-xs text-ink-muted">{f.size ?? '—'}</p>
                  </div>
                </div>
                <FirmwareDownloadButton firmware={f} />
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}
