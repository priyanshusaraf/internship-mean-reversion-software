'use client';

import { useState, useEffect, useRef } from 'react';
import { api } from '@/lib/api';
import { useWorkstationStore, useUIStore } from '@/lib/store';

export function InstrumentPanel() {
  // ── Load tab state ────────────────────────────────────────────────────
  const [filePath, setFilePath] = useState('');
  const [instrumentId, setInstrumentId] = useState('');
  const [loadError, setLoadError] = useState<string | null>(null);
  const [loadingFile, setLoadingFile] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const [uploadLabel, setUploadLabel] = useState<string | null>(null);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [suggestionIndex, setSuggestionIndex] = useState(-1);
  const [showSuggestions, setShowSuggestions] = useState(false);

  // ── Spread tab state ──────────────────────────────────────────────────
  const [activeTab, setActiveTab] = useState<'load' | 'spread'>('load');
  const [spreadLegA, setSpreadLegA] = useState('');
  const [spreadLegB, setSpreadLegB] = useState('');
  const [spreadBeta, setSpreadBeta] = useState('1');
  const [spreadName, setSpreadName] = useState('');
  const [spreadError, setSpreadError] = useState<string | null>(null);
  const [spreadLoading, setSpreadLoading] = useState(false);

  const dragCounter = useRef(0);
  const suggestTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  const { instruments, selectedInstrumentId, selectInstrument, setInstruments } =
    useWorkstationStore();
  const { leftWidth, fontScale } = useUIStore();
  const sc = (base: number) => Math.round(base * fontScale);

  useEffect(() => {
    api.listInstruments().then(setInstruments).catch(() => {});
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  // ── Load handlers ─────────────────────────────────────────────────────
  async function handleLoad() {
    if (!filePath.trim() || !instrumentId.trim()) return;
    setLoadingFile(true);
    setLoadError(null);
    try {
      await api.loadInstrument({
        file_path: filePath.trim(),
        instrument_id: instrumentId.trim().toUpperCase(),
      });
      const updated = await api.listInstruments();
      setInstruments(updated);
      setFilePath('');
      setInstrumentId('');
    } catch (e: unknown) {
      setLoadError(e instanceof Error ? e.message : 'Load failed');
    } finally {
      setLoadingFile(false);
    }
  }

  async function handleReload(fp: string, iid: string) {
    try {
      await api.loadInstrument({ file_path: fp, instrument_id: iid });
      const updated = await api.listInstruments();
      setInstruments(updated);
    } catch { /* silently ignore */ }
  }

  // ── Path suggestions ──────────────────────────────────────────────────
  function triggerSuggest(value: string) {
    if (suggestTimer.current) clearTimeout(suggestTimer.current);
    if (value.length < 1) { setSuggestions([]); setShowSuggestions(false); return; }
    suggestTimer.current = setTimeout(async () => {
      try {
        const r = await api.suggestPaths(value);
        setSuggestions(r.suggestions);
        setShowSuggestions(r.suggestions.length > 0);
      } catch { setSuggestions([]); setShowSuggestions(false); }
    }, 180);
  }

  function handlePathChange(value: string) {
    setFilePath(value);
    setSuggestionIndex(-1);
    triggerSuggest(value);
  }

  function handlePathKeyDown(e: React.KeyboardEvent) {
    if (!showSuggestions || suggestions.length === 0) { if (e.key === 'Enter') handleLoad(); return; }
    if (e.key === 'ArrowDown') { e.preventDefault(); setSuggestionIndex(i => Math.min(i + 1, suggestions.length - 1)); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); setSuggestionIndex(i => Math.max(i - 1, -1)); }
    else if (e.key === 'Enter') {
      e.preventDefault();
      if (suggestionIndex >= 0) { pickSuggestion(suggestions[suggestionIndex]); }
      else handleLoad();
    } else if (e.key === 'Escape') { setShowSuggestions(false); setSuggestionIndex(-1); }
  }

  function pickSuggestion(s: string) {
    setFilePath(s); setShowSuggestions(false); setSuggestionIndex(-1);
    if (s.endsWith('/')) triggerSuggest(s);
  }

  // ── Drag & drop ───────────────────────────────────────────────────────
  function onDragEnter(e: React.DragEvent) {
    e.preventDefault(); dragCounter.current++;
    if (e.dataTransfer.items?.length) setIsDragging(true);
  }
  function onDragLeave(e: React.DragEvent) {
    e.preventDefault(); if (--dragCounter.current === 0) setIsDragging(false);
  }
  function onDragOver(e: React.DragEvent) { e.preventDefault(); }

  async function onDrop(e: React.DragEvent) {
    e.preventDefault(); dragCounter.current = 0; setIsDragging(false);
    const files = Array.from(e.dataTransfer.files).filter(f => /\.(csv|parquet|txt)$/i.test(f.name));
    if (files.length === 0) { setLoadError('Drop .csv or .parquet files'); return; }
    setLoadingFile(true); setLoadError(null);
    setUploadLabel(`Uploading ${files.length} file${files.length > 1 ? 's' : ''}…`);
    try {
      await api.uploadInstruments(files);
      setInstruments(await api.listInstruments());
    } catch (ex: unknown) { setLoadError(ex instanceof Error ? ex.message : 'Upload failed'); }
    finally { setLoadingFile(false); setUploadLabel(null); }
  }

  // ── Spread handler ────────────────────────────────────────────────────
  async function handleCreateSpread() {
    const beta = parseFloat(spreadBeta);
    if (!spreadLegA || !spreadLegB) { setSpreadError('Select both legs'); return; }
    if (spreadLegA === spreadLegB) { setSpreadError('Legs must differ'); return; }
    if (isNaN(beta)) { setSpreadError('β must be a number'); return; }
    setSpreadLoading(true); setSpreadError(null);
    try {
      await api.createSpread({
        instrument_a: spreadLegA,
        instrument_b: spreadLegB,
        beta,
        spread_id: spreadName.trim() || undefined,
      });
      setInstruments(await api.listInstruments());
      setSpreadName('');
    } catch (e: unknown) { setSpreadError(e instanceof Error ? e.message : 'Failed'); }
    finally { setSpreadLoading(false); }
  }

  const canLoad = !loadingFile && filePath.trim().length > 0 && instrumentId.trim().length > 0;
  const canSpread = !spreadLoading && !!spreadLegA && !!spreadLegB && spreadLegA !== spreadLegB && spreadBeta.trim() !== '';

  // shared select style
  const selStyle: React.CSSProperties = {
    background: '#0d1520', border: '1px solid #1a2230', borderRadius: 3,
    padding: '5px 8px', fontSize: sc(11), color: '#c9d1d9', outline: 'none', width: '100%',
    cursor: 'pointer', appearance: 'none', WebkitAppearance: 'none',
  };

  return (
    <aside
      className="flex flex-col overflow-y-auto"
      style={{ width: leftWidth, flexShrink: 0, background: '#090d13', borderRight: '1px solid #161d27' }}
      onDragEnter={onDragEnter}
      onDragLeave={onDragLeave}
      onDragOver={onDragOver}
      onDrop={onDrop}
    >
      {/* Header + tabs */}
      <div className="shrink-0" style={{ borderBottom: '1px solid #161d27' }}>
        <div className="flex items-center px-3" style={{ height: 36 }}>
          <span className="font-data" style={{ fontSize: sc(9), fontWeight: 700, color: 'var(--amr-text-dim)', letterSpacing: '0.14em', textTransform: 'uppercase' }}>
            Instruments
          </span>
        </div>

        {/* Tab bar */}
        <div style={{ display: 'flex', padding: '0 8px 6px' }}>
          {(['load', 'spread'] as const).map(tab => {
            const active = activeTab === tab;
            return (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className="font-data"
                style={{
                  flex: 1, padding: '4px 0',
                  fontSize: sc(10), fontWeight: active ? 600 : 400,
                  background: active ? 'rgba(56,139,253,0.1)' : 'transparent',
                  border: `1px solid ${active ? 'rgba(56,139,253,0.3)' : '#161d27'}`,
                  borderRadius: 3, letterSpacing: '0.06em',
                  color: active ? '#58a6ff' : '#2d3a4a',
                  cursor: 'pointer', transition: 'all 0.12s',
                  marginRight: tab === 'load' ? 3 : 0,
                }}
              >
                {tab === 'load' ? 'Load' : 'Spread'}
              </button>
            );
          })}
        </div>
      </div>

      {/* ── LOAD TAB ─────────────────────────────────────────────────── */}
      {activeTab === 'load' && (
        <div
          style={{
            padding: '10px 12px', borderBottom: '1px solid #161d27',
            display: 'flex', flexDirection: 'column', gap: 6,
            position: 'relative', transition: 'background 0.12s',
            background: isDragging ? 'rgba(56,139,253,0.04)' : 'transparent',
          }}
        >
          {isDragging && (
            <div style={{
              position: 'absolute', inset: 0, zIndex: 20,
              display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 5,
              background: 'rgba(9,13,19,0.88)', border: '1px solid rgba(56,139,253,0.35)', borderRadius: 3,
            }}>
              <span style={{ fontSize: 20, color: '#388bfd', lineHeight: 1 }}>↓</span>
              <span className="font-data" style={{ fontSize: sc(10), color: '#58a6ff', letterSpacing: '0.08em' }}>Drop files</span>
              <span className="font-data" style={{ fontSize: sc(9), color: 'var(--amr-text-dim)' }}>.csv · .parquet</span>
            </div>
          )}

          <div style={{ border: '1px dashed #1a2230', borderRadius: 3, padding: '5px 8px', textAlign: 'center', userSelect: 'none' }}>
            <span className="font-data" style={{ fontSize: sc(9), color: 'var(--amr-text-dim)', letterSpacing: '0.06em' }}>
              drag & drop · multi-file ok
            </span>
          </div>

          <input
            className="font-data"
            style={{ background: '#0d1520', border: '1px solid #1a2230', borderRadius: 3, padding: '5px 8px', fontSize: sc(11), color: '#c9d1d9', outline: 'none', width: '100%', letterSpacing: '0.05em' }}
            placeholder="INSTRUMENT_ID"
            value={instrumentId}
            onChange={(e) => setInstrumentId(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleLoad()}
            onFocus={(e) => { e.target.style.borderColor = '#388bfd'; }}
            onBlur={(e) => { e.target.style.borderColor = '#1a2230'; }}
          />

          <div style={{ position: 'relative' }}>
            <input
              style={{ background: '#0d1520', border: '1px solid #1a2230', borderRadius: showSuggestions ? '3px 3px 0 0' : 3, padding: '5px 8px', fontSize: sc(10), color: '#8b99a8', outline: 'none', width: '100%' }}
              placeholder="/path/to/data.csv or .parquet"
              value={filePath}
              onChange={(e) => handlePathChange(e.target.value)}
              onKeyDown={handlePathKeyDown}
              onFocus={(e) => { e.target.style.borderColor = '#388bfd'; e.target.style.color = '#c9d1d9'; if (suggestions.length > 0) setShowSuggestions(true); }}
              onBlur={(e) => { e.target.style.borderColor = '#1a2230'; e.target.style.color = '#8b99a8'; setTimeout(() => setShowSuggestions(false), 160); }}
            />
            {showSuggestions && suggestions.length > 0 && (
              <div style={{ position: 'absolute', left: 0, right: 0, top: '100%', background: '#0d1520', border: '1px solid rgba(56,139,253,0.4)', borderTop: 'none', borderRadius: '0 0 3px 3px', zIndex: 50, maxHeight: 168, overflowY: 'auto' }}>
                {suggestions.map((s, i) => {
                  const isDir = s.endsWith('/');
                  const label = s.split('/').filter(Boolean).pop() ?? s;
                  return (
                    <div key={s} onMouseDown={() => pickSuggestion(s)} onMouseEnter={() => setSuggestionIndex(i)} onMouseLeave={() => setSuggestionIndex(-1)}
                      style={{ padding: '4px 8px', fontSize: sc(10), cursor: 'pointer', color: i === suggestionIndex ? '#58a6ff' : (isDir ? '#8b99a8' : '#c9d1d9'), background: i === suggestionIndex ? 'rgba(56,139,253,0.09)' : 'transparent', display: 'flex', alignItems: 'center', gap: 5, overflow: 'hidden' }}>
                      <span style={{ color: 'var(--amr-text-dim)', flexShrink: 0, fontSize: 8 }}>{isDir ? '▸' : '·'}</span>
                      <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{label}{isDir ? '/' : ''}</span>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          <button onClick={handleLoad} disabled={!canLoad}
            style={{ background: canLoad ? 'rgba(56,139,253,0.09)' : 'transparent', border: `1px solid ${canLoad ? 'rgba(56,139,253,0.35)' : '#161d27'}`, borderRadius: 3, padding: '5px 0', fontSize: sc(11), fontWeight: 600, color: canLoad ? '#58a6ff' : '#2d3a4a', cursor: canLoad ? 'pointer' : 'not-allowed', boxShadow: canLoad ? '0 0 12px rgba(56,139,253,0.1)' : 'none', transition: 'all 0.15s', letterSpacing: '0.04em' }}>
            {loadingFile
              ? <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 6 }}>
                  <span style={{ width: 5, height: 5, borderRadius: '50%', background: '#388bfd', animation: 'pulse 1s infinite' }} />
                  {uploadLabel ?? 'Loading'}
                </span>
              : 'Load File'}
          </button>

          {loadError && (
            <div style={{ background: 'rgba(248,81,73,0.05)', border: '1px solid rgba(248,81,73,0.2)', borderRadius: 3, padding: '5px 8px' }}>
              <span style={{ fontSize: sc(10), color: '#f85149', lineHeight: 1.4, display: 'block' }}>{loadError}</span>
            </div>
          )}
        </div>
      )}

      {/* ── SPREAD TAB ───────────────────────────────────────────────── */}
      {activeTab === 'spread' && (
        <div style={{ padding: '10px 12px', borderBottom: '1px solid #161d27', display: 'flex', flexDirection: 'column', gap: 7 }}>

          {/* Leg A */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
            <span className="font-data" style={{ fontSize: sc(9), color: 'var(--amr-text-dim)', letterSpacing: '0.1em', textTransform: 'uppercase' }}>Leg A</span>
            <div style={{ position: 'relative' }}>
              <select value={spreadLegA} onChange={e => setSpreadLegA(e.target.value)} style={selStyle}
                onFocus={e => { e.target.style.borderColor = '#388bfd'; }}
                onBlur={e => { e.target.style.borderColor = '#1a2230'; }}>
                <option value="">— select —</option>
                {instruments.map(i => <option key={i.instrument_id} value={i.instrument_id}>{i.instrument_id}</option>)}
              </select>
              <span style={{ position: 'absolute', right: 8, top: '50%', transform: 'translateY(-50%)', color: 'var(--amr-text-dim)', fontSize: 8, pointerEvents: 'none' }}>▾</span>
            </div>
          </div>

          {/* Leg B */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
            <span className="font-data" style={{ fontSize: sc(9), color: 'var(--amr-text-dim)', letterSpacing: '0.1em', textTransform: 'uppercase' }}>Leg B</span>
            <div style={{ position: 'relative' }}>
              <select value={spreadLegB} onChange={e => setSpreadLegB(e.target.value)} style={selStyle}
                onFocus={e => { e.target.style.borderColor = '#388bfd'; }}
                onBlur={e => { e.target.style.borderColor = '#1a2230'; }}>
                <option value="">— select —</option>
                {instruments.map(i => <option key={i.instrument_id} value={i.instrument_id}>{i.instrument_id}</option>)}
              </select>
              <span style={{ position: 'absolute', right: 8, top: '50%', transform: 'translateY(-50%)', color: 'var(--amr-text-dim)', fontSize: 8, pointerEvents: 'none' }}>▾</span>
            </div>
          </div>

          {/* β */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
            <span className="font-data" style={{ fontSize: sc(9), color: 'var(--amr-text-dim)', letterSpacing: '0.1em', textTransform: 'uppercase' }}>β hedge ratio</span>
            <input
              className="font-data"
              type="number" step="0.0001"
              placeholder="1.0"
              value={spreadBeta}
              onChange={e => setSpreadBeta(e.target.value)}
              style={{ background: '#0d1520', border: '1px solid #1a2230', borderRadius: 3, padding: '5px 8px', fontSize: sc(11), color: '#c9d1d9', outline: 'none', width: '100%' }}
              onFocus={e => { e.target.style.borderColor = '#388bfd'; }}
              onBlur={e => { e.target.style.borderColor = '#1a2230'; }}
            />
          </div>

          {/* Preview formula */}
          {spreadLegA && spreadLegB && (
            <div style={{ background: 'rgba(56,139,253,0.04)', border: '1px solid rgba(56,139,253,0.12)', borderRadius: 3, padding: '5px 8px' }}>
              <span className="font-data" style={{ fontSize: sc(10), color: '#388bfd' }}>
                {spreadLegA} − {parseFloat(spreadBeta) || 1}×{spreadLegB}
              </span>
            </div>
          )}

          {/* Optional name */}
          <input
            className="font-data"
            placeholder="Name (optional)"
            value={spreadName}
            onChange={e => setSpreadName(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleCreateSpread()}
            style={{ background: '#0d1520', border: '1px solid #1a2230', borderRadius: 3, padding: '5px 8px', fontSize: sc(10), color: '#8b99a8', outline: 'none', width: '100%' }}
            onFocus={e => { e.target.style.borderColor = '#388bfd'; e.target.style.color = '#c9d1d9'; }}
            onBlur={e => { e.target.style.borderColor = '#1a2230'; e.target.style.color = '#8b99a8'; }}
          />

          {/* Create button */}
          <button onClick={handleCreateSpread} disabled={!canSpread}
            style={{ background: canSpread ? 'rgba(56,139,253,0.09)' : 'transparent', border: `1px solid ${canSpread ? 'rgba(56,139,253,0.35)' : '#161d27'}`, borderRadius: 3, padding: '5px 0', fontSize: sc(11), fontWeight: 600, color: canSpread ? '#58a6ff' : '#2d3a4a', cursor: canSpread ? 'pointer' : 'not-allowed', transition: 'all 0.15s', letterSpacing: '0.04em' }}>
            {spreadLoading
              ? <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 6 }}>
                  <span style={{ width: 5, height: 5, borderRadius: '50%', background: '#388bfd', animation: 'pulse 1s infinite' }} />
                  Building…
                </span>
              : 'Create Spread'}
          </button>

          {spreadError && (
            <div style={{ background: 'rgba(248,81,73,0.05)', border: '1px solid rgba(248,81,73,0.2)', borderRadius: 3, padding: '5px 8px' }}>
              <span style={{ fontSize: sc(10), color: '#f85149', lineHeight: 1.4, display: 'block' }}>{spreadError}</span>
            </div>
          )}
        </div>
      )}

      {/* ── Instrument list ──────────────────────────────────────────── */}
      <div style={{ padding: '6px 8px', display: 'flex', flexDirection: 'column', gap: 2 }}>
        {instruments.length === 0 && (
          <div style={{ padding: '16px 4px', textAlign: 'center' }}>
            <span style={{ fontSize: sc(10), color: '#1e2833' }}>No instruments loaded</span>
          </div>
        )}
        {instruments.map((inst) => {
          const active = selectedInstrumentId === inst.instrument_id;
          const isSpread = inst.file_path.startsWith('spread://');
          return (
            <div
              key={inst.instrument_id}
              role="button"
              tabIndex={0}
              onClick={() => selectInstrument(inst.instrument_id)}
              onKeyDown={(e) => e.key === 'Enter' && selectInstrument(inst.instrument_id)}
              style={{
                textAlign: 'left', padding: '7px 10px', borderRadius: 4,
                background: active ? 'rgba(56,139,253,0.06)' : 'transparent',
                border: `1px solid ${active ? 'rgba(56,139,253,0.22)' : 'transparent'}`,
                boxShadow: active ? '0 0 0 1px rgba(56,139,253,0.08), 0 2px 8px rgba(56,139,253,0.05)' : 'none',
                cursor: 'pointer', transition: 'all 0.15s', width: '100%',
              }}
              onMouseEnter={(e) => {
                if (!active) { (e.currentTarget as HTMLDivElement).style.background = 'rgba(255,255,255,0.02)'; (e.currentTarget as HTMLDivElement).style.border = '1px solid #1a2230'; }
              }}
              onMouseLeave={(e) => {
                if (!active) { (e.currentTarget as HTMLDivElement).style.background = 'transparent'; (e.currentTarget as HTMLDivElement).style.border = '1px solid transparent'; }
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 2 }}>
                <div className="font-data" style={{ fontSize: sc(11), fontWeight: 700, color: active ? '#58a6ff' : '#7a8898', letterSpacing: '0.04em', display: 'flex', alignItems: 'center', gap: 4 }}>
                  {isSpread && <span style={{ fontSize: sc(8), color: active ? 'rgba(88,166,255,0.6)' : '#2d3a4a', letterSpacing: 0 }}>⇌</span>}
                  {inst.instrument_id}
                </div>
                {!isSpread && (
                  <button onClick={(e) => { e.stopPropagation(); handleReload(inst.file_path, inst.instrument_id); }} title="Reload from file"
                    style={{ background: 'none', border: 'none', cursor: 'pointer', padding: '1px 3px', borderRadius: 2, color: 'var(--amr-text-dim)', fontSize: sc(10), lineHeight: 1 }}
                    onMouseEnter={(e) => { (e.currentTarget as HTMLButtonElement).style.color = '#58a6ff'; }}
                    onMouseLeave={(e) => { (e.currentTarget as HTMLButtonElement).style.color = 'var(--amr-text-dim)'; }}>
                    ↺
                  </button>
                )}
              </div>
              <div className="font-data" style={{ fontSize: sc(10), color: 'var(--amr-text-dim)' }}>
                {inst.start_date} – {inst.end_date}
              </div>
              <div className="font-data" style={{ fontSize: sc(10), color: '#1e2833', marginTop: 1 }}>
                {inst.row_count.toLocaleString()} bars
              </div>
            </div>
          );
        })}
      </div>
    </aside>
  );
}
