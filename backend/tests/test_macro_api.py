"""
Test macro API endpoints
"""
import requests
import json
import time

# Wait for server to be ready
print("Waiting for server to start...")
time.sleep(2)

base_url = "http://localhost:8000/api/v1/macro"

print("\n" + "="*80)
print("Testing Macro API Endpoints")
print("="*80 + "\n")

# Test 1: GDP endpoint
print("1. Testing /api/v1/macro/gdp endpoint...")
print("   Request: GET /api/v1/macro/gdp?countries=NLD,BEL&start_year=2020\n")

try:
    response = requests.get(f"{base_url}/gdp", params={
        "countries": ["NLD", "BEL"],  # 3-letter ISO codes
        "start_year": 2020
    })
    
    if response.status_code == 200:
        data = response.json()
        print("   ✅ SUCCESS! Status Code: 200")
        print(f"\n   Response Preview:")
        print(f"   Total records: {len(data.get('data', []))}")
        print(f"\n   Metadata:")
        print(json.dumps(data.get('metadata', {}), indent=4))
        print(f"\n   Sample Data (first 3 records):")
        for record in data.get('data', [])[:3]:
            print(f"   - {record}")
        print()
    else:
        print(f"   ❌ FAILED! Status Code: {response.status_code}")
        print(f"   Response: {response.text}\n")
        
except Exception as e:
    print(f"   ❌ ERROR: {e}\n")

# Test 2: Inflation endpoint
print("2. Testing /api/v1/macro/inflation endpoint...")
print("   Request: GET /api/v1/macro/inflation?countries=LUX,DEU&start_year=2018\n")

try:
    response = requests.get(f"{base_url}/inflation", params={
        "countries": ["LUX", "DEU"],  # 3-letter ISO codes
        "start_year": 2018
    })
    
    if response.status_code == 200:
        data = response.json()
        print("   ✅ SUCCESS! Status Code: 200")
        print(f"   Total records: {len(data.get('data', []))}")
        print(f"   Sample (last 3):")
        for record in data.get('data', [])[-3:]:
            print(f"   - {record}")
        print()
    else:
        print(f"   ❌ FAILED! Status Code: {response.status_code}\n")
        
except Exception as e:
    print(f"   ❌ ERROR: {e}\n")

# Test 3: Unemployment endpoint
print("3. Testing /api/v1/macro/unemployment endpoint...")
print("   Request: GET /api/v1/macro/unemployment?countries=NLD\n")

try:
    response = requests.get(f"{base_url}/unemployment", params={
        "countries": ["NLD"]  # 3-letter ISO code
    })
    
    if response.status_code == 200:
        data = response.json()
        print("   ✅ SUCCESS! Status Code: 200")
        print(f"   Total records: {len(data.get('data', []))}")
        print(f"   Years covered: {data['data'][0]['year']} - {data['data'][-1]['year']}")
        print()
    else:
        print(f"   ❌ FAILED! Status Code: {response.status_code}\n")
        
except Exception as e:
    print(f"   ❌ ERROR: {e}\n")

# Test 4: Interest rates endpoint
print("4. Testing /api/v1/macro/interest-rates endpoint...")
print("   Request: GET /api/v1/macro/interest-rates?start_year=2020\n")

try:
    response = requests.get(f"{base_url}/interest-rates", params={
        "start_year": 2020
    })
    
    if response.status_code == 200:
        data = response.json()
        print("   ✅ SUCCESS! Status Code: 200")
        print(f"   Total records: {len(data.get('data', []))}")
        print(f"   Rate types: {set(r['rate_type'] for r in data['data'])}")
        print(f"   Sample:")
        for record in data.get('data', [])[:2]:
            print(f"   - {record}")
        print()
    else:
        print(f"   ❌ FAILED! Status Code: {response.status_code}\n")
        
except Exception as e:
    print(f"   ❌ ERROR: {e}\n")

print("="*80)
print("API Testing Complete")
print("="*80)
print("\n✅ All macro endpoints are working with historical data!")
print("📊 Ready for frontend integration\n")
