import { useState } from 'react';
import DemosSection from './components/DemosSection';
import DemoLibrary from './components/DemoLibrary';

export default function App() {
  const [dark, setDark] = useState(true);
  return (
    <div style={{ background: dark ? 'var(--color-bg-base)' : '#f8fafc', minHeight: '100vh', fontFamily: 'var(--font-sans)', transition: 'background 0.3s ease' }}>

      <header style={{ position: 'sticky', top: 0, zIndex: 100, background: 'rgba(10,14,26,0.92)', backdropFilter: 'blur(12px)', borderBottom: '1px solid var(--color-border)', height: '56px', display: 'flex', alignItems: 'center', padding: '0 var(--space-8)', justifyContent: 'space-between' }}>
        <a href='https://privatevault.ai' style={{ display: 'flex', alignItems: 'center', gap: '10px', textDecoration: 'none' }}>
          <svg width='28' height='28' viewBox='0 0 28 28' fill='none'>
            <rect width='28' height='28' rx='6' fill='var(--color-accent)' fillOpacity='0.12' />
            <path d='M14 5L20 8.5V15.5C20 18.5 17.5 21.2 14 22.5C10.5 21.2 8 18.5 8 15.5V8.5L14 5Z' stroke='var(--color-accent)' strokeWidth='1.5' strokeLinejoin='round' fill='none' />
            <path d='M11.5 14L13.5 16L17 12' stroke='var(--color-accent)' strokeWidth='1.5' strokeLinecap='round' strokeLinejoin='round' />
          </svg>
          <div>
            <div style={{ fontWeight: 700, fontSize: '0.875rem', color: 'var(--color-text-primary)', lineHeight: 1 }}>PrivateVault <span style={{ color: 'var(--color-accent)' }}>AI</span></div>
            <div style={{ fontSize: '0.6875rem', color: 'var(--color-text-muted)', lineHeight: 1, marginTop: '2px' }}>Interactive Demo Environment</div>
          </div>
        </a>
        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-4)' }}>
          <a href='https://privatevault.ai/sandbox' style={{ fontSize: '0.8125rem', color: 'var(--color-text-secondary)', textDecoration: 'none' }}>API Sandbox →</a>
          <button onClick={() => setDark(d => !d)} style={{ width: 32, height: 32, borderRadius: 'var(--radius-md)', border: '1px solid var(--color-border)', background: 'var(--color-bg-elevated)', cursor: 'pointer', fontSize: '0.875rem' }}>{dark ? '☀️' : '🌙'}</button>
          <a href='mailto:chandan.galani@privatevault.ai' style={{ padding: '6px 16px', borderRadius: 'var(--radius-md)', background: 'var(--color-accent)', color: '#000', fontWeight: 600, fontSize: '0.8125rem', textDecoration: 'none' }}>Book Live Demo</a>
        </div>
      </header>

      <div style={{ background: 'var(--color-bg-surface)', borderBottom: '1px solid var(--color-border)', padding: '32px var(--space-8)' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', textAlign: 'center' }}>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', padding: '4px 12px', borderRadius: '20px', background: 'var(--color-accent-dim)', border: '1px solid rgba(0,229,195,0.25)', fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-accent)', letterSpacing: '0.06em', textTransform: 'uppercase', marginBottom: '12px' }}>
            Live Demo Environment
          </div>
          <h1 style={{ fontSize: 'clamp(1.5rem, 3vw, 2.25rem)', fontWeight: 800, color: 'var(--color-text-primary)', margin: '0 0 10px', letterSpacing: '-0.02em' }}>
            See PrivateVault AI Enforce Policy in Real Time
          </h1>
          <p style={{ color: 'var(--color-text-muted)', fontSize: '0.9375rem', margin: '0 0 24px', maxWidth: '560px', marginLeft: 'auto', marginRight: 'auto' }}>
            17 real-world enforcement scenarios. Click any demo and watch pre-execution interception step by step.
          </p>
          <div style={{ display: 'flex', gap: '32px', justifyContent: 'center', flexWrap: 'wrap' }}>
            {[['17', 'Enforcement Scenarios'], ['<2ms', 'Decision Latency'], ['99.65%', 'Consensus Accuracy'], ['100%', 'Pre-Execution']].map(([v,l]) => (
              <div key={l} style={{ textAlign: 'center' }}>
                <div style={{ fontFamily: 'var(--font-mono)', fontSize: '1.5rem', fontWeight: 700, color: 'var(--color-accent)' }}>{v}</div>
                <div style={{ fontSize: '0.6875rem', color: 'var(--color-text-muted)', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.06em', marginTop: '4px' }}>{l}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <DemosSection />
      <DemoLibrary />

      <footer style={{ borderTop: '1px solid var(--color-border)', background: 'var(--color-bg-surface)', padding: '24px var(--space-8)', textAlign: 'center' }}>
        <p style={{ margin: 0, fontSize: '0.8125rem', color: 'var(--color-text-muted)' }}>
          These are simulated enforcement demos using synthetic data. 
          <a href='https://privatevault.ai' style={{ color: 'var(--color-accent)', textDecoration: 'none', marginLeft: '8px' }}>privatevault.ai</a>
          <span style={{ margin: '0 8px' }}>·</span>
          <a href='mailto:chandan.galani@privatevault.ai' style={{ color: 'var(--color-accent)', textDecoration: 'none' }}>chandan.galani@privatevault.ai</a>
          <span style={{ margin: '0 8px' }}>·</span>
          <a href='https://wa.me/919326176427' style={{ color: 'var(--color-accent)', textDecoration: 'none' }}>WhatsApp</a>
        </p>
      </footer>
    </div>
  );
}
