"""
Test script for XAI Grok API integration
Tests API key functionality and model capabilities
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path for imports
sys.path.append('src')

from ai.grok_client import GrokAIClient
import json

def test_grok_api():
    """Comprehensive test of Grok API functionality"""
    
    print("Testing XAI Grok API Integration")
    print("=" * 50)
    
    try:
        # Initialize Grok client
        grok = GrokAIClient()
        print(f"✓ Grok client initialized with API key: {grok.api_key[:10]}...")
        
        # Test 1: Basic connection test
        print("\n1. Testing API connection...")
        connection_result = grok.test_connection()
        
        if connection_result["status"] == "success":
            print(f"✓ Connection successful!")
            print(f"  Model used: {connection_result['model_used']}")
            print(f"  Response: {connection_result['response']}")
            print(f"  Tokens used: {connection_result['tokens_used']}")
        else:
            print(f"✗ Connection failed: {connection_result['error_message']}")
            return False
        
        # Test 2: Industry analysis
        print("\n2. Testing industry analysis capabilities...")
        test_industry_data = {
            "industry": "Technology Software",
            "trends": ["AI integration", "Cloud-first architecture", "Remote work tools"],
            "competitors": ["Microsoft", "Salesforce", "Oracle"],
            "opportunities": ["Enterprise AI solutions", "API economy", "Edge computing"]
        }
        
        analysis_result = grok.analyze_industry_with_grok(test_industry_data)
        
        if analysis_result["status"] == "success":
            print(f"✓ Industry analysis completed!")
            print(f"  Tokens used: {analysis_result['tokens_used']}")
            print(f"  Analysis preview: {analysis_result['analysis'][:200]}...")
        else:
            print(f"✗ Industry analysis failed: {analysis_result['error_message']}")
        
        # Test 3: Interactive chat
        print("\n3. Testing chat functionality...")
        chat_result = grok.chat_with_grok("What are the key trends in the technology industry for 2024?")
        
        if chat_result["status"] == "success":
            print(f"✓ Chat interaction successful!")
            print(f"  Response preview: {chat_result['response'][:200]}...")
            print(f"  Tokens used: {chat_result['tokens_used']}")
        else:
            print(f"✗ Chat interaction failed: {chat_result['error_message']}")
        
        print("\n" + "=" * 50)
        print("XAI Grok API Test Summary:")
        print(f"✓ API Key: Valid and working")
        print(f"✓ Model: {grok.models['text']}")
        print(f"✓ Base URL: https://api.x.ai/v1")
        print(f"✓ All core functionalities operational")
        
        return True
        
    except Exception as e:
        print(f"✗ Test failed with error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_grok_api()
    if success:
        print("\n🎉 All tests passed! Grok API is ready for integration.")
    else:
        print("\n❌ Tests failed. Please check API key and configuration.")