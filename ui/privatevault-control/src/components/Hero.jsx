export default function Hero() {
  return (
    <section style={{ padding: '72px var(--space-8) 56px', maxWidth: '1600px', margin: '0 auto', width: '100%' }}>
      <div style={{ maxWidth: '780px' }}>

        <div style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', padding: '4px 14px', borderRadius: '20px', background: 'var(--color-accent-dim)', border: '1px solid rgba(0,229,195,0.3)', fontSize: '0.75rem', fontWeight: 700, color: 'var(--color-accent)', letterSpacing: '0.08em', textTransform: 'uppercase', marginBottom: '28px' }}>
          <span style={{ width: 6, height: 6, borderRadius: '50%', background: 'var(--color-accent)', display: 'inline-block' }} />
          Decision Security Control Plane · NVIDIA Inception Member
        </div>

        <h1 style={{ fontSize: 'clamp(2.25rem, 4.5vw, 3.75rem)', fontWeight: 800, lineHeight: 1.1, letterSpacing: '-0.03em', color: 'var(--color-text-primary)', marginBottom: '12px' }}>
          Prevent AI Agents From<br />
          <span style={{ background: 'linear-gradient(135deg, #00e5c3 0%, #00b4ff 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text' }}>
            Making Costly Decisions
          </span>
        </h1>

        <p style={{ fontSize: '1.125rem', color: 'var(--color-text-secondary)', lineHeight: 1.7, marginBottom: '16px', maxWidth: '620px', fontWeight: 400 }}>
          <strong style={{ color: 'var(--color-text-primary)', fontWeight: 600 }}>Enforce policy. Validate intent. Block unsafe actions before execution.</strong>
        </p>

        <p style={{ fontSize: '0.9375rem', color: 'var(--color-text-muted)', lineHeight: 1.75, marginBottom: '40px', maxWidth: '580px' }}>
          PrivateVault sits between your AI agents and execution. Every agent decision is intercepted, verified against policy, and either allowed, reviewed, or blocked — with a cryptographic audit trail regulators can verify.
        </p>

        <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap', marginBottom: '56px' }}>
          <a href='#demo' style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', padding: '13px 28px', borderRadius: 'var(--radius-md)', background: 'var(--color-accent)', color: '#000', fontWeight: 700, fontSize: '0.9375rem', textDecoration: 'none', boxShadow: '0 0 32px rgba(0,229,195,0.3)', transition: 'all 0.2s ease' }}>
            Book a Demo
            <svg width='16' height='16' viewBox='0 0 16 16' fill='none'><path d='M3 8h10M9 4l4 4-4 4' stroke='currentColor' strokeWidth='1.5' strokeLinecap='round' strokeLinejoin='round'/></svg>
          </a>
          <a href='#demos' style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', padding: '13px 24px', borderRadius: 'var(--radius-md)', background: 'var(--color-bg-elevated)', border: '1px solid var(--color-border-strong)', color: 'var(--color-text-primary)', fontWeight: 500, fontSize: '0.9375rem', textDecoration: 'none' }}>
            See Runtime in Action →
          </a>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, auto)', gap: '32px', paddingTop: '32px', borderTop: '1px solid var(--color-border)', width: 'fit-content' }}>
          {[
            { value: '99.65%', label: 'Consensus Accuracy' },
            { value: '<2ms',   label: 'Pre-Execution Latency' },
            { value: '10K+',   label: 'Agent Decisions Benchmarked' },
            { value: 'Zero',   label: 'Post-Execution Exposure' },
          ].map(s => (
            <div key={s.label}>
              <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--color-accent)', lineHeight: 1, fontFamily: 'var(--font-mono)' }}>{s.value}</div>
              <div style={{ fontSize: '0.6875rem', color: 'var(--color-text-muted)', marginTop: '5px', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.07em' }}>{s.label}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
