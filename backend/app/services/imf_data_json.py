"""
IMF Data Service using JSON API (more reliable than SDMX)
"""

import requests
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class IMFDataService:
    """
    Service to fetch data from IMF using their JSON API
    More reliable than SDMX for now
    """
    
    def __init__(self):
        """Initialize IMF data service with JSON API"""
        self.base_url = "http://dataservices.imf.org/REST/SDMX_JSON.svc"
        self.session = requests.Session()
        logger.info("IMF JSON API service initialized")
    
    def _make_request(self, endpoint: str) -> Optional[Dict]:
        """Make API request and return JSON response"""
        try:
            url = f"{self.base_url}/{endpoint}"
            logger.info(f"Requesting: {url}")
            
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return None
    
    def get_indicator_data(
        self,
        database: str,
        indicator: str,
        countries: List[str],
        start_year: int = 2015
    ) -> pd.DataFrame:
        """
        Get indicator data from IMF
        
        Common databases:
        - IFS: International Financial Statistics
        - BOP: Balance of Payments
        - DOT: Direction of Trade
        - FM: Financial Markets
        - FSI: Financial Soundness Indicators
        
        Args:
            database: Database code (e.g., 'IFS')
            indicator: Indicator code
            countries: List of 2-letter country codes (NL, BE, LU, DE)
            start_year: Start year for data
            
        Returns:
            DataFrame with time series data
        """
        # Build endpoint: Database/Frequency.Area.Indicator?startPeriod=year
        # Note: IMF uses 2-letter codes (NL) not 3-letter (NLD)
        country_str = "+".join(countries)
        endpoint = f"CompactData/{database}/A.{country_str}.{indicator}?startPeriod={start_year}"
        
        data = self._make_request(endpoint)
        
        if not data:
            logger.warning(f"No data returned for {database}/{indicator}")
            return pd.DataFrame()
        
        try:
            # Parse JSON structure
            series_list = []
            
            # IMF JSON structure: CompactData -> DataSet -> Series
            if 'CompactData' in data and 'DataSet' in data['CompactData']:
                dataset = data['CompactData']['DataSet']
                
                if 'Series' in dataset:
                    series = dataset['Series']
                    
                    # Handle both single series and multiple series
                    if isinstance(series, dict):
                        series = [series]
                    
                    for s in series:
                        country = s.get('@REF_AREA', '')
                        obs_list = s.get('Obs', [])
                        
                        if isinstance(obs_list, dict):
                            obs_list = [obs_list]
                        
                        for obs in obs_list:
                            series_list.append({
                                'country': country,
                                'period': obs.get('@TIME_PERIOD', ''),
                                'value': float(obs.get('@OBS_VALUE', 0))
                            })
            
            df = pd.DataFrame(series_list)
            
            if not df.empty:
                df['period'] = pd.to_datetime(df['period'])
                df = df.sort_values(['country', 'period'])
            
            logger.info(f"Retrieved {len(df)} observations")
            return df
            
        except Exception as e:
            logger.error(f"Error parsing IMF data: {e}")
            return pd.DataFrame()
    
    def get_gdp_growth(
        self,
        countries: List[str] = None,
        start_year: int = 2015
    ) -> Dict[str, pd.Series]:
        """
        Get real GDP growth rates
        Using IFS (International Financial Statistics) database
        
        Args:
            countries: List of 2-letter country codes
            start_year: Start year
            
        Returns:
            Dictionary mapping country to GDP growth series
        """
        if countries is None:
            countries = ['NL', 'BE', 'LU', 'DE']  # 2-letter codes
        
        # NGDP_R_PC_CP_A_PT: GDP, constant prices, % change
        df = self.get_indicator_data('IFS', 'NGDP_R_PC_CP_A_PT', countries, start_year)
        
        if df.empty:
            logger.warning("No GDP growth data available")
            return {}
        
        result = {}
        for country in df['country'].unique():
            country_data = df[df['country'] == country]
            result[country] = pd.Series(
                country_data['value'].values,
                index=country_data['period'].values
            )
        
        return result
    
    def get_inflation_rate(
        self,
        countries: List[str] = None,
        start_year: int = 2015
    ) -> Dict[str, pd.Series]:
        """Get CPI inflation rates"""
        if countries is None:
            countries = ['NL', 'BE', 'LU', 'DE']
        
        # PCPI_PC_CP_A_PT: CPI, % change
        df = self.get_indicator_data('IFS', 'PCPI_PC_CP_A_PT', countries, start_year)
        
        if df.empty:
            return {}
        
        result = {}
        for country in df['country'].unique():
            country_data = df[df['country'] == country]
            result[country] = pd.Series(
                country_data['value'].values,
                index=country_data['period'].values
            )
        
        return result
    
    def get_unemployment_rate(
        self,
        countries: List[str] = None,
        start_year: int = 2015
    ) -> Dict[str, pd.Series]:
        """Get unemployment rates"""
        if countries is None:
            countries = ['NL', 'BE', 'LU', 'DE']
        
        # LUR_PT: Unemployment rate
        df = self.get_indicator_data('IFS', 'LUR_PT', countries, start_year)
        
        if df.empty:
            return {}
        
        result = {}
        for country in df['country'].unique():
            country_data = df[df['country'] == country]
            result[country] = pd.Series(
                country_data['value'].values,
                index=country_data['period'].values
            )
        
        return result
    
    def get_interest_rates(
        self,
        countries: List[str] = None,
        start_year: int = 2015
    ) -> Dict[str, pd.Series]:
        """Get policy interest rates"""
        if countries is None:
            countries = ['NL', 'BE', 'LU', 'DE']
        
        # FPOLM_PA: Central bank policy rate
        df = self.get_indicator_data('IFS', 'FPOLM_PA', countries, start_year)
        
        if df.empty:
            return {}
        
        result = {}
        for country in df['country'].unique():
            country_data = df[df['country'] == country]
            result[country] = pd.Series(
                country_data['value'].values,
                index=country_data['period'].values
            )
        
        return result
    
    def get_comprehensive_indicators(
        self,
        countries: List[str] = None,
        start_year: int = 2020
    ) -> pd.DataFrame:
        """
        Get all key economic indicators
        
        Returns:
            DataFrame with multiple indicators
        """
        if countries is None:
            countries = ['NL', 'BE', 'LU', 'DE']
        
        all_data = []
        
        # Fetch each indicator
        indicators = {
            'gdp_growth': self.get_gdp_growth(countries, start_year),
            'inflation': self.get_inflation_rate(countries, start_year),
            'unemployment': self.get_unemployment_rate(countries, start_year),
            'interest_rate': self.get_interest_rates(countries, start_year)
        }
        
        # Combine into single DataFrame
        for indicator_name, country_data in indicators.items():
            for country, series in country_data.items():
                for date, value in series.items():
                    all_data.append({
                        'country': country,
                        'indicator': indicator_name,
                        'date': date,
                        'value': value
                    })
        
        df = pd.DataFrame(all_data)
        
        if not df.empty:
            df = df.pivot_table(
                index=['country', 'date'],
                columns='indicator',
                values='value'
            ).reset_index()
        
        return df


# For backwards compatibility with test script
IMFDataService.__name__ = 'IMFDataService'
