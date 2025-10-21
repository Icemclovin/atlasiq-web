"""
Company data models
Stores company information, financial statements, and cash flows
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Integer, Float, Boolean, Date, ForeignKey, Index, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Company(Base):
    """
    Company information
    Stores basic company details and classification
    """
    __tablename__ = "companies"
    
    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Company identification
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    country_code: Mapped[str] = mapped_column(String(2), nullable=False, index=True)  # NL, BE, LU, DE
    
    # Classification
    nace_code: Mapped[Optional[str]] = mapped_column(String(10), index=True)  # NACE industry code
    sector: Mapped[Optional[str]] = mapped_column(String(100), index=True)  # Sector name
    
    # Additional info
    is_listed: Mapped[bool] = mapped_column(Boolean, default=False)  # Public or private
    ticker: Mapped[Optional[str]] = mapped_column(String(20), unique=True)  # Stock ticker if listed
    website: Mapped[Optional[str]] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(String(1000))
    
    # External IDs
    opencorporates_id: Mapped[Optional[str]] = mapped_column(String(100), unique=True)
    lei_code: Mapped[Optional[str]] = mapped_column(String(20), unique=True)  # Legal Entity Identifier
    
    # Metadata
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    data_source: Mapped[Optional[str]] = mapped_column(String(50))  # yahoo, opencorporates, etc.
    
    # Relationships
    financial_statements: Mapped[List["FinancialStatement"]] = relationship(
        "FinancialStatement", 
        back_populates="company",
        cascade="all, delete-orphan"
    )
    cashflows: Mapped[List["CashFlow"]] = relationship(
        "CashFlow",
        back_populates="company",
        cascade="all, delete-orphan"
    )
    risk_scores: Mapped[List["CompanyRiskScore"]] = relationship(
        "CompanyRiskScore",
        back_populates="company",
        cascade="all, delete-orphan"
    )
    
    # Indexes
    __table_args__ = (
        Index('idx_company_country_sector', 'country_code', 'sector'),
        Index('idx_company_nace', 'nace_code'),
    )
    
    def __repr__(self):
        return f"<Company(id={self.id}, name={self.name}, country={self.country_code})>"


class FinancialStatement(Base):
    """
    Company financial statements
    Annual income statement and balance sheet data
    """
    __tablename__ = "financial_statements"
    
    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False, index=True)
    
    # Period
    fiscal_year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    period_end_date: Mapped[Optional[datetime]] = mapped_column(Date)
    
    # Income Statement (all in EUR)
    revenue: Mapped[Optional[float]] = mapped_column(Float)
    cost_of_revenue: Mapped[Optional[float]] = mapped_column(Float)
    gross_profit: Mapped[Optional[float]] = mapped_column(Float)
    operating_expenses: Mapped[Optional[float]] = mapped_column(Float)
    ebitda: Mapped[Optional[float]] = mapped_column(Float)
    ebit: Mapped[Optional[float]] = mapped_column(Float)
    interest_expense: Mapped[Optional[float]] = mapped_column(Float)
    tax_expense: Mapped[Optional[float]] = mapped_column(Float)
    net_income: Mapped[Optional[float]] = mapped_column(Float)
    
    # Balance Sheet (all in EUR)
    total_assets: Mapped[Optional[float]] = mapped_column(Float)
    current_assets: Mapped[Optional[float]] = mapped_column(Float)
    cash_and_equivalents: Mapped[Optional[float]] = mapped_column(Float)
    accounts_receivable: Mapped[Optional[float]] = mapped_column(Float)
    inventory: Mapped[Optional[float]] = mapped_column(Float)
    
    total_liabilities: Mapped[Optional[float]] = mapped_column(Float)
    current_liabilities: Mapped[Optional[float]] = mapped_column(Float)
    long_term_debt: Mapped[Optional[float]] = mapped_column(Float)
    short_term_debt: Mapped[Optional[float]] = mapped_column(Float)
    
    total_equity: Mapped[Optional[float]] = mapped_column(Float)
    retained_earnings: Mapped[Optional[float]] = mapped_column(Float)
    
    # Metadata
    currency: Mapped[str] = mapped_column(String(3), default="EUR")
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    data_source: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Relationships
    company: Mapped["Company"] = relationship("Company", back_populates="financial_statements")
    
    # Constraints
    __table_args__ = (
        Index('idx_financial_company_year', 'company_id', 'fiscal_year', unique=True),
        CheckConstraint('fiscal_year >= 2000 AND fiscal_year <= 2100', name='valid_fiscal_year'),
    )
    
    def __repr__(self):
        return f"<FinancialStatement(company_id={self.company_id}, year={self.fiscal_year})>"


class CashFlow(Base):
    """
    Company cash flow statements
    Annual cash flow from operations, investing, and financing
    """
    __tablename__ = "cashflows"
    
    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False, index=True)
    
    # Period
    fiscal_year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    period_end_date: Mapped[Optional[datetime]] = mapped_column(Date)
    
    # Cash Flow Statement (all in EUR)
    operating_cashflow: Mapped[Optional[float]] = mapped_column(Float)
    capex: Mapped[Optional[float]] = mapped_column(Float)  # Capital expenditures
    investing_cashflow: Mapped[Optional[float]] = mapped_column(Float)
    financing_cashflow: Mapped[Optional[float]] = mapped_column(Float)
    free_cashflow: Mapped[Optional[float]] = mapped_column(Float)  # Operating CF - CapEx
    
    dividends_paid: Mapped[Optional[float]] = mapped_column(Float)
    debt_issued: Mapped[Optional[float]] = mapped_column(Float)
    debt_repaid: Mapped[Optional[float]] = mapped_column(Float)
    equity_issued: Mapped[Optional[float]] = mapped_column(Float)
    
    net_change_in_cash: Mapped[Optional[float]] = mapped_column(Float)
    
    # Metadata
    currency: Mapped[str] = mapped_column(String(3), default="EUR")
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    data_source: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Relationships
    company: Mapped["Company"] = relationship("Company", back_populates="cashflows")
    
    # Constraints
    __table_args__ = (
        Index('idx_cashflow_company_year', 'company_id', 'fiscal_year', unique=True),
        CheckConstraint('fiscal_year >= 2000 AND fiscal_year <= 2100', name='valid_fiscal_year'),
    )
    
    def __repr__(self):
        return f"<CashFlow(company_id={self.company_id}, year={self.fiscal_year})>"


class CompanyRiskScore(Base):
    """
    Company risk scoring
    Combines macro risk, sector risk, and financial health metrics
    """
    __tablename__ = "company_risk_scores"
    
    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False, index=True)
    
    # Calculation date
    calculation_date: Mapped[datetime] = mapped_column(Date, nullable=False, index=True)
    fiscal_year: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Risk components (0-100 scale, higher = more risk)
    macro_risk_score: Mapped[Optional[float]] = mapped_column(Float)  # From country macro data
    sector_risk_score: Mapped[Optional[float]] = mapped_column(Float)  # From NACE sector benchmarks
    financial_health_score: Mapped[Optional[float]] = mapped_column(Float)  # From financial ratios
    
    # Composite score
    overall_risk_score: Mapped[Optional[float]] = mapped_column(Float)  # Weighted average
    risk_category: Mapped[Optional[str]] = mapped_column(String(20))  # Low, Medium, High, Critical
    
    # Financial ratios
    debt_to_ebitda: Mapped[Optional[float]] = mapped_column(Float)
    ebitda_margin: Mapped[Optional[float]] = mapped_column(Float)
    roa: Mapped[Optional[float]] = mapped_column(Float)  # Return on Assets
    roe: Mapped[Optional[float]] = mapped_column(Float)  # Return on Equity
    current_ratio: Mapped[Optional[float]] = mapped_column(Float)
    quick_ratio: Mapped[Optional[float]] = mapped_column(Float)
    free_cashflow_yield: Mapped[Optional[float]] = mapped_column(Float)
    
    # Metadata
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    # Relationships
    company: Mapped["Company"] = relationship("Company", back_populates="risk_scores")
    
    # Constraints
    __table_args__ = (
        Index('idx_risk_company_date', 'company_id', 'calculation_date', unique=True),
        CheckConstraint('overall_risk_score >= 0 AND overall_risk_score <= 100', name='valid_risk_score'),
    )
    
    def __repr__(self):
        return f"<CompanyRiskScore(company_id={self.company_id}, score={self.overall_risk_score})>"
