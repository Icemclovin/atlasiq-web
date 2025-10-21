import requests
import json

# Create test/developer account
url = "http://localhost:8000/api/v1/auth/register"
data = {
    "email": "dev@atlasiq.com",
    "password": "developer123",
    "full_name": "Developer Account"
}

try:
    response = requests.post(url, json=data)
    print("Status Code:", response.status_code)
    print("\nResponse:")
    print(json.dumps(response.json(), indent=2))
    
    if response.status_code == 200:
        print("\n✅ SUCCESS! Test account created:")
        print("   Email: dev@atlasiq.com")
        print("   Password: developer123")
    else:
        print("\n⚠️ Registration failed or account already exists")
        
except requests.exceptions.ConnectionError:
    print("❌ Error: Backend server is not running!")
    print("Please start the backend first at http://localhost:8000")
except Exception as e:
    print(f"❌ Error: {e}")
