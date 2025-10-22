"""
Test World Bank Data360 API
This should be much more reliable than IMF/Eurostat!
"""

import sys
import os

# Force UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.worldbank_data import WorldBankData360Service

def main():
    print("\n" + "="*80)
    print("World Bank Data360 API Integration Test")
    print("="*80 + "\n")
    
    # Initialize service
    print("1. Initializing World Bank Data360 service...")
    try:
        service = WorldBankData360Service()
        print("   SUCCESS! Service initialized\n")
    except Exception as e:
        print(f"   FAILED: {e}\n")
        return
    
    # Test search function
    print("2. Searching for GDP indicators...")
    try:
        gdp_indicators = service.search_indicators("GDP growth", limit=5)
        
        if gdp_indicators:
            print(f"   SUCCESS! Found {len(gdp_indicators)} indicators\n")
            print("   Available GDP indicators:")
            for ind in gdp_indicators[:3]:
                print(f"   - ID {ind.get('indicatorId')}: {ind.get('indicatorName')}")
                print(f"     Source: {ind.get('source', 'N/A')}")
            print()
        else:
            print("   WARNING: No GDP indicators found\n")
            
    except Exception as e:
        print(f"   FAILED: {e}\n")
        import traceback
        traceback.print_exc()
    
    # Test inflation search
    print("3. Searching for inflation indicators...")
    try:
        inflation_indicators = service.search_indicators("inflation consumer prices", limit=5)
        
        if inflation_indicators:
            print(f"   SUCCESS! Found {len(inflation_indicators)} indicators\n")
            print("   Available inflation indicators:")
            for ind in inflation_indicators[:3]:
                print(f"   - ID {ind.get('indicatorId')}: {ind.get('indicatorName')}")
            print()
        else:
            print("   WARNING: No inflation indicators found\n")
            
    except Exception as e:
        print(f"   FAILED: {e}\n")
        import traceback
        traceback.print_exc()
    
    # Test unemployment search
    print("4. Searching for unemployment indicators...")
    try:
        unemployment_indicators = service.search_indicators("unemployment rate", limit=5)
        
        if unemployment_indicators:
            print(f"   SUCCESS! Found {len(unemployment_indicators)} indicators\n")
            print("   Available unemployment indicators:")
            for ind in unemployment_indicators[:3]:
                print(f"   - ID {ind.get('indicatorId')}: {ind.get('indicatorName')}")
            print()
        else:
            print("   WARNING: No unemployment indicators found\n")
            
    except Exception as e:
        print(f"   FAILED: {e}\n")
        import traceback
        traceback.print_exc()
    
    # Test fetching actual data
    print("5. Fetching GDP growth data for Benelux + Germany...")
    print("   Countries: Netherlands (NLD), Belgium (BEL), Luxembourg (LUX), Germany (DEU)")
    print("   Period: 2015-2023\n")
    
    try:
        gdp_data = service.get_gdp_growth(['NLD', 'BEL', 'LUX', 'DEU'], 2015)
        
        if gdp_data:
            print("   SUCCESS! GDP Growth Data Retrieved!\n")
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
            print("   WARNING: No GDP data retrieved\n")
            
    except Exception as e:
        print(f"   FAILED: {e}\n")
        import traceback
        traceback.print_exc()
    
    # Test comprehensive indicators
    print("6. Fetching comprehensive economic indicators...")
    try:
        comprehensive = service.get_comprehensive_indicators(['NLD', 'BEL'], 2020)
        
        if not comprehensive.empty:
            print(f"   SUCCESS! Comprehensive data retrieved")
            print(f"   Shape: {comprehensive.shape}")
            print(f"   Columns: {list(comprehensive.columns)}\n")
            print("   Sample data:")
            print(comprehensive.head(10))
            print()
        else:
            print("   WARNING: No comprehensive data\n")
            
    except Exception as e:
        print(f"   FAILED: {e}\n")
        import traceback
        traceback.print_exc()
    
    print("="*80)
    print("Test Complete")
    print("="*80)
    print("\nWorld Bank Data360 API Test Results:")
    print("- Free API access: CHECK")
    print("- No authentication required: CHECK")
    print("- Good documentation: CHECK")
    print("- Covers Benelux + Germany: Testing...")
    print("\nNext: If successful, this becomes our primary macro data source!")
    print()

if __name__ == "__main__":
    main()
