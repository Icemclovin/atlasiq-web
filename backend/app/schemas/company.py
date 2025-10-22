"""
Pydantic schemas for company data
"""
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, Field, validator


# Company Schemas
class CompanyBase(BaseModel):
    """Base company schema"""
    name: str = Field(..., min_length=1, max_length=255)
    country_code: str = Field(..., min_length=2, max_length=2)
    nace_code: Optional[str] = Field(None, max_length=10)
    sector: Optional[str] = Field(None, max_length=100)
    is_listed: bool = False
    ticker: Optional[str] = Field(None, max_length=20)
    website: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)


class CompanyCreate(CompanyBase):
    """Schema for creating a company"""
    opencorporates_id: Optional[str] = None
    lei_code: Optional[str] = None
    data_source: Optional[str] = None


class CompanyUpdate(BaseModel):
    """Schema for updating a company"""
    name: Optional[str] = None
    sector: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None


class CompanyResponse(CompanyBase):
    """Schema for company response"""
    id: int
    opencorporates_id: Optional[str]
    lei_code: Optional[str]
    created_at: datetime
    updated_at: datetime
    data_source: Optional[str]
    
    class Config:
        from_attributes = True


class CompanySummary(BaseModel):
    """Compact company summary for lists"""
    id: int
    name: str
    country_code: str
    sector: Optional[str]
    ticker: Optional[str]
    is_listed: bool
    
    class Config:
        from_attributes = True


# Financial Statement Schemas
class FinancialStatementBase(BaseModel):
    """Base financial statement schema"""
    fiscal_year: int = Field(..., ge=2000, le=2100)
    period_end_date: Optional[date] = None
    
    # Income Statement
    revenue: Optional[float] = None
    cost_of_revenue: Optional[float] = None
    gross_profit: Optional[float] = None
    operating_expenses: Optional[float] = None
    ebitda: Optional[float] = None
    ebit: Optional[float] = None
    interest_expense: Optional[float] = None
    tax_expense: Optional[float] = None
    net_income: Optional[float] = None
    
    # Balance Sheet
    total_assets: Optional[float] = None
    current_assets: Optional[float] = None
    cash_and_equivalents: Optional[float] = None
    accounts_receivable: Optional[float] = None
    inventory: Optional[float] = None
    total_liabilities: Optional[float] = None
    current_liabilities: Optional[float] = None
    long_term_debt: Optional[float] = None
    short_term_debt: Optional[float] = None
    total_equity: Optional[float] = None
    retained_earnings: Optional[float] = None
    
    currency: str = "EUR"


class FinancialStatementCreate(FinancialStatementBase):
    """Schema for creating financial statement"""
    company_id: int
    data_source: Optional[str] = None


class FinancialStatementResponse(FinancialStatementBase):
    """Schema for financial statement response"""
    id: int
    company_id: int
    created_at: datetime
    updated_at: datetime
    data_source: Optional[str]
    
    class Config:
        from_attributes = True


# Cash Flow Schemas
class CashFlowBase(BaseModel):
    """Base cash flow schema"""
    fiscal_year: int = Field(..., ge=2000, le=2100)
    period_end_date: Optional[date] = None
    
    operating_cashflow: Optional[float] = None
    capex: Optional[float] = None
    investing_cashflow: Optional[float] = None
    financing_cashflow: Optional[float] = None
    free_cashflow: Optional[float] = None
    dividends_paid: Optional[float] = None
    debt_issued: Optional[float] = None
    debt_repaid: Optional[float] = None
    equity_issued: Optional[float] = None
    net_change_in_cash: Optional[float] = None
    
    currency: str = "EUR"


class CashFlowCreate(CashFlowBase):
    """Schema for creating cash flow"""
    company_id: int
    data_source: Optional[str] = None


class CashFlowResponse(CashFlowBase):
    """Schema for cash flow response"""
    id: int
    company_id: int
    created_at: datetime
    updated_at: datetime
    data_source: Optional[str]
    
    class Config:
        from_attributes = True


# Risk Score Schemas
class CompanyRiskScoreResponse(BaseModel):
    """Schema for risk score response"""
    id: int
    company_id: int
    calculation_date: date
    fiscal_year: int
    
    macro_risk_score: Optional[float]
    sector_risk_score: Optional[float]
    financial_health_score: Optional[float]
    overall_risk_score: Optional[float]
    risk_category: Optional[str]
    
    # Financial ratios
    debt_to_ebitda: Optional[float]
    ebitda_margin: Optional[float]
    roa: Optional[float]
    roe: Optional[float]
    current_ratio: Optional[float]
    quick_ratio: Optional[float]
    free_cashflow_yield: Optional[float]
    
    created_at: datetime
    
    class Config:
        from_attributes = True


# Combined Schemas
class CompanyDetailResponse(CompanyResponse):
    """Detailed company response with latest financial data"""
    latest_financial: Optional[FinancialStatementResponse] = None
    latest_cashflow: Optional[CashFlowResponse] = None
    latest_risk_score: Optional[CompanyRiskScoreResponse] = None


class CompanyFinancialsResponse(BaseModel):
    """Company with multiple years of financial data"""
    company: CompanyResponse
    financial_statements: List[FinancialStatementResponse]
    cashflows: List[CashFlowResponse]


class CompanyRiskAnalysis(BaseModel):
    """Complete risk analysis for a company"""
    company: CompanySummary
    risk_score: CompanyRiskScoreResponse
    financial_statement: FinancialStatementResponse
    cashflow: Optional[CashFlowResponse]
    peer_comparison: Optional[dict] = None


# Search and Filter Schemas
class CompanySearchParams(BaseModel):
    """Parameters for company search"""
    query: Optional[str] = Field(None, description="Search by company name")
    country_code: Optional[str] = Field(None, min_length=2, max_length=2)
    sector: Optional[str] = None
    nace_code: Optional[str] = None
    is_listed: Optional[bool] = None
    min_revenue: Optional[float] = None
    max_revenue: Optional[float] = None
    min_risk_score: Optional[float] = Field(None, ge=0, le=100)
    max_risk_score: Optional[float] = Field(None, ge=0, le=100)
    sort_by: Optional[str] = Field("name", pattern="^(name|revenue|risk_score|country_code)$")
    sort_order: Optional[str] = Field("asc", pattern="^(asc|desc)$")
    skip: int = Field(0, ge=0)
    limit: int = Field(20, ge=1, le=100)


class CompanySearchResult(BaseModel):
    """Search result with company and key metrics"""
    company: CompanySummary
    latest_revenue: Optional[float] = None
    latest_net_income: Optional[float] = None
    latest_ebitda: Optional[float] = None
    risk_score: Optional[float] = None
    risk_category: Optional[str] = None


class CompanySearchResponse(BaseModel):
    """Paginated search response"""
    results: List[CompanySearchResult]
    total: int
    skip: int
    limit: int


class CompanyComparisonRequest(BaseModel):
    """Request for comparing companies"""
    company_ids: List[int] = Field(..., min_items=2, max_items=5)
    fiscal_year: Optional[int] = None


class CompanyComparisonResponse(BaseModel):
    """Response with compared companies"""
    companies: List[CompanyDetailResponse]
    fiscal_year: int


# Data Ingestion Schemas
class CompanyIngestRequest(BaseModel):
    """Request to ingest company data"""
    ticker: str = Field(..., min_length=1, max_length=20)
    years: int = Field(5, ge=1, le=10)


class CompanyIngestResponse(BaseModel):
    """Response from data ingestion"""
    success: bool
    company_id: Optional[int] = None
    message: str
    financial_years: List[int] = []
    validation_errors: List[str] = []
