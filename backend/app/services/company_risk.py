"""
Company risk scoring service
Calculates risk scores based on macro, sector, and financial health
"""
from typing import Dict, Any, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.company import Company, FinancialStatement, CashFlow, CompanyRiskScore


class CompanyRiskScoringService:
    """
    Service for calculating company risk scores
    """
    
    # Risk weights
    MACRO_WEIGHT = 0.30
    SECTOR_WEIGHT = 0.20
    FINANCIAL_WEIGHT = 0.50
    
    # Risk thresholds
    RISK_THRESHOLDS = {
        'low': 30,
        'medium': 50,
        'high': 70,
    }
    
    async def calculate_company_risk(
        self,
        db: AsyncSession,
        company_id: int,
        fiscal_year: int
    ) -> Optional[Dict[str, Any]]:
        """
        Calculate comprehensive risk score for a company
        
        Args:
            db: Database session
            company_id: Company ID
            fiscal_year: Fiscal year to analyze
        
        Returns:
            Risk score dict or None
        """
        # Get company data
        company = await db.get(Company, company_id)
        if not company:
            return None
        
        # Get financial statement for the year
        stmt = select(FinancialStatement).where(
            FinancialStatement.company_id == company_id,
            FinancialStatement.fiscal_year == fiscal_year
        )
        result = await db.execute(stmt)
        financial = result.scalar_one_or_none()
        
        if not financial:
            return None
        
        # Get cash flow statement
        stmt = select(CashFlow).where(
            CashFlow.company_id == company_id,
            CashFlow.fiscal_year == fiscal_year
        )
        result = await db.execute(stmt)
        cashflow = result.scalar_one_or_none()
        
        # Calculate risk components
        macro_risk = await self._calculate_macro_risk(db, company.country_code)
        sector_risk = await self._calculate_sector_risk(db, company.nace_code)
        financial_health = self._calculate_financial_health_score(financial, cashflow)
        
        # Calculate financial ratios
        ratios = self._calculate_financial_ratios(financial, cashflow)
        
        # Weighted overall risk score
        overall_risk = (
            (macro_risk or 50) * self.MACRO_WEIGHT +
            (sector_risk or 50) * self.SECTOR_WEIGHT +
            (financial_health or 50) * self.FINANCIAL_WEIGHT
        )
        
        # Determine risk category
        risk_category = self._get_risk_category(overall_risk)
        
        return {
            'company_id': company_id,
            'calculation_date': datetime.utcnow().date(),
            'fiscal_year': fiscal_year,
            'macro_risk_score': macro_risk,
            'sector_risk_score': sector_risk,
            'financial_health_score': financial_health,
            'overall_risk_score': round(overall_risk, 2),
            'risk_category': risk_category,
            **ratios
        }
    
    def _calculate_financial_health_score(
        self,
        financial: FinancialStatement,
        cashflow: Optional[CashFlow]
    ) -> float:
        """
        Calculate financial health score (0-100, higher = more risk)
        """
        risk_points = 0
        max_points = 100
        
        # 1. Profitability (20 points)
        if financial.net_income and financial.revenue:
            net_margin = (financial.net_income / financial.revenue) * 100
            if net_margin < -10:
                risk_points += 20
            elif net_margin < 0:
                risk_points += 15
            elif net_margin < 5:
                risk_points += 10
            elif net_margin < 10:
                risk_points += 5
        else:
            risk_points += 10  # Missing data = medium risk
        
        # 2. Leverage (30 points)
        if financial.long_term_debt and financial.ebitda:
            debt_to_ebitda = financial.long_term_debt / financial.ebitda
            if debt_to_ebitda > 5:
                risk_points += 30
            elif debt_to_ebitda > 3:
                risk_points += 20
            elif debt_to_ebitda > 2:
                risk_points += 10
        
        # 3. Liquidity (20 points)
        if financial.current_assets and financial.current_liabilities:
            current_ratio = financial.current_assets / financial.current_liabilities
            if current_ratio < 0.8:
                risk_points += 20
            elif current_ratio < 1.0:
                risk_points += 15
            elif current_ratio < 1.2:
                risk_points += 10
        
        # 4. Cash Flow (20 points)
        if cashflow and cashflow.operating_cashflow:
            if cashflow.operating_cashflow < 0:
                risk_points += 20
            elif cashflow.free_cashflow and cashflow.free_cashflow < 0:
                risk_points += 10
        
        # 5. Solvency (10 points)
        if financial.total_equity and financial.total_assets:
            equity_ratio = (financial.total_equity / financial.total_assets) * 100
            if equity_ratio < 10:
                risk_points += 10
            elif equity_ratio < 20:
                risk_points += 5
        
        return (risk_points / max_points) * 100
    
    def _calculate_financial_ratios(
        self,
        financial: FinancialStatement,
        cashflow: Optional[CashFlow]
    ) -> Dict[str, Optional[float]]:
        """
        Calculate key financial ratios
        """
        ratios = {
            'debt_to_ebitda': None,
            'ebitda_margin': None,
            'roa': None,
            'roe': None,
            'current_ratio': None,
            'quick_ratio': None,
            'free_cashflow_yield': None,
        }
        
        # Debt to EBITDA
        if financial.long_term_debt and financial.ebitda and financial.ebitda > 0:
            ratios['debt_to_ebitda'] = round(financial.long_term_debt / financial.ebitda, 2)
        
        # EBITDA Margin
        if financial.ebitda and financial.revenue and financial.revenue > 0:
            ratios['ebitda_margin'] = round((financial.ebitda / financial.revenue) * 100, 2)
        
        # Return on Assets (ROA)
        if financial.net_income and financial.total_assets and financial.total_assets > 0:
            ratios['roa'] = round((financial.net_income / financial.total_assets) * 100, 2)
        
        # Return on Equity (ROE)
        if financial.net_income and financial.total_equity and financial.total_equity > 0:
            ratios['roe'] = round((financial.net_income / financial.total_equity) * 100, 2)
        
        # Current Ratio
        if financial.current_assets and financial.current_liabilities and financial.current_liabilities > 0:
            ratios['current_ratio'] = round(financial.current_assets / financial.current_liabilities, 2)
        
        # Quick Ratio (Current Assets - Inventory) / Current Liabilities
        if financial.current_assets and financial.current_liabilities and financial.current_liabilities > 0:
            quick_assets = financial.current_assets
            if financial.inventory:
                quick_assets -= financial.inventory
            ratios['quick_ratio'] = round(quick_assets / financial.current_liabilities, 2)
        
        # Free Cash Flow Yield
        if cashflow and cashflow.free_cashflow and financial.total_assets and financial.total_assets > 0:
            ratios['free_cashflow_yield'] = round((cashflow.free_cashflow / financial.total_assets) * 100, 2)
        
        return ratios
    
    async def _calculate_macro_risk(self, db: AsyncSession, country_code: str) -> Optional[float]:
        """
        Calculate macro risk based on country economic indicators
        Placeholder - should integrate with existing macro data
        """
        # TODO: Query actual macro risk from countries/indicators tables
        # For now, return default risk by country
        country_risks = {
            'NL': 25,  # Netherlands - low risk
            'LU': 20,  # Luxembourg - very low risk
            'BE': 30,  # Belgium - low-medium risk
            'DE': 25,  # Germany - low risk
        }
        return country_risks.get(country_code, 50)
    
    async def _calculate_sector_risk(self, db: AsyncSession, nace_code: Optional[str]) -> Optional[float]:
        """
        Calculate sector risk based on NACE code
        Placeholder - should integrate with sector benchmarks
        """
        if not nace_code:
            return 50
        
        # TODO: Query actual sector risk from benchmarks
        # Approximate sector risks by NACE section
        section = nace_code[0] if nace_code else ''
        sector_risks = {
            'A': 40,  # Agriculture
            'B': 55,  # Mining
            'C': 35,  # Manufacturing
            'D': 30,  # Electricity
            'E': 30,  # Water supply
            'F': 45,  # Construction
            'G': 35,  # Wholesale/retail
            'H': 50,  # Transportation
            'I': 45,  # Accommodation/food
            'J': 30,  # Information/communication
            'K': 40,  # Financial/insurance
            'L': 25,  # Real estate
            'M': 30,  # Professional services
            'N': 35,  # Administrative services
            'P': 20,  # Education
            'Q': 20,  # Health
            'R': 45,  # Arts/entertainment
        }
        return sector_risks.get(section, 50)
    
    def _get_risk_category(self, risk_score: float) -> str:
        """Categorize risk score into Low/Medium/High/Critical"""
        if risk_score < self.RISK_THRESHOLDS['low']:
            return 'Low'
        elif risk_score < self.RISK_THRESHOLDS['medium']:
            return 'Medium'
        elif risk_score < self.RISK_THRESHOLDS['high']:
            return 'High'
        else:
            return 'Critical'


# Singleton instance
risk_scoring_service = CompanyRiskScoringService()
