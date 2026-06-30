const CASES = [
  {
    icon: '🏦', industry: 'Banking & BFSI',
    tag: 'RBI FREE-AI · MAS TRM · SOC 2',
    risk: 'AI credit agent approves Rs 50L loan on falsified ITR. No human sees it.',
    solution: 'PrivateVault cross-references ITR, GST, bank statements before approval. Discrepancy detected. Action blocked. Audit logged.',
    metrics: ['Rs 50L prevented per incident', 'RBI FREE-AI compliant audit', '100% pre-execution'],
  },
  {
    icon: '🚨', industry: 'Government & Law Enforcement',
    tag: 'DPDP 2023 · Evidence Integrity',
    risk: 'Cyber Cell voice AI freezes wrong bank account based on misheard complaint. Citizen sues.',
    solution: 'PrivateVault validates evidence before action. Wrong account identified. Escalated to human officer. Legal liability prevented.',
    metrics: ['Zero wrongful actions', 'Full replay evidence', 'Human escalation gates'],
  },
  {
    icon: '🏥', industry: 'Healthcare',
    tag: 'HIPAA · DPDP · Clinical Safety',
    risk: 'LLM returns patient PAN, phone, diagnosis in plaintext to downstream billing system.',
    solution: 'PrivateVault intercepts LLM output, redacts 6 PII fields before delivery. HIPAA and DPDP compliant. Logged and auditable.',
    metrics: ['6 PII fields redacted', 'Zero downstream exposure', 'HIPAA audit ready'],
  },
  {
    icon: '🏛️', industry: 'Insurance & Risk',
    tag: 'IRDAI · APRA CPS 234',
    risk: 'AI claims agent approves fraudulent claim based on context-poisoned documents.',
    solution: 'PrivateVault validates document integrity before agent acts. Poisoned context detected. Claim escalated for human review.',
    metrics: ['Context poisoning blocked', 'Fraud prevented pre-execution', 'IRDAI audit export'],
  },
  {
    icon: '⚡', industry: 'Critical Infrastructure',
    tag: 'ICS Security · Zero Trust',
    risk: 'Multi-agent system reaches wrong consensus when 3 of 9 nodes are compromised.',
    solution: 'Byzantine fault-tolerant consensus isolates adversarial agents. Correct decision reached with 6/6 honest quorum. Cryptographic proof.',
    metrics: ['99.65% accuracy at 33% adversarial', 'Cryptographic consensus proof', 'Immutable decision log'],
  },
  {
    icon: '🏢', industry: 'Enterprise SaaS',
    tag: 'SOC 2 · EU AI Act · ISO 27001',
    risk: 'AI agents waste 40-60% of LLM context on redundant, policy-violating content. Token costs spiral.',
    solution: 'PrivateVault WasteEngine eliminates redundant context before execution. Governance pays for itself in token cost reduction.',
    metrics: ['40-60% context waste eliminated', 'LLM cost reduction', 'EU AI Act compliant'],
  },
];

export default function IndustriesSection() {
  return (
    <section id='industries' style={{ padding: 'var(--space-12) var(--space-8)', borderTop: '1px solid var(--color-border)', background: 'var(--color-bg-surface)' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '48px' }}>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', padding: '4px 12px', borderRadius: '20px', background: 'var(--color-accent-dim)', border: '1px solid rgba(0,229,195,0.25)', fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-accent)', letterSpacing: '0.06em', textTransform: 'uppercase', marginBottom: '16px' }}>
            Industry Use Cases
          </div>
          <h2 style={{ margin: '0 0 12px', color: 'var(--color-text-primary)', letterSpacing: '-0.02em' }}>Built for Regulated Industries</h2>
          <p style={{ margin: 0, color: 'var(--color-text-muted)', fontSize: '0.9375rem', maxWidth: '520px', marginLeft: 'auto', marginRight: 'auto' }}>
            Real risks. Real prevention. Click any industry to see exactly what PrivateVault stops.
          </p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '20px' }}>
          {CASES.map((c, i) => (
            <div key={i} style={{ background: 'var(--color-bg-card)', border: '1px solid var(--color-border)', borderRadius: 'var(--radius-lg)', padding: '24px', transition: 'border-color 0.2s, transform 0.2s' }}
              onMouseEnter={e => { e.currentTarget.style.borderColor = 'var(--color-accent)'; e.currentTarget.style.transform = 'translateY(-2px)'; }}
              onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--color-border)'; e.currentTarget.style.transform = 'none'; }}
            >
              <div style={{ fontSize: '1.75rem', marginBottom: '10px' }}>{c.icon}</div>
              <div style={{ fontSize: '0.875rem', fontWeight: 700, color: 'var(--color-text-primary)', marginBottom: '4px' }}>{c.industry}</div>
              <div style={{ fontSize: '0.6875rem', color: 'var(--color-accent)', fontWeight: 600, letterSpacing: '0.04em', marginBottom: '16px' }}>{c.tag}</div>

              <div style={{ marginBottom: '14px' }}>
                <div style={{ fontSize: '0.6875rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.07em', color: 'var(--color-block)', marginBottom: '6px' }}>The Risk</div>
                <p style={{ margin: 0, fontSize: '0.8125rem', color: 'var(--color-text-muted)', lineHeight: 1.6 }}>{c.risk}</p>
              </div>

              <div style={{ marginBottom: '16px' }}>
                <div style={{ fontSize: '0.6875rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.07em', color: 'var(--color-allow)', marginBottom: '6px' }}>PrivateVault Response</div>
                <p style={{ margin: 0, fontSize: '0.8125rem', color: 'var(--color-text-secondary)', lineHeight: 1.6 }}>{c.solution}</p>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                {c.metrics.map(m => (
                  <div key={m} style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>
                    <span style={{ color: 'var(--color-accent)', fontWeight: 700 }}>→</span> {m}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
