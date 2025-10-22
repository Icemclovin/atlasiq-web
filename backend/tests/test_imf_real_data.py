"""
Test IMF SDMX API with actual available dataflows
Using the real dataflow IDs from the API
"""

import sdmx
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def main():
    print("\n" + "="*80)
    print("IMF SDMX API Real Data Test")
    print("="*80 + "\n")
    
    # Initialize client
    print("1. Initializing IMF SDMX client...")
    client = sdmx.Client('IMF')
    print("   ✅ Client initialized\n")
    
    # Test BOP (Balance of Payments) - this one exists
    print("2. Testing BOP_BPM6 (Balance of Payments)...")
    try:
        # Get dataflow structure first
        flow = client.dataflow('BOP_BPM6')
        print(f"   ✅ Dataflow found: {flow.dataflow['BOP_BPM6'].name}\n")
        
        # Try to get some data
        print("   Fetching Netherlands BoP data...")
        msg = client.data(
            resource_id='BOP_BPM6',
            key={'FREQ': 'A', 'REF_AREA': 'NL'},  # Annual, Netherlands
            params={'startPeriod': '2015', 'endPeriod': '2023'}
        )
        
        if msg.data:
            df = sdmx.to_pandas(msg.data[0])
            print(f"   ✅ Got data! Shape: {df.shape}")
            print(f"\n   First few rows:\n{df.head(10)}\n")
        else:
            print("   ⚠️  No data returned\n")
            
    except Exception as e:
        print(f"   ❌ Failed: {e}\n")
    
    # Test another one - Interest Rates
    print("3. Testing 6SR (Interest Rates and Share Prices)...")
    try:
        msg = client.data(
            resource_id='6SR',
            key={'FREQ': 'M', 'REF_AREA': 'NL'},
            params={'startPeriod': '2020'}
        )
        
        if msg.data:
            df = sdmx.to_pandas(msg.data[0])
            print(f"   ✅ Got data! Shape: {df.shape}")
            print(f"\n   First few rows:\n{df.head(10)}\n")
        else:
            print("   ⚠️  No data returned\n")
            
    except Exception as e:
        print(f"   ❌ Failed: {e}\n")
    
    # Test National Accounts
    print("4. Testing 90R (National Accounts)...")
    try:
        msg = client.data(
            resource_id='90R',
            key={'FREQ': 'A', 'REF_AREA': 'NL'},
            params={'startPeriod': '2015'}
        )
        
        if msg.data:
            df = sdmx.to_pandas(msg.data[0])
            print(f"   ✅ Got data! Shape: {df.shape}")
            print(f"\n   First few rows:\n{df.head(10)}\n")
        else:
            print("   ⚠️  No data returned\n")
            
    except Exception as e:
        print(f"   ❌ Failed: {e}\n")
    
    print("="*80)
    print("Test Complete")
    print("="*80)
    print("\n💡 Next: Update imf_data.py service to use working dataflows\n")

if __name__ == "__main__":
    main()
