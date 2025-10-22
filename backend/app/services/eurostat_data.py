"""
Eurostat Data Service
Official EU statistical office - using official Python client
Perfect for Benelux + Germany region
"""

import eurostat
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class EurostatDataService:
    """
    Service to fetch data from Eurostat using official Python library
    Covers all EU countries with official statistical data
    """
    
    def __init__(self):
        """Initialize Eurostat data service"""
        logger.info("Eurostat service initialized")
    
    def get_gdp_growth(
        self,
        countries: List[str] = None,
        start_year: int = 2015
    ) -> Dict[str, pd.Series]:
        """
        Get real GDP growth rates from Eurostat
        
        Dataset: nama_10_gdp (National accounts - GDP)
        
        Args:
            countries: List of 2-letter country codes (NL, BE, LU, DE)
            start_year: Start year
            
        Returns:
            Dictionary mapping country to GDP growth series
        """
        if countries is None:
            countries = ['NL', 'BE', 'LU', 'DE']
        
        try:
            logger.info(f"Fetching GDP data for {countries} from {start_year}")
            
            # Get GDP in chain linked volumes (real GDP)
            df = eurostat.get_data_df(
                'nama_10_gdp',
                flags=False,
                filter_pars={
                    'geo': countries,
                    'unit': 'CLV10_EUR',  # Chain linked volumes
                    'na_item': 'B1GQ'  # Gross domestic product
                }
            )
            
            if df.empty:
                logger.warning("No GDP data returned from Eurostat")
                return {}
            
            # Calculate year-over-year growth rates
            result = {}
            
            # Filter by start year and pivot
            time_cols = [col for col in df.columns if col.isdigit()]
            time_cols = [col for col in time_cols if int(col) >= start_year]
            
            for country in countries:
                country_data = df[df['geo'] == country]
                
                if not country_data.empty:
                    # Extract time series
                    values = country_data[time_cols].iloc[0]
                    
                    # Calculate growth rates
                    growth_rates = values.pct_change() * 100
                    
                    # Convert to Series with datetime index
                    dates = pd.to_datetime([f"{year}-12-31" for year in time_cols])
                    series = pd.Series(growth_rates.values, index=dates, name=country)
                    
                    result[country] = series
            
            logger.info(f"Retrieved GDP growth for {len(result)} countries")
            return result
            
        except Exception as e:
            logger.error(f"Failed to fetch GDP data: {e}")
            return {}
    
    def get_inflation_rate(
        self,
        countries: List[str] = None,
        start_year: int = 2015
    ) -> Dict[str, pd.Series]:
        """
        Get HICP inflation rates from Eurostat
        
        Dataset: prc_hicp_manr (HICP - monthly annual rate of change)
        
        Args:
            countries: List of 2-letter country codes
            start_year: Start year
            
        Returns:
            Dictionary mapping country to inflation series
        """
        if countries is None:
            countries = ['NL', 'BE', 'LU', 'DE']
        
        try:
            logger.info(f"Fetching inflation data for {countries} from {start_year}")
            
            # Get HICP annual rate of change
            df = eurostat.get_data_df(
                'prc_hicp_manr',
                flags=False,
                filter_pars={
                    'geo': countries,
                    'coicop': 'CP00',  # All-items HICP
                    'unit': 'RCH_A'  # Rate of change, annual
                }
            )
            
            if df.empty:
                logger.warning("No inflation data returned from Eurostat")
                return {}
            
            result = {}
            
            # Get time columns (format: YYYY-MM)
            time_cols = [col for col in df.columns if '-' in str(col)]
            time_cols = [col for col in time_cols if int(col[:4]) >= start_year]
            
            for country in countries:
                country_data = df[df['geo'] == country]
                
                if not country_data.empty:
                    values = country_data[time_cols].iloc[0]
                    
                    # Convert to datetime index
                    dates = pd.to_datetime(time_cols)
                    series = pd.Series(values.values, index=dates, name=country)
                    
                    result[country] = series
            
            logger.info(f"Retrieved inflation data for {len(result)} countries")
            return result
            
        except Exception as e:
            logger.error(f"Failed to fetch inflation data: {e}")
            return {}
    
    def get_unemployment_rate(
        self,
        countries: List[str] = None,
        start_year: int = 2015
    ) -> Dict[str, pd.Series]:
        """
        Get unemployment rates from Eurostat
        
        Dataset: une_rt_a (Unemployment rate - annual)
        
        Args:
            countries: List of 2-letter country codes
            start_year: Start year
            
        Returns:
            Dictionary mapping country to unemployment series
        """
        if countries is None:
            countries = ['NL', 'BE', 'LU', 'DE']
        
        try:
            logger.info(f"Fetching unemployment data for {countries} from {start_year}")
            
            # Get unemployment rate
            df = eurostat.get_data_df(
                'une_rt_a',
                flags=False,
                filter_pars={
                    'geo': countries,
                    'sex': 'T',  # Total (both sexes)
                    'age': 'Y15-74',  # Age 15-74
                    'unit': 'PC_ACT'  # Percentage of active population
                }
            )
            
            if df.empty:
                logger.warning("No unemployment data returned from Eurostat")
                return {}
            
            result = {}
            
            # Get time columns (years)
            time_cols = [col for col in df.columns if col.isdigit()]
            time_cols = [col for col in time_cols if int(col) >= start_year]
            
            for country in countries:
                country_data = df[df['geo'] == country]
                
                if not country_data.empty:
                    values = country_data[time_cols].iloc[0]
                    
                    # Convert to datetime index
                    dates = pd.to_datetime([f"{year}-12-31" for year in time_cols])
                    series = pd.Series(values.values, index=dates, name=country)
                    
                    result[country] = series
            
            logger.info(f"Retrieved unemployment data for {len(result)} countries")
            return result
            
        except Exception as e:
            logger.error(f"Failed to fetch unemployment data: {e}")
            return {}
    
    def get_business_confidence(
        self,
        countries: List[str] = None,
        start_year: int = 2020
    ) -> Dict[str, pd.Series]:
        """
        Get business confidence indicator
        
        Dataset: ei_bssi_m_r2 (Business and consumer surveys)
        
        Args:
            countries: List of 2-letter country codes
            start_year: Start year
            
        Returns:
            Dictionary mapping country to confidence series
        """
        if countries is None:
            countries = ['NL', 'BE', 'LU', 'DE']
        
        try:
            logger.info(f"Fetching business confidence for {countries} from {start_year}")
            
            # Get business confidence indicator
            df = eurostat.get_data_df(
                'ei_bssi_m_r2',
                flags=False,
                filter_pars={
                    'geo': countries,
                    'indic': 'BS-ICI',  # Business confidence indicator
                    's_adj': 'SA'  # Seasonally adjusted
                }
            )
            
            if df.empty:
                logger.warning("No business confidence data returned from Eurostat")
                return {}
            
            result = {}
            
            # Get time columns (format: YYYY-MM)
            time_cols = [col for col in df.columns if '-' in str(col)]
            time_cols = [col for col in time_cols if int(col[:4]) >= start_year]
            
            for country in countries:
                country_data = df[df['geo'] == country]
                
                if not country_data.empty:
                    values = country_data[time_cols].iloc[0]
                    
                    # Convert to datetime index
                    dates = pd.to_datetime(time_cols)
                    series = pd.Series(values.values, index=dates, name=country)
                    
                    result[country] = series
            
            logger.info(f"Retrieved business confidence for {len(result)} countries")
            return result
            
        except Exception as e:
            logger.error(f"Failed to fetch business confidence: {e}")
            return {}
    
    def get_comprehensive_indicators(
        self,
        countries: List[str] = None,
        start_year: int = 2020
    ) -> pd.DataFrame:
        """
        Get all key economic indicators in one DataFrame
        
        Args:
            countries: List of 2-letter country codes
            start_year: Start year
            
        Returns:
            DataFrame with all indicators
        """
        if countries is None:
            countries = ['NL', 'BE', 'LU', 'DE']
        
        try:
            logger.info(f"Fetching comprehensive indicators for {countries}")
            
            all_data = []
            
            # Fetch each indicator
            indicators = {
                'gdp_growth': self.get_gdp_growth(countries, start_year),
                'inflation': self.get_inflation_rate(countries, start_year),
                'unemployment': self.get_unemployment_rate(countries, start_year),
                'business_confidence': self.get_business_confidence(countries, start_year)
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
                # Pivot to wide format
                df = df.pivot_table(
                    index=['country', 'date'],
                    columns='indicator',
                    values='value'
                ).reset_index()
            
            logger.info(f"Retrieved comprehensive data: {len(df)} rows")
            return df
            
        except Exception as e:
            logger.error(f"Failed to fetch comprehensive indicators: {e}")
            return pd.DataFrame()

