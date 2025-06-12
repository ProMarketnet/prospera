import json
import os
from datetime import datetime
from typing import Dict, List, Any
from openai import OpenAI

from ..utils.config import config
from ..utils.logger import setup_logger
from ..profile.business_profile import BusinessProfileManager

logger = setup_logger(__name__)

class AIAnalyzer:
    """AI-powered business intelligence analyzer using OpenAI"""
    
    def __init__(self):
        if not config.OPENAI_API_KEY:
            raise ValueError("OpenAI API key is required")
        
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        self.model = config.OPENAI_MODEL
        self.max_tokens = config.MAX_TOKENS
        self.temperature = config.TEMPERATURE
        self.profile_manager = BusinessProfileManager()
    
    def analyze_industry_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive AI analysis of industry data"""
        logger.info(f"Starting AI analysis for industry: {data.get('industry', 'unknown')}")
        
        try:
            # Prepare data summary for AI analysis
            data_summary = self._prepare_data_summary(data)
            
            # Perform different types of analysis
            market_analysis = self._analyze_market_trends(data_summary, data)
            competitive_analysis = self._analyze_competitors(data_summary, data)
            lead_analysis = self._analyze_leads(data_summary, data)
            recommendations = self._generate_recommendations(data_summary, data)
            
            analysis_results = {
                "analysis_timestamp": datetime.now().isoformat(),
                "industry": data.get('industry'),
                "market_summary": market_analysis.get('summary', ''),
                "opportunities": market_analysis.get('opportunities', []),
                "risks": market_analysis.get('risks', []),
                "competitive_landscape": competitive_analysis.get('landscape', ''),
                "lead_insights": lead_analysis.get('insights', ''),
                "recommendations": recommendations,
                "confidence_score": self._calculate_confidence_score(data)
            }
            
            logger.info("AI analysis completed successfully")
            return analysis_results
            
        except Exception as e:
            logger.error(f"Error in AI analysis: {str(e)}")
            raise
    
    def _prepare_data_summary(self, data: Dict[str, Any]) -> str:
        """Prepare a concise summary of the data for AI analysis"""
        
        summary_parts = []
        
        # Industry info
        industry_name = config.INDUSTRIES.get(data.get('industry', ''), {}).get('name', 'Unknown')
        summary_parts.append(f"Industry: {industry_name}")
        
        # Trends summary
        trends = data.get('trends', [])
        if trends:
            trend_count = len(trends)
            summary_parts.append(f"Trends analyzed: {trend_count}")
            
            # Get top keywords/headlines
            trend_keywords = []
            for trend in trends[:3]:
                if 'keyword' in trend:
                    trend_keywords.append(trend['keyword'])
                elif 'headlines' in trend and trend['headlines']:
                    trend_keywords.extend(trend['headlines'][:2])
            
            if trend_keywords:
                summary_parts.append(f"Key trending topics: {', '.join(trend_keywords[:5])}")
        
        # News summary
        news = data.get('news', [])
        if news:
            news_count = len(news)
            top_sources = list(set([article.get('source', 'Unknown') for article in news[:5]]))
            summary_parts.append(f"News articles analyzed: {news_count}")
            summary_parts.append(f"Top news sources: {', '.join(top_sources)}")
        
        # Leads summary
        leads = data.get('leads', [])
        if leads:
            summary_parts.append(f"Potential leads discovered: {len(leads)}")
        
        # Competitors summary
        competitors = data.get('competitors', [])
        if competitors:
            summary_parts.append(f"Competitors analyzed: {len(competitors)}")
        
        return "; ".join(summary_parts)
    
    def _analyze_market_trends(self, data_summary: str, full_data: Dict) -> Dict[str, Any]:
        """Analyze market trends using AI"""
        
        try:
            # Prepare detailed trend data
            trends_text = ""
            for trend in full_data.get('trends', []):
                if 'keyword' in trend:
                    trends_text += f"Keyword: {trend['keyword']}, Score: {trend.get('trend_score', 0)}\n"
                    if 'top_headlines' in trend:
                        for headline in trend['top_headlines'][:3]:
                            trends_text += f"- {headline['title']}\n"
                elif 'headlines' in trend:
                    trends_text += f"Source: {trend.get('source', 'Unknown')}\n"
                    for headline in trend['headlines'][:3]:
                        trends_text += f"- {headline}\n"
                trends_text += "\n"
            
            prompt = f"""
            As a senior business intelligence analyst, analyze the following market data and provide insights:
            
            Data Summary: {data_summary}
            
            Detailed Trends:
            {trends_text}
            
            Please provide your analysis in JSON format with the following structure:
            {{
                "summary": "Overall market summary in 2-3 sentences",
                "opportunities": ["list of specific opportunities"],
                "risks": ["list of potential risks"],
                "trend_strength": "Strong/Moderate/Weak",
                "market_direction": "Growing/Stable/Declining"
            }}
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a senior business intelligence analyst specializing in market trend analysis. Provide concise, actionable insights."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            content = response.choices[0].message.content or "{}"
            result = json.loads(content)
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing market trends: {str(e)}")
            return {
                "summary": "Unable to analyze market trends due to processing error.",
                "opportunities": [],
                "risks": [],
                "trend_strength": "Unknown",
                "market_direction": "Unknown"
            }
    
    def _analyze_competitors(self, data_summary: str, full_data: Dict) -> Dict[str, Any]:
        """Analyze competitive landscape using AI"""
        
        try:
            competitors_text = ""
            for competitor in full_data.get('competitors', []):
                competitors_text += f"Name: {competitor.get('name', 'Unknown')}\n"
                competitors_text += f"Position: {competitor.get('market_position', 'Unknown')}\n"
                competitors_text += f"Size: {competitor.get('estimated_size', 'Unknown')}\n"
                competitors_text += f"Focus: {competitor.get('focus_area', 'Unknown')}\n\n"
            
            prompt = f"""
            As a competitive intelligence expert, analyze the following competitive landscape:
            
            Data Summary: {data_summary}
            
            Competitor Information:
            {competitors_text}
            
            Provide analysis in JSON format:
            {{
                "landscape": "Overall competitive landscape description",
                "competition_level": "High/Medium/Low",
                "market_concentration": "Concentrated/Fragmented",
                "key_insights": ["list of key competitive insights"],
                "positioning_opportunities": ["opportunities for market positioning"]
            }}
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a competitive intelligence expert. Provide strategic insights about market competition."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            content = response.choices[0].message.content
            result = json.loads(content) if content else {}
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing competitors: {str(e)}")
            return {
                "landscape": "Unable to analyze competitive landscape due to processing error.",
                "competition_level": "Unknown",
                "market_concentration": "Unknown",
                "key_insights": [],
                "positioning_opportunities": []
            }
    
    def _analyze_leads(self, data_summary: str, full_data: Dict) -> Dict[str, Any]:
        """Analyze lead quality and potential using AI"""
        
        try:
            leads_text = ""
            for lead in full_data.get('leads', []):
                leads_text += f"Company: {lead.get('company_name', 'Unknown')}\n"
                leads_text += f"Score: {lead.get('lead_score', 0)}\n"
                leads_text += f"Source: {lead.get('source', 'Unknown')}\n\n"
            
            prompt = f"""
            As a sales intelligence analyst, evaluate the following leads:
            
            Data Summary: {data_summary}
            
            Lead Information:
            {leads_text}
            
            Provide analysis in JSON format:
            {{
                "insights": "Overall assessment of lead quality and potential",
                "lead_quality_score": 8.5,
                "conversion_likelihood": "High/Medium/Low",
                "recommended_approach": ["list of recommended approaches for lead conversion"],
                "prioritization": ["ordered list of leads by priority"]
            }}
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a sales intelligence analyst specializing in lead qualification and conversion strategies."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            content = response.choices[0].message.content
            result = json.loads(content) if content else {}
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing leads: {str(e)}")
            return {
                "insights": "Unable to analyze leads due to processing error.",
                "lead_quality_score": 0,
                "conversion_likelihood": "Unknown",
                "recommended_approach": [],
                "prioritization": []
            }
    
    def _generate_recommendations(self, data_summary: str, full_data: Dict) -> List[str]:
        """Generate actionable business recommendations using AI"""
        
        try:
            industry_name = config.INDUSTRIES.get(full_data.get('industry', ''), {}).get('name', 'Unknown')
            
            prompt = f"""
            As a senior business consultant specializing in {industry_name}, provide actionable recommendations based on this market intelligence:
            
            {data_summary}
            
            Please provide 5-7 specific, actionable recommendations for an SME in this industry. Focus on:
            1. Market opportunities to pursue
            2. Competitive positioning strategies
            3. Lead generation and conversion tactics
            4. Risk mitigation approaches
            5. Growth strategies
            
            Respond in JSON format:
            {{
                "recommendations": [
                    "Specific recommendation 1 with clear action steps",
                    "Specific recommendation 2 with clear action steps",
                    ...
                ]
            }}
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"You are a senior business consultant with expertise in {industry_name}. Provide specific, actionable recommendations for SMEs."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            content = response.choices[0].message.content
            if not content:
                return []
            result = json.loads(content)
            return result.get('recommendations', [])
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return [
                "Unable to generate specific recommendations due to processing error.",
                "Please ensure all required data is available and try again."
            ]
    
    def _calculate_confidence_score(self, data: Dict) -> float:
        """Calculate confidence score based on data quality and completeness"""
        
        score = 0.0
        max_score = 10.0
        
        # Data completeness factors
        if data.get('trends'):
            score += 2.5
        if data.get('news'):
            score += 2.5
        if data.get('leads'):
            score += 2.5
        if data.get('competitors'):
            score += 2.5
        
        # Data quality factors
        news_count = len(data.get('news', []))
        if news_count > 10:
            score += 1.0
        elif news_count > 5:
            score += 0.5
        
        trends_count = len(data.get('trends', []))
        if trends_count > 3:
            score += 1.0
        elif trends_count > 1:
            score += 0.5
        
        return min(max_score, score)
