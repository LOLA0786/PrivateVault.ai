import { useState } from 'react';

const NAV_LINKS = [
  { label: 'Demos', href: '#demos' },
  { label: 'Why Us', href: '#why-us' },
  { label: 'Pricing', href: '#pricing' },
  { label: 'Book Demo', href: '#demo' },
];

const PULSE_CSS = '@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.4}}';

function LogoMark() {
  return (
    <svg width='28' height='28' viewBox='0 0 28 28' fill='none'>
      <rect width='28' height='28' rx='6' fill='var(--color-accent)' fillOpacity='0.12' />
      <path d='M14 5L20 8.5V15.5C20 18.5 17.5 21.2 14 22.5C10.5 21.2 8 18.5 8 15.5V8.5L14 5Z' stroke='var(--color-accent)' strokeWidth='1.5' strokeLinejoin='round' fill='none' />
      <path d='M11.5 14L13.5 16L17 12' stroke='var(--color-accent)' strokeWidth='1.5' strokeLinecap='round' strokeLinejoin='round' />
    </svg>
  );
}

function NavLink({ href, label }) {
  const [hov, setHov] = useState(false);
  const base = { padding: '6px 12px', borderRadius: 'var(--radius-md)', fontSize: '0.8125rem', fontWeight: 500, textDecoration: 'none', transition: 'all var(--transition-fast)' };
  const on  = { ...base, color: 'var(--color-text-primary)', background: 'var(--color-bg-elevated)' };
  const off = { ...base, color: 'var(--color-text-secondary)', background: 'transparent' };
  return <a href={href} style={hov ? on : off} onMouseEnter={() => setHov(true)} onMouseLeave={() => setHov(false)}>{label}</a>;
}

export default function Navbar({ dark, toggleTheme }) {
  return (
    <header style={{ position: 'sticky', top: 0, zIndex: 100, background: 'rgba(10,14,26,0.9)', backdropFilter: 'blur(12px)', WebkitBackdropFilter: 'blur(12px)', borderBottom: '1px solid var(--color-border)', height: '56px', display: 'flex', alignItems: 'center', padding: '0 var(--space-8)', gap: 'var(--space-8)' }}>
      <style>{PULSE_CSS}</style>
      <a href='/' style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)', textDecoration: 'none', flexShrink: 0 }}>
        <LogoMark />
        <span style={{ fontWeight: 700, fontSize: '0.9375rem', color: 'var(--color-text-primary)', letterSpacing: '-0.01em' }}>
          PrivateVault<span style={{ color: 'var(--color-accent)' }}> AI</span>
        </span>
      </a>
      <nav style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-1)', flex: 1 }}>
        {NAV_LINKS.map(l => <NavLink key={l.label} href={l.href} label={l.label} />)}
      </nav>
      <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)', flexShrink: 0 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', padding: '4px 10px', borderRadius: '20px', background: 'rgba(16,185,129,0.08)', border: '1px solid rgba(16,185,129,0.2)', fontSize: '0.75rem', fontWeight: 500, color: 'var(--color-success)' }}>
          <span style={{ width: 6, height: 6, borderRadius: '50%', background: 'var(--color-success)', display: 'inline-block', boxShadow: '0 0 6px var(--color-success)', animation: 'pulse 2s infinite' }} />
          All Systems Operational
        </div>
        <button onClick={toggleTheme} title='Toggle theme' style={{ width: 36, height: 36, borderRadius: 'var(--radius-md)', border: '1px solid var(--color-border-strong)', background: 'var(--color-bg-elevated)', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1rem', color: 'var(--color-text-secondary)', flexShrink: 0 }}>
          {dark ? '☀️' : '🌙'}
        </button>
        <a href='mailto:chandan.galani@privatevault.ai' style={{ display: 'inline-flex', alignItems: 'center', padding: '6px 16px', borderRadius: 'var(--radius-md)', background: 'var(--color-accent)', color: '#000', fontWeight: 600, fontSize: '0.8125rem', textDecoration: 'none' }}>
          Request Pilot
        </a>
      </div>
    </header>
  );
}
