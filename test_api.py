"""
Quick API test script
"""
import requests
import json
import time

def test_api():
    base_url = "http://localhost:8000"
    
    print("=" * 60)
    print("  API TEST")
    print("=" * 60)
    print()
    
    # Test 1: Health check
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"   ✓ Status: {response.status_code}")
        print(f"   ✓ Response: {response.json()}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        print("\n   Note: Make sure server is running with: python main.py")
        return
    
    print()
    
    # Test 2: Root endpoint
    print("2. Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"   ✓ Status: {response.status_code}")
        print(f"   ✓ Response: {response.json()}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print()
    
    # Test 3: Invalid secret (should get 403)
    print("3. Testing with invalid secret (should fail)...")
    payload = {
        "email": "23f3004345@ds.study.iitm.ac.in",
        "secret": "wrong_secret",
        "url": "https://tds-llm-analysis.s-anand.net/demo"
    }
    try:
        response = requests.post(f"{base_url}/quiz", json=payload, timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 403:
            print(f"   ✓ Correctly rejected invalid secret")
        else:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print()
    
    # Test 4: Valid request
    print("4. Testing with valid credentials...")
    payload = {
        "email": "23f3004345@ds.study.iitm.ac.in",
        "secret": "my-secure-secret-123",
        "url": "https://tds-llm-analysis.s-anand.net/demo"
    }
    print(f"   Request: {json.dumps(payload, indent=2)}")
    print()
    try:
        response = requests.post(f"{base_url}/quiz", json=payload, timeout=5)
        print(f"   ✓ Status: {response.status_code}")
        print(f"   ✓ Response: {json.dumps(response.json(), indent=2)}")
        print()
        print("   📝 Note: The quiz will be solved in the background.")
        print("      Check the server terminal for progress logs.")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print()
    print("=" * 60)
    print("  Test Complete!")
    print("=" * 60)

if __name__ == "__main__":
    test_api()
