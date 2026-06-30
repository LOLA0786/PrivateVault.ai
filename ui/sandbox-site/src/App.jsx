import { useState } from 'react';

const ENDPOINTS = [
  {
    method: 'POST',
    path: '/v1/enforce',
    desc: 'Submit an agent intent for pre-execution enforcement',
    color: '#10b981',
    defaultBody: JSON.stringify({
      agent_id: 'loan-agent-01',
      action: 'transfer_funds',
      amount: 5000000,
      recipient: 'HDFC-4821-XXXX',
      domain: 'BFSI',
      context: { itrs_income: 2100000, bank_deposits: 1200000 }
    }, null, 2),
  },
  {
    method: 'POST',
    path: '/v1/pii/scan',
    desc: 'Scan LLM output for PII and redact before delivery',
    color: '#a78bfa',
    defaultBody: JSON.stringify({
      content: 'Customer: Rahul Sharma, PAN: ABCDE1234F, Phone: 9876543210, Email: rahul@gmail.com',
      policy: 'DPDP_2023',
      redact: true
    }, null, 2),
  },
  {
    method: 'POST',
    path: '/v1/consensus',
    desc: 'Submit multi-agent votes for Byzantine consensus evaluation',
    color: '#00b4ff',
    defaultBody: JSON.stringify({
      decision_id: 'credit-committee-001',
      agents: [
        { id: 'agent-1', vote: 'ALLOW', trust_score: 0.92 },
        { id: 'agent-2', vote: 'ALLOW', trust_score: 0.88 },
        { id: 'agent-3', vote: 'BLOCK', trust_score: 0.21 },
        { id: 'agent-4', vote: 'ALLOW', trust_score: 0.95 },
        { id: 'agent-5', vote: 'BLOCK', trust_score: 0.19 },
        { id: 'agent-6', vote: 'ALLOW', trust_score: 0.91 },
        { id: 'agent-7', vote: 'BLOCK', trust_score: 0.22 },
        { id: 'agent-8', vote: 'ALLOW', trust_score: 0.89 },
        { id: 'agent-9', vote: 'ALLOW', trust_score: 0.94 }
      ]
    }, null, 2),
  },
  {
    method: 'POST',
    path: '/v1/drift/detect',
    desc: 'Detect numerical or semantic drift between instruction and agent output',
    color: '#f59e0b',
    defaultBody: JSON.stringify({
      original_instruction: { action: 'wire_transfer', amount: 1478590, currency: 'USD' },
      agent_output: { action: 'wire_transfer', amount: 14785990, currency: 'USD' },
      threshold_pct: 10
    }, null, 2),
  },
  {
    method: 'GET',
    path: '/v1/audit/{intent_hash}',
    desc: 'Retrieve Merkle-chained audit entry for a decision',
    color: '#00e5c3',
    defaultBody: 'intent_hash: a3f9c2e14d88b7c1',
  },
  {
    method: 'POST',
    path: '/v1/context/verify',
    desc: 'Verify retrieved RAG documents for context poisoning',
    color: '#ef4444',
    defaultBody: JSON.stringify({
      documents: [
        { id: 'policy-001', content: 'Claims above Rs 500L require medical board approval', hash: '8f3a...' }
      ],
      expected_hashes: { 'policy-001': '2c91...' }
    }, null, 2),
  },
];

function mockResponse(endpoint) {
  const latency = Math.floor(Math.random() * 3) + 1;
  const hash = Math.random().toString(36).slice(2, 14);
  const ts = new Date().toISOString();

  if (endpoint.path === '/v1/enforce') {
    return {
      decision: 'BLOCK',
      reason: 'Income falsification detected — ITR Rs 21,00,000 vs bank deposits Rs 12,00,000 (75% mismatch)',
      policy_triggered: 'INCOME_VERIFICATION_MISMATCH',
      intent_hash: hash,
      merkle_entry: `${hash} -> ${Math.random().toString(36).slice(2,14)}`,
      latency_ms: latency,
      timestamp: ts,
      audit_logged: true,
      compliance: ['RBI_FREE_AI', 'SOC2']
    };
  }
  if (endpoint.path === '/v1/pii/scan') {
    return {
      pii_detected: true,
      count: 3,
      findings: [
        { type: 'PAN', value: 'ABCDE****', position: 28 },
        { type: 'PHONE', value: '98765*****', position: 48 },
        { type: 'EMAIL', value: 'r***@gmail.com', position: 58 }
      ],
      sanitized_output: 'Customer: Rahul Sharma, PAN: [REDACTED], Phone: [REDACTED], Email: [REDACTED]',
      dpdp_compliant: true,
      latency_ms: latency,
      timestamp: ts
    };
  }
  if (endpoint.path === '/v1/consensus') {
    return {
      consensus: 'ALLOW',
      honest_quorum: 6,
      adversarial_detected: 3,
      adversarial_agents: ['agent-3', 'agent-5', 'agent-7'],
      accuracy: '99.65%',
      byzantine_resilient: true,
      merkle_proof: hash,
      latency_ms: latency + 1,
      timestamp: ts
    };
  }
  if (endpoint.path === '/v1/drift/detect') {
    return {
      drift_detected: true,
      drift_type: 'NUMERICAL',
      original_amount: 1478590,
      agent_amount: 14785990,
      deviation_pct: 900,
      pattern: 'DECIMAL_POINT_HALLUCINATION',
      action: 'BLOCK',
      financial_impact_prevented: '$13,307,400',
      latency_ms: latency,
      timestamp: ts
    };
  }
  if (endpoint.path.includes('audit')) {
    return {
      intent_hash: 'a3f9c2e14d88b7c1',
      previous_hash: '0000000000000000',
      decision: 'BLOCK',
      agent_id: 'loan-agent-01',
      action: 'transfer_funds',
      policy: 'INCOME_VERIFICATION_MISMATCH',
      timestamp: ts,
      merkle_valid: true,
      tamper_evident: true,
      replay_available: true
    };
  }
  if (endpoint.path === '/v1/context/verify') {
    return {
      poisoning_detected: true,
      documents_checked: 1,
      tampered: [{ id: 'policy-001', expected: '2c91...', actual: '8f3a...', status: 'TAMPERED' }],
      action: 'BLOCK',
      context_integrity: false,
      latency_ms: latency,
      timestamp: ts
    };
  }
  return { status: 'ok', latency_ms: latency, timestamp: ts };
}

export default function App() {
  const [active, setActive] = useState(0);
  const [body, setBody] = useState(ENDPOINTS[0].defaultBody);
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [dark, setDark] = useState(true);

  const selectEndpoint = (i) => {
    setActive(i);
    setBody(ENDPOINTS[i].defaultBody);
    setResponse(null);
  };

  const execute = async () => {
    setLoading(true);
    setResponse(null);
    await new Promise(r => setTimeout(r, 800 + Math.random() * 400));
    setResponse(mockResponse(ENDPOINTS[active]));
    setLoading(false);
  };

  const ep = ENDPOINTS[active];

  return (
    <div style={{ background: dark ? '#0a0e1a' : '#f8fafc', minHeight: '100vh', fontFamily: 'Inter, system-ui, sans-serif', color: dark ? '#f0f4ff' : '#0f172a' }}>
      <style>{'@import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap");'}</style>

      <header style={{ position: 'sticky', top: 0, zIndex: 100, background: dark ? 'rgba(10,14,26,0.92)' : 'rgba(248,250,252,0.92)', backdropFilter: 'blur(12px)', borderBottom: '1px solid rgba(255,255,255,0.08)', height: '56px', display: 'flex', alignItems: 'center', padding: '0 32px', justifyContent: 'space-between' }}>
        <a href='https://privatevault.ai' style={{ display: 'flex', alignItems: 'center', gap: '10px', textDecoration: 'none' }}>
          <svg width='28' height='28' viewBox='0 0 28 28' fill='none'>
            <rect width='28' height='28' rx='6' fill='#00e5c3' fillOpacity='0.12' />
            <path d='M14 5L20 8.5V15.5C20 18.5 17.5 21.2 14 22.5C10.5 21.2 8 18.5 8 15.5V8.5L14 5Z' stroke='#00e5c3' strokeWidth='1.5' strokeLinejoin='round' fill='none' />
            <path d='M11.5 14L13.5 16L17 12' stroke='#00e5c3' strokeWidth='1.5' strokeLinecap='round' strokeLinejoin='round' />
          </svg>
          <div>
            <div style={{ fontWeight: 700, fontSize: '0.875rem', color: dark ? '#f0f4ff' : '#0f172a', lineHeight: 1 }}>PrivateVault <span style={{ color: '#00e5c3' }}>AI</span></div>
            <div style={{ fontSize: '0.6875rem', color: '#4a5578', lineHeight: 1, marginTop: '2px' }}>API Sandbox</div>
          </div>
        </a>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <span style={{ fontSize: '0.75rem', color: '#4a5578', fontFamily: 'JetBrains Mono, monospace' }}>v1.0 · Mock API</span>
          <a href='https://demo.privatevault.ai' style={{ fontSize: '0.8125rem', color: '#8b9cc8', textDecoration: 'none' }}>← Demo Environment</a>
          <button onClick={() => setDark(d => !d)} style={{ width: 32, height: 32, borderRadius: '8px', border: '1px solid rgba(255,255,255,0.1)', background: 'rgba(255,255,255,0.05)', cursor: 'pointer', fontSize: '0.875rem' }}>{dark ? '☀️' : '🌙'}</button>
          <a href='mailto:chandan.galani@privatevault.ai' style={{ padding: '6px 16px', borderRadius: '8px', background: '#00e5c3', color: '#000', fontWeight: 600, fontSize: '0.8125rem', textDecoration: 'none' }}>Get API Access</a>
        </div>
      </header>

      <div style={{ background: dark ? '#0f1524' : '#fff', borderBottom: '1px solid rgba(255,255,255,0.06)', padding: '24px 32px' }}>
        <div style={{ maxWidth: '1400px', margin: '0 auto' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '8px' }}>
            <div style={{ padding: '3px 10px', borderRadius: '20px', background: 'rgba(0,229,195,0.12)', border: '1px solid rgba(0,229,195,0.25)', fontSize: '0.6875rem', fontWeight: 600, color: '#00e5c3', letterSpacing: '0.06em', textTransform: 'uppercase' }}>API Sandbox</div>
            <div style={{ padding: '3px 10px', borderRadius: '20px', background: 'rgba(245,158,11,0.1)', border: '1px solid rgba(245,158,11,0.25)', fontSize: '0.6875rem', fontWeight: 600, color: '#f59e0b', letterSpacing: '0.06em', textTransform: 'uppercase' }}>Mock Responses</div>
          </div>
          <h1 style={{ fontSize: '1.5rem', fontWeight: 800, margin: '0 0 6px', letterSpacing: '-0.02em' }}>PrivateVault AI — API Reference</h1>
          <p style={{ margin: 0, color: '#8b9cc8', fontSize: '0.875rem' }}>
            Test enforcement endpoints interactively. Mock API returns realistic enforcement responses. Production API available on request.
          </p>
        </div>
      </div>

      <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '24px 32px', display: 'grid', gridTemplateColumns: '300px 1fr', gap: '24px', alignItems: 'start' }}>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', position: 'sticky', top: '72px' }}>
          <div style={{ fontSize: '0.6875rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em', color: '#4a5578', marginBottom: '8px', paddingLeft: '4px' }}>Endpoints</div>
          {ENDPOINTS.map((ep, i) => (
            <button key={i} onClick={() => selectEndpoint(i)} style={{
              display: 'flex', alignItems: 'flex-start', gap: '10px', padding: '12px 14px',
              borderRadius: '8px', border: active === i ? `1px solid ${ep.color}40` : '1px solid rgba(255,255,255,0.06)',
              background: active === i ? `${ep.color}10` : dark ? '#0f1524' : '#fff',
              cursor: 'pointer', textAlign: 'left', transition: 'all 0.15s ease',
              fontFamily: 'inherit',
            }}>
              <span style={{ padding: '2px 6px', borderRadius: '4px', background: ep.color + '20', color: ep.color, fontSize: '0.625rem', fontWeight: 700, letterSpacing: '0.04em', fontFamily: 'JetBrains Mono, monospace', flexShrink: 0, marginTop: '1px' }}>{ep.method}</span>
              <div>
                <div style={{ fontFamily: 'JetBrains Mono, monospace', fontSize: '0.75rem', color: active === i ? ep.color : dark ? '#f0f4ff' : '#0f172a', fontWeight: 500, lineHeight: 1.3 }}>{ep.path}</div>
                <div style={{ fontSize: '0.6875rem', color: '#4a5578', lineHeight: 1.4, marginTop: '3px' }}>{ep.desc}</div>
              </div>
            </button>
          ))}
          <div style={{ marginTop: '16px', padding: '14px', borderRadius: '8px', background: dark ? '#0f1524' : '#fff', border: '1px solid rgba(255,255,255,0.06)' }}>
            <div style={{ fontSize: '0.6875rem', fontWeight: 600, color: '#4a5578', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '10px' }}>Base URL</div>
            <div style={{ fontFamily: 'JetBrains Mono, monospace', fontSize: '0.75rem', color: '#00e5c3', wordBreak: 'break-all' }}>https://api.privatevault.ai</div>
            <div style={{ fontSize: '0.6875rem', color: '#4a5578', marginTop: '8px' }}>Auth: Bearer token required in production</div>
          </div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div style={{ background: dark ? '#0f1524' : '#fff', border: '1px solid rgba(255,255,255,0.06)', borderRadius: '12px', overflow: 'hidden' }}>
            <div style={{ padding: '14px 18px', borderBottom: '1px solid rgba(255,255,255,0.06)', background: dark ? '#141c2e' : '#f8fafc', display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span style={{ padding: '3px 8px', borderRadius: '4px', background: ep.color + '20', color: ep.color, fontSize: '0.75rem', fontWeight: 700, fontFamily: 'JetBrains Mono, monospace' }}>{ep.method}</span>
              <span style={{ fontFamily: 'JetBrains Mono, monospace', fontSize: '0.875rem', color: dark ? '#f0f4ff' : '#0f172a' }}>https://api.privatevault.ai{ep.path}</span>
            </div>
            <div style={{ padding: '16px 18px' }}>
              <div style={{ fontSize: '0.6875rem', fontWeight: 600, color: '#4a5578', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '8px' }}>
                {ep.method === 'GET' ? 'Parameters' : 'Request Body'}
              </div>
              <textarea
                value={body}
                onChange={e => setBody(e.target.value)}
                style={{
                  width: '100%', minHeight: '180px', padding: '14px', borderRadius: '8px',
                  background: dark ? '#0a0e1a' : '#f8fafc',
                  border: '1px solid rgba(255,255,255,0.08)',
                  color: '#00e5c3', fontFamily: 'JetBrains Mono, monospace', fontSize: '0.8125rem',
                  lineHeight: 1.6, resize: 'vertical', outline: 'none', boxSizing: 'border-box',
                }}
              />
              <button onClick={execute} disabled={loading} style={{
                marginTop: '12px', padding: '10px 24px', borderRadius: '8px',
                background: loading ? 'rgba(255,255,255,0.05)' : '#00e5c3',
                border: 'none', color: loading ? '#4a5578' : '#000',
                fontWeight: 700, fontSize: '0.875rem', cursor: loading ? 'wait' : 'pointer',
                fontFamily: 'inherit', transition: 'all 0.15s ease',
              }}>
                {loading ? 'Executing...' : `▶  Execute ${ep.method} ${ep.path.split('/').pop()}`}
              </button>
            </div>
          </div>

          {response && (
            <div style={{ background: dark ? '#0f1524' : '#fff', border: '1px solid rgba(16,185,129,0.3)', borderRadius: '12px', overflow: 'hidden' }}>
              <div style={{ padding: '14px 18px', borderBottom: '1px solid rgba(255,255,255,0.06)', background: dark ? '#141c2e' : '#f8fafc', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <span style={{ width: 8, height: 8, borderRadius: '50%', background: '#10b981', display: 'inline-block', boxShadow: '0 0 6px #10b981' }} />
                  <span style={{ fontSize: '0.8125rem', fontWeight: 600, color: '#10b981' }}>200 OK</span>
                </div>
                <span style={{ fontFamily: 'JetBrains Mono, monospace', fontSize: '0.6875rem', color: '#4a5578' }}>
                  {response.latency_ms}ms · application/json
                </span>
              </div>
              <pre style={{
                margin: 0, padding: '18px', fontFamily: 'JetBrains Mono, monospace',
                fontSize: '0.8125rem', lineHeight: 1.6,
                color: dark ? '#f0f4ff' : '#0f172a', overflow: 'auto',
                maxHeight: '400px',
              }}>
                {JSON.stringify(response, null, 2)
                  .replace(/"BLOCK"/g, '"\u001b[31mBLOCK\u001b[0m"')
                }
              </pre>
            </div>
          )}

          <div style={{ background: dark ? '#0f1524' : '#fff', border: '1px solid rgba(255,255,255,0.06)', borderRadius: '12px', padding: '20px' }}>
            <div style={{ fontSize: '0.75rem', fontWeight: 600, color: '#4a5578', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '14px' }}>Quick Code Examples</div>
            <div style={{ fontFamily: 'JetBrains Mono, monospace', fontSize: '0.775rem', lineHeight: 1.7, color: '#8b9cc8', background: dark ? '#0a0e1a' : '#f8fafc', padding: '14px', borderRadius: '8px', overflow: 'auto' }}>
              <code style={{ display: 'block', whiteSpace: 'pre', color: '#8b9cc8' }}>{`# Python SDK
import privatevault
client = privatevault.Client(api_key="pv_live_...")

# Enforce before execution
result = client.enforce(
    agent_id="loan-agent-01",
    action="transfer_funds",
    amount=5000000
)

if result.decision == "ALLOW":
    # proceed with execution
    execute_transfer()`}</code>
            </div>
          </div>
        </div>
      </div>

      <footer style={{ borderTop: '1px solid rgba(255,255,255,0.06)', background: dark ? '#0f1524' : '#fff', padding: '20px 32px', textAlign: 'center', marginTop: '24px' }}>
        <p style={{ margin: 0, fontSize: '0.8125rem', color: '#4a5578' }}>
          Mock API for evaluation. Production API access: <a href='mailto:chandan.galani@privatevault.ai' style={{ color: '#00e5c3', textDecoration: 'none' }}>chandan.galani@privatevault.ai</a>
          <span style={{ margin: '0 8px' }}>·</span>
          <a href='https://privatevault.ai' style={{ color: '#00e5c3', textDecoration: 'none' }}>privatevault.ai</a>
        </p>
      </footer>
    </div>
  );
}
