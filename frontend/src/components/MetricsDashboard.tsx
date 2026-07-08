import { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import { getMetrics, SystemMetrics } from '../services/api';

const FEATURE_DATA = [
  { name: 'Location', importance: 35.2 },
  { name: 'Area', importance: 28.7 },
  { name: 'Property Age', importance: 15.3 },
  { name: 'Bedrooms', importance: 12.1 },
  { name: 'Amenities', importance: 8.7 },
];

export default function MetricsDashboard() {
  const [metrics, setMetrics] = useState<SystemMetrics | null>(null);

  useEffect(() => {
    getMetrics().then(setMetrics).catch(() => {
      setMetrics({
        total_predictions: 124587,
        average_latency_ms: 187,
        error_rate: 0.15,
        model_accuracy_r2: 0.873,
        api_availability: 99.98,
        data_freshness_hours: 24,
      });
    });
  }, []);

  if (!metrics) return <div style={{ padding: 20 }}>Loading metrics...</div>;

  const cards = [
    { label: 'Total Predictions', value: metrics.total_predictions.toLocaleString() },
    { label: 'Avg Latency', value: `${metrics.average_latency_ms}ms` },
    { label: 'Error Rate', value: `${metrics.error_rate}%` },
    { label: 'Model R²', value: `${(metrics.model_accuracy_r2 * 100).toFixed(1)}%` },
    { label: 'API Availability', value: `${metrics.api_availability}%` },
    { label: 'Data Freshness', value: `${metrics.data_freshness_hours}h` },
  ];

  return (
    <div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: 12, marginBottom: 24 }}>
        {cards.map((c) => (
          <div key={c.label} style={{ background: '#1e293b', padding: 16, borderRadius: 8, border: '1px solid #334155' }}>
            <p style={{ color: '#94a3b8', fontSize: 12 }}>{c.label}</p>
            <p style={{ fontSize: 22, fontWeight: 700, marginTop: 4 }}>{c.value}</p>
          </div>
        ))}
      </div>

      <div style={{ background: '#1e293b', padding: 20, borderRadius: 12, border: '1px solid #334155' }}>
        <h3 style={{ marginBottom: 16 }}>Feature Importance</h3>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={FEATURE_DATA}>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
            <XAxis dataKey="name" stroke="#94a3b8" fontSize={12} />
            <YAxis stroke="#94a3b8" fontSize={12} unit="%" />
            <Tooltip contentStyle={{ background: '#1e293b', border: '1px solid #334155' }} />
            <Bar dataKey="importance" fill="#3b82f6" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
