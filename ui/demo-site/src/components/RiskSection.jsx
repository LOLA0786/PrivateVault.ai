export default function RiskSection() {
  return (
    <section style={{ borderTop: '1px solid var(--color-border)', borderBottom: '1px solid var(--color-border)', background: 'var(--color-bg-surface)', padding: 'var(--space-10) var(--space-8)' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>

        <div style={{ textAlign: 'center', marginBottom: '48px' }}>
          <h2 style={{ margin: '0 0 12px', fontSize: 'clamp(1.5rem, 3vw, 2.25rem)', color: 'var(--color-text-primary)', fontWeight: 700, letterSpacing: '-0.02em' }}>
            Every Enterprise Will Have AI Agents.<br />
            <span style={{ color: 'var(--color-accent)' }}>Who Controls Them?</span>
          </h2>
          <p style={{ margin: 0, color: 'var(--color-text-muted)', fontSize: '0.9375rem', maxWidth: '540px', marginLeft: 'auto', marginRight: 'auto' }}>
            AI agents act autonomously. Without a control plane, they execute decisions that should require human approval — and the board finds out after the damage is done.
          </p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr auto 1fr', gap: '24px', alignItems: 'start' }}>

          <div style={{ background: 'rgba(239,68,68,0.05)', border: '1px solid rgba(239,68,68,0.2)', borderRadius: 'var(--radius-xl)', padding: '32px' }}>
            <div style={{ fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--color-block)', marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span>✗</span> Without PrivateVault
            </div>
            {[
              'Unauthorized fund transfers executed',
              'AI hallucinates and takes wrong action',
              'PII leaked to downstream systems',
              'Compliance violations with no audit trail',
              'Wrong account frozen by cyber cell AI',
              'Regulatory fines with no evidence',
              'Board-level reputational risk',
            ].map(r => (
              <div key={r} style={{ display: 'flex', gap: '10px', marginBottom: '12px', alignItems: 'flex-start' }}>
                <span style={{ color: 'var(--color-block)', fontSize: '0.875rem', flexShrink: 0, marginTop: '1px' }}>✗</span>
                <span style={{ fontSize: '0.875rem', color: 'var(--color-text-secondary)', lineHeight: 1.5 }}>{r}</span>
              </div>
            ))}
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: '8px', padding: '0 8px' }}>
            <div style={{ width: 1, height: '40px', background: 'var(--color-border)' }} />
            <div style={{ width: 40, height: 40, borderRadius: '50%', background: 'var(--color-accent-dim)', border: '1px solid var(--color-accent)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1rem' }}>🛡️</div>
            <div style={{ width: 1, height: '40px', background: 'var(--color-border)' }} />
          </div>

          <div style={{ background: 'rgba(0,229,195,0.04)', border: '1px solid rgba(0,229,195,0.2)', borderRadius: 'var(--radius-xl)', padding: '32px' }}>
            <div style={{ fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--color-accent)', marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span>✓</span> With PrivateVault
            </div>
            {[
              'Every agent decision intercepted pre-execution',
              'Policy enforcement before any tool is called',
              'PII redacted before downstream delivery',
              'Merkle-chained audit trail for every decision',
              'Human approval gates on high-risk actions',
              'Regulator-ready evidence exports (RBI, MAS, SOC 2)',
              'Board-level AI risk accountability',
            ].map(r => (
              <div key={r} style={{ display: 'flex', gap: '10px', marginBottom: '12px', alignItems: 'flex-start' }}>
                <span style={{ color: 'var(--color-allow)', fontSize: '0.875rem', flexShrink: 0, marginTop: '1px' }}>✓</span>
                <span style={{ fontSize: '0.875rem', color: 'var(--color-text-secondary)', lineHeight: 1.5 }}>{r}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
