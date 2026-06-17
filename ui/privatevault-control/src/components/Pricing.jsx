import { useState } from 'react';

const PLANS = [
  {
    name: 'Starter',
    price: '$4,999',
    period: '/mo',
    description: 'For teams evaluating AI governance before full deployment.',
    highlight: false,
    badge: null,
    features: [
      'Up to 5 AI agents',
      'Pre-execution policy enforcement',
      'PII detection & redaction',
      'Basic intent verification',
      'Merkle-chained audit ledger',
      'REST API + Python SDK',
      'Email support',
    ],
    cta: 'Start Pilot',
  },
  {
    name: 'Enterprise',
    price: '$18,999',
    period: '/mo',
    description: 'Full runtime governance for regulated production environments.',
    highlight: true,
    badge: 'Most Popular',
    features: [
      'Unlimited AI agents',
      'Byzantine fault-tolerant consensus (33% adversarial)',
      'Context poisoning & retrieval integrity',
      'Prompt injection blocking',
      'Multi-agent trust propagation',
      'Context waste analytics (FinOps)',
      'Human-in-the-loop approval flows',
      'SOC 2 / MAS TRM / RBI FREE-AI export',
      'Redis-persisted enforcement state',
      'Slack + SIEM integration',
      'Dedicated CSM + SLA',
    ],
    cta: 'Request Pilot',
  },
  {
    name: 'Sovereign',
    price: 'Custom',
    period: '',
    description: 'Air-gapped, on-premise deployment for central banks and government.',
    highlight: false,
    badge: 'Government / CBs',
    features: [
      'Everything in Enterprise',
      'On-premise / VPC deployment',
      'Air-gapped audit ledger',
      'Custom policy engine',
      'Regulatory compliance pack (RBI, MAS, APRA, EU AI Act)',
      'Multi-jurisdiction support',
      'Dedicated security review',
      'Custom SLA & MSA',
    ],
    cta: 'Contact Us',
  },
];

const CHECK = (
  <svg width='14' height='14' viewBox='0 0 14 14' fill='none'>
    <path d='M2.5 7L5.5 10L11.5 4' stroke='var(--color-accent)' strokeWidth='1.5' strokeLinecap='round' strokeLinejoin='round'/>
  </svg>
);

export default function Pricing() {
  const [hov, setHov] = useState(null);
  return (
    <section id='pricing' style={{ padding: 'var(--space-12) var(--space-8)', background: 'var(--color-bg-surface)', borderTop: '1px solid var(--color-border)' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '48px' }}>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', padding: '4px 12px', borderRadius: '20px', background: 'var(--color-accent-dim)', border: '1px solid rgba(0,229,195,0.25)', fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-accent)', letterSpacing: '0.06em', textTransform: 'uppercase', marginBottom: '16px' }}>
            Transparent Pricing
          </div>
          <h2 style={{ margin: '0 0 12px', color: 'var(--color-text-primary)' }}>Runtime Governance, Priced for Scale</h2>
          <p style={{ margin: 0, color: 'var(--color-text-muted)', fontSize: '0.9375rem' }}>
            All plans include pre-execution enforcement. No per-decision charges.
          </p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '24px' }}>
          {PLANS.map((plan, i) => (
            <div key={plan.name}
              onMouseEnter={() => setHov(i)}
              onMouseLeave={() => setHov(null)}
              style={{
                position: 'relative',
                background: plan.highlight ? 'var(--color-bg-card)' : 'var(--color-bg-elevated)',
                border: plan.highlight ? '1px solid var(--color-accent)' : '1px solid var(--color-border)',
                borderRadius: 'var(--radius-xl)',
                padding: '32px',
                display: 'flex', flexDirection: 'column',
                boxShadow: plan.highlight ? '0 0 40px var(--color-accent-glow)' : 'none',
                transition: 'transform var(--transition-base), box-shadow var(--transition-base)',
                transform: hov === i ? 'translateY(-4px)' : 'none',
              }}
            >
              {plan.badge && (
                <div style={{
                  position: 'absolute', top: '-12px', left: '50%', transform: 'translateX(-50%)',
                  padding: '3px 14px', borderRadius: '12px',
                  background: plan.highlight ? 'var(--color-accent)' : 'var(--color-bg-elevated)',
                  border: plan.highlight ? 'none' : '1px solid var(--color-border)',
                  color: plan.highlight ? '#000' : 'var(--color-text-secondary)',
                  fontSize: '0.6875rem', fontWeight: 700, letterSpacing: '0.06em', whiteSpace: 'nowrap',
                }}>
                  {plan.badge}
                </div>
              )}

              <div style={{ marginBottom: '8px', fontSize: '0.75rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em', color: plan.highlight ? 'var(--color-accent)' : 'var(--color-text-muted)' }}>
                {plan.name}
              </div>
              <div style={{ display: 'flex', alignItems: 'baseline', gap: '4px', marginBottom: '8px' }}>
                <span style={{ fontSize: '2.25rem', fontWeight: 800, color: 'var(--color-text-primary)', letterSpacing: '-0.02em', fontFamily: 'var(--font-mono)' }}>{plan.price}</span>
                <span style={{ fontSize: '0.875rem', color: 'var(--color-text-muted)' }}>{plan.period}</span>
              </div>
              <p style={{ fontSize: '0.8125rem', color: 'var(--color-text-muted)', marginBottom: '24px', lineHeight: 1.6 }}>{plan.description}</p>

              <div style={{ flex: 1, marginBottom: '28px' }}>
                {plan.features.map(f => (
                  <div key={f} style={{ display: 'flex', alignItems: 'flex-start', gap: '8px', marginBottom: '10px' }}>
                    <span style={{ flexShrink: 0, marginTop: '1px' }}>{CHECK}</span>
                    <span style={{ fontSize: '0.8125rem', color: 'var(--color-text-secondary)', lineHeight: 1.5 }}>{f}</span>
                  </div>
                ))}
              </div>

              <a href='mailto:chandan.galani@privatevault.ai'
                style={{
                  display: 'block', textAlign: 'center',
                  padding: '11px 20px', borderRadius: 'var(--radius-md)',
                  background: plan.highlight ? 'var(--color-accent)' : 'transparent',
                  border: plan.highlight ? 'none' : '1px solid var(--color-border-strong)',
                  color: plan.highlight ? '#000' : 'var(--color-text-primary)',
                  fontWeight: 600, fontSize: '0.875rem', textDecoration: 'none',
                  transition: 'all var(--transition-fast)',
                }}
              >
                {plan.cta}
              </a>
            </div>
          ))}
        </div>

        <p style={{ textAlign: 'center', marginTop: '32px', fontSize: '0.8125rem', color: 'var(--color-text-muted)' }}>
          All plans billed annually. Monthly available at +20%. Pilot pricing available — <a href='mailto:chandan.galani@privatevault.ai' style={{ color: 'var(--color-accent)', textDecoration: 'none' }}>contact us</a>.
        </p>
      </div>
    </section>
  );
}
