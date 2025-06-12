"""
Automated outreach campaign manager for Prospera
Sends proactive opportunity notifications to companies via email
"""
import os
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import smtplib

from ..utils.logger import setup_logger
from ..matching.opportunity_matcher import Match, Opportunity
from ..profile.business_profile import BusinessProfile

logger = setup_logger(__name__)

@dataclass
class Campaign:
    """Email campaign data structure"""
    id: str
    company_id: str
    campaign_type: str
    matches_included: List[str]
    sent_at: Optional[datetime] = None
    opened_at: Optional[datetime] = None
    clicked_at: Optional[datetime] = None
    status: str = 'draft'

class CampaignManager:
    """Manages automated email campaigns for opportunity delivery"""
    
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.email_user = os.getenv('EMAIL_USER')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        self.from_email = os.getenv('FROM_EMAIL', 'opportunities@prospera.ai')
        
    def create_opportunity_digest(self, profile: BusinessProfile, matches: List[Match], 
                                opportunities: Dict[str, Opportunity]) -> str:
        """Create HTML email content for opportunity digest"""
        
        if not matches:
            return self._create_no_opportunities_email(profile)
        
        # Sort matches by relevance score
        top_matches = sorted(matches, key=lambda x: x.relevance_score, reverse=True)[:5]
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>New Business Opportunities - {profile.company_name}</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                           color: white; padding: 30px; text-align: center; border-radius: 8px; }}
                .opportunity {{ border: 1px solid #ddd; margin: 15px 0; padding: 20px; 
                               border-radius: 8px; background: #f9f9f9; }}
                .score {{ background: #2ecc71; color: white; padding: 5px 10px; 
                         border-radius: 15px; font-size: 12px; display: inline-block; }}
                .cta-button {{ background: #3498db; color: white; padding: 12px 25px; 
                              text-decoration: none; border-radius: 5px; display: inline-block; 
                              margin: 10px 0; }}
                .footer {{ text-align: center; margin-top: 30px; padding: 20px; 
                          border-top: 1px solid #eee; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 New Opportunities for {profile.company_name}</h1>
                    <p>We found {len(top_matches)} high-relevance business opportunities for you</p>
                </div>
                
                <div style="padding: 20px 0;">
                    <h2>Top Opportunities This Week</h2>
        """
        
        for match in top_matches:
            opportunity = opportunities.get(match.opportunity_id)
            if not opportunity:
                continue
                
            score_color = self._get_score_color(match.relevance_score)
            
            html_content += f"""
                <div class="opportunity">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h3 style="margin: 0; color: #2c3e50;">{opportunity.title}</h3>
                        <span class="score" style="background: {score_color};">
                            {match.relevance_score:.0%} Match
                        </span>
                    </div>
                    
                    <p style="margin: 10px 0; color: #666;">
                        <strong>Source:</strong> {opportunity.source} | 
                        <strong>Type:</strong> {opportunity.opportunity_type.title()}
                    </p>
                    
                    <p>{opportunity.description}</p>
                    
                    <div style="background: #e8f4fd; padding: 15px; border-radius: 5px; margin: 10px 0;">
                        <strong>Why this matches:</strong> {match.reasoning[:200]}...
                    </div>
                    
                    <a href="https://prospera.ai/opportunities/{match.opportunity_id}" 
                       class="cta-button">View Full Details (1 Credit)</a>
                </div>
            """
        
        html_content += f"""
                </div>
                
                <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3>📊 Your Opportunity Summary</h3>
                    <ul>
                        <li><strong>{len(matches)}</strong> total opportunities found</li>
                        <li><strong>{len([m for m in matches if m.relevance_score >= 0.8])}</strong> high-relevance matches</li>
                        <li><strong>{profile.industry}</strong> industry focus</li>
                        <li>Updated {datetime.now().strftime('%B %d, %Y')}</li>
                    </ul>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="https://prospera.ai/dashboard" class="cta-button" style="font-size: 16px;">
                        View All Opportunities
                    </a>
                </div>
                
                <div class="footer">
                    <p>This email was sent by Prospera AI - Your Business Intelligence Partner</p>
                    <p>
                        <a href="https://prospera.ai/unsubscribe">Unsubscribe</a> | 
                        <a href="https://prospera.ai/preferences">Email Preferences</a>
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_content
    
    def send_opportunity_campaign(self, profile: BusinessProfile, matches: List[Match], 
                                opportunities: Dict[str, Opportunity]) -> bool:
        """Send opportunity digest email campaign (simulation for demo)"""
        
        # Create email content for logging/preview
        html_content = self.create_opportunity_digest(profile, matches, opportunities)
        
        # Log email content (in production this would send actual emails)
        logger.info(f"Email campaign prepared for {profile.company_name}")
        
        # Simulate successful send
        return True
    
    def _get_score_color(self, score: float) -> str:
        """Get color for relevance score badge"""
        
        if score >= 0.9:
            return "#27ae60"  # Green
        elif score >= 0.8:
            return "#f39c12"  # Orange
        elif score >= 0.7:
            return "#3498db"  # Blue
        else:
            return "#95a5a6"  # Gray
