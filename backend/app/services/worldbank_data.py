"""
World Bank Data360 API Service
Much more accessible than IMF/Eurostat - great for economic indicators!
"""

import requests
import pandas as pd
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class WorldBankData360Service:
    """
    Service to fetch economic data from World Bank Data360 API
    Free API, no authentication required, excellent documentation
    """
    
    def __init__(self):
        """Initialize World Bank Data360 service"""
        self.base_url = "https://data360api.worldbank.org/data360"
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': 'AtlasIQ/1.0'
        })
        logger.info("World Bank Data360 API service initialized")
    
    def search_indicators(
        self,
        query: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search for indicators by keyword
        
        Args:
            query: Search term (e.g., "GDP growth", "inflation", "unemployment")
            limit: Max results to return
            
        Returns:
            List of matching indicators with metadata
        """
        try:
            url = f"{self.base_url}/searchv2"
            
            payload = {
                "query": query,
                "limit": limit
            }
            
            logger.info(f"Searching indicators: {query}")
            response = self.session.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Found {len(data)} indicators")
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Search failed: {e}")
            return []
    
    def get_data(
        self,
        indicator_ids: List[int],
        countries: List[str] = None,
        start_year: int = 2015,
        end_year: int = 2023
    ) -> pd.DataFrame:
        """
        Get data for specific indicators
        
        Args:
            indicator_ids: List of indicator IDs from search results
            countries: List of country codes (NLD, BEL, LUX, DEU)
            start_year: Start year
            end_year: End year
            
        Returns:
            DataFrame with time series data
        """
        if countries is None:
            countries = ['NLD', 'BEL', 'LUX', 'DEU']
        
        try:
            url = f"{self.base_url}/data"
            
            params = {
                'indicatorIds': ','.join(map(str, indicator_ids)),
                'countries': ','.join(countries),
                'startYear': start_year,
                'endYear': end_year
            }
            
            logger.info(f"Fetching data for indicators: {indicator_ids}")
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Parse response into DataFrame
            records = []
            for item in data:
                records.append({
                    'indicator_id': item.get('indicatorId'),
                    'indicator_name': item.get('indicatorName'),
                    'country': item.get('countryCode'),
                    'country_name': item.get('countryName'),
                    'year': item.get('year'),
                    'value': item.get('value'),
                    'source': item.get('source')
                })
            
            df = pd.DataFrame(records)
            logger.info(f"Retrieved {len(df)} data points")
            return df
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Data fetch failed: {e}")
            return pd.DataFrame()
    
    def get_metadata(
        self,
        indicator_ids: List[int]
    ) -> Dict[int, Dict[str, Any]]:
        """
        Get metadata for indicators
        
        Args:
            indicator_ids: List of indicator IDs
            
        Returns:
            Dictionary mapping indicator ID to metadata
        """
        try:
            url = f"{self.base_url}/metadata"
            
            payload = {
                'indicatorIds': indicator_ids
            }
            
            logger.info(f"Fetching metadata for {len(indicator_ids)} indicators")
            response = self.session.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Map by indicator ID
            metadata = {}
            for item in data:
                ind_id = item.get('indicatorId')
                metadata[ind_id] = {
                    'name': item.get('indicatorName'),
                    'description': item.get('description'),
                    'unit': item.get('unit'),
                    'source': item.get('source'),
                    'frequency': item.get('frequency'),
                    'last_updated': item.get('lastUpdated')
                }
            
            return metadata
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Metadata fetch failed: {e}")
            return {}
    
    def get_gdp_growth(
        self,
        countries: List[str] = None,
        start_year: int = 2015
    ) -> Dict[str, pd.Series]:
        """
        Get real GDP growth rates
        
        Args:
            countries: List of 3-letter country codes (NLD, BEL, LUX, DEU)
            start_year: Start year
            
        Returns:
            Dictionary mapping country to GDP growth series
        """
        if countries is None:
            countries = ['NLD', 'BEL', 'LUX', 'DEU']
        
        try:
            # First search for GDP growth indicator
            indicators = self.search_indicators("GDP growth annual", limit=5)
            
            if not indicators:
                logger.warning("No GDP growth indicators found")
                return {}
            
            # Use first matching indicator
            indicator_id = indicators[0].get('indicatorId')
            logger.info(f"Using GDP indicator: {indicators[0].get('indicatorName')}")
            
            # Fetch data
            df = self.get_data([indicator_id], countries, start_year, 2023)
            
            if df.empty:
                return {}
            
            # Convert to country series
            result = {}
            for country in countries:
                country_data = df[df['country'] == country]
                
                if not country_data.empty:
                    # Sort by year
                    country_data = country_data.sort_values('year')
                    
                    # Create datetime index
                    dates = pd.to_datetime([f"{year}-12-31" for year in country_data['year']])
                    series = pd.Series(
                        country_data['value'].values,
                        index=dates,
                        name=country
                    )
                    
                    result[country] = series
            
            logger.info(f"Retrieved GDP growth for {len(result)} countries")
            return result
            
        except Exception as e:
            logger.error(f"Failed to fetch GDP growth: {e}")
            return {}
    
    def get_inflation_rate(
        self,
        countries: List[str] = None,
        start_year: int = 2015
    ) -> Dict[str, pd.Series]:
        """
        Get inflation rates (CPI)
        
        Args:
            countries: List of country codes
            start_year: Start year
            
        Returns:
            Dictionary mapping country to inflation series
        """
        if countries is None:
            countries = ['NLD', 'BEL', 'LUX', 'DEU']
        
        try:
            # Search for inflation indicator
            indicators = self.search_indicators("inflation consumer prices", limit=5)
            
            if not indicators:
                logger.warning("No inflation indicators found")
                return {}
            
            indicator_id = indicators[0].get('indicatorId')
            logger.info(f"Using inflation indicator: {indicators[0].get('indicatorName')}")
            
            df = self.get_data([indicator_id], countries, start_year, 2023)
            
            if df.empty:
                return {}
            
            result = {}
            for country in countries:
                country_data = df[df['country'] == country]
                
                if not country_data.empty:
                    country_data = country_data.sort_values('year')
                    dates = pd.to_datetime([f"{year}-12-31" for year in country_data['year']])
                    series = pd.Series(
                        country_data['value'].values,
                        index=dates,
                        name=country
                    )
                    result[country] = series
            
            logger.info(f"Retrieved inflation for {len(result)} countries")
            return result
            
        except Exception as e:
            logger.error(f"Failed to fetch inflation: {e}")
            return {}
    
    def get_unemployment_rate(
        self,
        countries: List[str] = None,
        start_year: int = 2015
    ) -> Dict[str, pd.Series]:
        """
        Get unemployment rates
        
        Args:
            countries: List of country codes
            start_year: Start year
            
        Returns:
            Dictionary mapping country to unemployment series
        """
        if countries is None:
            countries = ['NLD', 'BEL', 'LUX', 'DEU']
        
        try:
            # Search for unemployment indicator
            indicators = self.search_indicators("unemployment rate", limit=5)
            
            if not indicators:
                logger.warning("No unemployment indicators found")
                return {}
            
            indicator_id = indicators[0].get('indicatorId')
            logger.info(f"Using unemployment indicator: {indicators[0].get('indicatorName')}")
            
            df = self.get_data([indicator_id], countries, start_year, 2023)
            
            if df.empty:
                return {}
            
            result = {}
            for country in countries:
                country_data = df[df['country'] == country]
                
                if not country_data.empty:
                    country_data = country_data.sort_values('year')
                    dates = pd.to_datetime([f"{year}-12-31" for year in country_data['year']])
                    series = pd.Series(
                        country_data['value'].values,
                        index=dates,
                        name=country
                    )
                    result[country] = series
            
            logger.info(f"Retrieved unemployment for {len(result)} countries")
            return result
            
        except Exception as e:
            logger.error(f"Failed to fetch unemployment: {e}")
            return {}
    
    def get_comprehensive_indicators(
        self,
        countries: List[str] = None,
        start_year: int = 2020
    ) -> pd.DataFrame:
        """
        Get all key economic indicators
        
        Args:
            countries: List of country codes
            start_year: Start year
            
        Returns:
            DataFrame with all indicators
        """
        if countries is None:
            countries = ['NLD', 'BEL', 'LUX', 'DEU']
        
        try:
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
            
        except Exception as e:
            logger.error(f"Failed to fetch comprehensive indicators: {e}")
            return pd.DataFrame()
