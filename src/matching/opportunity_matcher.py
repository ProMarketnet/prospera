"""
AI-powered opportunity matching engine for Prospera
Matches companies with relevant business opportunities using LLM analysis
"""
import os
import json
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import openai
from dataclasses import dataclass

from ..utils.logger import setup_logger
from ..profile.business_profile import BusinessProfile

logger = setup_logger(__name__)

@dataclass
class Opportunity:
    """Business opportunity data structure"""
    id: str
    title: str
    description: str
    content: str
    source: str
    source_url: str
    opportunity_type: str  # 'news', 'supplier', 'event', 'trend'
    tags: List[str]
    published_at: datetime
    metadata: Dict[str, Any]

@dataclass
class Match:
    """Company-opportunity match with AI scoring"""
    company_id: str
    opportunity_id: str
    relevance_score: float  # 0.0 to 1.0
    reasoning: str
    match_status: str = 'pending'
    created_at: Optional[datetime] = None

class OpportunityMatcher:
    """AI-powered matching engine using OpenAI for relevance scoring"""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def analyze_company_profile(self, profile: BusinessProfile) -> Dict[str, Any]:
        """Analyze company profile to understand business focus and needs"""
        
        profile_text = f"""
        Company: {profile.company_name}
        Industry: {profile.industry}
        Business Type: {profile.business_type}
        Company Size: {profile.company_size}
        Description: {profile.description}
        Services: {', '.join(profile.services)}
        Target Markets: {', '.join(profile.target_markets)}
        Key Challenges: {', '.join(profile.key_challenges)}
        """
        
        prompt = f"""
        Analyze this business profile and extract key characteristics for opportunity matching:
        
        {profile_text}
        
        Return JSON with:
        - industry_focus: primary industry category
        - business_stage: startup/growth/established/enterprise
        - target_customers: key customer segments
        - growth_priorities: main areas for business growth
        - technology_adoption: low/medium/high tech adoption level
        - geographic_scope: local/regional/national/international
        - key_capabilities: core business capabilities
        - partnership_interests: types of partnerships they might seek
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a business analyst expert at understanding company profiles and matching them with opportunities. Respond with JSON only."
                    },
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            if content:
                analysis = json.loads(content)
            else:
                analysis = {"industry_focus": "Unknown", "business_stage": "Unknown"}
            logger.info(f"Company profile analyzed for {profile.company_name}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing company profile: {str(e)}")
            return {
                "industry_focus": profile.industry,
                "business_stage": "unknown",
                "error": str(e)
            }
    
    def score_opportunity_relevance(self, company_analysis: Dict[str, Any], 
                                  opportunity: Opportunity) -> Match:
        """Score how relevant an opportunity is for a company using AI"""
        
        prompt = f"""
        Analyze the relevance of this business opportunity for the company:
        
        Company Profile:
        Industry Focus: {company_analysis.get('industry_focus', 'Unknown')}
        Business Stage: {company_analysis.get('business_stage', 'Unknown')}
        Target Customers: {company_analysis.get('target_customers', 'Unknown')}
        Growth Priorities: {company_analysis.get('growth_priorities', 'Unknown')}
        Technology Adoption: {company_analysis.get('technology_adoption', 'Unknown')}
        Geographic Scope: {company_analysis.get('geographic_scope', 'Unknown')}
        
        Opportunity:
        Title: {opportunity.title}
        Description: {opportunity.description}
        Type: {opportunity.opportunity_type}
        Source: {opportunity.source}
        Tags: {', '.join(opportunity.tags)}
        Content Preview: {opportunity.content[:500] if opportunity.content else 'No content'}
        
        Analyze relevance considering:
        1. Industry alignment and market fit
        2. Business stage appropriateness
        3. Geographic relevance
        4. Potential business impact
        5. Timing and urgency
        
        Return JSON with:
        - relevance_score: float between 0.0 and 1.0 (1.0 = highly relevant)
        - reasoning: detailed explanation of why this opportunity matches or doesn't match
        - key_match_factors: array of specific reasons for the score
        - actionability: how actionable this opportunity is for the company
        
        Be strict with scoring - only score above 0.7 for highly relevant opportunities.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a business opportunity analyst. Provide precise relevance scoring with detailed reasoning. Respond only with valid JSON."
                    },
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.2
            )
            
            content = response.choices[0].message.content
            if content:
                scoring = json.loads(content)
            else:
                scoring = {"relevance_score": 0.0, "reasoning": "No analysis available"}
            
            match = Match(
                company_id="placeholder",
                opportunity_id=opportunity.id,
                relevance_score=max(0.0, min(1.0, scoring.get('relevance_score', 0.0))),
                reasoning=scoring.get('reasoning', 'AI analysis completed'),
                created_at=datetime.now()
            )
            
            logger.info(f"Opportunity scored: {match.relevance_score:.2f} for {opportunity.title}")
            return match
            
        except Exception as e:
            logger.error(f"Error scoring opportunity relevance: {str(e)}")
            return Match(
                company_id="placeholder",
                opportunity_id=opportunity.id,
                relevance_score=0.0,
                reasoning=f"Analysis unavailable: {str(e)}",
                created_at=datetime.now()
            )
    
    def find_matches_for_company(self, profile: BusinessProfile, opportunities: List[Opportunity], 
                                min_score: float = 0.6) -> List[Match]:
        """Find and score all relevant opportunities for a company"""
        
        company_analysis = self.analyze_company_profile(profile)
        
        matches = []
        for opportunity in opportunities:
            match = self.score_opportunity_relevance(company_analysis, opportunity)
            match.company_id = profile.company_name
            
            if match.relevance_score >= min_score:
                matches.append(match)
        
        # Sort by relevance score (highest first)
        matches.sort(key=lambda x: x.relevance_score, reverse=True)
        
        logger.info(f"Found {len(matches)} relevant opportunities for {profile.company_name}")
        return matches
