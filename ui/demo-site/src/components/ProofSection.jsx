export default function ProofSection() {
  const proofs = [
    { stat: '10,000+', label: 'Agent decisions benchmarked', sub: 'across simulation trials' },
    { stat: '<2ms',    label: 'Pre-execution enforcement', sub: 'avg interception latency' },
    { stat: '99.65%',  label: 'Consensus accuracy', sub: 'at 33% Byzantine adversarial' },
    { stat: '0.1ms',   label: 'Agent isolation speed', sub: 'deterministic enforcement' },
    { stat: '17',      label: 'Formal invariants tested', sub: 'property-based test suite' },
    { stat: '100%',    label: 'Pre-execution coverage', sub: 'no post-execution exposure' },
  ];

  const trust = [
    { label: 'NVIDIA Inception', color: '#76b900' },
    { label: 'SOC 2 Ready',      color: '#00e5c3' },
    { label: 'RBI FREE-AI',      color: '#00b4ff' },
    { label: 'MAS TRM',          color: '#a78bfa' },
    { label: 'APRA CPS 234',     color: '#f59e0b' },
    { label: 'EU AI Act',        color: '#00e5c3' },
    { label: 'DPDP 2023',        color: '#00b4ff' },
    { label: 'HIPAA',            color: '#10b981' },
  ];

  return (
    <section style={{ borderTop: '1px solid var(--color-border)', background: 'var(--color-bg-surface)' }}>

      <div style={{ padding: 'var(--space-10) var(--space-8)', maxWidth: '1200px', margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '40px' }}>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', padding: '4px 12px', borderRadius: '20px', background: 'var(--color-accent-dim)', border: '1px solid rgba(0,229,195,0.25)', fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-accent)', letterSpacing: '0.06em', textTransform: 'uppercase', marginBottom: '16px' }}>
            Proof, Not Promises
          </div>
          <h2 style={{ margin: '0 0 12px', color: 'var(--color-text-primary)', letterSpacing: '-0.02em' }}>
            Numbers That Matter to a CISO
          </h2>
          <p style={{ margin: 0, color: 'var(--color-text-muted)', fontSize: '0.9375rem' }}>
            Every metric is from real benchmarks. No marketing numbers.
          </p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(6, 1fr)', gap: '1px', background: 'var(--color-border)', borderRadius: 'var(--radius-lg)', overflow: 'hidden', marginBottom: '48px' }}>
          {proofs.map(p => (
            <div key={p.stat} style={{ background: 'var(--color-bg-card)', padding: '24px 20px', textAlign: 'center' }}>
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: '1.75rem', fontWeight: 800, color: 'var(--color-accent)', lineHeight: 1, marginBottom: '8px' }}>{p.stat}</div>
              <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-text-primary)', marginBottom: '4px', lineHeight: 1.3 }}>{p.label}</div>
              <div style={{ fontSize: '0.6875rem', color: 'var(--color-text-muted)' }}>{p.sub}</div>
            </div>
          ))}
        </div>

        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '0.6875rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--color-text-muted)', marginBottom: '16px' }}>Compliance & Recognition</div>
          <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', justifyContent: 'center' }}>
            {trust.map(t => (
              <div key={t.label} style={{ padding: '6px 14px', borderRadius: '20px', background: 'var(--color-bg-elevated)', border: '1px solid var(--color-border)', fontSize: '0.75rem', fontWeight: 700, color: t.color, letterSpacing: '0.04em' }}>
                {t.label}
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
