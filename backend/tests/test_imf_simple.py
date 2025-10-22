"""
Simple IMF SDMX API exploration script
Tests what data sources and flows are actually available
"""

import sdmx
import sys
import os

# Add parent directory to path to import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def main():
    print("\n" + "="*80)
    print("IMF SDMX API Exploration")
    print("="*80 + "\n")
    
    # Initialize IMF client
    print("1. Initializing IMF SDMX client...")
    try:
        client = sdmx.Client('IMF')
        print("   ✅ Client initialized successfully!\n")
    except Exception as e:
        print(f"   ❌ Failed to initialize client: {e}\n")
        return
    
    # List available dataflows
    print("2. Fetching available dataflows...")
    try:
        flows = client.dataflow()
        print(f"   ✅ Found {len(flows.dataflow)} dataflows\n")
        
        print("   Available dataflows:")
        for flow_id, flow in list(flows.dataflow.items())[:20]:  # Show first 20
            print(f"   - {flow_id}: {flow.name}")
        
        if len(flows.dataflow) > 20:
            print(f"   ... and {len(flows.dataflow) - 20} more\n")
        else:
            print()
            
    except Exception as e:
        print(f"   ❌ Failed to fetch dataflows: {e}\n")
        return
    
    # Try fetching IFS (International Financial Statistics) data - more reliable
    print("3. Testing IFS (International Financial Statistics) data...")
    try:
        # Try to get data for Netherlands (NLD)
        # Using a simple indicator like exchange rate
        print("   Fetching Netherlands exchange rate data...")
        
        # IFS dataflow with key structure
        msg = client.data(
            resource_id='IFS',
            key={'FREQ': 'M', 'REF_AREA': 'NL', 'INDICATOR': 'ENDA_XDC_USD_RATE'},
            params={'startPeriod': '2020'}
        )
        
        print(f"   Response type: {type(msg)}")
        print(f"   Has data: {msg.data is not None}")
        
        if msg.data:
            # Convert to pandas
            df = sdmx.to_pandas(msg.data[0])
            print(f"   ✅ Got data! Shape: {df.shape}")
            print(f"\n   Sample data:\n{df.head()}\n")
        else:
            print("   ⚠️  No data returned\n")
            
    except Exception as e:
        print(f"   ⚠️  IFS test failed: {e}\n")
    
    # Try DOT (Direction of Trade) - another common one
    print("4. Testing DOT (Direction of Trade Statistics) data...")
    try:
        print("   Fetching Netherlands trade data...")
        
        msg = client.data(
            resource_id='DOT',
            key={'FREQ': 'M', 'REF_AREA': 'NL', 'INDICATOR': 'TXG_FOB_USD'},
            params={'startPeriod': '2020'}
        )
        
        if msg.data:
            df = sdmx.to_pandas(msg.data[0])
            print(f"   ✅ Got data! Shape: {df.shape}")
            print(f"\n   Sample data:\n{df.head()}\n")
        else:
            print("   ⚠️  No data returned\n")
            
    except Exception as e:
        print(f"   ⚠️  DOT test failed: {e}\n")
    
    # Check WEO availability
    print("5. Checking WEO (World Economic Outlook) availability...")
    try:
        # WEO might have different key structure
        msg = client.data(
            resource_id='WEO',
            key={},  # Empty key to see what's available
            params={'startPeriod': '2020'}
        )
        
        if msg.data:
            print(f"   ✅ WEO data is available!")
            df = sdmx.to_pandas(msg.data[0])
            print(f"   Shape: {df.shape}")
            print(f"\n   Sample data:\n{df.head()}\n")
        else:
            print("   ⚠️  WEO returned no data\n")
            
    except Exception as e:
        print(f"   ⚠️  WEO not available or different format: {e}\n")
    
    print("="*80)
    print("Exploration Complete")
    print("="*80)
    
    print("\n💡 Key Findings:")
    print("   - IMF SDMX API client works")
    print("   - Need to test which dataflows return actual data")
    print("   - May need to use IFS or DOT instead of WEO")
    print("   - Country codes might need different format (NL vs NLD)")
    print()

if __name__ == "__main__":
    main()
