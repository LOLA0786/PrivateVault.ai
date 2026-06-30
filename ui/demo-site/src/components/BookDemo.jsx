import { useState } from 'react';

const SHEET_ID = '1Rp4-pnhiS1q7A6YamrfJOYPROjHM6VxMCEERIvoDZE0';
const SHEET_URL = 'https://script.google.com/macros/s/PASTE_SCRIPT_ID_HERE/exec';

export default function BookDemo() {
  const [form, setForm] = useState({ name: '', company: '', email: '', role: '', agents: '', message: '' });
  const [status, setStatus] = useState('idle');
  const set = k => e => setForm(f => ({ ...f, [k]: e.target.value }));

  const submit = async () => {
    if (!form.name || !form.email || !form.company) return;
    setStatus('sending');
    try {
      const params = new URLSearchParams({ ...form, timestamp: new Date().toISOString(), sheet_id: SHEET_ID });
      await fetch(SHEET_URL + '?' + params, { method: 'GET', mode: 'no-cors' });
    } catch {}
    setStatus('done');
  };

  const inp = {
    width: '100%', padding: '10px 14px',
    background: 'var(--color-bg-base)',
    border: '1px solid var(--color-border-strong)',
    borderRadius: 'var(--radius-md)',
    color: 'var(--color-text-primary)',
    fontSize: '0.875rem', fontFamily: 'var(--font-sans)',
    outline: 'none', boxSizing: 'border-box',
  };

  return (
    <section id='demo' style={{ padding: 'var(--space-12) var(--space-8)', borderTop: '1px solid var(--color-border)' }}>
      <div style={{ maxWidth: '640px', margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '40px' }}>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', padding: '4px 12px', borderRadius: '20px', background: 'var(--color-accent-dim)', border: '1px solid rgba(0,229,195,0.25)', fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-accent)', letterSpacing: '0.06em', textTransform: 'uppercase', marginBottom: '16px' }}>
            Book a Demo
          </div>
          <h2 style={{ margin: '0 0 12px', color: 'var(--color-text-primary)' }}>See PrivateVault in Your Environment</h2>
          <p style={{ margin: 0, color: 'var(--color-text-muted)', fontSize: '0.9375rem' }}>
            30-minute live session. Engineers on the call. We connect to your agent stack and show real-time enforcement.
          </p>
        </div>

        {status === 'done' ? (
          <div style={{ textAlign: 'center', padding: '48px', background: 'var(--color-bg-card)', border: '1px solid var(--color-accent)', borderRadius: 'var(--radius-xl)' }}>
            <div style={{ fontSize: '2.5rem', marginBottom: '16px' }}>✓</div>
            <h3 style={{ color: 'var(--color-accent)', margin: '0 0 8px' }}>Request Received</h3>
            <p style={{ color: 'var(--color-text-muted)', margin: '0 0 16px' }}>Chandan will reach out within 24 hours.</p>
            <div style={{ display: 'flex', justifyContent: 'center', gap: '12px', flexWrap: 'wrap' }}>
              <a href='https://wa.me/919326176427' target='_blank' rel='noreferrer' style={{ padding: '8px 18px', borderRadius: 'var(--radius-md)', background: '#25d366', color: '#fff', fontWeight: 600, fontSize: '0.875rem', textDecoration: 'none' }}>WhatsApp Chandan</a>
              <a href='mailto:chandan.galani@privatevault.ai' style={{ padding: '8px 18px', borderRadius: 'var(--radius-md)', border: '1px solid var(--color-border)', color: 'var(--color-text-primary)', fontWeight: 500, fontSize: '0.875rem', textDecoration: 'none' }}>Send Email</a>
            </div>
          </div>
        ) : (
          <div style={{ background: 'var(--color-bg-card)', border: '1px solid var(--color-border)', borderRadius: 'var(--radius-xl)', padding: '32px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
              <div><label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '6px' }}>Full Name *</label><input style={inp} placeholder='Sameer Gupta' value={form.name} onChange={set('name')} /></div>
              <div><label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '6px' }}>Company *</label><input style={inp} placeholder='Lloyds Banking Group' value={form.company} onChange={set('company')} /></div>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
              <div><label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '6px' }}>Work Email *</label><input style={inp} type='email' placeholder='you@company.com' value={form.email} onChange={set('email')} /></div>
              <div><label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '6px' }}>Role</label><input style={inp} placeholder='CISO / Chief AI Officer' value={form.role} onChange={set('role')} /></div>
            </div>
            <div><label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '6px' }}>AI Agents in Production</label><input style={inp} placeholder='e.g. 12' value={form.agents} onChange={set('agents')} /></div>
            <div><label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '6px' }}>What are you trying to govern?</label><textarea style={{ ...inp, height: '88px', resize: 'vertical' }} placeholder='e.g. LLM agents doing loan approvals, fraud detection...' value={form.message} onChange={set('message')} /></div>
            <button onClick={submit} disabled={status === 'sending'} style={{ padding: '13px', borderRadius: 'var(--radius-md)', background: 'var(--color-accent)', border: 'none', color: '#000', fontWeight: 700, fontSize: '0.9375rem', cursor: status === 'sending' ? 'wait' : 'pointer', fontFamily: 'var(--font-sans)', opacity: status === 'sending' ? 0.7 : 1 }}>
              {status === 'sending' ? 'Sending...' : 'Book a 30-min Demo →'}
            </button>
            <p style={{ textAlign: 'center', margin: 0, fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>No sales pitch. Engineers on the call. Or <a href='https://wa.me/919326176427' target='_blank' rel='noreferrer' style={{ color: 'var(--color-accent)', textDecoration: 'none' }}>WhatsApp us directly</a>.</p>
          </div>
        )}
      </div>
    </section>
  );
}
