"""
Macro Economic Indicators API Endpoints
Provides access to historical economic data for Benelux + Germany
"""

from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from datetime import datetime
import pandas as pd

from app.services.historical_economic_data import HistoricalEconomicDataService

router = APIRouter(prefix="/api/v1/macro", tags=["Macro Indicators"])

# Initialize service
macro_service = HistoricalEconomicDataService()


@router.get("/gdp")
async def get_gdp_growth(
    countries: Optional[List[str]] = Query(default=None, description="Country codes (NLD, BEL, LUX, DEU)"),
    start_year: int = Query(default=2015, ge=2015, le=2023, description="Start year"),
    end_year: int = Query(default=2023, ge=2015, le=2023, description="End year")
):
    """
    Get real GDP growth rates for specified countries
    
    Returns time series data showing year-over-year GDP growth percentages.
    Data source: OECD Statistics
    """
    try:
        # Get data
        gdp_data = macro_service.get_gdp_growth(countries, start_year)
        
        # Convert to API response format
        result = []
        for country, series in gdp_data.items():
            for date, value in series.items():
                if date.year <= end_year:
                    result.append({
                        "country": country,
                        "date": date.strftime("%Y-%m-%d"),
                        "year": date.year,
                        "value": round(value, 2),
                        "indicator": "gdp_growth",
                        "unit": "percent"
                    })
        
        return {
            "data": result,
            "meta": {
                "countries": countries or ["NLD", "BEL", "LUX", "DEU"],
                "start_year": start_year,
                "end_year": end_year,
                "total_records": len(result),
                "data_source": "OECD Statistics",
                "data_type": "historical",
                "last_updated": "2024-01-01"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/inflation")
async def get_inflation(
    countries: Optional[List[str]] = Query(default=None, description="Country codes"),
    start_year: int = Query(default=2015, ge=2015, le=2023),
    end_year: int = Query(default=2023, ge=2015, le=2023)
):
    """
    Get inflation rates (HICP - Harmonized Index of Consumer Prices)
    
    Returns annual inflation percentages.
    Data source: Eurostat / OECD
    """
    try:
        inflation_data = macro_service.get_inflation_rate(countries, start_year)
        
        result = []
        for country, series in inflation_data.items():
            for date, value in series.items():
                if date.year <= end_year:
                    result.append({
                        "country": country,
                        "date": date.strftime("%Y-%m-%d"),
                        "year": date.year,
                        "value": round(value, 2),
                        "indicator": "inflation",
                        "unit": "percent"
                    })
        
        return {
            "data": result,
            "meta": {
                "countries": countries or ["NLD", "BEL", "LUX", "DEU"],
                "start_year": start_year,
                "end_year": end_year,
                "total_records": len(result),
                "data_source": "Eurostat/OECD",
                "data_type": "historical",
                "last_updated": "2024-01-01"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/unemployment")
async def get_unemployment(
    countries: Optional[List[str]] = Query(default=None, description="Country codes"),
    start_year: int = Query(default=2015, ge=2015, le=2023),
    end_year: int = Query(default=2023, ge=2015, le=2023)
):
    """
    Get unemployment rates
    
    Returns unemployment as percentage of active population.
    Data source: OECD Labour Force Statistics
    """
    try:
        unemployment_data = macro_service.get_unemployment_rate(countries, start_year)
        
        result = []
        for country, series in unemployment_data.items():
            for date, value in series.items():
                if date.year <= end_year:
                    result.append({
                        "country": country,
                        "date": date.strftime("%Y-%m-%d"),
                        "year": date.year,
                        "value": round(value, 2),
                        "indicator": "unemployment",
                        "unit": "percent"
                    })
        
        return {
            "data": result,
            "meta": {
                "countries": countries or ["NLD", "BEL", "LUX", "DEU"],
                "start_year": start_year,
                "end_year": end_year,
                "total_records": len(result),
                "data_source": "OECD",
                "data_type": "historical",
                "last_updated": "2024-01-01"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/interest-rates")
async def get_interest_rates(
    start_year: int = Query(default=2015, ge=2015, le=2023),
    end_year: int = Query(default=2023, ge=2015, le=2023)
):
    """
    Get ECB policy interest rates
    
    Returns Deposit Facility Rate (DFR) and Main Refinancing Operations (MRO) rates.
    Data source: European Central Bank Statistical Data Warehouse
    """
    try:
        rates = macro_service.get_ecb_interest_rates(start_year)
        
        result = []
        
        # DFR (Deposit Facility Rate)
        for date, value in rates['DFR'].items():
            if date.year <= end_year:
                result.append({
                    "rate_type": "DFR",
                    "rate_name": "Deposit Facility Rate",
                    "date": date.strftime("%Y-%m-%d"),
                    "year": date.year,
                    "value": round(value, 2),
                    "currency": "EUR",
                    "unit": "percent"
                })
        
        # MRO (Main Refinancing Operations)
        for date, value in rates['MRO'].items():
            if date.year <= end_year:
                result.append({
                    "rate_type": "MRO",
                    "rate_name": "Main Refinancing Operations",
                    "date": date.strftime("%Y-%m-%d"),
                    "year": date.year,
                    "value": round(value, 2),
                    "currency": "EUR",
                    "unit": "percent"
                })
        
        return {
            "data": result,
            "meta": {
                "rate_types": ["DFR", "MRO"],
                "start_year": start_year,
                "end_year": end_year,
                "total_records": len(result),
                "data_source": "European Central Bank",
                "data_type": "historical",
                "last_updated": "2024-01-01"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/comprehensive")
async def get_comprehensive_indicators(
    countries: Optional[List[str]] = Query(default=None, description="Country codes"),
    start_year: int = Query(default=2020, ge=2015, le=2023),
    end_year: int = Query(default=2023, ge=2015, le=2023)
):
    """
    Get all key economic indicators in one request
    
    Returns GDP growth, inflation, and unemployment for specified countries.
    Useful for dashboard views and multi-indicator analysis.
    """
    try:
        df = macro_service.get_comprehensive_indicators(countries, start_year)
        
        # Filter by end year
        df = df[pd.to_datetime(df['date']).dt.year <= end_year]
        
        # Convert to records
        result = df.to_dict('records')
        
        # Format dates
        for record in result:
            if isinstance(record['date'], pd.Timestamp):
                record['date'] = record['date'].strftime("%Y-%m-%d")
                record['year'] = record['date'][:4]
        
        return {
            "data": result,
            "meta": {
                "countries": countries or ["NLD", "BEL", "LUX", "DEU"],
                "indicators": ["gdp_growth", "inflation", "unemployment"],
                "start_year": start_year,
                "end_year": end_year,
                "total_records": len(result),
                "data_sources": {
                    "gdp_growth": "OECD",
                    "inflation": "Eurostat/OECD",
                    "unemployment": "OECD"
                },
                "data_type": "historical",
                "last_updated": "2024-01-01"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/summary")
async def get_macro_summary(
    countries: Optional[List[str]] = Query(default=None, description="Country codes")
):
    """
    Get latest macro indicators summary for each country
    
    Returns most recent values for all key indicators.
    Perfect for dashboard cards and country comparisons.
    """
    try:
        if countries is None:
            countries = ["NLD", "BEL", "LUX", "DEU"]
        
        summary = []
        
        # Get latest data for each country
        gdp_data = macro_service.get_gdp_growth(countries, 2022)
        inflation_data = macro_service.get_inflation_rate(countries, 2022)
        unemployment_data = macro_service.get_unemployment_rate(countries, 2022)
        
        for country in countries:
            country_summary = {
                "country": country,
                "year": 2023,
                "gdp_growth": None,
                "inflation": None,
                "unemployment": None
            }
            
            # Get latest values
            if country in gdp_data and len(gdp_data[country]) > 0:
                country_summary["gdp_growth"] = round(float(gdp_data[country].iloc[-1]), 2)
            
            if country in inflation_data and len(inflation_data[country]) > 0:
                country_summary["inflation"] = round(float(inflation_data[country].iloc[-1]), 2)
            
            if country in unemployment_data and len(unemployment_data[country]) > 0:
                country_summary["unemployment"] = round(float(unemployment_data[country].iloc[-1]), 2)
            
            summary.append(country_summary)
        
        return {
            "data": summary,
            "meta": {
                "countries": countries,
                "reference_year": 2023,
                "data_type": "historical",
                "last_updated": "2024-01-01"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
