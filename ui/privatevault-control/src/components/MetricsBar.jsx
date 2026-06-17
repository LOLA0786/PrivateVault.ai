import { useState, useEffect } from 'react';

const METRICS = [
  { id: 'decisions', label: 'Decisions / sec', base: 847,   unit: '',   decimals: 0 },
  { id: 'blocked',   label: 'Threats Blocked', base: 12043, unit: '',   decimals: 0 },
  { id: 'latency',   label: 'Avg Latency',     base: 1.8,   unit: 'ms', decimals: 1 },
  { id: 'accuracy',  label: 'Consensus',        base: 99.65, unit: '%',  decimals: 2, max: 99.99 },
  { id: 'pii',       label: 'PII Intercepted',  base: 3821,  unit: '',   decimals: 0 },
  { id: 'uptime',    label: 'Uptime',           base: 99.98, unit: '%',  decimals: 2, max: 99.99 },
];

function tick(m) {
  const jitter = (Math.random() - 0.5) * m.base * 0.015;
  let val = m.base + jitter;
  if (m.max) val = Math.min(val, m.max);
  if (m.decimals) return val.toFixed(m.decimals);
  return Math.round(val).toLocaleString();
}

export default function MetricsBar() {
  const [vals, setVals] = useState(() =>
    Object.fromEntries(METRICS.map(m => [m.id, tick(m)]))
  );

  useEffect(() => {
    const t = setInterval(() => {
      setVals(Object.fromEntries(METRICS.map(m => [m.id, tick(m)])));
    }, 1800);
    return () => clearInterval(t);
  }, []);

  return (
    <div style={{
      borderTop: '1px solid var(--color-border)',
      borderBottom: '1px solid var(--color-border)',
      background: 'var(--color-bg-surface)',
      padding: '0 var(--space-8)',
    }}>
      <div style={{
        maxWidth: '1600px', margin: '0 auto',
        display: 'grid',
        gridTemplateColumns: 'repeat(6, 1fr)',
      }}>
        {METRICS.map((m, i) => (
          <div key={m.id} style={{
            padding: '16px 20px',
            borderLeft: i > 0 ? '1px solid var(--color-border)' : 'none',
          }}>
            <div style={{ fontSize: '0.6875rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--color-text-muted)', marginBottom: '6px' }}>
              {m.label}
            </div>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '1.25rem', fontWeight: 600, color: 'var(--color-accent)', lineHeight: 1 }}>
              {vals[m.id]}{m.unit}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
