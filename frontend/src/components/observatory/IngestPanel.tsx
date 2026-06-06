'use client';

/**
 * Ingestion + column-map step. Upload one CSV → preview header → map timestamp/close/OHLC,
 * pick a date format (auto / unix / iso / dd-mm-yyyy) → POST /api/v2/datasets.
 * Auto-detect is best-effort header matching for CONVENIENCE; the parse/quality truth comes
 * from the backend response (no statistic computed here).
 */
import { useState } from 'react';
import { observatory, type DateFormat, type IngestResponse } from '@/lib/observatory';
import { C, mono, Badge } from './ui';

type Role = 'timestamp' | 'close' | 'open' | 'high' | 'low' | 'volume';

const ALIASES: Record<Role, string[]> = {
  timestamp: ['time', 'timestamp', 'date', 'datetime', 'dt'],
  close: ['close', 'adj close', 'adj_close', 'price', 'last', 'settle'],
  open: ['open', 'o'],
  high: ['high', 'h'],
  low: ['low', 'l'],
  volume: ['volume', 'vol', 'v'],
};

function autodetect(headers: string[]): Record<Role, string> {
  const lower = headers.map((h) => h.toLowerCase().trim());
  const pick = (role: Role): string => {
    for (const a of ALIASES[role]) {
      const i = lower.indexOf(a);
      if (i >= 0) return headers[i];
    }
    return '';
  };
  return {
    timestamp: pick('timestamp'),
    close: pick('close'),
    open: pick('open'),
    high: pick('high'),
    low: pick('low'),
    volume: pick('volume'),
  };
}

const sel: React.CSSProperties = {
  ...mono,
  fontSize: 11,
  background: C.bgRaised,
  color: C.textBright,
  border: `1px solid ${C.border}`,
  borderRadius: 3,
  padding: '3px 6px',
  width: '100%',
};

export function IngestPanel({ onIngested }: { onIngested: (r: IngestResponse) => void }) {
  const [file, setFile] = useState<File | null>(null);
  const [headers, setHeaders] = useState<string[]>([]);
  const [map, setMap] = useState<Record<Role, string>>({ timestamp: '', close: '', open: '', high: '', low: '', volume: '' });
  const [dateFormat, setDateFormat] = useState<DateFormat>('auto');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function onPick(f: File) {
    setError(null);
    setFile(f);
    const text = await f.slice(0, 4096).text();
    const firstLine = text.split(/\r?\n/)[0] ?? '';
    const hs = firstLine.split(',').map((h) => h.trim());
    setHeaders(hs);
    setMap(autodetect(hs));
  }

  async function submit() {
    if (!file) return;
    if (!map.close) {
      setError('Map a close column before ingesting.');
      return;
    }
    setBusy(true);
    setError(null);
    try {
      const column_map = {
        timestamp: map.timestamp || null,
        close: map.close || null,
        open: map.open || null,
        high: map.high || null,
        low: map.low || null,
        volume: map.volume || null,
      };
      const res = await observatory.createDataset(file, { column_map, date_format: dateFormat });
      onIngested(res);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Ingest failed');
    } finally {
      setBusy(false);
    }
  }

  const roles: Role[] = ['timestamp', 'close', 'open', 'high', 'low', 'volume'];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
      <label
        style={{
          ...mono,
          fontSize: 11,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: 8,
          color: C.accent,
          background: C.accentBg,
          border: `1px dashed ${C.accentBorder}`,
          borderRadius: 4,
          padding: '12px',
          cursor: 'pointer',
        }}
      >
        <input
          type="file"
          accept=".csv,text/csv"
          style={{ display: 'none' }}
          onChange={(e) => {
            const f = e.target.files?.[0];
            if (f) void onPick(f);
          }}
        />
        {file ? `▸ ${file.name}` : '＋ choose CSV'}
      </label>

      {headers.length > 0 && (
        <>
          <div style={{ ...mono, fontSize: 9, letterSpacing: '0.1em', textTransform: 'uppercase', color: C.textDim }}>
            column mapping
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '70px 1fr', gap: 6, alignItems: 'center' }}>
            {roles.map((role) => (
              <RoleRow
                key={role}
                role={role}
                headers={headers}
                value={map[role]}
                onChange={(v) => setMap((m) => ({ ...m, [role]: v }))}
                sel={sel}
              />
            ))}
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '70px 1fr', gap: 6, alignItems: 'center' }}>
            <span style={{ ...mono, fontSize: 10, color: C.text }}>date fmt</span>
            <select value={dateFormat} onChange={(e) => setDateFormat(e.target.value as DateFormat)} style={sel}>
              <option value="auto">auto-detect</option>
              <option value="unix">unix epoch</option>
              <option value="iso">ISO-8601</option>
              <option value="dd-mm-yyyy">dd-mm-yyyy</option>
            </select>
          </div>

          <button
            onClick={submit}
            disabled={busy || !map.close}
            style={{
              ...mono,
              fontSize: 11,
              padding: '6px',
              borderRadius: 4,
              cursor: busy || !map.close ? 'not-allowed' : 'pointer',
              color: map.close ? C.accent : C.textDim,
              background: map.close ? C.accentBg : 'transparent',
              border: `1px solid ${map.close ? C.accentBorder : C.border}`,
              opacity: busy ? 0.6 : 1,
            }}
          >
            {busy ? 'ingesting…' : 'ingest → quality report'}
          </button>
        </>
      )}

      {error && (
        <div style={{ ...mono, fontSize: 10, color: C.danger, background: C.dangerBg, border: `1px solid ${C.dangerBorder}`, borderRadius: 3, padding: '5px 8px' }}>
          {error}
        </div>
      )}
    </div>
  );
}

function RoleRow({
  role,
  headers,
  value,
  onChange,
  sel,
}: {
  role: Role;
  headers: string[];
  value: string;
  onChange: (v: string) => void;
  sel: React.CSSProperties;
}) {
  const required = role === 'timestamp' || role === 'close';
  return (
    <>
      <span style={{ ...mono, fontSize: 10, color: required ? C.textBright : C.text, display: 'flex', gap: 4, alignItems: 'center' }}>
        {role}
        {required && <Badge tone="accent">req</Badge>}
      </span>
      <select value={value} onChange={(e) => onChange(e.target.value)} style={sel}>
        <option value="">— none —</option>
        {headers.map((h) => (
          <option key={h} value={h}>
            {h}
          </option>
        ))}
      </select>
    </>
  );
}
