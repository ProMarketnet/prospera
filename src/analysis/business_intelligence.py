import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
import statistics

from ..utils.config import config
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class BusinessIntelligence:
    """Business intelligence analysis and insights generation"""
    
    def __init__(self):
        pass
    
    def generate_insights(self, scraped_data: Dict, ai_analysis: Dict) -> Dict[str, Any]:
        """Generate comprehensive business intelligence insights"""
        logger.info("Generating business intelligence insights")
        
        try:
            insights = {
                "generation_timestamp": datetime.now().isoformat(),
                "industry": scraped_data.get('industry'),
                "key_metrics": self._calculate_key_metrics(scraped_data, ai_analysis),
                "market_trends": self._analyze_market_trends(scraped_data, ai_analysis),
                "competitive_landscape": self._analyze_competitive_landscape(scraped_data, ai_analysis),
                "lead_intelligence": self._analyze_lead_intelligence(scraped_data, ai_analysis),
                "risk_assessment": self._assess_risks(scraped_data, ai_analysis),
                "growth_opportunities": self._identify_growth_opportunities(scraped_data, ai_analysis),
                "executive_summary": self._generate_executive_summary(scraped_data, ai_analysis)
            }
            
            logger.info("Business intelligence insights generated successfully")
            return insights
            
        except Exception as e:
            logger.error(f"Error generating business intelligence insights: {str(e)}")
            raise
    
    def _calculate_key_metrics(self, scraped_data: Dict, ai_analysis: Dict) -> Dict[str, Any]:
        """Calculate key business metrics"""
        
        try:
            # Market opportunity score (1-10)
            opportunity_score = self._calculate_opportunity_score(scraped_data, ai_analysis)
            
            # Competition level assessment
            competition_level = self._assess_competition_level(scraped_data, ai_analysis)
            
            # Lead quality score (1-10)
            lead_quality = self._calculate_lead_quality_score(scraped_data)
            
            # Trend momentum assessment
            trend_momentum = self._assess_trend_momentum(scraped_data)
            
            return {
                "opportunity_score": opportunity_score,
                "opportunity_trend": self._calculate_trend_direction(scraped_data),
                "competition_level": competition_level,
                "competition_change": self._assess_competition_change(scraped_data),
                "lead_quality": lead_quality,
                "trend_momentum": trend_momentum,
                "data_freshness": self._calculate_data_freshness(scraped_data),
                "confidence_level": ai_analysis.get('confidence_score', 0)
            }
            
        except Exception as e:
            logger.error(f"Error calculating key metrics: {str(e)}")
            return {}
    
    def _analyze_market_trends(self, scraped_data: Dict, ai_analysis: Dict) -> List[str]:
        """Analyze market trends and provide insights"""
        
        trends_insights = []
        
        try:
            # Analyze trend data
            trends = scraped_data.get('trends', [])
            if trends:
                # Calculate average trend scores
                trend_scores = []
                for trend in trends:
                    if 'trend_score' in trend:
                        trend_scores.append(trend['trend_score'])
                
                if trend_scores:
                    avg_score = statistics.mean(trend_scores)
                    max_score = max(trend_scores)
                    
                    if avg_score > 50:
                        trends_insights.append("Strong market momentum detected across key industry keywords")
                    elif avg_score > 25:
                        trends_insights.append("Moderate market activity with selective opportunities")
                    else:
                        trends_insights.append("Limited market activity suggests careful market entry strategy needed")
                
                # Identify hot topics
                hot_topics = []
                for trend in trends:
                    if trend.get('trend_score', 0) > 75:
                        if 'keyword' in trend:
                            hot_topics.append(trend['keyword'])
                
                if hot_topics:
                    trends_insights.append(f"High-opportunity keywords identified: {', '.join(hot_topics)}")
            
            # Analyze news sentiment and volume
            news = scraped_data.get('news', [])
            if news:
                news_volume = len(news)
                if news_volume > 15:
                    trends_insights.append("High news volume indicates active market with frequent developments")
                elif news_volume > 8:
                    trends_insights.append("Moderate news activity suggests stable market conditions")
                else:
                    trends_insights.append("Limited news coverage may indicate niche market or emerging sector")
                
                # Analyze relevance scores
                relevance_scores = [article.get('relevance_score', 0) for article in news]
                if relevance_scores:
                    avg_relevance = statistics.mean(relevance_scores)
                    if avg_relevance > 7:
                        trends_insights.append("Highly relevant market content available for strategic insights")
                    elif avg_relevance > 4:
                        trends_insights.append("Moderately relevant market information available")
                    else:
                        trends_insights.append("Limited relevant market information suggests need for broader data sources")
            
            # Incorporate AI analysis trends
            if ai_analysis.get('market_direction'):
                direction = ai_analysis['market_direction']
                trends_insights.append(f"AI analysis indicates market is {direction.lower()}")
            
            if ai_analysis.get('trend_strength'):
                strength = ai_analysis['trend_strength']
                trends_insights.append(f"Overall trend strength assessed as {strength.lower()}")
            
        except Exception as e:
            logger.error(f"Error analyzing market trends: {str(e)}")
            trends_insights.append("Unable to complete market trend analysis")
        
        return trends_insights[:5]  # Return top 5 insights
    
    def _analyze_competitive_landscape(self, scraped_data: Dict, ai_analysis: Dict) -> str:
        """Analyze competitive landscape"""
        
        try:
            competitors = scraped_data.get('competitors', [])
            
            if not competitors:
                return "Limited competitive intelligence available. Recommend expanding competitor research."
            
            # Analyze competitor distribution
            large_competitors = sum(1 for c in competitors if c.get('estimated_size') == 'Large')
            medium_competitors = sum(1 for c in competitors if c.get('estimated_size') == 'Medium')
            small_competitors = sum(1 for c in competitors if c.get('estimated_size') == 'Small')
            
            total_competitors = len(competitors)
            
            landscape_description = f"Competitive landscape analysis based on {total_competitors} identified competitors: "
            
            if large_competitors > total_competitors * 0.5:
                landscape_description += "Market dominated by large players, suggesting high barriers to entry but potential for niche positioning. "
            elif medium_competitors > total_competitors * 0.5:
                landscape_description += "Market with balanced mix of established and emerging players, indicating opportunities for growth. "
            else:
                landscape_description += "Fragmented market with many smaller players, suggesting opportunities for consolidation or specialization. "
            
            # Market leaders analysis
            market_leaders = [c for c in competitors if c.get('market_position') == 'Market Leader']
            if market_leaders:
                landscape_description += f"Identified {len(market_leaders)} market leaders focusing on areas such as: "
                focus_areas = [c.get('focus_area', 'general market') for c in market_leaders]
                landscape_description += ", ".join(set(focus_areas)) + ". "
            
            # AI insights integration
            if ai_analysis.get('competition_level'):
                level = ai_analysis['competition_level']
                landscape_description += f"AI analysis indicates {level.lower()} competition level overall."
            
            return landscape_description
            
        except Exception as e:
            logger.error(f"Error analyzing competitive landscape: {str(e)}")
            return "Unable to complete competitive landscape analysis due to data processing error."
    
    def _analyze_lead_intelligence(self, scraped_data: Dict, ai_analysis: Dict) -> Dict[str, Any]:
        """Analyze lead intelligence and conversion potential"""
        
        try:
            leads = scraped_data.get('leads', [])
            
            if not leads:
                return {
                    "summary": "No leads discovered in current data collection cycle",
                    "recommendations": ["Expand data sources for lead discovery", "Consider manual prospecting in target segments"]
                }
            
            # Calculate lead metrics
            total_leads = len(leads)
            lead_scores = [lead.get('lead_score', 0) for lead in leads]
            avg_lead_score = statistics.mean(lead_scores) if lead_scores else 0
            
            # Quality assessment
            high_quality_leads = sum(1 for score in lead_scores if score >= 8)
            medium_quality_leads = sum(1 for score in lead_scores if 5 <= score < 8)
            
            summary = f"Discovered {total_leads} potential leads with average quality score of {avg_lead_score:.1f}/10. "
            
            if high_quality_leads > 0:
                summary += f"{high_quality_leads} high-quality leads identified for immediate follow-up. "
            
            if medium_quality_leads > 0:
                summary += f"{medium_quality_leads} medium-quality leads suitable for nurturing campaigns."
            
            # Lead source analysis
            lead_sources = {}
            for lead in leads:
                source = lead.get('source', 'Unknown')
                lead_sources[source] = lead_sources.get(source, 0) + 1
            
            best_source = max(lead_sources.items(), key=lambda x: x[1]) if lead_sources else None
            if best_source:
                summary += f" Most productive lead source: {best_source[0]} ({best_source[1]} leads)."
            
            recommendations = []
            
            if avg_lead_score < 6:
                recommendations.append("Focus on improving lead qualification criteria")
                recommendations.append("Expand to higher-quality data sources")
            
            if high_quality_leads > 0:
                recommendations.append("Prioritize immediate outreach to high-scoring leads")
                recommendations.append("Develop personalized engagement strategies for top prospects")
            
            if total_leads < 5:
                recommendations.append("Increase lead generation activities")
                recommendations.append("Consider expanding to additional market segments")
            
            return {
                "summary": summary,
                "total_leads": total_leads,
                "average_score": avg_lead_score,
                "high_quality_count": high_quality_leads,
                "recommendations": recommendations
            }
            
        except Exception as e:
            logger.error(f"Error analyzing lead intelligence: {str(e)}")
            return {"summary": "Unable to analyze lead intelligence", "recommendations": []}
    
    def _assess_risks(self, scraped_data: Dict, ai_analysis: Dict) -> List[str]:
        """Assess business risks based on market intelligence"""
        
        risks = []
        
        try:
            # Market trend risks
            trends = scraped_data.get('trends', [])
            if trends:
                trend_scores = [t.get('trend_score', 0) for t in trends if 'trend_score' in t]
                if trend_scores and statistics.mean(trend_scores) < 25:
                    risks.append("Low market momentum may indicate declining interest or oversaturation")
            
            # News volume risks
            news = scraped_data.get('news', [])
            if len(news) < 5:
                risks.append("Limited news coverage suggests low market visibility or emerging sector uncertainty")
            
            # Competitive risks
            competitors = scraped_data.get('competitors', [])
            large_competitors = sum(1 for c in competitors if c.get('estimated_size') == 'Large')
            if large_competitors > len(competitors) * 0.6:
                risks.append("Market dominated by large players presents high competitive barriers")
            
            # Lead generation risks
            leads = scraped_data.get('leads', [])
            if len(leads) < 3:
                risks.append("Limited lead discovery suggests challenging customer acquisition environment")
            
            # AI-identified risks
            if ai_analysis.get('risks'):
                risks.extend(ai_analysis['risks'][:3])  # Add top 3 AI-identified risks
            
            # Data quality risks
            data_age = self._calculate_data_age(scraped_data)
            if data_age > 24:  # hours
                risks.append("Data freshness concerns may impact decision accuracy")
                
        except Exception as e:
            logger.error(f"Error assessing risks: {str(e)}")
            risks.append("Unable to complete comprehensive risk assessment")
        
        return risks[:5]  # Return top 5 risks
    
    def _identify_growth_opportunities(self, scraped_data: Dict, ai_analysis: Dict) -> List[str]:
        """Identify growth opportunities based on market intelligence"""
        
        opportunities = []
        
        try:
            # High-trending keyword opportunities
            trends = scraped_data.get('trends', [])
            for trend in trends:
                if trend.get('trend_score', 0) > 75:
                    keyword = trend.get('keyword', 'Unknown')
                    opportunities.append(f"High-growth opportunity in {keyword} segment with strong market momentum")
            
            # News-based opportunities
            news = scraped_data.get('news', [])
            high_relevance_news = [n for n in news if n.get('relevance_score', 0) > 8]
            if len(high_relevance_news) > 5:
                opportunities.append("Strong market discourse indicates active customer engagement and sales opportunities")
            
            # Competitive gap opportunities
            competitors = scraped_data.get('competitors', [])
            if competitors:
                focus_areas = [c.get('focus_area', '') for c in competitors]
                industry_keywords = config.INDUSTRIES.get(scraped_data.get('industry', ''), {}).get('keywords', [])
                
                # Find underserved keywords
                underserved = [kw for kw in industry_keywords if kw not in focus_areas]
                if underserved:
                    opportunities.append(f"Underserved market segments identified: {', '.join(underserved[:3])}")
            
            # Lead quality opportunities
            leads = scraped_data.get('leads', [])
            high_quality_leads = sum(1 for lead in leads if lead.get('lead_score', 0) >= 8)
            if high_quality_leads > 0:
                opportunities.append(f"Immediate sales opportunities with {high_quality_leads} high-quality prospects identified")
            
            # AI-identified opportunities
            if ai_analysis.get('opportunities'):
                opportunities.extend(ai_analysis['opportunities'][:3])  # Add top 3 AI opportunities
                
        except Exception as e:
            logger.error(f"Error identifying growth opportunities: {str(e)}")
            opportunities.append("Unable to complete comprehensive opportunity analysis")
        
        return opportunities[:5]  # Return top 5 opportunities
    
    def _generate_executive_summary(self, scraped_data: Dict, ai_analysis: Dict) -> str:
        """Generate executive summary of business intelligence"""
        
        try:
            industry_name = config.INDUSTRIES.get(scraped_data.get('industry', ''), {}).get('name', 'Unknown Industry')
            
            # Key metrics
            total_data_points = (
                len(scraped_data.get('trends', [])) +
                len(scraped_data.get('news', [])) +
                len(scraped_data.get('leads', [])) +
                len(scraped_data.get('competitors', []))
            )
            
            summary_parts = []
            
            # Opening
            summary_parts.append(f"Business Intelligence Summary for {industry_name}:")
            summary_parts.append(f"Analysis based on {total_data_points} data points collected on {datetime.now().strftime('%Y-%m-%d')}.")
            
            # Market assessment
            if ai_analysis.get('market_summary'):
                summary_parts.append(f"Market Overview: {ai_analysis['market_summary']}")
            
            # Key opportunities
            opportunities = ai_analysis.get('opportunities', [])
            if opportunities:
                summary_parts.append(f"Primary Opportunity: {opportunities[0]}")
            
            # Key risks
            risks = ai_analysis.get('risks', [])
            if risks:
                summary_parts.append(f"Primary Risk: {risks[0]}")
            
            # Competitive landscape
            competitors_count = len(scraped_data.get('competitors', []))
            if competitors_count > 0:
                summary_parts.append(f"Analyzed {competitors_count} competitors in the competitive landscape.")
            
            # Lead potential
            leads_count = len(scraped_data.get('leads', []))
            if leads_count > 0:
                summary_parts.append(f"Identified {leads_count} potential leads for business development.")
            
            # Confidence and recommendations
            confidence = ai_analysis.get('confidence_score', 0)
            summary_parts.append(f"Analysis confidence level: {confidence:.1f}/10.")
            
            recommendations_count = len(ai_analysis.get('recommendations', []))
            if recommendations_count > 0:
                summary_parts.append(f"Generated {recommendations_count} actionable business recommendations.")
            
            return " ".join(summary_parts)
            
        except Exception as e:
            logger.error(f"Error generating executive summary: {str(e)}")
            return f"Executive summary for {industry_name} - analysis completed with limited data processing capability."
    
    # Helper methods
    
    def _calculate_opportunity_score(self, scraped_data: Dict, ai_analysis: Dict) -> float:
        """Calculate overall market opportunity score (1-10)"""
        score = 5.0  # Base score
        
        # Trend momentum factor
        trends = scraped_data.get('trends', [])
        if trends:
            trend_scores = [t.get('trend_score', 0) for t in trends if 'trend_score' in t]
            if trend_scores:
                avg_trend = statistics.mean(trend_scores)
                score += (avg_trend / 100) * 3  # Max 3 points from trends
        
        # News activity factor
        news_count = len(scraped_data.get('news', []))
        if news_count > 15:
            score += 1.5
        elif news_count > 8:
            score += 1.0
        elif news_count > 3:
            score += 0.5
        
        # Lead potential factor
        leads = scraped_data.get('leads', [])
        if leads:
            avg_lead_score = statistics.mean([l.get('lead_score', 0) for l in leads])
            score += (avg_lead_score / 10) * 1.5  # Max 1.5 points from leads
        
        return min(10.0, max(1.0, round(score, 1)))
    
    def _assess_competition_level(self, scraped_data: Dict, ai_analysis: Dict) -> str:
        """Assess competition level"""
        competitors = scraped_data.get('competitors', [])
        
        if not competitors:
            return "Unknown"
        
        large_competitors = sum(1 for c in competitors if c.get('estimated_size') == 'Large')
        total_competitors = len(competitors)
        
        if large_competitors > total_competitors * 0.6:
            return "High"
        elif large_competitors > total_competitors * 0.3:
            return "Medium"
        else:
            return "Low"
    
    def _calculate_lead_quality_score(self, scraped_data: Dict) -> float:
        """Calculate average lead quality score"""
        leads = scraped_data.get('leads', [])
        if not leads:
            return 0.0
        
        lead_scores = [lead.get('lead_score', 0) for lead in leads]
        return round(statistics.mean(lead_scores), 1) if lead_scores else 0.0
    
    def _assess_trend_momentum(self, scraped_data: Dict) -> str:
        """Assess overall trend momentum"""
        trends = scraped_data.get('trends', [])
        if not trends:
            return "Unknown"
        
        trend_scores = [t.get('trend_score', 0) for t in trends if 'trend_score' in t]
        if not trend_scores:
            return "Stable"
        
        avg_score = statistics.mean(trend_scores)
        
        if avg_score > 60:
            return "Strong Growth"
        elif avg_score > 30:
            return "Moderate Growth"
        elif avg_score > 15:
            return "Stable"
        else:
            return "Declining"
    
    def _calculate_trend_direction(self, scraped_data: Dict) -> float:
        """Calculate trend direction indicator"""
        # This would typically compare with historical data
        # For now, return a simple indicator based on current data
        trends = scraped_data.get('trends', [])
        if not trends:
            return 0.0
        
        trend_scores = [t.get('trend_score', 0) for t in trends if 'trend_score' in t]
        if not trend_scores:
            return 0.0
        
        avg_score = statistics.mean(trend_scores)
        
        # Simple heuristic: above average market activity = positive trend
        if avg_score > 40:
            return 1.5
        elif avg_score > 25:
            return 0.5
        elif avg_score < 15:
            return -1.0
        else:
            return 0.0
    
    def _assess_competition_change(self, scraped_data: Dict) -> str:
        """Assess competition level change"""
        # This would typically compare with historical data
        # For now, return neutral indicator
        return ""
    
    def _calculate_data_freshness(self, scraped_data: Dict) -> float:
        """Calculate data freshness score (hours since collection)"""
        try:
            timestamp_str = scraped_data.get('timestamp')
            if not timestamp_str:
                return 0.0
            
            data_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            current_time = datetime.now()
            
            # Calculate hours difference
            hours_diff = (current_time - data_time).total_seconds() / 3600
            
            # Score: 10 for <1 hour, decreasing linearly to 1 for 24+ hours
            freshness_score = max(1.0, 10.0 - (hours_diff / 24.0) * 9.0)
            return round(freshness_score, 1)
            
        except Exception as e:
            logger.error(f"Error calculating data freshness: {str(e)}")
            return 5.0  # Default moderate score
    
    def _calculate_data_age(self, scraped_data: Dict) -> float:
        """Calculate data age in hours"""
        try:
            timestamp_str = scraped_data.get('timestamp')
            if not timestamp_str:
                return 0.0
            
            data_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            current_time = datetime.now()
            
            return (current_time - data_time).total_seconds() / 3600
            
        except Exception as e:
            logger.error(f"Error calculating data age: {str(e)}")
            return 0.0
