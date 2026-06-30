export default function Footer() {
  return (
    <footer style={{ borderTop: '1px solid var(--color-border)', background: 'var(--color-bg-surface)', padding: 'var(--space-10) var(--space-8) var(--space-8)' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr 1fr 1fr', gap: '48px', marginBottom: '48px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
              <svg width='28' height='28' viewBox='0 0 28 28' fill='none'>
                <rect width='28' height='28' rx='6' fill='var(--color-accent)' fillOpacity='0.12' />
                <path d='M14 5L20 8.5V15.5C20 18.5 17.5 21.2 14 22.5C10.5 21.2 8 18.5 8 15.5V8.5L14 5Z' stroke='var(--color-accent)' strokeWidth='1.5' strokeLinejoin='round' fill='none' />
                <path d='M11.5 14L13.5 16L17 12' stroke='var(--color-accent)' strokeWidth='1.5' strokeLinecap='round' strokeLinejoin='round' />
              </svg>
              <span style={{ fontWeight: 700, fontSize: '0.9375rem', color: 'var(--color-text-primary)' }}>PrivateVault <span style={{ color: 'var(--color-accent)' }}>AI</span></span>
            </div>
            <p style={{ fontSize: '0.8125rem', color: 'var(--color-text-muted)', lineHeight: 1.7, maxWidth: '280px', margin: '0 0 12px' }}>
              Runtime AI governance and control layer for enterprise AI agents. Pre-execution enforcement for regulated industries.
            </p>
            <p style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)', margin: '0 0 8px' }}>
              A product of <span style={{ color: 'var(--color-text-secondary)' }}>Pentaprime Solutions, Inc.</span>
            </p>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
              <a href='mailto:chandan.galani@privatevault.ai' style={{ fontSize: '0.8125rem', color: 'var(--color-accent)', textDecoration: 'none' }}>chandan.galani@privatevault.ai</a>
              <a href='https://wa.me/919326176427' target='_blank' rel='noreferrer' style={{ fontSize: '0.8125rem', color: 'var(--color-accent)', textDecoration: 'none' }}>WhatsApp: +91-9326176427</a>
            </div>
          </div>

          <div>
            <div style={{ fontSize: '0.6875rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--color-text-muted)', marginBottom: '16px' }}>Product</div>
            {[['How it Works','#why-us'],['Demos','#demos'],['Pricing','#pricing'],['Book Demo','#demo'],['GitHub','https://github.com/LOLA0786/PrivateVault.ai']].map(([l,h]) => (
              <div key={l} style={{ marginBottom: '10px' }}>
                <a href={h} target={h.startsWith('http') ? '_blank' : undefined} rel='noreferrer' style={{ fontSize: '0.8125rem', color: 'var(--color-text-secondary)', textDecoration: 'none' }}>{l}</a>
              </div>
            ))}
          </div>

          <div>
            <div style={{ fontSize: '0.6875rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--color-text-muted)', marginBottom: '16px' }}>Compliance</div>
            {['SOC 2 Type II','RBI FREE-AI','MAS TRM','APRA CPS 234','EU AI Act','DPDP Act 2023','HIPAA'].map(l => (
              <div key={l} style={{ marginBottom: '10px' }}>
                <span style={{ fontSize: '0.8125rem', color: 'var(--color-text-secondary)' }}>{l}</span>
              </div>
            ))}
          </div>

          <div>
            <div style={{ fontSize: '0.6875rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--color-text-muted)', marginBottom: '16px' }}>Connect</div>
            {[
              ['LinkedIn (Company)','https://www.linkedin.com/company/106346972/'],
              ['Founder — Chandan Galani','https://www.linkedin.com/in/chandangalani/'],
              ['GitHub','https://github.com/LOLA0786/PrivateVault.ai'],
              ['WhatsApp','https://wa.me/919326176427'],
              ['Email Us','mailto:chandan.galani@privatevault.ai'],
            ].map(([l,h]) => (
              <div key={l} style={{ marginBottom: '10px' }}>
                <a href={h} target='_blank' rel='noreferrer' style={{ fontSize: '0.8125rem', color: 'var(--color-text-secondary)', textDecoration: 'none' }}>{l}</a>
              </div>
            ))}
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingTop: '24px', borderTop: '1px solid var(--color-border)', flexWrap: 'wrap', gap: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flexWrap: 'wrap' }}>
            {['NVIDIA Inception','SOC 2','MAS TRM','RBI FREE-AI','DPDP 2023'].map(badge => (
              <div key={badge} style={{ padding: '4px 10px', borderRadius: '4px', background: 'var(--color-bg-elevated)', border: '1px solid var(--color-border)', fontSize: '0.6875rem', fontWeight: 600, color: 'var(--color-text-muted)', letterSpacing: '0.04em' }}>{badge}</div>
            ))}
          </div>
          <p style={{ margin: 0, fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>© 2026 Pentaprime Solutions, Inc. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}
