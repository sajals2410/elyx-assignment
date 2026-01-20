#!/usr/bin/env python3
"""
Test script for Gemini API integration
Run this to test if Gemini API is working correctly
"""

import os
from data_generator_gemini import GeminiDataGenerator

def test_gemini():
    """Test Gemini API integration."""
    print("=" * 60)
    print("🧪 Testing Gemini API Integration")
    print("=" * 60)
    
    # Check API key
    api_key = os.getenv('GEMINI_API_KEY', '')
    if not api_key:
        print("\nGEMINI_API_KEY not found!")
        print("   Set it with: export GEMINI_API_KEY='your_key'")
        print("   Get key from: https://makersuite.google.com/app/apikey")
        return False
    
    print(f"\nAPI Key found: {api_key[:10]}...")
    
    # Test generator
    try:
        print("\n📝 Creating generator...")
        generator = GeminiDataGenerator(
            start_date="2026-01-15",
            duration_months=1  # Short test
        )
        
        if not generator.model:
            print("❌ Failed to initialize Gemini model")
            return False
        
        print("✅ Generator created successfully")
        
        # Test a small generation
        print("\n🤖 Testing activity generation (this may take 30-60 seconds)...")
        print("   Generating 5 fitness activities...")
        
        prompt = """
Generate 5 realistic fitness activities for a health schedule system.
Return JSON array with: name, details, duration, facilitator, location, equipment (array), metrics (array), can_be_remote (boolean), prep_requirements, frequency_suggestion, priority_range.
"""
        
        response = generator._generate_with_gemini(prompt)
        if response:
            print("✅ Gemini API is working!")
            print(f"\n📄 Sample response (first 200 chars):")
            print(response[:200] + "...")
            return True
        else:
            print("❌ Failed to get response from Gemini")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_gemini()
    print("\n" + "=" * 60)
    if success:
        print("✅ Gemini API test PASSED")
        print("   You can now use Gemini for data generation!")
    else:
        print("❌ Gemini API test FAILED")
        print("   Check your API key and try again")
    print("=" * 60)
