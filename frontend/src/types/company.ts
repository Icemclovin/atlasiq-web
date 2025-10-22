/**
 * Company data types
 */

export interface Company {
  id: number;
  name: string;
  country_code: string;
  nace_code?: string;
  sector?: string;
  is_listed: boolean;
  ticker?: string;
  website?: string;
  description?: string;
  opencorporates_id?: string;
  lei_code?: string;
  created_at: string;
  updated_at: string;
  data_source?: string;
}

export interface CompanySummary {
  id: number;
  name: string;
  country_code: string;
  sector?: string;
  ticker?: string;
  is_listed: boolean;
}

export interface FinancialStatement {
  id: number;
  company_id: number;
  fiscal_year: number;
  period_end_date?: string;
  
  // Income Statement
  revenue?: number;
  cost_of_revenue?: number;
  gross_profit?: number;
  operating_expenses?: number;
  ebitda?: number;
  ebit?: number;
  interest_expense?: number;
  tax_expense?: number;
  net_income?: number;
  
  // Balance Sheet
  total_assets?: number;
  current_assets?: number;
  cash_and_equivalents?: number;
  accounts_receivable?: number;
  inventory?: number;
  total_liabilities?: number;
  current_liabilities?: number;
  long_term_debt?: number;
  short_term_debt?: number;
  total_equity?: number;
  retained_earnings?: number;
  
  currency: string;
  created_at: string;
  updated_at: string;
  data_source?: string;
}

export interface CashFlow {
  id: number;
  company_id: number;
  fiscal_year: number;
  period_end_date?: string;
  
  operating_cashflow?: number;
  capex?: number;
  investing_cashflow?: number;
  financing_cashflow?: number;
  free_cashflow?: number;
  dividends_paid?: number;
  debt_issued?: number;
  debt_repaid?: number;
  equity_issued?: number;
  net_change_in_cash?: number;
  
  currency: string;
  created_at: string;
  updated_at: string;
  data_source?: string;
}

export interface CompanyRiskScore {
  id: number;
  company_id: number;
  calculation_date: string;
  fiscal_year: number;
  
  macro_risk_score?: number;
  sector_risk_score?: number;
  financial_health_score?: number;
  overall_risk_score?: number;
  risk_category?: string;
  
  // Financial ratios
  debt_to_ebitda?: number;
  ebitda_margin?: number;
  roa?: number;
  roe?: number;
  current_ratio?: number;
  quick_ratio?: number;
  free_cashflow_yield?: number;
  
  created_at: string;
}

export interface CompanyDetail extends Company {
  latest_financial?: FinancialStatement;
  latest_cashflow?: CashFlow;
  latest_risk_score?: CompanyRiskScore;
}

export interface CompanySearchResult {
  company: CompanySummary;
  latest_revenue?: number;
  latest_net_income?: number;
  latest_ebitda?: number;
  risk_score?: number;
  risk_category?: string;
}

export interface CompanySearchParams {
  query?: string;
  country_code?: string;
  sector?: string;
  is_listed?: boolean;
  min_risk_score?: number;
  max_risk_score?: number;
  sort_by?: 'name' | 'revenue' | 'risk_score';
  sort_order?: 'asc' | 'desc';
  skip?: number;
  limit?: number;
}

export interface CompanySearchResponse {
  results: CompanySearchResult[];
  total: number;
  skip: number;
  limit: number;
}

export interface CompanyFinancials {
  company: Company;
  financial_statements: FinancialStatement[];
  cashflows: CashFlow[];
}

export interface CompanyRiskAnalysis {
  company: CompanySummary;
  risk_score: CompanyRiskScore;
  financial_statement: FinancialStatement;
  cashflow?: CashFlow;
  peer_comparison?: any;
}

export interface CompanyIngestRequest {
  ticker: string;
  years?: number;
}

export interface CompanyIngestResponse {
  success: boolean;
  company_id?: number;
  message: string;
  financial_years: number[];
  validation_errors: string[];
}
