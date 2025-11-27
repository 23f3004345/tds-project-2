#!/usr/bin/env python3
"""
Test script for deployed TDS Project 2 Quiz API
"""

import requests
import json
import sys

def test_deployed_api(base_url):
    """Test the deployed API endpoint"""
    
    print(f"🚀 Testing deployed API at: {base_url}")
    print("-" * 50)
    
    # Test 1: Health check
    try:
        print("1. Testing health endpoint...")
        response = requests.get(f"{base_url}/health", timeout=30)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Health check passed!")
        else:
            print("   ❌ Health check failed!")
            
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
    
    print()
    
    # Test 2: Root endpoint
    try:
        print("2. Testing root endpoint...")
        response = requests.get(base_url, timeout=30)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Root endpoint working!")
        else:
            print("   ❌ Root endpoint failed!")
            
    except Exception as e:
        print(f"   ❌ Root endpoint error: {e}")
    
    print()
    
    # Test 3: Quiz endpoint with invalid credentials
    try:
        print("3. Testing quiz endpoint with invalid credentials...")
        test_data = {
            "email": "invalid@test.com",
            "secret": "wrong-secret",
            "quiz_url": "https://example.com"
        }
        
        response = requests.post(
            f"{base_url}/quiz",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 403:
            print("   ✅ Authentication working correctly!")
        else:
            print(f"   ⚠️  Expected 403, got {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Quiz endpoint error: {e}")
    
    print()
    
    # Test 4: Quiz endpoint with valid credentials (but test URL)
    try:
        print("4. Testing quiz endpoint with valid credentials...")
        test_data = {
            "email": "23f3004345@ds.study.iitm.ac.in",
            "secret": "my-secure-secret-123",
            "quiz_url": "https://httpbin.org/json"  # Simple test URL
        }
        
        response = requests.post(
            f"{base_url}/quiz",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=60  # Longer timeout for quiz processing
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:500]}...")  # Truncate long responses
        
        if response.status_code == 200:
            print("   ✅ Quiz endpoint accepting valid credentials!")
        else:
            print(f"   ⚠️  Quiz processing issue: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Quiz endpoint error: {e}")
    
    print()
    print("🏁 Testing complete!")
    print("If all tests pass, your API is ready for evaluation!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_deployed_api.py <RAILWAY_URL>")
        print("Example: python test_deployed_api.py https://your-app.up.railway.app")
        sys.exit(1)
    
    base_url = sys.argv[1].rstrip('/')
    test_deployed_api(base_url)