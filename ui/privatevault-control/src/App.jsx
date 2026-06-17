import { useState } from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import RiskSection from './components/RiskSection';
import MetricsBar from './components/MetricsBar';
import CategorySection from './components/CategorySection';
import IndustriesSection from './components/IndustriesSection';
import DemosSection from './components/DemosSection';
import ProofSection from './components/ProofSection';
import MoatSection from './components/MoatSection';
import IntentTable from './components/IntentTable';
import ShadowImpactPanel from './components/ShadowImpactPanel';
import Pricing from './components/Pricing';
import BookDemo from './components/BookDemo';
import Footer from './components/Footer';

export default function App() {
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
      <Footer />
    </div>
  );
}
