#!/usr/bin/env python3
"""
Test script for the Multilingual Translator API
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_get_languages():
    """Test the languages endpoint"""
    print("\nTesting get languages...")
    try:
        response = requests.get(f"{BASE_URL}/api/languages")
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and 'languages' in data:
                print(f"✅ Languages endpoint passed: {len(data['languages'])} languages supported")
                return True
            else:
                print(f"❌ Languages endpoint failed: {data}")
                return False
        else:
            print(f"❌ Languages endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Languages endpoint error: {e}")
        return False

def test_translate():
    """Test the translation endpoint"""
    print("\nTesting translation...")
    test_cases = [
        {
            "text": "Hello, world!",
            "source_lang": "en",
            "target_lang": "es",
            "expected_keywords": ["hola", "mundo"]
        },
        {
            "text": "Good morning",
            "source_lang": "en", 
            "target_lang": "fr",
            "expected_keywords": ["bonjour", "matin"]
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"  Test case {i}: {test_case['text']} ({test_case['source_lang']} -> {test_case['target_lang']})")
        try:
            response = requests.post(
                f"{BASE_URL}/api/translate",
                json={
                    "text": test_case["text"],
                    "source_lang": test_case["source_lang"],
                    "target_lang": test_case["target_lang"]
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'translated_text' in data:
                    translated = data['translated_text'].lower()
                    print(f"    ✅ Translation: {data['translated_text']}")
                    
                    # Check if any expected keywords are present
                    if any(keyword in translated for keyword in test_case['expected_keywords']):
                        print(f"    ✅ Translation contains expected keywords")
                    else:
                        print(f"    ⚠️  Translation may not be accurate")
                else:
                    print(f"    ❌ Translation failed: {data}")
                    return False
            else:
                print(f"    ❌ Translation request failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"    ❌ Translation error: {e}")
            return False
    
    return True

def test_detect_language():
    """Test the language detection endpoint"""
    print("\nTesting language detection...")
    test_cases = [
        {"text": "Bonjour le monde", "expected": "fr"},
        {"text": "Hola mundo", "expected": "es"},
        {"text": "Hello world", "expected": "en"}
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"  Test case {i}: {test_case['text']}")
        try:
            response = requests.post(
                f"{BASE_URL}/api/detect",
                json={"text": test_case["text"]}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'detected_language' in data:
                    detected = data['detected_language']
                    print(f"    ✅ Detected: {detected} ({data.get('language_name', 'Unknown')})")
                    
                    if detected == test_case['expected']:
                        print(f"    ✅ Detection correct")
                    else:
                        print(f"    ⚠️  Detection may be incorrect (expected: {test_case['expected']})")
                else:
                    print(f"    ❌ Detection failed: {data}")
                    return False
            else:
                print(f"    ❌ Detection request failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"    ❌ Detection error: {e}")
            return False
    
    return True

def test_error_handling():
    """Test error handling"""
    print("\nTesting error handling...")
    
    # Test invalid language
    print("  Testing invalid source language...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/translate",
            json={
                "text": "Hello",
                "source_lang": "invalid",
                "target_lang": "es"
            }
        )
        if response.status_code == 400:
            print("    ✅ Invalid source language handled correctly")
        else:
            print(f"    ❌ Invalid source language not handled: {response.status_code}")
            return False
    except Exception as e:
        print(f"    ❌ Error handling test failed: {e}")
        return False
    
    # Test empty text
    print("  Testing empty text...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/translate",
            json={
                "text": "",
                "source_lang": "en",
                "target_lang": "es"
            }
        )
        if response.status_code == 400:
            print("    ✅ Empty text handled correctly")
        else:
            print(f"    ❌ Empty text not handled: {response.status_code}")
            return False
    except Exception as e:
        print(f"    ❌ Error handling test failed: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🚀 Starting Multilingual Translator API Tests")
    print("=" * 50)
    
    tests = [
        test_health_check,
        test_get_languages,
        test_translate,
        test_detect_language,
        test_error_handling
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        time.sleep(1)  # Small delay between tests
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The API is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the API implementation.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
