"""
Test IMF Data Integration
Run this to verify IMF SDMX API connection and data fetching
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.imf_data import IMFDataService
import pandas as pd
from datetime import datetime


def test_imf_connection():
    """Test basic IMF API connection"""
    print("=" * 80)
    print("IMF SDMX API Integration Test")
    print("=" * 80)
    print()
    
    try:
        # Initialize service
        print("1. Initializing IMF SDMX client...")
        imf_service = IMFDataService()
        print("   ✅ Client initialized successfully!")
        print()
        
        return imf_service
        
    except Exception as e:
        print(f"   ❌ Failed to initialize: {e}")
        return None


def test_gdp_growth(imf_service):
    """Test GDP growth data fetching"""
    print("2. Fetching Real GDP Growth data...")
    print("   Countries: Netherlands, Belgium, Luxembourg, Germany")
    print("   Period: 2015-2025")
    print()
    
    try:
        countries = ['NLD', 'BEL', 'LUX', 'DEU']
        gdp_data = imf_service.get_gdp_growth(countries=countries, start_year=2015)
        
        print("   ✅ GDP Growth Data Retrieved!")
        print()
        
        for country, data in gdp_data.items():
            if not data.empty:
                print(f"   📊 {country}:")
                print(f"      Records: {len(data)}")
                if len(data) > 0:
                    # Show last 5 years
                    recent = data.tail(5)
                    for idx, value in recent.items():
                        try:
                            year = idx[1] if isinstance(idx, tuple) else idx
                            print(f"      {year}: {value:.2f}%")
                        except:
                            print(f"      {idx}: {value:.2f}%")
                print()
            else:
                print(f"   ⚠️  {country}: No data available")
                print()
        
        return True
        
    except Exception as e:
        print(f"   ❌ Failed to fetch GDP data: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_inflation(imf_service):
    """Test inflation data fetching"""
    print("3. Fetching Inflation (CPI) data...")
    print()
    
    try:
        countries = ['NLD', 'BEL', 'LUX', 'DEU']
        inflation_data = imf_service.get_inflation_rate(countries=countries, start_year=2015)
        
        print("   ✅ Inflation Data Retrieved!")
        print()
        
        for country, data in inflation_data.items():
            if not data.empty:
                print(f"   📈 {country}:")
                print(f"      Records: {len(data)}")
                if len(data) > 0:
                    recent = data.tail(5)
                    for idx, value in recent.items():
                        try:
                            year = idx[1] if isinstance(idx, tuple) else idx
                            print(f"      {year}: {value:.2f}%")
                        except:
                            print(f"      {idx}: {value:.2f}%")
                print()
            else:
                print(f"   ⚠️  {country}: No data available")
                print()
        
        return True
        
    except Exception as e:
        print(f"   ❌ Failed to fetch inflation data: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_unemployment(imf_service):
    """Test unemployment data fetching"""
    print("4. Fetching Unemployment Rate data...")
    print()
    
    try:
        countries = ['NLD', 'BEL', 'LUX', 'DEU']
        unemp_data = imf_service.get_unemployment_rate(countries=countries, start_year=2015)
        
        print("   ✅ Unemployment Data Retrieved!")
        print()
        
        for country, data in unemp_data.items():
            if not data.empty:
                print(f"   📉 {country}:")
                print(f"      Records: {len(data)}")
                if len(data) > 0:
                    recent = data.tail(5)
                    for idx, value in recent.items():
                        try:
                            year = idx[1] if isinstance(idx, tuple) else idx
                            print(f"      {year}: {value:.2f}%")
                        except:
                            print(f"      {idx}: {value:.2f}%")
                print()
            else:
                print(f"   ⚠️  {country}: No data available")
                print()
        
        return True
        
    except Exception as e:
        print(f"   ❌ Failed to fetch unemployment data: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_government_debt(imf_service):
    """Test government debt data fetching"""
    print("5. Fetching Government Debt (% of GDP) data...")
    print()
    
    try:
        countries = ['NLD', 'BEL', 'LUX', 'DEU']
        debt_data = imf_service.get_government_debt(countries=countries, start_year=2015)
        
        print("   ✅ Government Debt Data Retrieved!")
        print()
        
        for country, data in debt_data.items():
            if not data.empty:
                print(f"   💰 {country}:")
                print(f"      Records: {len(data)}")
                if len(data) > 0:
                    recent = data.tail(5)
                    for idx, value in recent.items():
                        try:
                            year = idx[1] if isinstance(idx, tuple) else idx
                            print(f"      {year}: {value:.2f}%")
                        except:
                            print(f"      {idx}: {value:.2f}%")
                print()
            else:
                print(f"   ⚠️  {country}: No data available")
                print()
        
        return True
        
    except Exception as e:
        print(f"   ❌ Failed to fetch government debt data: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_comprehensive(imf_service):
    """Test comprehensive indicator fetching"""
    print("6. Fetching Comprehensive Economic Indicators...")
    print()
    
    try:
        countries = ['NLD', 'BEL', 'LUX', 'DEU']
        df = imf_service.get_comprehensive_indicators(countries=countries, start_year=2020)
        
        if not df.empty:
            print("   ✅ Comprehensive Data Retrieved!")
            print(f"   Total records: {len(df)}")
            print()
            print("   Sample data:")
            print(df.head(10))
            print()
        else:
            print("   ⚠️  No comprehensive data available")
            print()
        
        return True
        
    except Exception as e:
        print(f"   ❌ Failed to fetch comprehensive data: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print()
    print("🚀 Starting IMF Data Integration Tests")
    print()
    
    # Test connection
    imf_service = test_imf_connection()
    if not imf_service:
        print("❌ Cannot proceed without IMF connection")
        return
    
    # Run tests
    results = []
    
    results.append(("GDP Growth", test_gdp_growth(imf_service)))
    results.append(("Inflation", test_inflation(imf_service)))
    results.append(("Unemployment", test_unemployment(imf_service)))
    results.append(("Government Debt", test_government_debt(imf_service)))
    results.append(("Comprehensive", test_comprehensive(imf_service)))
    
    # Summary
    print("=" * 80)
    print("Test Summary")
    print("=" * 80)
    print()
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:20} {status}")
    
    print()
    print(f"Total: {passed}/{total} tests passed")
    print()
    
    if passed == total:
        print("🎉 All tests passed! IMF integration is working correctly.")
        print()
        print("Next steps:")
        print("  1. Install dependencies: pip install -r requirements.prod.txt")
        print("  2. Run this test: python tests/test_imf_integration.py")
        print("  3. Proceed with Eurostat and ECB integration")
    else:
        print("⚠️  Some tests failed. Check error messages above.")
        print()
        print("Common issues:")
        print("  - Missing sdmx1 library: pip install sdmx1")
        print("  - Missing pandas: pip install pandas")
        print("  - Network issues: Check internet connection")
        print("  - IMF API down: Try again later")
    
    print()


if __name__ == "__main__":
    main()
