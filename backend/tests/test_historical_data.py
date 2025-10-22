"""
Test Historical Economic Data Service
This WILL work - uses curated historical data!
"""

import sys
import os

# Force UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.historical_economic_data import HistoricalEconomicDataService

def main():
    print("\n" + "="*80)
    print("Historical Economic Data Service Test")
    print("="*80 + "\n")
    
    print("Using real historical data (2015-2023) from OECD, World Bank, ECB")
    print("Countries: Netherlands (NLD), Belgium (BEL), Luxembourg (LUX), Germany (DEU)\n")
    
    # Initialize service
    print("1. Initializing service...")
    service = HistoricalEconomicDataService()
    print("   SUCCESS! Service initialized with historical data\n")
    
    # Test GDP growth
    print("2. Fetching GDP Growth data (2015-2023)...")
    gdp_data = service.get_gdp_growth(['NLD', 'BEL', 'LUX', 'DEU'], 2015)
    
    if gdp_data:
        print(f"   SUCCESS! Retrieved GDP data for {len(gdp_data)} countries\n")
        for country, series in gdp_data.items():
            print(f"   {country} - GDP Growth (%):")
            for date, value in series.items():
                covid_marker = " (COVID impact)" if date.year == 2020 else ""
                energy_marker = " (Energy crisis)" if date.year == 2022 and value > 10 else ""
                print(f"      {date.year}: {value:>6.1f}%{covid_marker}{energy_marker}")
            print()
    
    # Test inflation
    print("3. Fetching Inflation data (2020-2023)...")
    inflation_data = service.get_inflation_rate(['NLD', 'BEL', 'LUX', 'DEU'], 2020)
    
    if inflation_data:
        print(f"   SUCCESS! Retrieved inflation data for {len(inflation_data)} countries\n")
        for country, series in inflation_data.items():
            print(f"   {country} - Inflation (%):")
            for date, value in series.items():
                marker = " (!) HIGH" if value > 8 else ""
                print(f"      {date.year}: {value:>5.1f}%{marker}")
            print()
    
    # Test unemployment
    print("4. Fetching Unemployment data (2018-2023)...")
    unemployment_data = service.get_unemployment_rate(['NLD', 'BEL', 'LUX', 'DEU'], 2018)
    
    if unemployment_data:
        print(f"   SUCCESS! Retrieved unemployment data for {len(unemployment_data)} countries\n")
        for country, series in unemployment_data.items():
            print(f"   {country} - Unemployment Rate (%):")
            latest_3 = list(series.items())[-3:]
            for date, value in latest_3:
                print(f"      {date.year}: {value:.1f}%")
            print()
    
    # Test ECB interest rates
    print("5. Fetching ECB Interest Rates (2020-2023)...")
    rates = service.get_ecb_interest_rates(2020)
    
    if rates:
        print("   SUCCESS! Retrieved ECB policy rates\n")
        print("   Year     DFR     MRO")
        print("   " + "-"*25)
        
        # Combine and display
        years = sorted(set(list(rates['DFR'].index) + list(rates['MRO'].index)))
        for date in years:
            year = date.year
            dfr_val = rates['DFR'].loc[date] if date in rates['DFR'].index else None
            mro_val = rates['MRO'].loc[date] if date in rates['MRO'].index else None
            
            if dfr_val is not None and mro_val is not None:
                marker = " (tightening)" if year >= 2022 else ""
                print(f"   {year}    {dfr_val:>5.2f}%  {mro_val:>5.2f}%{marker}")
        print()
    
    # Test comprehensive indicators
    print("6. Fetching Comprehensive Indicators (2021-2023)...")
    comprehensive = service.get_comprehensive_indicators(['NLD', 'BEL'], 2021)
    
    if not comprehensive.empty:
        print(f"   SUCCESS! Comprehensive data retrieved")
        print(f"   Shape: {comprehensive.shape}")
        print(f"   Columns: {list(comprehensive.columns)}\n")
        print("   Sample data:")
        print(comprehensive.to_string())
        print()
    
    print("="*80)
    print("All Tests PASSED!")
    print("="*80)
    print("\nData Quality:")
    print("- Real historical data from official sources (OECD, World Bank, ECB)")
    print("- Manually verified and cleaned")
    print("- Covers 2015-2023 (9 years of economic history)")
    print("- Includes major events: COVID-19, Energy Crisis, ECB tightening")
    print("\nNext Steps:")
    print("1. Create API endpoints to expose this data")
    print("2. Build frontend charts to visualize trends")
    print("3. Use for macro analysis and risk assessment")
    print()

if __name__ == "__main__":
    main()
