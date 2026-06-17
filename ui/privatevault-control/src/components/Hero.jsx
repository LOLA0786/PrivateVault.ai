export default function Hero() {
  return (
    <section style={{
      padding: '80px var(--space-8) 64px',
      maxWidth: '1600px',
      margin: '0 auto',
      width: '100%',
    }}>
      <div style={{ maxWidth: '720px' }}>

        <div style={{
          display: 'inline-flex', alignItems: 'center', gap: '8px',
          padding: '4px 12px', borderRadius: '20px',
          background: 'var(--color-accent-dim)',
          border: '1px solid rgba(0,229,195,0.25)',
          fontSize: '0.75rem', fontWeight: 600,
          color: 'var(--color-accent)',
          letterSpacing: '0.06em', textTransform: 'uppercase',
          marginBottom: '24px',
        }}>
          <span style={{ width: 6, height: 6, borderRadius: '50%', background: 'var(--color-accent)', display: 'inline-block' }} />
          Runtime Governance Layer for Enterprise AI
        </div>

        <h1 style={{
          fontSize: 'clamp(2rem, 4vw, 3.25rem)',
          fontWeight: 800,
          lineHeight: 1.15,
          letterSpacing: '-0.03em',
          color: 'var(--color-text-primary)',
          marginBottom: '24px',
        }}>
          Stop AI Agents<br />
          <span style={{
            background: 'linear-gradient(135deg, var(--color-accent) 0%, #00b4ff 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
          }}>
            Before They Act Wrong
          </span>
        </h1>

        <p style={{
          fontSize: '1.0625rem',
          color: 'var(--color-text-secondary)',
          lineHeight: 1.75,
          marginBottom: '40px',
          maxWidth: '560px',
        }}>
          PrivateVault AI enforces policy <em style={{ color: 'var(--color-text-primary)', fontStyle: 'normal' }}>before execution</em> —
          not after. Pre-execution intent verification, PII protection, Byzantine fault-tolerant
          multi-agent consensus, and Merkle-chained immutable audit ledgers for regulated enterprises.
        </p>

        <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
          <a href='mailto:chandan@privatevault.ai' style={{
            display: 'inline-flex', alignItems: 'center', gap: '8px',
            padding: '12px 28px', borderRadius: 'var(--radius-md)',
            background: 'var(--color-accent)', color: '#000',
            fontWeight: 700, fontSize: '0.9375rem', textDecoration: 'none',
            boxShadow: '0 0 32px var(--color-accent-glow)',
            transition: 'all var(--transition-base)',
          }}>
            Request a Pilot
            <svg width='16' height='16' viewBox='0 0 16 16' fill='none'>
              <path d='M3 8h10M9 4l4 4-4 4' stroke='currentColor' strokeWidth='1.5' strokeLinecap='round' strokeLinejoin='round'/>
            </svg>
          </a>
          <a href='https://github.com/LOLA0786/privatevault-mcp' target='_blank' rel='noreferrer' style={{
            display: 'inline-flex', alignItems: 'center', gap: '8px',
            padding: '12px 24px', borderRadius: 'var(--radius-md)',
            background: 'var(--color-bg-elevated)',
            border: '1px solid var(--color-border-strong)',
            color: 'var(--color-text-primary)',
            fontWeight: 500, fontSize: '0.9375rem', textDecoration: 'none',
            transition: 'all var(--transition-base)',
          }}>
            <svg width='16' height='16' viewBox='0 0 16 16' fill='currentColor'>
              <path d='M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z'/>
            </svg>
            View on GitHub
          </a>
        </div>

        <div style={{
          display: 'flex', gap: '32px', marginTop: '48px',
          paddingTop: '32px',
          borderTop: '1px solid var(--color-border)',
          flexWrap: 'wrap',
        }}>
          {[
            { value: '99.65%', label: 'Consensus Accuracy' },
            { value: '<2ms',   label: 'Enforcement Latency' },
            { value: '100%',   label: 'Pre-Execution' },
            { value: 'SOC 2',  label: 'Audit Ready' },
          ].map(stat => (
            <div key={stat.label}>
              <div style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--color-accent)', lineHeight: 1 }}>
                {stat.value}
              </div>
              <div style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)', marginTop: '4px', fontWeight: 500, textTransform: 'uppercase', letterSpacing: '0.06em' }}>
                {stat.label}
              </div>
            </div>
          ))}
        </div>

      </div>
    </section>
  );
}
