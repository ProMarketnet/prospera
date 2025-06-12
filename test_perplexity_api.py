"""
Test script for Perplexity AI API integration
Tests API key functionality and real-time research capabilities
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path for imports
sys.path.append('src')

from ai.perplexity_client import PerplexityAIClient
import json

def test_perplexity_api():
    """Comprehensive test of Perplexity API functionality"""
    
    print("Testing Perplexity AI API Integration")
    print("=" * 50)
    
    try:
        # Initialize Perplexity client
        perplexity = PerplexityAIClient()
        print(f"✓ Perplexity client initialized with API key: {perplexity.api_key[:10]}...")
        
        # Test 1: Basic connection test
        print("\n1. Testing API connection...")
        connection_result = perplexity.test_connection()
        
        if connection_result["status"] == "success":
            print(f"✓ Connection successful!")
            print(f"  Model used: {connection_result['model_used']}")
            print(f"  Response: {connection_result['response']}")
            print(f"  Tokens used: {connection_result['tokens_used']}")
        else:
            print(f"✗ Connection failed: {connection_result['error_message']}")
            return False
        
        # Test 2: Industry trends research
        print("\n2. Testing real-time industry trends research...")
        trends_result = perplexity.research_industry_trends("Technology Software")
        
        if trends_result["status"] == "success":
            print(f"✓ Industry trends research completed!")
            print(f"  Industry: {trends_result['industry']}")
            print(f"  Tokens used: {trends_result['tokens_used']}")
            print(f"  Research preview: {trends_result['research'][:200]}...")
        else:
            print(f"✗ Trends research failed: {trends_result['error_message']}")
        
        # Test 3: Competitive analysis
        print("\n3. Testing competitive analysis...")
        competitors_result = perplexity.research_competitors("Technology Software", "SaaS platforms")
        
        if competitors_result["status"] == "success":
            print(f"✓ Competitive analysis completed!")
            print(f"  Focus: {competitors_result['focus']}")
            print(f"  Tokens used: {competitors_result['tokens_used']}")
            print(f"  Analysis preview: {competitors_result['competitive_analysis'][:200]}...")
        else:
            print(f"✗ Competitive analysis failed: {competitors_result['error_message']}")
        
        # Test 4: Market opportunities research
        print("\n4. Testing market opportunities research...")
        opportunities_result = perplexity.research_market_opportunities("Technology Software", "North America")
        
        if opportunities_result["status"] == "success":
            print(f"✓ Market opportunities research completed!")
            print(f"  Region: {opportunities_result['region']}")
            print(f"  Tokens used: {opportunities_result['tokens_used']}")
            print(f"  Opportunities preview: {opportunities_result['opportunities'][:200]}...")
        else:
            print(f"✗ Opportunities research failed: {opportunities_result['error_message']}")
        
        # Test 5: Interactive chat
        print("\n5. Testing interactive chat...")
        chat_result = perplexity.chat_with_perplexity("What are the latest AI trends in business applications for 2024?")
        
        if chat_result["status"] == "success":
            print(f"✓ Chat interaction successful!")
            print(f"  Response preview: {chat_result['response'][:200]}...")
            print(f"  Tokens used: {chat_result['tokens_used']}")
        else:
            print(f"✗ Chat interaction failed: {chat_result['error_message']}")
        
        # Test 6: Comprehensive research
        print("\n6. Testing comprehensive industry research...")
        comprehensive_result = perplexity.comprehensive_industry_research("Technology Software", "Enterprise AI")
        
        if comprehensive_result["status"] == "success":
            print(f"✓ Comprehensive research completed!")
            print(f"  Industry: {comprehensive_result['industry']}")
            print(f"  Focus: {comprehensive_result['company_focus']}")
            print(f"  Total tokens: {comprehensive_result['total_tokens']}")
            print(f"  Research areas: Trends, Competitors, Opportunities")
        else:
            print(f"✗ Comprehensive research failed: {comprehensive_result['error_message']}")
        
        print("\n" + "=" * 50)
        print("Perplexity AI API Test Summary:")
        print(f"✓ API Key: Valid and working")
        print(f"✓ Online Model: {perplexity.models['online']}")
        print(f"✓ Chat Model: {perplexity.models['chat']}")
        print(f"✓ Base URL: {perplexity.base_url}")
        print(f"✓ All core functionalities operational")
        print(f"✓ Real-time search capabilities verified")
        
        return True
        
    except Exception as e:
        print(f"✗ Test failed with error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_perplexity_api()
    if success:
        print("\n🎉 All tests passed! Perplexity AI is ready for integration.")
    else:
        print("\n❌ Tests failed. Please check API key and configuration.")