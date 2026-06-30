const MOATS = [
  {
    icon: '\u26A1',
    title: 'Pre-Execution Enforcement',
    subtitle: 'Not detection. Prevention.',
    body: 'Every competitor operates post-execution — scanning logs, alerting after harm. PrivateVault enforces policy before the agent acts. The action never reaches the tool if it violates policy. Zero blast radius.',
    stat: '0ms', statLabel: 'Post-execution exposure',
  },
  {
    icon: '\u{1F517}',
    title: 'Byzantine Fault-Tolerant Consensus',
    subtitle: '33% adversarial agents. Still correct.',
    body: 'Multi-agent systems fail when any node is compromised. PrivateVault consensus engine maintains 99.65% accuracy even when 1 in 3 agents is adversarial, corrupted, or injected — proven across 1,000 trials.',
    stat: '99.65%', statLabel: 'Accuracy at 33% adversarial',
  },
  {
    icon: '\u{1F9E0}',
    title: 'Intent Verification + Authority Binding',
    subtitle: 'Who ordered this action, and did they have the right?',
    body: 'Cryptographic binding of agent identity to declared intent. If an agent claims authority it was never granted, PrivateVault detects the cognitive state mismatch before execution. No other platform does this.',
    stat: '<2ms', statLabel: 'Enforcement latency',
  },
  {
    icon: '\u{1F6E1}\uFE0F',
    title: 'Context Poisoning Detection',
    subtitle: 'Compromised retrieval = compromised decision.',
    body: 'Competitors detect prompt injection at the scanning layer after context assembly. PrivateVault enforces context integrity before execution — tamper-evident chain-of-custody on every retrieved document.',
    stat: '100%', statLabel: 'Pre-execution coverage',
  },
  {
    icon: '\u{1F4D2}',
    title: 'Merkle-Chained Immutable Audit Ledger',
    subtitle: 'Every decision. Cryptographically provable. Forever.',
    body: 'Every enforcement decision is Merkle-chained — tamper-evident, append-only, and replayable. Regulators can verify any historical decision without trusting the system. SOC 2, RBI FREE-AI, MAS TRM ready.',
    stat: 'SOC 2', statLabel: 'Audit ready out of box',
  },
  {
    icon: '\u{1F4B0}',
    title: 'AI FinOps — Context Waste Engine',
    subtitle: 'Governance that pays for itself.',
    body: 'Most enterprises waste 40-60% of LLM context budget on redundant or policy-violating content. PrivateVault WasteEngine identifies and eliminates it — reducing token costs while enforcing governance simultaneously.',
    stat: '40-60%', statLabel: 'Avg context waste eliminated',
  },
];

export default function MoatSection() {
  return (
    <section id='why-us' style={{ padding: 'var(--space-12) var(--space-8)', borderTop: '1px solid var(--color-border)' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '48px' }}>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', padding: '4px 12px', borderRadius: '20px', background: 'var(--color-accent-dim)', border: '1px solid rgba(0,229,195,0.25)', fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-accent)', letterSpacing: '0.06em', textTransform: 'uppercase', marginBottom: '16px' }}>
            Defensible Moat
          </div>
          <h2 style={{ margin: '0 0 12px', color: 'var(--color-text-primary)' }}>Why No One Else Does What We Do</h2>
          <p style={{ margin: 0, color: 'var(--color-text-muted)', fontSize: '0.9375rem', maxWidth: '600px', marginLeft: 'auto', marginRight: 'auto' }}>
            Six capabilities that do not exist together anywhere else. Each one is a moat. Together they are a category.
          </p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '20px' }}>
          {MOATS.map((m, i) => (
            <div key={i} style={{
              background: 'var(--color-bg-card)',
              border: '1px solid var(--color-border)',
              borderRadius: 'var(--radius-lg)',
              padding: '28px',
              transition: 'border-color var(--transition-base), transform var(--transition-base)',
              cursor: 'default',
            }}
            onMouseEnter={e => { e.currentTarget.style.borderColor = 'var(--color-accent)'; e.currentTarget.style.transform = 'translateY(-2px)'; }}
            onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--color-border)'; e.currentTarget.style.transform = 'none'; }}
            >
              <div style={{ fontSize: '1.75rem', marginBottom: '12px' }}>{m.icon}</div>
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: '1.5rem', fontWeight: 700, color: 'var(--color-accent)', lineHeight: 1, marginBottom: '4px' }}>{m.stat}</div>
              <div style={{ fontSize: '0.6875rem', color: 'var(--color-text-muted)', fontWeight: 500, textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '14px' }}>{m.statLabel}</div>
              <h3 style={{ margin: '0 0 4px', fontSize: '0.9375rem', color: 'var(--color-text-primary)' }}>{m.title}</h3>
              <div style={{ fontSize: '0.75rem', color: 'var(--color-accent)', fontWeight: 600, marginBottom: '10px' }}>{m.subtitle}</div>
              <p style={{ margin: 0, fontSize: '0.8125rem', color: 'var(--color-text-muted)', lineHeight: 1.7 }}>{m.body}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
