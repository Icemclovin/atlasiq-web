// User and Authentication Types
export interface User {
  id: number;
  email: string;
  full_name: string;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  full_name: string;
}

export interface Token {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface AuthResponse {
  user: User;
  access_token: string;
  refresh_token: string;
  token_type: string;
}

// Country and Indicator Types
export interface Country {
  code: string;
  name: string;
  region: string;
}

export interface Indicator {
  id: number;
  code: string;
  name: string;
  description: string;
  category: string;
  unit: string;
  frequency: string;
  source_id: number;
  created_at: string;
  updated_at: string;
}

export interface DataSource {
  id: number;
  name: string;
  code: string;
  description: string;
  base_url: string;
  api_type: string;
  requires_auth: boolean;
  is_active: boolean;
  created_at: string;
}

// Time Series Data Types
export interface DataPoint {
  id: number;
  indicator_id: number;
  country_code: string;
  sector_code?: string;
  date: string;
  value: number;
  period_type: string;
  extra_metadata?: Record<string, any>;
  created_at: string;
}

export interface TimeSeriesData {
  indicator: Indicator;
  country: Country;
  data: DataPoint[];
}

// Dashboard Types
export interface KPICard {
  title: string;
  value: number | string;
  change: number;
  changeType: 'increase' | 'decrease' | 'neutral';
  unit?: string;
  trend?: number[];
}

export interface CountrySummary {
  country: Country;
  gdp_growth: number;
  unemployment: number;
  inflation: number;
  business_confidence: number;
  risk_score: number;
}

export interface SectorData {
  sector_code: string;
  sector_name: string;
  value: number;
  growth: number;
  indicators: Record<string, number>;
}

export interface RiskScore {
  country_code: string;
  sector_code?: string;
  overall_score: number;
  factors: RiskFactor[];
  updated_at: string;
}

export interface RiskFactor {
  name: string;
  weight: number;
  score: number;
  description: string;
}

// Dashboard Response Types
export interface DashboardSummary {
  countries: CountrySummary[];
  last_updated: string;
  total_indicators: number;
  data_freshness: number;
}

export interface CountryDetail {
  country: Country;
  kpis: KPICard[];
  sectors: SectorData[];
  risk_scores: RiskScore[];
  time_series: TimeSeriesData[];
}

// Chart Data Types
export interface ChartDataPoint {
  date: string;
  value: number;
  [key: string]: any;
}

export interface ChartConfig {
  title: string;
  type: 'line' | 'bar' | 'area' | 'pie';
  data: ChartDataPoint[];
  xAxisKey: string;
  yAxisKey: string;
  color?: string;
}

// API Response Types
export interface ApiResponse<T> {
  data: T;
  message?: string;
  status: number;
}

export interface ApiError {
  detail: string;
  status: number;
}

// Query Parameters
export interface DataQueryParams {
  country_code?: string;
  indicator_code?: string;
  sector_code?: string;
  start_date?: string;
  end_date?: string;
  limit?: number;
  offset?: number;
}

export interface ExportParams {
  format: 'csv' | 'excel';
  country_code?: string;
  indicator_codes?: string[];
  start_date?: string;
  end_date?: string;
}
