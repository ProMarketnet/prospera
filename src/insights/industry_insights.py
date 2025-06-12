"""
Industry-specific insights and recommendations engine
Provides tailored business intelligence based on NAICS industry classification
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import streamlit as st

class IndustryInsightsEngine:
    """Generates industry-specific insights and recommendations"""
    
    def __init__(self):
        self.industry_insights = {
            "fashion_apparel": {
                "key_trends": [
                    "Sustainable fashion gaining 40% market share",
                    "Direct-to-consumer brands disrupting retail",
                    "AI-powered personalization driving sales",
                    "Circular economy models reducing waste"
                ],
                "opportunities": [
                    "Eco-friendly materials market expanding rapidly",
                    "Rental and resale platforms growing 25% annually",
                    "Customization technology creating premium segments",
                    "Cross-border e-commerce opening new markets"
                ],
                "challenges": [
                    "Fast fashion competition pressuring margins",
                    "Supply chain sustainability requirements increasing",
                    "Inventory management complexity rising",
                    "Consumer price sensitivity heightened"
                ],
                "success_metrics": [
                    "Inventory turnover ratio",
                    "Gross margin percentage", 
                    "Customer acquisition cost",
                    "Return rate optimization"
                ]
            },
            "manufacturing": {
                "key_trends": [
                    "Industry 4.0 adoption accelerating automation",
                    "Supply chain localization reducing dependencies",
                    "Predictive maintenance cutting downtime 30%",
                    "Additive manufacturing enabling customization"
                ],
                "opportunities": [
                    "Smart factory technology improving efficiency",
                    "Sustainable materials creating new product lines",
                    "Workforce upskilling programs expanding capacity",
                    "Digital twin technology optimizing processes"
                ],
                "challenges": [
                    "Skilled labor shortage affecting production",
                    "Raw material price volatility impacting costs",
                    "Regulatory compliance requirements increasing",
                    "Cybersecurity threats targeting industrial systems"
                ],
                "success_metrics": [
                    "Overall equipment effectiveness (OEE)",
                    "Production cycle time",
                    "Quality defect rates",
                    "Energy efficiency ratios"
                ]
            },
            "technology_software": {
                "key_trends": [
                    "AI and machine learning integration across industries",
                    "Cloud-first architecture becoming standard",
                    "No-code/low-code platforms democratizing development",
                    "Cybersecurity-by-design gaining importance"
                ],
                "opportunities": [
                    "Enterprise AI solutions market expanding rapidly",
                    "Remote work tools creating permanent demand",
                    "Edge computing enabling new applications",
                    "API economy facilitating business integration"
                ],
                "challenges": [
                    "Talent acquisition competition intensifying",
                    "Data privacy regulations increasing compliance costs",
                    "Technical debt accumulation slowing innovation",
                    "Market saturation in consumer applications"
                ],
                "success_metrics": [
                    "Monthly recurring revenue (MRR)",
                    "Customer lifetime value (CLV)",
                    "Churn rate optimization",
                    "Development velocity metrics"
                ]
            }
        }
    
    def get_industry_insights(self, industry_key: str) -> Dict[str, Any]:
        """Get comprehensive insights for specific industry"""
        
        insights = self.industry_insights.get(industry_key, {}).copy()
        
        if not insights:
            insights = self._generate_generic_insights(industry_key)
        
        # Add additional context without type conflicts
        market_context = self._get_current_market_context(industry_key)
        recommended_actions = self._get_recommended_actions(industry_key, insights)
        
        result = dict(insights)
        result["market_context"] = market_context
        result["recommended_actions"] = recommended_actions
        
        return result
    
    def _generate_generic_insights(self, industry_key: str) -> Dict[str, Any]:
        """Generate generic insights for industries not specifically covered"""
        
        return {
            "key_trends": [
                "Digital transformation accelerating across all sectors",
                "Sustainability initiatives becoming competitive advantage",
                "Customer experience differentiation driving loyalty",
                "Data-driven decision making improving outcomes"
            ],
            "opportunities": [
                "Technology adoption creating efficiency gains",
                "Market expansion through digital channels",
                "Operational optimization reducing costs",
                "Strategic partnerships enabling growth"
            ],
            "challenges": [
                "Economic uncertainty affecting consumer spending",
                "Talent acquisition competition intensifying",
                "Regulatory compliance requirements increasing",
                "Supply chain resilience becoming critical"
            ],
            "success_metrics": [
                "Revenue growth rate",
                "Customer satisfaction scores",
                "Operational efficiency ratios",
                "Market share progression"
            ]
        }
    
    def _get_current_market_context(self, industry_key: str) -> Dict[str, str]:
        """Get current market context and conditions"""
        
        return {
            "market_stage": "Growth phase with consolidation trends",
            "competitive_intensity": "High with new entrants disrupting",
            "regulatory_environment": "Evolving with increased oversight",
            "economic_factors": "Interest rates and inflation impacting costs",
            "technology_impact": "AI and automation reshaping operations"
        }
    
    def _get_recommended_actions(self, industry_key: str, insights: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate specific recommended actions based on insights"""
        
        actions = []
        
        if insights.get("key_trends"):
            actions.append({
                "category": "Strategic Planning",
                "action": "Develop digital transformation roadmap",
                "priority": "High",
                "timeline": "3-6 months",
                "impact": "Position for future market leadership"
            })
        
        if insights.get("challenges"):
            actions.append({
                "category": "Operational Excellence",
                "action": "Implement supply chain risk management",
                "priority": "Medium",
                "timeline": "2-4 months", 
                "impact": "Reduce disruption risks and costs"
            })
        
        if insights.get("opportunities"):
            actions.append({
                "category": "Growth Strategy",
                "action": "Explore new market segments",
                "priority": "Medium",
                "timeline": "6-12 months",
                "impact": "Expand revenue streams and reduce dependency"
            })
        
        actions.append({
            "category": "Performance Management",
            "action": "Establish key performance indicators tracking",
            "priority": "High",
            "timeline": "1-2 months",
            "impact": "Enable data-driven decision making"
        })
        
        return actions
    
    def render_industry_insights_widget(self, industry_key: str):
        """Render industry insights widget in Streamlit"""
        
        insights = self.get_industry_insights(industry_key)
        
        st.markdown("### Industry Intelligence")
        
        with st.expander("Key Market Trends", expanded=True):
            for i, trend in enumerate(insights.get("key_trends", [])[:4], 1):
                st.markdown(f"**{i}.** {trend}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Opportunities**")
            for opp in insights.get("opportunities", [])[:3]:
                st.markdown(f"• {opp}")
        
        with col2:
            st.markdown("**Challenges**")
            for challenge in insights.get("challenges", [])[:3]:
                st.markdown(f"• {challenge}")
        
        if insights.get("recommended_actions"):
            st.markdown("### Recommended Actions")
            
            for action in insights["recommended_actions"][:3]:
                with st.container():
                    priority_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
                    priority_icon = priority_color.get(action["priority"], "🔵")
                    
                    st.markdown(f"""
                    **{priority_icon} {action['action']}**
                    - Category: {action['category']}
                    - Timeline: {action['timeline']}
                    - Impact: {action['impact']}
                    """)
        
        if insights.get("success_metrics"):
            st.markdown("### Key Success Metrics")
            metrics_cols = st.columns(2)
            
            for i, metric in enumerate(insights["success_metrics"][:4]):
                col_idx = i % 2
                with metrics_cols[col_idx]:
                    st.markdown(f"• {metric}")

def get_industry_key_from_config(industry_name: str) -> str:
    """Map industry display name to configuration key"""
    
    mapping = {
        "Fashion & Apparel (SME Focus)": "fashion_apparel",
        "Manufacturing": "manufacturing", 
        "Technology & Software": "technology_software",
        "Health Care & Social Assistance": "healthcare",
        "Finance & Insurance": "finance_insurance",
        "Retail Trade": "retail_trade"
    }
    
    return mapping.get(industry_name, "general")