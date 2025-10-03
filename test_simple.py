#!/usr/bin/env python3
"""
Simple Test Script for Alt Text Generator
"""

import os
import json
from simple_alt_generator import SimpleAltTextGenerator

def test_config_loading():
    """Test if config file loads correctly"""
    print("🔍 Testing config loading...")
    try:
        with open('simple_config.json', 'r') as f:
            config = json.load(f)
        print(f"✅ Config loaded: {len(config.get('sheets', []))} sheets")
        return True
    except Exception as e:
        print(f"❌ Config loading failed: {e}")
        return False

def test_environment_variables():
    """Test if environment variables are set"""
    print("🔍 Testing environment variables...")
    
    gemini_key = os.environ.get('GEMINI_API_KEY')
    google_creds = os.environ.get('GOOGLE_SHEETS_CREDENTIALS')
    
    if not gemini_key:
        print("❌ GEMINI_API_KEY not set")
        return False
    else:
        print(f"✅ GEMINI_API_KEY: {gemini_key[:10]}...")
    
    if not google_creds:
        print("❌ GOOGLE_SHEETS_CREDENTIALS not set")
        return False
    else:
        print("✅ GOOGLE_SHEETS_CREDENTIALS: Set")
    
    return True

def test_generator_initialization():
    """Test if generator initializes correctly"""
    print("🔍 Testing generator initialization...")
    try:
        generator = SimpleAltTextGenerator()
        print("✅ Generator initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Generator initialization failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Simple Alt Text Generator - Test Suite")
    print("=" * 50)
    
    tests = [
        ("Config Loading", test_config_loading),
        ("Environment Variables", test_environment_variables),
        ("Generator Initialization", test_generator_initialization),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} - PASSED")
            else:
                print(f"❌ {test_name} - FAILED")
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to run.")
        print("\n🚀 Next steps:")
        print("1. python simple_alt_generator.py")
    else:
        print("⚠️ Some tests failed. Please check the setup.")
        print("\n🔧 Setup steps:")
        print("1. python simple_setup.py")

if __name__ == "__main__":
    main()
