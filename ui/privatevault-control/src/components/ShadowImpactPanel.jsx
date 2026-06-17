import { useState, useEffect } from 'react';

const VIOLATION_FEED = [
  { type: 'BLOCK',  msg: 'PII export blocked — loan-agent-01',    time: '04:40:07' },
  { type: 'BLOCK',  msg: 'Unauthorised trade — trade-agent-06',   time: '04:39:51' },
  { type: 'REVIEW', msg: 'Prescription anomaly — rx-agent-03',    time: '04:39:43' },
  { type: 'BLOCK',  msg: 'CDR mass query — fraud-agent-02',       time: '04:39:31' },
  { type: 'REVIEW', msg: 'Credit threshold breach — risk-agent-04', time: '04:39:18' },
];

const NEW_VIOLATIONS = [
  'Prompt injection attempt — kyc-agent-07',
  'PII batch export — doc-agent-11',
  'Anomalous transfer — loan-agent-01',
  'Policy drift detected — risk-agent-04',
  'Replay attack blocked — trade-agent-06',
];

function VBadge({ type }) {
  const isBlock = type === 'BLOCK';
  return (
    <span style={{
      fontSize: '0.625rem', fontWeight: 700, letterSpacing: '0.06em',
      padding: '1px 6px', borderRadius: '3px',
      color: isBlock ? 'var(--color-block)' : 'var(--color-review)',
      background: isBlock ? 'var(--color-block-bg)' : 'var(--color-review-bg)',
    }}>
      {type}
    </span>
  );
}

export default function ShadowImpactPanel() {
  const [blocked,  setBlocked]  = useState(12);
  const [exposure, setExposure] = useState(4280000);
  const [violations, setViolations] = useState(VIOLATION_FEED);

  useEffect(() => {
    const t = setInterval(() => {
      const addBlock = Math.random() > 0.55;
      if (addBlock) {
        setBlocked(b => b + 1);
        setExposure(e => e + Math.floor(Math.random() * 250000 + 50000));
        const msg = NEW_VIOLATIONS[Math.floor(Math.random() * NEW_VIOLATIONS.length)];
        const type = Math.random() > 0.4 ? 'BLOCK' : 'REVIEW';
        const now = new Date().toISOString().slice(11, 19);
        setViolations(v => [{ type, msg, time: now }, ...v.slice(0, 7)]);
      }
    }, 2800);
    return () => clearInterval(t);
  }, []);

  const fmtCurrency = n => {
    if (n >= 1000000) return '$' + (n / 1000000).toFixed(2) + 'M';
    return '$' + (n / 1000).toFixed(0) + 'K';
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-4)' }}>

      <div style={{ background: 'var(--color-bg-card)', border: '1px solid var(--color-border)', borderRadius: 'var(--radius-lg)', overflow: 'hidden' }}>
        <div style={{ padding: '14px 16px', borderBottom: '1px solid var(--color-border)', background: 'var(--color-bg-elevated)', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <h4 style={{ margin: 0, fontSize: '0.6875rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--color-text-muted)' }}>
            Shadow Impact
          </h4>
          <span style={{ fontSize: '0.625rem', color: 'var(--color-text-muted)', fontFamily: 'var(--font-mono)' }}>LIVE</span>
        </div>

        <div style={{ padding: '16px' }}>
          <div style={{ marginBottom: '16px', paddingBottom: '16px', borderBottom: '1px solid var(--color-border)' }}>
            <div style={{ fontSize: '0.6875rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--color-text-muted)', marginBottom: '6px' }}>
              Threats Blocked
            </div>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '2rem', fontWeight: 700, color: 'var(--color-block)', lineHeight: 1 }}>
              {blocked}
            </div>
            <div style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)', marginTop: '4px' }}>this session</div>
          </div>

          <div style={{ marginBottom: '16px', paddingBottom: '16px', borderBottom: '1px solid var(--color-border)' }}>
            <div style={{ fontSize: '0.6875rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--color-text-muted)', marginBottom: '6px' }}>
              Exposure Prevented
            </div>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '1.5rem', fontWeight: 700, color: 'var(--color-success)', lineHeight: 1 }}>
              {fmtCurrency(exposure)}
            </div>
            <div style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)', marginTop: '4px' }}>estimated risk value</div>
          </div>

          <div>
            <div style={{ fontSize: '0.6875rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--color-text-muted)', marginBottom: '10px' }}>
              Enforcement Breakdown
            </div>
            {[
              { label: 'Allowed',  pct: 68, color: 'var(--color-allow)'  },
              { label: 'Review',   pct: 21, color: 'var(--color-review)' },
              { label: 'Blocked',  pct: 11, color: 'var(--color-block)'  },
            ].map(b => (
              <div key={b.label} style={{ marginBottom: '8px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '3px' }}>
                  <span style={{ fontSize: '0.75rem', color: 'var(--color-text-secondary)' }}>{b.label}</span>
                  <span style={{ fontSize: '0.75rem', fontFamily: 'var(--font-mono)', color: b.color }}>{b.pct}%</span>
                </div>
                <div style={{ height: '4px', borderRadius: '2px', background: 'var(--color-bg-base)', overflow: 'hidden' }}>
                  <div style={{ height: '100%', width: b.pct + '%', background: b.color, borderRadius: '2px', transition: 'width 0.6s ease' }} />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div style={{ background: 'var(--color-bg-card)', border: '1px solid var(--color-border)', borderRadius: 'var(--radius-lg)', overflow: 'hidden' }}>
        <div style={{ padding: '14px 16px', borderBottom: '1px solid var(--color-border)', background: 'var(--color-bg-elevated)' }}>
          <h4 style={{ margin: 0, fontSize: '0.6875rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--color-text-muted)' }}>
            Violation Log
          </h4>
        </div>
        <div style={{ padding: '8px 0' }}>
          {violations.map((v, i) => (
            <div key={i} style={{ display: 'flex', alignItems: 'flex-start', gap: '8px', padding: '8px 14px', borderBottom: i < violations.length - 1 ? '1px solid var(--color-border)' : 'none' }}>
              <VBadge type={v.type} />
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--color-text-secondary)', lineHeight: 1.4, wordBreak: 'break-word' }}>{v.msg}</div>
                <div style={{ fontSize: '0.6875rem', fontFamily: 'var(--font-mono)', color: 'var(--color-text-muted)', marginTop: '2px' }}>{v.time}</div>
              </div>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}
