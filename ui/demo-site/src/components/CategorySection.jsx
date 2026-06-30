export default function CategorySection() {
  const rows = [
    { cat: 'AI Observability',  does: 'Shows what happened after execution',      pv: false },
    { cat: 'AI Monitoring',     does: 'Tracks agent performance and drift',        pv: false },
    { cat: 'AI Governance',     does: 'Defines policies in documentation',         pv: false },
    { cat: 'AI Security',       does: 'Protects infrastructure and models',        pv: false },
    { cat: 'Agent Frameworks',  does: 'Orchestrates agent workflows',              pv: false },
    { cat: 'PrivateVault AI',   does: 'Controls decisions BEFORE execution',       pv: true  },
  ];

  return (
    <section id='category' style={{ padding: 'var(--space-12) var(--space-8)', borderTop: '1px solid var(--color-border)' }}>
      <div style={{ maxWidth: '900px', margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '48px' }}>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', padding: '4px 12px', borderRadius: '20px', background: 'var(--color-accent-dim)', border: '1px solid rgba(0,229,195,0.25)', fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-accent)', letterSpacing: '0.06em', textTransform: 'uppercase', marginBottom: '16px' }}>
            New Category
          </div>
          <h2 style={{ margin: '0 0 12px', color: 'var(--color-text-primary)', letterSpacing: '-0.02em' }}>
            Existing Tools <span style={{ color: 'var(--color-text-muted)' }}>Watch</span> AI Agents.<br />
            PrivateVault <span style={{ color: 'var(--color-accent)' }}>Controls</span> Them.
          </h2>
          <p style={{ margin: 0, color: 'var(--color-text-muted)', fontSize: '0.9375rem', maxWidth: '500px', marginLeft: 'auto', marginRight: 'auto' }}>
            Every other platform operates post-execution. We are the only control plane that intercepts decisions before they happen.
          </p>
        </div>

        <div style={{ background: 'var(--color-bg-card)', border: '1px solid var(--color-border)', borderRadius: 'var(--radius-xl)', overflow: 'hidden' }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr 120px', borderBottom: '1px solid var(--color-border)', background: 'var(--color-bg-elevated)', padding: '12px 24px' }}>
            {['Category', 'What It Does', 'Controls AI?'].map(h => (
              <div key={h} style={{ fontSize: '0.6875rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--color-text-muted)' }}>{h}</div>
            ))}
          </div>
          {rows.map((r, i) => (
            <div key={r.cat} style={{ display: 'grid', gridTemplateColumns: '1fr 2fr 120px', padding: '16px 24px', borderBottom: i < rows.length - 1 ? '1px solid var(--color-border)' : 'none', background: r.pv ? 'rgba(0,229,195,0.04)' : 'transparent', transition: 'background 0.2s' }}>
              <div style={{ fontSize: '0.875rem', fontWeight: r.pv ? 700 : 500, color: r.pv ? 'var(--color-accent)' : 'var(--color-text-primary)' }}>{r.cat}</div>
              <div style={{ fontSize: '0.875rem', color: r.pv ? 'var(--color-text-primary)' : 'var(--color-text-muted)' }}>{r.does}</div>
              <div style={{ fontSize: '0.875rem', fontWeight: 700, color: r.pv ? 'var(--color-allow)' : 'var(--color-block)' }}>{r.pv ? '✓ YES' : '✗ No'}</div>
            </div>
          ))}
        </div>

        <p style={{ textAlign: 'center', marginTop: '20px', fontSize: '0.8125rem', color: 'var(--color-text-muted)', fontStyle: 'italic' }}>
          "Decision Security Engineering" — a new category PrivateVault AI is defining.
        </p>
      </div>
    </section>
  );
}
