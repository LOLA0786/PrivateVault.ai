import { useState, useEffect } from 'react';

const MOCK = [
  { timestamp: '2026-06-17T04:01:12Z', domain: 'BFSI',       actor: 'loan-agent-01',    action: 'transfer_funds',      decision: 'BLOCK',  intent_hash: 'a3f9c2e14d88' },
  { timestamp: '2026-06-17T04:01:09Z', domain: 'Healthcare',  actor: 'rx-agent-03',     action: 'write_prescription',  decision: 'REVIEW', intent_hash: 'b7d1a0f23c91' },
  { timestamp: '2026-06-17T04:01:07Z', domain: 'BFSI',       actor: 'kyc-agent-07',     action: 'verify_identity',     decision: 'ALLOW',  intent_hash: 'c2e8b5a91d44' },
  { timestamp: '2026-06-17T04:01:05Z', domain: 'Telecom',    actor: 'fraud-agent-02',   action: 'query_cdr',           decision: 'ALLOW',  intent_hash: 'd4f0c7b32e10' },
  { timestamp: '2026-06-17T04:01:02Z', domain: 'Government', actor: 'doc-agent-11',     action: 'export_pii_batch',    decision: 'BLOCK',  intent_hash: 'e9a3d1c08f72' },
  { timestamp: '2026-06-17T04:00:59Z', domain: 'BFSI',       actor: 'risk-agent-04',    action: 'approve_credit',      decision: 'REVIEW', intent_hash: 'f1b6e4a27c53' },
  { timestamp: '2026-06-17T04:00:55Z', domain: 'Healthcare',  actor: 'claims-agent-09', action: 'process_claim',       decision: 'ALLOW',  intent_hash: '02c9f5d38b61' },
  { timestamp: '2026-06-17T04:00:51Z', domain: 'BFSI',       actor: 'trade-agent-06',   action: 'execute_trade',       decision: 'BLOCK',  intent_hash: '13d0a6e49c70' },
];

const BADGE = {
  ALLOW:  { color: 'var(--color-allow)',  bg: 'var(--color-allow-bg)',  label: 'ALLOW'  },
  REVIEW: { color: 'var(--color-review)', bg: 'var(--color-review-bg)', label: 'REVIEW' },
  BLOCK:  { color: 'var(--color-block)',  bg: 'var(--color-block-bg)',  label: 'BLOCK'  },
};

function DecisionBadge({ decision }) {
  const s = BADGE[decision] || BADGE.REVIEW;
  return (
    <span style={{
      display: 'inline-flex', alignItems: 'center', gap: '4px',
      padding: '2px 8px', borderRadius: '4px',
      background: s.bg, color: s.color,
      fontSize: '0.6875rem', fontWeight: 700,
      letterSpacing: '0.06em',
    }}>
      <span style={{ width: 5, height: 5, borderRadius: '50%', background: s.color, display: 'inline-block' }} />
      {s.label}
    </span>
  );
}

export default function IntentTable() {
  const [rows, setRows] = useState(MOCK);

  useEffect(() => {
    const ACTIONS  = ['transfer_funds','query_cdr','write_prescription','export_pii_batch','approve_credit','execute_trade','verify_identity'];
    const DOMAINS  = ['BFSI','Healthcare','Telecom','Government'];
    const ACTORS   = ['loan-agent-01','rx-agent-03','kyc-agent-07','fraud-agent-02','risk-agent-04','trade-agent-06'];
    const DECISIONS= ['ALLOW','ALLOW','ALLOW','REVIEW','BLOCK'];
    const rand = arr => arr[Math.floor(Math.random() * arr.length)];

    const t = setInterval(() => {
      const newRow = {
        timestamp: new Date().toISOString(),
        domain: rand(DOMAINS),
        actor: rand(ACTORS),
        action: rand(ACTIONS),
        decision: rand(DECISIONS),
        intent_hash: Math.random().toString(36).slice(2, 14),
      };
      setRows(prev => [newRow, ...prev.slice(0, 19)]);
    }, 2200);
    return () => clearInterval(t);
  }, []);

  const fmt = ts => ts.slice(11, 19);

  return (
    <div style={{ padding: '0 0 var(--space-8)' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 'var(--space-4)', padding: '0 2px' }}>
        <div>
          <h3 style={{ margin: 0, color: 'var(--color-text-primary)' }}>Live Intent Stream</h3>
          <p style={{ margin: '2px 0 0', fontSize: '0.8125rem', color: 'var(--color-text-muted)' }}>
            Real-time pre-execution enforcement decisions
          </p>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.75rem', color: 'var(--color-success)', fontWeight: 500 }}>
          <span style={{ width: 6, height: 6, borderRadius: '50%', background: 'var(--color-success)', display: 'inline-block', animation: 'pulse 1.5s infinite' }} />
          LIVE
        </div>
      </div>

      <div style={{ background: 'var(--color-bg-card)', border: '1px solid var(--color-border)', borderRadius: 'var(--radius-lg)', overflow: 'hidden' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.8125rem' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid var(--color-border)', background: 'var(--color-bg-elevated)' }}>
              {['Time','Domain','Actor','Action','Decision','Hash'].map(h => (
                <th key={h} style={{ padding: '10px 16px', textAlign: 'left', fontSize: '0.6875rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--color-text-muted)', whiteSpace: 'nowrap' }}>
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((r, i) => (
              <tr key={r.intent_hash + i} style={{ borderBottom: '1px solid var(--color-border)', transition: 'background var(--transition-fast)' }}
                onMouseEnter={e => e.currentTarget.style.background = 'var(--color-bg-elevated)'}
                onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
              >
                <td style={{ padding: '10px 16px', fontFamily: 'var(--font-mono)', fontSize: '0.75rem', color: 'var(--color-text-muted)', whiteSpace: 'nowrap' }}>{fmt(r.timestamp)}</td>
                <td style={{ padding: '10px 16px', color: 'var(--color-text-secondary)', whiteSpace: 'nowrap' }}>{r.domain}</td>
                <td style={{ padding: '10px 16px', fontFamily: 'var(--font-mono)', fontSize: '0.75rem', color: 'var(--color-text-primary)', whiteSpace: 'nowrap' }}>{r.actor}</td>
                <td style={{ padding: '10px 16px', fontFamily: 'var(--font-mono)', fontSize: '0.75rem', color: 'var(--color-accent)', whiteSpace: 'nowrap' }}>{r.action}</td>
                <td style={{ padding: '10px 16px' }}><DecisionBadge decision={r.decision} /></td>
                <td style={{ padding: '10px 16px', fontFamily: 'var(--font-mono)', fontSize: '0.7rem', color: 'var(--color-text-muted)' }}>{r.intent_hash.slice(0,10)}…</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
