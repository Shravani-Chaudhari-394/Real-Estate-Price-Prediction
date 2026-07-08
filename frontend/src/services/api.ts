const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface PropertyInput {
  area: number;
  bedrooms: number;
  bathrooms: number;
  age: number;
  location: string;
  property_type: string;
  floor?: number;
  facing?: string;
  amenities_score?: number;
}

export interface PredictionResult {
  prediction_id: string;
  timestamp: string;
  predicted_price: number;
  currency: string;
  confidence_interval: { lower_bound: number; upper_bound: number };
  model_version: string;
  metadata: Record<string, unknown>;
}

export interface SystemMetrics {
  total_predictions: number;
  average_latency_ms: number;
  error_rate: number;
  model_accuracy_r2: number;
  api_availability: number;
  data_freshness_hours: number;
}

export async function predictPrice(property: PropertyInput): Promise<PredictionResult> {
  const res = await fetch(`${API_BASE}/api/v1/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(property),
  });
  if (!res.ok) throw new Error('Prediction failed');
  return res.json();
}

export async function getMetrics(): Promise<SystemMetrics> {
  const res = await fetch(`${API_BASE}/api/v1/metrics`);
  if (!res.ok) throw new Error('Failed to fetch metrics');
  return res.json();
}

export async function getHealth(): Promise<{ status: string; version: string }> {
  const res = await fetch(`${API_BASE}/api/v1/health`);
  if (!res.ok) throw new Error('Health check failed');
  return res.json();
}
