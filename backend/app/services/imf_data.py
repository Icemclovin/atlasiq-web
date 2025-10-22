"""
IMF Data Service
Connects to IMF SDMX API to fetch economic indicators and forecasts
Uses sdmx1 library as recommended by IMF
"""
import sdmx
import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)


class IMFDataService:
    """
    Service for fetching data from IMF SDMX API
    Supports public access (no authentication required)
    """
    
    def __init__(self):
        """Initialize IMF SDMX client"""
        try:
            self.client = sdmx.Client('IMF')
            logger.info("IMF SDMX client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize IMF client: {e}")
            raise
    
    def get_cpi_data(
        self,
        countries: List[str] = None,
        start_period: int = 2015
    ) -> pd.DataFrame:
        """
        Fetch CPI (Consumer Price Index) data
        
        Args:
            countries: List of ISO 3-letter country codes
            start_period: Start year for data
            
        Returns:
            DataFrame with CPI data
        """
        if countries is None:
            countries = ['USA', 'CAN', 'NLD', 'BEL', 'LUX', 'DEU']
        
        try:
            # Join countries with + as per IMF API spec
            country_key = '+'.join(countries)
            
            # Request data
            logger.info(f"Fetching CPI data for {country_key} from {start_period}")
            data_msg = self.client.data(
                'CPI',
                key=f'{country_key}.CPI.CP01.IX.M',  # Monthly CPI, All items index
                params={'startPeriod': start_period}
            )
            
            # Convert to pandas DataFrame
            df = sdmx.to_pandas(data_msg)
            
            logger.info(f"Successfully fetched {len(df)} CPI records")
            return df
            
        except Exception as e:
            logger.error(f"Failed to fetch CPI data: {e}")
            raise
    
    def get_weo_data(
        self,
        countries: List[str] = None,
        indicators: List[str] = None,
        start_period: int = 2015
    ) -> pd.DataFrame:
        """
        Fetch World Economic Outlook (WEO) data
        
        Common WEO indicators:
        - NGDP_RPCH: Real GDP growth (%)
        - PCPIPCH: Inflation, average consumer prices (%)
        - LUR: Unemployment rate (%)
        - GGXWDG_NGDP: General government gross debt (% of GDP)
        - BCA_NGDPD: Current account balance (% of GDP)
        
        Args:
            countries: List of ISO 3-letter country codes
            indicators: List of WEO indicator codes
            start_period: Start year for data
            
        Returns:
            DataFrame with WEO data
        """
        if countries is None:
            countries = ['NLD', 'BEL', 'LUX', 'DEU', 'USA']
        if indicators is None:
            indicators = ['NGDP_RPCH', 'PCPIPCH', 'LUR', 'GGXWDG_NGDP']
        
        try:
            country_key = '+'.join(countries)
            indicator_key = '+'.join(indicators)
            
            logger.info(f"Fetching WEO data for {country_key}, indicators: {indicator_key}")
            
            data_msg = self.client.data(
                'WEO',
                key=f'{country_key}.{indicator_key}.A',  # Annual frequency
                params={'startPeriod': start_period}
            )
            
            df = sdmx.to_pandas(data_msg)
            
            logger.info(f"Successfully fetched {len(df)} WEO records")
            return df
            
        except Exception as e:
            logger.error(f"Failed to fetch WEO data: {e}")
            raise
    
    def get_ifs_data(
        self,
        countries: List[str] = None,
        indicators: List[str] = None,
        start_period: int = 2015
    ) -> pd.DataFrame:
        """
        Fetch International Financial Statistics (IFS) data
        
        Common IFS indicators:
        - FITB_BP6_USD: Current account balance, USD
        - FPOLM_PA: Policy rate, % per annum
        - ENDA_XDC_USD_RATE: Exchange rate (end of period)
        - FI_RATIO: Financial soundness indicators
        
        Args:
            countries: List of ISO 3-letter country codes
            indicators: List of IFS indicator codes
            start_period: Start year for data
            
        Returns:
            DataFrame with IFS data
        """
        if countries is None:
            countries = ['NLD', 'BEL', 'LUX', 'DEU']
        if indicators is None:
            indicators = ['FITB_BP6_USD', 'FPOLM_PA']
        
        try:
            country_key = '+'.join(countries)
            indicator_key = '+'.join(indicators)
            
            logger.info(f"Fetching IFS data for {country_key}")
            
            data_msg = self.client.data(
                'IFS',
                key=f'{country_key}.{indicator_key}.M',  # Monthly frequency
                params={'startPeriod': start_period}
            )
            
            df = sdmx.to_pandas(data_msg)
            
            logger.info(f"Successfully fetched {len(df)} IFS records")
            return df
            
        except Exception as e:
            logger.error(f"Failed to fetch IFS data: {e}")
            raise
    
    def get_gdp_growth(
        self,
        countries: List[str] = None,
        start_year: int = 2015
    ) -> Dict[str, pd.Series]:
        """
        Get real GDP growth rates for specified countries
        
        Args:
            countries: List of ISO 3-letter country codes
            start_year: Start year for data
            
        Returns:
            Dictionary mapping country code to GDP growth series
        """
        if countries is None:
            countries = ['NLD', 'BEL', 'LUX', 'DEU']
        
        try:
            df = self.get_weo_data(
                countries=countries,
                indicators=['NGDP_RPCH'],
                start_period=start_year
            )
            
            # Parse multi-index and extract by country
            result = {}
            for country in countries:
                try:
                    country_data = df.xs(country, level='REF_AREA')
                    result[country] = country_data
                except KeyError:
                    logger.warning(f"No GDP growth data for {country}")
                    result[country] = pd.Series()
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to get GDP growth: {e}")
            return {country: pd.Series() for country in countries}
    
    def get_inflation_rate(
        self,
        countries: List[str] = None,
        start_year: int = 2015
    ) -> Dict[str, pd.Series]:
        """
        Get inflation rates for specified countries
        
        Args:
            countries: List of ISO 3-letter country codes
            start_year: Start year for data
            
        Returns:
            Dictionary mapping country code to inflation series
        """
        if countries is None:
            countries = ['NLD', 'BEL', 'LUX', 'DEU']
        
        try:
            df = self.get_weo_data(
                countries=countries,
                indicators=['PCPIPCH'],
                start_period=start_year
            )
            
            result = {}
            for country in countries:
                try:
                    country_data = df.xs(country, level='REF_AREA')
                    result[country] = country_data
                except KeyError:
                    logger.warning(f"No inflation data for {country}")
                    result[country] = pd.Series()
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to get inflation rate: {e}")
            return {country: pd.Series() for country in countries}
    
    def get_unemployment_rate(
        self,
        countries: List[str] = None,
        start_year: int = 2015
    ) -> Dict[str, pd.Series]:
        """
        Get unemployment rates for specified countries
        
        Args:
            countries: List of ISO 3-letter country codes
            start_year: Start year for data
            
        Returns:
            Dictionary mapping country code to unemployment series
        """
        if countries is None:
            countries = ['NLD', 'BEL', 'LUX', 'DEU']
        
        try:
            df = self.get_weo_data(
                countries=countries,
                indicators=['LUR'],
                start_period=start_year
            )
            
            result = {}
            for country in countries:
                try:
                    country_data = df.xs(country, level='REF_AREA')
                    result[country] = country_data
                except KeyError:
                    logger.warning(f"No unemployment data for {country}")
                    result[country] = pd.Series()
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to get unemployment rate: {e}")
            return {country: pd.Series() for country in countries}
    
    def get_government_debt(
        self,
        countries: List[str] = None,
        start_year: int = 2015
    ) -> Dict[str, pd.Series]:
        """
        Get government debt (% of GDP) for specified countries
        
        Args:
            countries: List of ISO 3-letter country codes
            start_year: Start year for data
            
        Returns:
            Dictionary mapping country code to debt series
        """
        if countries is None:
            countries = ['NLD', 'BEL', 'LUX', 'DEU']
        
        try:
            df = self.get_weo_data(
                countries=countries,
                indicators=['GGXWDG_NGDP'],
                start_period=start_year
            )
            
            result = {}
            for country in countries:
                try:
                    country_data = df.xs(country, level='REF_AREA')
                    result[country] = country_data
                except KeyError:
                    logger.warning(f"No debt data for {country}")
                    result[country] = pd.Series()
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to get government debt: {e}")
            return {country: pd.Series() for country in countries}
    
    def get_comprehensive_indicators(
        self,
        countries: List[str] = None,
        start_year: int = 2015
    ) -> pd.DataFrame:
        """
        Get comprehensive set of economic indicators for analysis
        
        Args:
            countries: List of ISO 3-letter country codes
            start_year: Start year for data
            
        Returns:
            DataFrame with all key indicators
        """
        if countries is None:
            countries = ['NLD', 'BEL', 'LUX', 'DEU']
        
        try:
            # Fetch all key WEO indicators in one call
            indicators = [
                'NGDP_RPCH',      # Real GDP growth
                'PCPIPCH',        # Inflation
                'LUR',            # Unemployment
                'GGXWDG_NGDP',    # Government debt
                'BCA_NGDPD',      # Current account balance
            ]
            
            df = self.get_weo_data(
                countries=countries,
                indicators=indicators,
                start_period=start_year
            )
            
            return df
            
        except Exception as e:
            logger.error(f"Failed to get comprehensive indicators: {e}")
            return pd.DataFrame()
    
    def clear_cache(self):
        """Clear any internal caching"""
        logger.info("IMF data cache cleared (no-op - removed LRU cache)")


# Singleton instance
_imf_service = None

def get_imf_service() -> IMFDataService:
    """Get or create IMF service instance"""
    global _imf_service
    if _imf_service is None:
        _imf_service = IMFDataService()
    return _imf_service
