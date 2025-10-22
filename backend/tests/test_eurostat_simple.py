"""
Simple Eurostat exploration to understand proper API usage
"""

import eurostat
import pandas as pd
import sys

# Force UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("\n" + "="*80)
    print("Eurostat Library Exploration")
    print("="*80 + "\n")
    
    # Test 1: Get dataset without filters
    print("1. Testing GDP dataset (nama_10_gdp) without filters...")
    try:
        df = eurostat.get_data_df('nama_10_gdp', flags=False)
        print(f"   SUCCESS! Got data! Shape: {df.shape}")
        print(f"\n   Columns: {list(df.columns)}\n")
        print("   First few rows:")
        print(df.head())
        print()
        
        # Check what values are in key columns
        if 'geo' in df.columns:
            geos = df['geo'].unique()[:10]
            print(f"   Sample geo values: {list(geos)}")
        
        if 'unit' in df.columns:
            units = df['unit'].unique()
            print(f"   Unit values: {list(units)}")
        
        if 'na_item' in df.columns:
            na_items = df['na_item'].unique()[:5]
            print(f"   Sample na_item values: {list(na_items)}")
        
        print()
        
    except Exception as e:
        print(f"   FAILED: {e}\n")
        import traceback
        traceback.print_exc()
    
    # Test 2: Try with simple filter
    print("2. Testing unemployment dataset (une_rt_a)...")
    try:
        df = eurostat.get_data_df('une_rt_a', flags=False)
        print(f"   SUCCESS! Got data! Shape: {df.shape}")
        print(f"\n   Columns: {list(df.columns)}\n")
        print("   First few rows:")
        print(df.head())
        print()
        
        # Filter manually for Netherlands
        if 'geo' in df.columns:
            nl_data = df[df['geo'] == 'NL']
            print(f"   Netherlands data: {len(nl_data)} rows")
            if not nl_data.empty:
                print(nl_data.head())
        
        print()
        
    except Exception as e:
        print(f"   FAILED: {e}\n")
        import traceback
        traceback.print_exc()
    
    # Test 3: Check available datasets
    print("3. Checking available datasets...")
    try:
        toc = eurostat.get_toc_df()
        print(f"   SUCCESS! Total datasets: {len(toc)}")
        print("\n   Economic datasets (sample):")
        
        # Find GDP related datasets
        gdp_datasets = toc[toc['title'].str.contains('GDP|gdp', na=False)].head(5)
        for idx, row in gdp_datasets.iterrows():
            print(f"   - {row['code']}: {row['title']}")
        
        print()
        
    except Exception as e:
        print(f"   FAILED: {e}\n")
        import traceback
        traceback.print_exc()
    
    print("="*80)
    print("Exploration Complete")
    print("="*80)

if __name__ == "__main__":
    main()
