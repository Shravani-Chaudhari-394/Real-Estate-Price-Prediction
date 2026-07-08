import { useState } from 'react';
import PredictionForm from './components/PredictionForm';
import MetricsDashboard from './components/MetricsDashboard';

export default function App() {
  const [tab, setTab] = useState<'predict' | 'dashboard'>('predict');

  return (
    <div style={{ maxWidth: 1000, margin: '0 auto', padding: '32px 16px' }}>
      <header style={{ marginBottom: 32 }}>
        <h1 style={{ fontSize: 28, fontWeight: 700 }}>🏢 Real Estate Price Prediction</h1>
        <p style={{ color: '#94a3b8', marginTop: 8 }}>Production-ready ML system · v1.2.0</p>
      </header>

      <nav style={{ display: 'flex', gap: 8, marginBottom: 24 }}>
        {(['predict', 'dashboard'] as const).map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            style={{
              padding: '8px 20px',
              borderRadius: 8,
              border: 'none',
              cursor: 'pointer',
              background: tab === t ? '#3b82f6' : '#1e293b',
              color: '#e2e8f0',
              fontWeight: 600,
            }}
          >
            {t === 'predict' ? 'Predict' : 'Dashboard'}
          </button>
        ))}
      </nav>

      {tab === 'predict' ? <PredictionForm /> : <MetricsDashboard />}
    </div>
  );
}
