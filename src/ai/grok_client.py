"""
XAI Grok API client for advanced business intelligence analysis
Integrates Grok models for enhanced market research and strategic insights
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from openai import OpenAI
from datetime import datetime

logger = logging.getLogger(__name__)

class GrokAIClient:
    """Client for XAI Grok API integration"""
    
    def __init__(self):
        self.api_key = os.getenv('XAI_API_KEY')
        if not self.api_key:
            raise ValueError("XAI_API_KEY environment variable is required")
        
        # Initialize Grok client using OpenAI-compatible interface
        self.client = OpenAI(
            base_url="https://api.x.ai/v1",
            api_key=self.api_key
        )
        
        # Available Grok models
        self.models = {
            "vision": "grok-2-vision-1212",
            "text": "grok-2-1212", 
            "vision_beta": "grok-vision-beta",
            "beta": "grok-beta"
        }
    
    def test_connection(self) -> Dict[str, Any]:
        """Test API key and connection to Grok services"""
        try:
            # Test with a simple prompt
            response = self.client.chat.completions.create(
                model=self.models["text"],
                messages=[
                    {
                        "role": "user",
                        "content": "Hello, please respond with 'Connection successful' to confirm API access."
                    }
                ],
                max_tokens=50,
                temperature=0.1
            )
            
            result = {
                "status": "success",
                "model_used": self.models["text"],
                "response": response.choices[0].message.content,
                "tokens_used": response.usage.total_tokens if response.usage else 0,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info("Grok API connection test successful")
            return result
            
        except Exception as e:
            error_result = {
                "status": "error",
                "error_message": str(e),
                "timestamp": datetime.now().isoformat()
            }
            logger.error(f"Grok API connection test failed: {str(e)}")
            return error_result
    
    def analyze_industry_with_grok(self, industry_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform advanced industry analysis using Grok AI"""
        try:
            prompt = f"""
            As an expert business analyst, analyze the following industry data and provide comprehensive insights:
            
            Industry: {industry_data.get('industry', 'Unknown')}
            Market Trends: {industry_data.get('trends', [])}
            Competitors: {industry_data.get('competitors', [])}
            Opportunities: {industry_data.get('opportunities', [])}
            
            Please provide:
            1. Strategic recommendations (3-5 specific actions)
            2. Market positioning advice
            3. Competitive advantages to focus on
            4. Potential risks and mitigation strategies
            5. Growth opportunities with probability assessments
            
            Format your response as structured analysis with clear sections.
            """
            
            response = self.client.chat.completions.create(
                model=self.models["text"],
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a senior business strategy consultant with expertise in market analysis, competitive intelligence, and strategic planning. Provide actionable, data-driven insights."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            analysis_result = {
                "status": "success",
                "analysis": response.choices[0].message.content,
                "model_used": self.models["text"],
                "tokens_used": response.usage.total_tokens if response.usage else 0,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info("Grok industry analysis completed successfully")
            return analysis_result
            
        except Exception as e:
            error_result = {
                "status": "error",
                "error_message": str(e),
                "timestamp": datetime.now().isoformat()
            }
            logger.error(f"Grok industry analysis failed: {str(e)}")
            return error_result
    
    def chat_with_grok(self, user_message: str, conversation_history: List[Dict] = None) -> Dict[str, Any]:
        """Interactive chat with Grok for business intelligence queries"""
        try:
            messages = [
                {
                    "role": "system",
                    "content": "You are Prospera AI, a business intelligence assistant powered by Grok. You help SMEs with market analysis, strategic planning, and business growth insights. Be conversational but professional, and provide actionable advice."
                }
            ]
            
            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history[-10:])  # Keep last 10 messages
            
            messages.append({
                "role": "user",
                "content": user_message
            })
            
            response = self.client.chat.completions.create(
                model=self.models["text"],
                messages=messages,
                max_tokens=1000,
                temperature=0.8
            )
            
            chat_result = {
                "status": "success",
                "response": response.choices[0].message.content,
                "model_used": self.models["text"],
                "tokens_used": response.usage.total_tokens if response.usage else 0,
                "timestamp": datetime.now().isoformat()
            }
            
            return chat_result
            
        except Exception as e:
            error_result = {
                "status": "error",
                "error_message": str(e),
                "timestamp": datetime.now().isoformat()
            }
            logger.error(f"Grok chat interaction failed: {str(e)}")
            return error_result