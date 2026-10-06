const API_URL = "http://127.0.0.1:8000";

export interface Portfolio {
  SP500: number;
  NASDAQ: number;
  GOLD: number;
  OIL: number;
  NIFTY: number;
}

export interface Performance {
  dates: string[];
  portfolio_value: number[];
  returns: number[];
  drawdown: number[];
}

export interface Metrics {
  cagr: number;
  sharpe: number;
  sortino: number;
  max_drawdown: number;
}

export interface ModelResult {
  name: string;
  total_return: number;
  cagr: number;
  volatility: number;
  sharpe: number;
  sortino: number;
  max_drawdown: number;
  calmar: number;
  average_turnover: number;
}

export async function getPortfolio(): Promise<Portfolio> {
  const response = await fetch(`${API_URL}/portfolio`);

  if (!response.ok) {
    throw new Error("Failed to fetch portfolio");
  }

  return response.json();
}

export async function getPerformance(): Promise<Performance> {
  const response = await fetch(`${API_URL}/performance`);

  if (!response.ok) {
    throw new Error("Failed to fetch performance");
  }

  return response.json();
}

export async function getMetrics(): Promise<Metrics> {
  const response = await fetch(`${API_URL}/metrics`);

  if (!response.ok) {
    throw new Error("Failed to fetch metrics");
  }

  return response.json();
}

export async function getComparison(): Promise<ModelResult[]> {
  const response = await fetch(`${API_URL}/comparison`);

  if (!response.ok) {
    throw new Error("Failed to fetch model comparison");
  }

  const data = await response.json();

  return data.models;
}