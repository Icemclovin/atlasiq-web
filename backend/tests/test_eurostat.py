"""
Test Eurostat integration using official Python library
Much more reliable than IMF SDMX
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.eurostat_data import EurostatDataService

def main():
    print("\n" + "="*80)
    print("Eurostat Integration Test")
    print("="*80 + "\n")
    
    # Initialize service
    print("1. Initializing Eurostat service...")
    try:
        service = EurostatDataService()
        print("   ✅ Service initialized successfully!\n")
    except Exception as e:
        print(f"   ❌ Failed: {e}\n")
        return
    
    # Test GDP growth
    print("2. Fetching GDP Growth data...")
    print("   Countries: Netherlands (NL), Belgium (BE), Luxembourg (LU), Germany (DE)")
    print("   Period: 2015-present\n")
    
    try:
        gdp_data = service.get_gdp_growth(['NL', 'BE', 'LU', 'DE'], 2015)
        
        if gdp_data:
            print("   ✅ GDP Growth Data Retrieved!\n")
            for country, series in gdp_data.items():
                print(f"   {country}:")
                if len(series) > 0:
                    print(f"      Data points: {len(series)}")
                    print(f"      Latest 3 years:")
                    for date, value in list(series.items())[-3:]:
                        print(f"      {date.year}: {value:.2f}%")
                else:
                    print(f"      No data available")
                print()
        else:
            print("   ⚠️  No GDP data available\n")
            
    except Exception as e:
        print(f"   ❌ Failed: {e}\n")
        import traceback
        traceback.print_exc()
    
    # Test inflation
    print("3. Fetching Inflation (HICP) data...")
    try:
        inflation_data = service.get_inflation_rate(['NL', 'BE', 'LU', 'DE'], 2020)
        
        if inflation_data:
            print("   ✅ Inflation Data Retrieved!\n")
            for country, series in inflation_data.items():
                print(f"   {country}:")
                if len(series) > 0:
                    print(f"      Data points: {len(series)}")
                    print(f"      Latest 6 months:")
                    for date, value in list(series.items())[-6:]:
                        print(f"      {date.strftime('%Y-%m')}: {value:.2f}%")
                else:
                    print(f"      No data available")
                print()
        else:
            print("   ⚠️  No inflation data available\n")
            
    except Exception as e:
        print(f"   ❌ Failed: {e}\n")
        import traceback
        traceback.print_exc()
    
    # Test unemployment
    print("4. Fetching Unemployment Rate data...")
    try:
        unemployment_data = service.get_unemployment_rate(['NL', 'BE', 'LU', 'DE'], 2018)
        
        if unemployment_data:
            print("   ✅ Unemployment Data Retrieved!\n")
            for country, series in unemployment_data.items():
                print(f"   {country}:")
                if len(series) > 0:
                    print(f"      Data points: {len(series)}")
                    print(f"      Latest 3 years:")
                    for date, value in list(series.items())[-3:]:
                        print(f"      {date.year}: {value:.2f}%")
                else:
                    print(f"      No data available")
                print()
        else:
            print("   ⚠️  No unemployment data available\n")
            
    except Exception as e:
        print(f"   ❌ Failed: {e}\n")
        import traceback
        traceback.print_exc()
    
    # Test comprehensive indicators
    print("5. Fetching Comprehensive Economic Indicators...")
    try:
        comprehensive_data = service.get_comprehensive_indicators(['NL', 'BE'], 2022)
        
        if not comprehensive_data.empty:
            print(f"   ✅ Comprehensive Data Retrieved!")
            print(f"   Shape: {comprehensive_data.shape}\n")
            print("   Sample data (first 10 rows):")
            print(comprehensive_data.head(10))
            print()
        else:
            print("   ⚠️  No comprehensive data available\n")
            
    except Exception as e:
        print(f"   ❌ Failed: {e}\n")
        import traceback
        traceback.print_exc()
    
    print("="*80)
    print("Test Complete")
    print("="*80)
    print("\n💡 Eurostat provides reliable EU economic data!")
    print("   Perfect for Benelux + Germany analysis\n")

if __name__ == "__main__":
    main()
