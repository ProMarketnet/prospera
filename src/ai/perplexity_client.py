"""
Perplexity AI client for real-time search and research capabilities
Integrates Perplexity's search-augmented AI for market research and business intelligence
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from openai import OpenAI

class PerplexityAIClient:
    """Client for Perplexity AI API integration"""
    
    def __init__(self):
        """Initialize Perplexity AI client"""
        self.api_key = os.getenv("PERPLEXITY_API_KEY", "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")
        self.base_url = "https://api.perplexity.ai"
        
        # Available models
        self.models = {
            "online": "llama-3.1-sonar-small-128k-online",
            "chat": "llama-3.1-sonar-small-128k-online"
        }
        
        # Initialize client
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
    
    def test_connection(self) -> Dict[str, Any]:
        """Test API key and connection to Perplexity services"""
        try:
            response = self.client.chat.completions.create(
                model=self.models["chat"],
                messages=[
                    {"role": "user", "content": "Test connection - respond with 'Connection successful'"}
                ],
                max_tokens=20
            )
            
            return {
                "status": "success",
                "response": response.choices[0].message.content,
                "model_used": self.models["chat"],
                "tokens_used": response.usage.total_tokens if response.usage else 0,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error_message": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def research_industry_trends(self, industry: str) -> Dict[str, Any]:
        """Research real-time industry trends using Perplexity's online model"""
        try:
            prompt = f"""
            Research the latest trends, developments, and market insights for the {industry} industry in 2024-2025.
            
            Focus on:
            1. Recent market developments and news
            2. Emerging technologies and innovations
            3. Key industry challenges and opportunities
            4. Market size and growth projections
            5. Regulatory changes or industry disruptions
            
            Provide specific, recent, and actionable insights with sources where possible.
            """
            
            response = self.client.chat.completions.create(
                model=self.models["online"],
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000
            )
            
            return {
                "status": "success",
                "industry": industry,
                "research": response.choices[0].message.content,
                "model_used": self.models["online"],
                "tokens_used": response.usage.total_tokens if response.usage else 0,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error_message": str(e),
                "industry": industry,
                "timestamp": datetime.now().isoformat()
            }
    
    def research_competitors(self, industry: str, company_focus: str = "") -> Dict[str, Any]:
        """Research competitors and market landscape using Perplexity"""
        try:
            focus_text = f"specifically for {company_focus}" if company_focus else ""
            
            prompt = f"""
            Research the competitive landscape for the {industry} industry {focus_text}.
            
            Provide:
            1. Top 5-10 key players and market leaders
            2. Emerging competitors and disruptors
            3. Market share information where available
            4. Competitive advantages and differentiators
            5. Recent partnerships, acquisitions, or strategic moves
            6. Pricing strategies and business models
            
            Include recent developments and cite sources where possible.
            """
            
            response = self.client.chat.completions.create(
                model=self.models["online"],
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000
            )
            
            return {
                "status": "success",
                "industry": industry,
                "focus": company_focus,
                "competitive_analysis": response.choices[0].message.content,
                "model_used": self.models["online"],
                "tokens_used": response.usage.total_tokens if response.usage else 0,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error_message": str(e),
                "industry": industry,
                "timestamp": datetime.now().isoformat()
            }
    
    def research_market_opportunities(self, industry: str, region: str = "global") -> Dict[str, Any]:
        """Research market opportunities and growth areas"""
        try:
            prompt = f"""
            Research market opportunities and growth potential in the {industry} industry for {region} markets.
            
            Analyze:
            1. Untapped market segments and niches
            2. Geographic expansion opportunities
            3. Technology-driven growth areas
            4. Customer pain points and unmet needs
            5. Investment trends and funding opportunities
            6. Government initiatives and support programs
            7. Emerging business models and revenue streams
            
            Focus on actionable opportunities with specific market data where available.
            """
            
            response = self.client.chat.completions.create(
                model=self.models["online"],
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000
            )
            
            return {
                "status": "success",
                "industry": industry,
                "region": region,
                "opportunities": response.choices[0].message.content,
                "model_used": self.models["online"],
                "tokens_used": response.usage.total_tokens if response.usage else 0,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error_message": str(e),
                "industry": industry,
                "timestamp": datetime.now().isoformat()
            }
    
    def chat_with_perplexity(self, user_message: str, conversation_history: List[Dict] = None) -> Dict[str, Any]:
        """Interactive chat with Perplexity for business research queries"""
        try:
            # Prepare messages
            messages = []
            
            # Add system message for business context
            messages.append({
                "role": "system",
                "content": "You are a business intelligence research assistant. Provide accurate, current information with sources when possible. Focus on actionable insights for business decision-making."
            })
            
            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history[-5:])  # Keep last 5 exchanges
            
            # Add user message
            messages.append({
                "role": "user",
                "content": user_message
            })
            
            response = self.client.chat.completions.create(
                model=self.models["online"],
                messages=messages,
                max_tokens=1500
            )
            
            return {
                "status": "success",
                "response": response.choices[0].message.content,
                "model_used": self.models["online"],
                "tokens_used": response.usage.total_tokens if response.usage else 0,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error_message": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def comprehensive_industry_research(self, industry: str, company_focus: str = "") -> Dict[str, Any]:
        """Conduct comprehensive industry research combining multiple research areas"""
        try:
            # Perform parallel research
            trends_result = self.research_industry_trends(industry)
            competitors_result = self.research_competitors(industry, company_focus)
            opportunities_result = self.research_market_opportunities(industry)
            
            # Combine results
            return {
                "status": "success",
                "industry": industry,
                "company_focus": company_focus,
                "trends": trends_result,
                "competitors": competitors_result,
                "opportunities": opportunities_result,
                "total_tokens": sum([
                    trends_result.get("tokens_used", 0),
                    competitors_result.get("tokens_used", 0),
                    opportunities_result.get("tokens_used", 0)
                ]),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error_message": str(e),
                "industry": industry,
                "timestamp": datetime.now().isoformat()
            }