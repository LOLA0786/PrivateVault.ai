import { useState } from 'react';
import Navbar from './Navbar';
import Hero from './Hero';
import RiskSection from './RiskSection';
import MetricsBar from './MetricsBar';
import CategorySection from './CategorySection';
import IndustriesSection from './IndustriesSection';
import DemosSection from './DemosSection';
import ProofSection from './ProofSection';
import MoatSection from './MoatSection';
import IntentTable from './IntentTable';
import ShadowImpactPanel from './ShadowImpactPanel';
import Pricing from './Pricing';
import BookDemo from './BookDemo';
import Footer from './Footer';
import DemoLibrary from './DemoLibrary';

export default function Home() {
  const [dark, setDark] = useState(true);
  return (
    <div style={{ background: dark ? 'var(--color-bg-base)' : '#f8fafc', minHeight: '100vh', color: dark ? 'var(--color-text-primary)' : '#0f172a', fontFamily: 'var(--font-sans)', display: 'flex', flexDirection: 'column', transition: 'background 0.3s ease' }}>
      <Navbar dark={dark} toggleTheme={() => setDark(d => !d)} />
      <Hero />
      <RiskSection />
      <MetricsBar />
      <CategorySection />
      <IndustriesSection />
      <DemosSection />
      <ProofSection />
      <MoatSection />
      <div id='intents' style={{ flex: 1, display: 'flex', gap: 'var(--space-6)', padding: 'var(--space-8)', maxWidth: '1600px', width: '100%', margin: '0 auto', alignSelf: 'stretch' }}>
        <div style={{ flex: 1, minWidth: 0 }}><IntentTable /></div>
        <div style={{ width: '280px', flexShrink: 0 }}><ShadowImpactPanel /></div>
      </div>
      <Pricing />
      <BookDemo />
      <DemoLibrary />
      <Footer />
    </div>
  );
}
