import { useState } from 'react';
import { predictPrice, PropertyInput, PredictionResult } from '../services/api';

const LOCATIONS = ['Mumbai', 'Delhi', 'Bangalore', 'Pune', 'Hyderabad', 'Chennai', 'Kolkata', 'Ahmedabad'];
const PROPERTY_TYPES = ['Apartment', 'Villa', 'Penthouse', 'Studio', 'Duplex'];

export default function PredictionForm() {
  const [form, setForm] = useState<PropertyInput>({
    area: 1200,
    bedrooms: 3,
    bathrooms: 2,
    age: 5,
    location: 'Mumbai',
    property_type: 'Apartment',
    floor: 5,
    facing: 'East',
    amenities_score: 7,
  });
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const prediction = await predictPrice(form);
      setResult(prediction);
    } catch {
      setError('Prediction failed. Ensure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const formatPrice = (price: number) =>
    new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(price);

  return (
    <div style={styles.card}>
      <h2 style={styles.title}>Property Price Predictor</h2>
      <form onSubmit={handleSubmit} style={styles.form}>
        <div style={styles.grid}>
          <label>
            Area (sqft)
            <input type="number" value={form.area} onChange={(e) => setForm({ ...form, area: +e.target.value })} style={styles.input} />
          </label>
          <label>
            Bedrooms
            <input type="number" value={form.bedrooms} onChange={(e) => setForm({ ...form, bedrooms: +e.target.value })} style={styles.input} />
          </label>
          <label>
            Bathrooms
            <input type="number" value={form.bathrooms} onChange={(e) => setForm({ ...form, bathrooms: +e.target.value })} style={styles.input} />
          </label>
          <label>
            Age (years)
            <input type="number" value={form.age} onChange={(e) => setForm({ ...form, age: +e.target.value })} style={styles.input} />
          </label>
          <label>
            Location
            <select value={form.location} onChange={(e) => setForm({ ...form, location: e.target.value })} style={styles.input}>
              {LOCATIONS.map((l) => <option key={l} value={l}>{l}</option>)}
            </select>
          </label>
          <label>
            Property Type
            <select value={form.property_type} onChange={(e) => setForm({ ...form, property_type: e.target.value })} style={styles.input}>
              {PROPERTY_TYPES.map((t) => <option key={t} value={t}>{t}</option>)}
            </select>
          </label>
        </div>
        <button type="submit" disabled={loading} style={styles.button}>
          {loading ? 'Predicting...' : 'Predict Price'}
        </button>
      </form>

      {error && <p style={styles.error}>{error}</p>}

      {result && (
        <div style={styles.result}>
          <h3>Predicted Price</h3>
          <p style={styles.price}>{formatPrice(result.predicted_price)}</p>
          <p style={styles.range}>
            Range: {formatPrice(result.confidence_interval.lower_bound)} – {formatPrice(result.confidence_interval.upper_bound)}
          </p>
          <p style={styles.meta}>Model v{result.model_version} · {result.prediction_id.slice(0, 8)}</p>
        </div>
      )}
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  card: { background: '#1e293b', borderRadius: 12, padding: 24, border: '1px solid #334155' },
  title: { marginBottom: 20, fontSize: 20 },
  form: { display: 'flex', flexDirection: 'column', gap: 16 },
  grid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: 12 },
  input: { display: 'block', width: '100%', marginTop: 4, padding: '8px 12px', borderRadius: 6, border: '1px solid #475569', background: '#0f172a', color: '#e2e8f0' },
  button: { padding: '12px 24px', background: '#3b82f6', color: '#fff', border: 'none', borderRadius: 8, cursor: 'pointer', fontSize: 16, fontWeight: 600 },
  error: { color: '#f87171', marginTop: 12 },
  result: { marginTop: 24, padding: 20, background: '#0f172a', borderRadius: 8, textAlign: 'center' },
  price: { fontSize: 32, fontWeight: 700, color: '#34d399', margin: '8px 0' },
  range: { color: '#94a3b8', fontSize: 14 },
  meta: { color: '#64748b', fontSize: 12, marginTop: 8 },
};
