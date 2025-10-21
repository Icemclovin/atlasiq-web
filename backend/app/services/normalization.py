"""
Data normalization service
Handles currency conversion, field standardization, and validation
"""
from typing import Dict, Any, Optional
from datetime import datetime
import asyncio


class DataNormalizationService:
    """
    Service for normalizing company financial data
    """
    
    # FX rates to EUR (approximate, should be updated from API in production)
    FX_RATES_TO_EUR = {
        'EUR': 1.0,
        'USD': 0.92,  # 1 USD = 0.92 EUR (approximate)
        'GBP': 1.16,  # 1 GBP = 1.16 EUR
        'CHF': 1.05,  # 1 CHF = 1.05 EUR
        'DKK': 0.134, # 1 DKK = 0.134 EUR
        'SEK': 0.088, # 1 SEK = 0.088 EUR
        'NOK': 0.086, # 1 NOK = 0.086 EUR
    }
    
    # Country code mapping
    COUNTRY_CODES = {
        'Netherlands': 'NL',
        'Belgium': 'BE',
        'Luxembourg': 'LU',
        'Germany': 'DE',
        'France': 'FR',
        'United Kingdom': 'GB',
    }
    
    def __init__(self):
        self.validation_errors = []
    
    async def normalize_company_info(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize company information
        
        Args:
            data: Raw company data from source
        
        Returns:
            Normalized company data
        """
        normalized = {
            'name': self._clean_string(data.get('name')),
            'country_code': self._normalize_country_code(data.get('country')),
            'sector': self._clean_string(data.get('sector')),
            'website': self._clean_string(data.get('website')),
            'description': self._clean_string(data.get('description'), max_length=1000),
            'is_listed': data.get('is_listed', True),
            'ticker': self._clean_string(data.get('ticker')),
        }
        
        return {k: v for k, v in normalized.items() if v is not None}
    
    async def normalize_financial_statement(
        self, 
        data: Dict[str, Any], 
        source_currency: str = 'USD'
    ) -> Dict[str, Any]:
        """
        Normalize financial statement data
        
        Args:
            data: Raw financial data
            source_currency: Original currency of the data
        
        Returns:
            Normalized financial data in EUR
        """
        self.validation_errors = []
        
        # Convert all amounts to EUR
        fx_rate = self.FX_RATES_TO_EUR.get(source_currency, 1.0)
        
        normalized = {
            'fiscal_year': data.get('fiscal_year'),
            'period_end_date': self._parse_date(data.get('period_end_date')),
            'currency': 'EUR',
        }
        
        # Convert financial fields
        financial_fields = [
            'revenue', 'cost_of_revenue', 'gross_profit', 'operating_expenses',
            'ebitda', 'ebit', 'interest_expense', 'tax_expense', 'net_income',
            'total_assets', 'current_assets', 'cash_and_equivalents',
            'accounts_receivable', 'inventory', 'total_liabilities',
            'current_liabilities', 'long_term_debt', 'short_term_debt',
            'total_equity', 'retained_earnings'
        ]
        
        for field in financial_fields:
            value = data.get(field)
            if value is not None:
                normalized[field] = self._convert_currency(value, fx_rate)
        
        # Validate financial statement
        self._validate_financial_statement(normalized)
        
        return normalized
    
    async def normalize_cashflow_statement(
        self,
        data: Dict[str, Any],
        source_currency: str = 'USD'
    ) -> Dict[str, Any]:
        """
        Normalize cash flow statement data
        
        Args:
            data: Raw cash flow data
            source_currency: Original currency
        
        Returns:
            Normalized cash flow data in EUR
        """
        fx_rate = self.FX_RATES_TO_EUR.get(source_currency, 1.0)
        
        normalized = {
            'fiscal_year': data.get('fiscal_year'),
            'period_end_date': self._parse_date(data.get('period_end_date')),
            'currency': 'EUR',
        }
        
        # Convert cash flow fields
        cashflow_fields = [
            'operating_cashflow', 'capex', 'investing_cashflow',
            'financing_cashflow', 'free_cashflow', 'dividends_paid',
            'debt_issued', 'debt_repaid', 'equity_issued', 'net_change_in_cash'
        ]
        
        for field in cashflow_fields:
            value = data.get(field)
            if value is not None:
                normalized[field] = self._convert_currency(value, fx_rate)
        
        return normalized
    
    def _convert_currency(self, amount: float, fx_rate: float) -> float:
        """Convert amount to EUR using FX rate"""
        return round(amount * fx_rate, 2)
    
    def _normalize_country_code(self, country: Optional[str]) -> Optional[str]:
        """Normalize country name to 2-letter code"""
        if not country:
            return None
        
        # Check if already a code
        if len(country) == 2 and country.isupper():
            return country
        
        # Look up in mapping
        return self.COUNTRY_CODES.get(country)
    
    def _clean_string(self, value: Optional[str], max_length: Optional[int] = None) -> Optional[str]:
        """Clean and truncate string"""
        if not value:
            return None
        
        cleaned = str(value).strip()
        if max_length and len(cleaned) > max_length:
            cleaned = cleaned[:max_length]
        
        return cleaned if cleaned else None
    
    def _parse_date(self, date_value: Any) -> Optional[str]:
        """Parse date to ISO format string"""
        if not date_value:
            return None
        
        if isinstance(date_value, str):
            try:
                dt = datetime.fromisoformat(date_value.replace('Z', '+00:00'))
                return dt.strftime('%Y-%m-%d')
            except Exception:
                return None
        
        if isinstance(date_value, datetime):
            return date_value.strftime('%Y-%m-%d')
        
        return None
    
    def _validate_financial_statement(self, data: Dict[str, Any]):
        """
        Validate financial statement for logical consistency
        """
        revenue = data.get('revenue')
        ebitda = data.get('ebitda')
        net_income = data.get('net_income')
        total_assets = data.get('total_assets')
        total_liabilities = data.get('total_liabilities')
        total_equity = data.get('total_equity')
        
        # Check EBITDA <= Revenue
        if revenue and ebitda and ebitda > revenue:
            self.validation_errors.append(f"EBITDA ({ebitda}) > Revenue ({revenue})")
        
        # Check Net Income <= Revenue
        if revenue and net_income and net_income > revenue * 2:  # Allow some margin for unusual cases
            self.validation_errors.append(f"Net Income ({net_income}) suspiciously high vs Revenue ({revenue})")
        
        # Check balance sheet equation: Assets = Liabilities + Equity
        if total_assets and total_liabilities and total_equity:
            balance_check = abs(total_assets - (total_liabilities + total_equity))
            tolerance = total_assets * 0.01  # 1% tolerance
            
            if balance_check > tolerance:
                self.validation_errors.append(
                    f"Balance sheet doesn't balance: Assets={total_assets}, L+E={total_liabilities + total_equity}"
                )
        
        # Flag outliers (extremely high margins)
        if revenue and ebitda:
            ebitda_margin = (ebitda / revenue) * 100
            if ebitda_margin > 80:
                self.validation_errors.append(f"EBITDA margin unusually high: {ebitda_margin:.1f}%")
    
    def has_validation_errors(self) -> bool:
        """Check if there are validation errors"""
        return len(self.validation_errors) > 0
    
    def get_validation_errors(self) -> list:
        """Get list of validation errors"""
        return self.validation_errors


# Singleton instance
normalization_service = DataNormalizationService()
