#!/usr/bin/env python3
"""
Simple test script for the Stock Ticker Service
"""

import requests
import json
import time

def test_health_endpoint(base_url="http://localhost:8000"):
    """Test the health endpoint"""
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"✅ Health check: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_stock_endpoint(base_url="http://localhost:8000"):
    """Test the main stock data endpoint"""
    try:
        response = requests.get(base_url, timeout=10)
        data = response.json()
        
        if response.status_code == 200:
            print(f"✅ Stock data: Symbol={data.get('symbol')}, Average=${data.get('average_close'):.2f}")
            print(f"   Data points: {len(data.get('data', []))}")
            return True
        else:
            print(f"❌ Stock endpoint error: {data}")
            return False
    except Exception as e:
        print(f"❌ Stock endpoint failed: {e}")
        return False

def main():
    print("🧪 Testing Stock Ticker Service...")
    print("-" * 40)
    
    # Test health endpoint
    health_ok = test_health_endpoint()
    
    # Wait a moment
    time.sleep(1)
    
    # Test stock endpoint
    stock_ok = test_stock_endpoint()
    
    # Summary
    print("-" * 40)
    if health_ok and stock_ok:
        print("🎉 All tests passed!")
    else:
        print("💥 Some tests failed!")
        exit(1)

if __name__ == "__main__":
    main()