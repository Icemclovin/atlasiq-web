"""
Historical Economic Data Service
Uses curated historical data (2015-2023) from reliable public sources
Much more reliable than real-time APIs for MVP

Data Sources:
- OECD.Stat (https://stats.oecd.org/)
- World Bank Open Data (https://data.worldbank.org/)
- ECB Statistical Data Warehouse (https://sdw.ecb.europa.eu/)

All data is real historical data, manually verified and cleaned.
"""

import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class HistoricalEconomicDataService:
    """
    Provides real historical economic data for Benelux + Germany (2015-2023)
    Reliable, proven data from official sources
    """
    
    def __init__(self):
        """Initialize with hardcoded historical data"""
        logger.info("Historical Economic Data service initialized")
        
        # Real GDP growth rates (%) - Source: OECD
        # Data verified from OECD.Stat - Real GDP forecast
        self.gdp_growth = {
            'NLD': {  # Netherlands
                2015: 2.0,
                2016: 2.2,
                2017: 2.9,
                2018: 2.4,
                2019: 1.7,
                2020: -3.9,  # COVID impact
                2021: 5.0,   # Recovery
                2022: 4.3,
                2023: 0.1
            },
            'BEL': {  # Belgium
                2015: 2.0,
                2016: 1.4,
                2017: 1.6,
                2018: 1.8,
                2019: 2.1,
                2020: -5.7,
                2021: 6.2,
                2022: 3.0,
                2023: 1.4
            },
            'LUX': {  # Luxembourg
                2015: 4.3,
                2016: 4.6,
                2017: 1.8,
                2018: 3.1,
                2019: 2.3,
                2020: -1.3,
                2021: 6.9,
                2022: 1.4,
                2023: 0.4
            },
            'DEU': {  # Germany
                2015: 1.5,
                2016: 2.2,
                2017: 2.7,
                2018: 1.0,
                2019: 1.1,
                2020: -3.7,
                2021: 3.2,
                2022: 1.8,
                2023: -0.3
            }
        }
        
        # Inflation rates (%) - Source: OECD/Eurostat HICP
        self.inflation = {
            'NLD': {
                2015: 0.2,
                2016: 0.1,
                2017: 1.3,
                2018: 1.6,
                2019: 2.7,
                2020: 1.1,
                2021: 2.8,
                2022: 11.6,  # Energy crisis
                2023: 3.8
            },
            'BEL': {
                2015: 0.6,
                2016: 1.8,
                2017: 2.2,
                2018: 2.3,
                2019: 1.2,
                2020: 0.4,
                2021: 3.2,
                2022: 10.3,
                2023: 2.3
            },
            'LUX': {
                2015: 0.1,
                2016: 0.0,
                2017: 2.1,
                2018: 2.0,
                2019: 1.6,
                2020: 0.0,
                2021: 3.5,
                2022: 8.2,
                2023: 2.9
            },
            'DEU': {
                2015: 0.1,
                2016: 0.4,
                2017: 1.7,
                2018: 1.9,
                2019: 1.4,
                2020: 0.4,
                2021: 3.2,
                2022: 8.7,
                2023: 5.9
            }
        }
        
        # Unemployment rates (%) - Source: OECD
        self.unemployment = {
            'NLD': {
                2015: 6.9,
                2016: 6.0,
                2017: 4.9,
                2018: 3.8,
                2019: 3.4,
                2020: 3.8,
                2021: 4.2,
                2022: 3.5,
                2023: 3.6
            },
            'BEL': {
                2015: 8.5,
                2016: 7.8,
                2017: 7.1,
                2018: 6.0,
                2019: 5.4,
                2020: 5.6,
                2021: 6.3,
                2022: 5.6,
                2023: 5.5
            },
            'LUX': {
                2015: 6.7,
                2016: 6.3,
                2017: 5.6,
                2018: 5.5,
                2019: 5.6,
                2020: 6.7,
                2021: 5.8,
                2022: 4.6,
                2023: 5.1
            },
            'DEU': {
                2015: 4.6,
                2016: 4.1,
                2017: 3.8,
                2018: 3.4,
                2019: 3.2,
                2020: 3.9,
                2021: 3.6,
                2022: 3.1,
                2023: 3.0
            }
        }
        
        # ECB Interest Rates (%) - Source: ECB Statistical Data Warehouse
        # Deposit Facility Rate (DFR)
        self.ecb_dfr = {
            2015: -0.30,
            2016: -0.40,
            2017: -0.40,
            2018: -0.40,
            2019: -0.50,
            2020: -0.50,
            2021: -0.50,
            2022: 2.00,  # Rapid tightening
            2023: 4.00
        }
        
        # Main Refinancing Operations (MRO)
        self.ecb_mro = {
            2015: 0.05,
            2016: 0.00,
            2017: 0.00,
            2018: 0.00,
            2019: 0.00,
            2020: 0.00,
            2021: 0.00,
            2022: 2.50,
            2023: 4.50
        }
    
    def get_gdp_growth(
        self,
        countries: List[str] = None,
        start_year: int = 2015
    ) -> Dict[str, pd.Series]:
        """
        Get real GDP growth rates
        
        Args:
            countries: List of 3-letter country codes (NLD, BEL, LUX, DEU)
            start_year: Start year (2015-2023)
            
        Returns:
            Dictionary mapping country to GDP growth series
        """
        if countries is None:
            countries = ['NLD', 'BEL', 'LUX', 'DEU']
        
        result = {}
        
        for country in countries:
            if country in self.gdp_growth:
                # Filter by start year
                country_data = {
                    year: value 
                    for year, value in self.gdp_growth[country].items()
                    if year >= start_year
                }
                
                # Convert to Series with datetime index
                years = list(country_data.keys())
                values = list(country_data.values())
                dates = pd.to_datetime([f"{year}-12-31" for year in years])
                
                series = pd.Series(values, index=dates, name=country)
                result[country] = series
                
                logger.info(f"Retrieved {len(series)} GDP growth points for {country}")
        
        return result
    
    def get_inflation_rate(
        self,
        countries: List[str] = None,
        start_year: int = 2015
    ) -> Dict[str, pd.Series]:
        """Get inflation rates (HICP)"""
        if countries is None:
            countries = ['NLD', 'BEL', 'LUX', 'DEU']
        
        result = {}
        
        for country in countries:
            if country in self.inflation:
                country_data = {
                    year: value 
                    for year, value in self.inflation[country].items()
                    if year >= start_year
                }
                
                years = list(country_data.keys())
                values = list(country_data.values())
                dates = pd.to_datetime([f"{year}-12-31" for year in years])
                
                series = pd.Series(values, index=dates, name=country)
                result[country] = series
                
                logger.info(f"Retrieved {len(series)} inflation points for {country}")
        
        return result
    
    def get_unemployment_rate(
        self,
        countries: List[str] = None,
        start_year: int = 2015
    ) -> Dict[str, pd.Series]:
        """Get unemployment rates"""
        if countries is None:
            countries = ['NLD', 'BEL', 'LUX', 'DEU']
        
        result = {}
        
        for country in countries:
            if country in self.unemployment:
                country_data = {
                    year: value 
                    for year, value in self.unemployment[country].items()
                    if year >= start_year
                }
                
                years = list(country_data.keys())
                values = list(country_data.values())
                dates = pd.to_datetime([f"{year}-12-31" for year in years])
                
                series = pd.Series(values, index=dates, name=country)
                result[country] = series
                
                logger.info(f"Retrieved {len(series)} unemployment points for {country}")
        
        return result
    
    def get_ecb_interest_rates(
        self,
        start_year: int = 2015
    ) -> Dict[str, pd.Series]:
        """
        Get ECB policy interest rates
        
        Returns:
            Dictionary with 'DFR' and 'MRO' series
        """
        result = {}
        
        # DFR (Deposit Facility Rate)
        dfr_data = {
            year: rate 
            for year, rate in self.ecb_dfr.items()
            if year >= start_year
        }
        years = list(dfr_data.keys())
        dates = pd.to_datetime([f"{year}-12-31" for year in years])
        result['DFR'] = pd.Series(list(dfr_data.values()), index=dates, name='DFR')
        
        # MRO (Main Refinancing Operations)
        mro_data = {
            year: rate 
            for year, rate in self.ecb_mro.items()
            if year >= start_year
        }
        result['MRO'] = pd.Series(list(mro_data.values()), index=dates, name='MRO')
        
        logger.info(f"Retrieved ECB interest rates from {start_year}")
        return result
    
    def get_comprehensive_indicators(
        self,
        countries: List[str] = None,
        start_year: int = 2020
    ) -> pd.DataFrame:
        """
        Get all key economic indicators in one DataFrame
        
        Args:
            countries: List of country codes
            start_year: Start year
            
        Returns:
            DataFrame with all indicators
        """
        if countries is None:
            countries = ['NLD', 'BEL', 'LUX', 'DEU']
        
        all_data = []
        
        # Fetch each indicator
        indicators = {
            'gdp_growth': self.get_gdp_growth(countries, start_year),
            'inflation': self.get_inflation_rate(countries, start_year),
            'unemployment': self.get_unemployment_rate(countries, start_year)
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
