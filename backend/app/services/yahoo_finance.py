"""
Yahoo Finance API client
Fetches company financial data from Yahoo Finance
"""
import asyncio
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import yfinance as yf
from app.config import settings


class YahooFinanceClient:
    """
    Client for fetching company data from Yahoo Finance
    """
    
    def __init__(self):
        self.cache: Dict[str, Any] = {}
        self.cache_ttl = timedelta(hours=24)
    
    async def get_company_info(self, ticker: str) -> Optional[Dict[str, Any]]:
        """
        Get company information by ticker
        
        Args:
            ticker: Stock ticker symbol (e.g., 'ASML.AS' for ASML in Amsterdam)
        
        Returns:
            Company information dict or None
        """
        cache_key = f"info_{ticker}"
        if self._is_cached(cache_key):
            return self.cache[cache_key]['data']
        
        try:
            # Run synchronous yfinance in thread pool
            stock = await asyncio.to_thread(yf.Ticker, ticker)
            info = await asyncio.to_thread(lambda: stock.info)
            
            result = {
                'ticker': ticker,
                'name': info.get('longName') or info.get('shortName'),
                'sector': info.get('sector'),
                'industry': info.get('industry'),
                'country': info.get('country'),
                'website': info.get('website'),
                'description': info.get('longBusinessSummary'),
                'market_cap': info.get('marketCap'),
                'currency': info.get('currency', 'USD'),
            }
            
            self._cache_data(cache_key, result)
            return result
            
        except Exception as e:
            print(f"Error fetching company info for {ticker}: {e}")
            return None
    
    async def get_financial_statements(self, ticker: str, years: int = 5) -> Optional[List[Dict[str, Any]]]:
        """
        Get financial statements (income statement + balance sheet)
        
        Args:
            ticker: Stock ticker symbol
            years: Number of years of historical data
        
        Returns:
            List of financial statement dicts by year
        """
        cache_key = f"financials_{ticker}"
        if self._is_cached(cache_key):
            return self.cache[cache_key]['data']
        
        try:
            stock = await asyncio.to_thread(yf.Ticker, ticker)
            
            # Get income statement and balance sheet
            income_stmt = await asyncio.to_thread(lambda: stock.financials)
            balance_sheet = await asyncio.to_thread(lambda: stock.balance_sheet)
            
            if income_stmt.empty or balance_sheet.empty:
                return None
            
            # Combine data by year
            statements = []
            for date in income_stmt.columns[:years]:
                year = date.year
                
                statement = {
                    'fiscal_year': year,
                    'period_end_date': date.strftime('%Y-%m-%d'),
                    
                    # Income Statement
                    'revenue': self._get_value(income_stmt, date, 'Total Revenue'),
                    'cost_of_revenue': self._get_value(income_stmt, date, 'Cost Of Revenue'),
                    'gross_profit': self._get_value(income_stmt, date, 'Gross Profit'),
                    'operating_expenses': self._get_value(income_stmt, date, 'Operating Expense'),
                    'ebitda': self._get_value(income_stmt, date, 'EBITDA'),
                    'ebit': self._get_value(income_stmt, date, 'EBIT'),
                    'interest_expense': self._get_value(income_stmt, date, 'Interest Expense'),
                    'tax_expense': self._get_value(income_stmt, date, 'Tax Provision'),
                    'net_income': self._get_value(income_stmt, date, 'Net Income'),
                    
                    # Balance Sheet
                    'total_assets': self._get_value(balance_sheet, date, 'Total Assets'),
                    'current_assets': self._get_value(balance_sheet, date, 'Current Assets'),
                    'cash_and_equivalents': self._get_value(balance_sheet, date, 'Cash And Cash Equivalents'),
                    'accounts_receivable': self._get_value(balance_sheet, date, 'Accounts Receivable'),
                    'inventory': self._get_value(balance_sheet, date, 'Inventory'),
                    
                    'total_liabilities': self._get_value(balance_sheet, date, 'Total Liabilities Net Minority Interest'),
                    'current_liabilities': self._get_value(balance_sheet, date, 'Current Liabilities'),
                    'long_term_debt': self._get_value(balance_sheet, date, 'Long Term Debt'),
                    'short_term_debt': self._get_value(balance_sheet, date, 'Current Debt'),
                    
                    'total_equity': self._get_value(balance_sheet, date, 'Total Equity Gross Minority Interest'),
                    'retained_earnings': self._get_value(balance_sheet, date, 'Retained Earnings'),
                }
                
                statements.append(statement)
            
            self._cache_data(cache_key, statements)
            return statements
            
        except Exception as e:
            print(f"Error fetching financials for {ticker}: {e}")
            return None
    
    async def get_cashflow_statements(self, ticker: str, years: int = 5) -> Optional[List[Dict[str, Any]]]:
        """
        Get cash flow statements
        
        Args:
            ticker: Stock ticker symbol
            years: Number of years of historical data
        
        Returns:
            List of cash flow dicts by year
        """
        cache_key = f"cashflow_{ticker}"
        if self._is_cached(cache_key):
            return self.cache[cache_key]['data']
        
        try:
            stock = await asyncio.to_thread(yf.Ticker, ticker)
            cashflow = await asyncio.to_thread(lambda: stock.cashflow)
            
            if cashflow.empty:
                return None
            
            statements = []
            for date in cashflow.columns[:years]:
                year = date.year
                
                operating_cf = self._get_value(cashflow, date, 'Operating Cash Flow')
                capex = self._get_value(cashflow, date, 'Capital Expenditure')
                
                statement = {
                    'fiscal_year': year,
                    'period_end_date': date.strftime('%Y-%m-%d'),
                    
                    'operating_cashflow': operating_cf,
                    'capex': abs(capex) if capex else None,  # CapEx usually negative
                    'investing_cashflow': self._get_value(cashflow, date, 'Investing Cash Flow'),
                    'financing_cashflow': self._get_value(cashflow, date, 'Financing Cash Flow'),
                    'free_cashflow': self._get_value(cashflow, date, 'Free Cash Flow'),
                    
                    'dividends_paid': self._get_value(cashflow, date, 'Cash Dividends Paid'),
                    'debt_issued': self._get_value(cashflow, date, 'Issuance Of Debt'),
                    'debt_repaid': self._get_value(cashflow, date, 'Repayment Of Debt'),
                    'equity_issued': self._get_value(cashflow, date, 'Issuance Of Capital Stock'),
                    
                    'net_change_in_cash': self._get_value(cashflow, date, 'Changes In Cash'),
                }
                
                # Calculate free cash flow if not provided
                if not statement['free_cashflow'] and operating_cf and capex:
                    statement['free_cashflow'] = operating_cf - abs(capex)
                
                statements.append(statement)
            
            self._cache_data(cache_key, statements)
            return statements
            
        except Exception as e:
            print(f"Error fetching cash flow for {ticker}: {e}")
            return None
    
    def _get_value(self, df, date, field_name: str) -> Optional[float]:
        """Extract value from DataFrame, handling missing data"""
        try:
            if field_name in df.index:
                value = df.loc[field_name, date]
                return float(value) if value is not None and not str(value).lower() == 'nan' else None
            return None
        except Exception:
            return None
    
    def _cache_data(self, key: str, data: Any):
        """Cache data with timestamp"""
        self.cache[key] = {
            'data': data,
            'timestamp': datetime.utcnow()
        }
    
    def _is_cached(self, key: str) -> bool:
        """Check if data is in cache and not expired"""
        if key not in self.cache:
            return False
        
        cache_age = datetime.utcnow() - self.cache[key]['timestamp']
        return cache_age < self.cache_ttl


# Singleton instance
yahoo_client = YahooFinanceClient()
