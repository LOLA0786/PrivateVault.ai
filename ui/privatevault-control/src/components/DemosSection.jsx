import { useState } from 'react';

const PII_RAW = 'Rahul Sharma | rahul@gmail.com | 9876543210 | PAN: ABCDE1234F\nPriya Singh | priya@gmail.com | 9988776655 | PAN: FGHIJ5678K';
const PII_CLEAN = '[NAME REDACTED] | [EMAIL REDACTED] | [PHONE REDACTED] | PAN: [REDACTED]\n[NAME REDACTED] | [EMAIL REDACTED] | [PHONE REDACTED] | PAN: [REDACTED]';
const AGENT_VOTES = 'Agent 1: ALLOW | Agent 2: ALLOW | Agent 3: BLOCK (adversarial)\nAgent 4: ALLOW | Agent 5: BLOCK (adversarial) | Agent 6: ALLOW\nAgent 7: BLOCK (adversarial) | Agent 8: ALLOW | Agent 9: ALLOW';

const DEMOS = [
  {
    id: 'sbi', label: 'SBI Lending', icon: '\u{1F3E6}', tag: 'BFSI', tagColor: 'var(--color-accent)',
    title: 'AI Credit Underwriter — Income Falsification Blocked',
    description: 'AI agent recommends a large loan approval based on falsified ITR. PrivateVault intercepts before any bank action.',
    steps: [
      { phase: 'Agent Input',      icon: '\u{1F916}', content: 'Loan application submitted. ITR shows income: Rs 21,00,000. AI recommends APPROVE Rs 50,00,000.', decision: null },
      { phase: 'PV Check',         icon: '\u{1F50D}', content: 'Cross-referencing ITR with GST returns, bank statements, Form 26AS. Extracting verified income signals.', decision: null },
      { phase: 'Evidence Mismatch',icon: '\u26A0\uFE0F', content: 'MISMATCH DETECTED — ITR: Rs 21,00,000 | Bank deposits: Rs 12,00,000 | GST turnover: Rs 8,40,000. Discrepancy: 75%.', decision: 'BLOCK' },
      { phase: 'Audit Entry',      icon: '\u{1F510}', content: 'Merkle-chained entry logged. Hash: a3f9c2e1... Intent bound to evidence. Cannot be altered post-decision.', decision: 'LOGGED' },
    ],
  },
  {
    id: 'pii', label: 'PII Intercept', icon: '\u{1F6E1}\uFE0F', tag: 'DATA PRIVACY', tagColor: '#a78bfa',
    title: 'LLM Response PII Redaction — Runtime',
    description: 'LLM returns customer records with PAN, phone, email in plaintext. PrivateVault sanitizes before downstream systems receive it.',
    steps: [
      { phase: 'LLM Raw Output',   icon: '\u{1F916}', content: PII_RAW, decision: null },
      { phase: 'PII Scanner',      icon: '\u{1F50D}', content: 'Scanning for: EMAIL, PHONE, PAN, AADHAAR, DOB, ADDRESS patterns. Found 6 PII instances across 2 records.', decision: null },
      { phase: 'Redaction Applied',icon: '\u2705',    content: PII_CLEAN, decision: 'REDACTED' },
      { phase: 'Audit Entry',      icon: '\u{1F510}', content: 'PII interception logged. 6 fields redacted. DPDP Act 2023 compliant. Downstream system receives sanitized output only.', decision: 'LOGGED' },
    ],
  },
  {
    id: 'cyber', label: 'Cyber Cell', icon: '\u{1F6A8}', tag: 'GOV / LAW ENFORCEMENT', tagColor: '#f59e0b',
    title: 'Mumbai Cyber Cell — Wrong Account Freeze Prevented',
    description: 'Voice AI processes fraud complaint and outputs freeze order for wrong account. PrivateVault intercepts before police action.',
    steps: [
      { phase: 'Citizen Report',   icon: '\u{1F4DE}', content: 'Citizen: "I transferred Rs 2,50,000 to a fraud account after receiving a fake banking call from 9876543210."', decision: null },
      { phase: 'AI Agent Output',  icon: '\u{1F916}', content: 'Freeze account: 9821 | Notify telecom: 9876543210 | Generate FIR automatically.', decision: null },
      { phase: 'PV Check',         icon: '\u{1F50D}', content: 'EVIDENCE MISMATCH — Account 9821 is the VICTIM account. Fraud recipient not identified. Action would freeze wrong party.', decision: 'BLOCK' },
      { phase: 'Corrected Action', icon: '\u2705',    content: 'Blocked incorrect freeze. Escalated to human officer. Prevented wrongful action, legal liability, and media escalation.', decision: 'ESCALATED' },
    ],
  },
  {
    id: 'consensus', label: 'Multi-Agent Consensus', icon: '\u26A1', tag: 'BYZANTINE RESILIENCE', tagColor: '#00b4ff',
    title: 'Byzantine Fault-Tolerant Consensus — 33% Adversarial Agents',
    description: '3 of 9 agents are compromised. PrivateVault detects and excludes them, reaching correct consensus with honest agents.',
    steps: [
      { phase: 'Agent Votes (9 nodes)', icon: '\u{1F5F3}\uFE0F', content: AGENT_VOTES, decision: null },
      { phase: 'Anomaly Detection',     icon: '\u{1F50D}',        content: 'Agents 3, 5, 7 flagged: trust score < 0.3, response latency outliers, signature mismatch. Isolating adversarial nodes.', decision: null },
      { phase: 'Consensus Reached',     icon: '\u2705',           content: 'Honest quorum: 6/6 => ALLOW. Adversarial agents excluded. Accuracy: 99.65% across 1,000 trials. Decision: ALLOW with cryptographic proof.', decision: 'ALLOW' },
      { phase: 'Audit Entry',           icon: '\u{1F510}',        content: 'Full consensus trace Merkle-chained. Byzantine nodes logged with evidence. Regulators can replay every vote.', decision: 'LOGGED' },
    ],
  },
];

const DECISION_COLORS = {
  BLOCK:     { color: 'var(--color-block)',   bg: 'var(--color-block-bg)'  },
  ALLOW:     { color: 'var(--color-allow)',   bg: 'var(--color-allow-bg)'  },
  REDACTED:  { color: '#a78bfa',             bg: 'rgba(167,139,250,0.1)'  },
  ESCALATED: { color: 'var(--color-warning)', bg: 'var(--color-review-bg)' },
  LOGGED:    { color: 'var(--color-text-muted)', bg: 'var(--color-bg-elevated)' },
};

export default function DemosSection() {
  const [active, setActive] = useState('sbi');
  const [runStep, setRunStep] = useState(-1);
  const [running, setRunning] = useState(false);
  const demo = DEMOS.find(d => d.id === active);

  const runDemo = async () => {
    setRunStep(-1);
    setRunning(true);
    for (let i = 0; i < demo.steps.length; i++) {
      await new Promise(r => setTimeout(r, 900));
      setRunStep(i);
    }
    setRunning(false);
  };

  const switchDemo = (id) => { setActive(id); setRunStep(-1); setRunning(false); };

  return (
    <section id='demos' style={{ padding: 'var(--space-12) var(--space-8)', borderTop: '1px solid var(--color-border)', background: 'var(--color-bg-surface)' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '48px' }}>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', padding: '4px 12px', borderRadius: '20px', background: 'var(--color-accent-dim)', border: '1px solid rgba(0,229,195,0.25)', fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-accent)', letterSpacing: '0.06em', textTransform: 'uppercase', marginBottom: '16px' }}>
            Live Demos
          </div>
          <h2 style={{ margin: '0 0 12px', color: 'var(--color-text-primary)' }}>See Enforcement in Action</h2>
          <p style={{ margin: 0, color: 'var(--color-text-muted)', fontSize: '0.9375rem' }}>Real scenarios. Real prevention. Click any demo and run it step by step.</p>
        </div>

        <div style={{ display: 'flex', gap: '8px', marginBottom: '32px', flexWrap: 'wrap', justifyContent: 'center' }}>
          {DEMOS.map(d => (
            <button key={d.id} onClick={() => switchDemo(d.id)} style={{
              padding: '10px 20px', borderRadius: 'var(--radius-md)',
              border: active === d.id ? '1px solid var(--color-accent)' : '1px solid var(--color-border)',
              background: active === d.id ? 'var(--color-accent-dim)' : 'var(--color-bg-elevated)',
              color: active === d.id ? 'var(--color-accent)' : 'var(--color-text-secondary)',
              fontWeight: 600, fontSize: '0.875rem', cursor: 'pointer',
              fontFamily: 'var(--font-sans)', transition: 'all var(--transition-fast)',
              display: 'flex', alignItems: 'center', gap: '8px',
            }}>
              <span>{d.icon}</span>{d.label}
            </button>
          ))}
        </div>

        <div style={{ background: 'var(--color-bg-card)', border: '1px solid var(--color-border)', borderRadius: 'var(--radius-xl)', overflow: 'hidden' }}>
          <div style={{ padding: '24px 28px', borderBottom: '1px solid var(--color-border)', background: 'var(--color-bg-elevated)', display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: '16px', flexWrap: 'wrap' }}>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
                <span style={{ fontSize: '1.25rem' }}>{demo.icon}</span>
                <span style={{ fontSize: '0.6875rem', fontWeight: 700, letterSpacing: '0.08em', textTransform: 'uppercase', color: demo.tagColor, padding: '2px 8px', borderRadius: '4px', background: demo.tagColor + '22' }}>{demo.tag}</span>
              </div>
              <h3 style={{ margin: '0 0 6px', color: 'var(--color-text-primary)', fontSize: '1.0625rem' }}>{demo.title}</h3>
              <p style={{ margin: 0, fontSize: '0.8125rem', color: 'var(--color-text-muted)', maxWidth: '560px' }}>{demo.description}</p>
            </div>
            <button onClick={runDemo} disabled={running} style={{
              padding: '10px 24px', borderRadius: 'var(--radius-md)',
              background: running ? 'var(--color-bg-base)' : 'var(--color-accent)',
              border: running ? '1px solid var(--color-border)' : 'none',
              color: running ? 'var(--color-text-muted)' : '#000',
              fontWeight: 700, fontSize: '0.875rem', cursor: running ? 'wait' : 'pointer',
              fontFamily: 'var(--font-sans)', flexShrink: 0, transition: 'all var(--transition-fast)',
            }}>
              {running ? 'Running...' : runStep >= 0 ? '\u21BA Run Again' : '\u25B6 Run Demo'}
            </button>
          </div>

          <div style={{ padding: '24px 28px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {demo.steps.map((step, i) => {
              const visible = runStep >= i;
              const dc = step.decision ? DECISION_COLORS[step.decision] : null;
              return (
                <div key={i} style={{
                  display: 'flex', gap: '16px', alignItems: 'flex-start',
                  opacity: visible ? 1 : 0.2,
                  transition: 'opacity 0.4s ease',
                  padding: '16px', borderRadius: 'var(--radius-md)',
                  background: visible ? 'var(--color-bg-elevated)' : 'transparent',
                  border: visible && dc ? '1px solid ' + dc.color + '44' : '1px solid transparent',
                }}>
                  <div style={{ fontSize: '1.25rem', flexShrink: 0, marginTop: '2px' }}>{step.icon}</div>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
                      <span style={{ fontSize: '0.6875rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--color-text-muted)' }}>{step.phase}</span>
                      {dc && (
                        <span style={{ fontSize: '0.6875rem', fontWeight: 700, padding: '1px 8px', borderRadius: '4px', color: dc.color, background: dc.bg, letterSpacing: '0.06em' }}>
                          {step.decision}
                        </span>
                      )}
                    </div>
                    <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.8rem', color: 'var(--color-text-secondary)', whiteSpace: 'pre-wrap', lineHeight: 1.6 }}>
                      {step.content}
                    </div>
                  </div>
                </div>
              );
            })}
            {runStep === -1 && (
              <div style={{ textAlign: 'center', padding: '32px', color: 'var(--color-text-muted)', fontSize: '0.875rem' }}>
                Click <strong style={{ color: 'var(--color-accent)' }}>Run Demo</strong> to see enforcement step by step
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
