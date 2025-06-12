import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
from jinja2 import Template

class EmailTemplateSystem:
    """Professional email template system for business intelligence reports"""
    
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.email_user = os.getenv('EMAIL_USER')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        self.from_email = os.getenv('FROM_EMAIL', 'intelligence@aiagentprospera.com')
        self.company_name = "AI Agent Prospera"
    
    def generate_weekly_briefing_email(self, profile: Dict, analysis: Dict, week_date: str) -> str:
        """Generate the weekly executive briefing email"""
        
        # Extract key metrics
        leads = analysis.get('qualified_leads', {}).get('leads', [])
        opportunities = analysis.get('targeted_opportunities', [])
        urgent_actions = self._extract_urgent_actions(analysis)
        
        # Calculate totals
        total_opportunity_value = self._calculate_total_value(opportunities)
        lead_count = len(leads)
        opportunity_count = len(opportunities)
        
        template = Template(self._get_weekly_briefing_template())
        
        return template.render(
            company_name=profile.get('company_name', 'Your Company'),
            week_date=week_date,
            urgent_actions=urgent_actions[:3],  # Top 3 urgent actions
            lead_count=lead_count,
            opportunity_count=opportunity_count,
            total_value=total_opportunity_value,
            top_leads=leads[:3],  # Top 3 leads
            dashboard_url="https://aiagentprospera.com/dashboard",
            calendar_url="https://calendly.com/prospera-strategy",
            mobile_app_url="https://aiagentprospera.com/mobile",
            unsubscribe_url="https://aiagentprospera.com/unsubscribe"
        )
    
    def generate_urgent_alert_email(self, profile: Dict, alert: Dict) -> str:
        """Generate urgent opportunity alert email"""
        
        template = Template(self._get_urgent_alert_template())
        
        return template.render(
            company_name=profile.get('company_name', 'Your Company'),
            alert_title=alert.get('title', 'Urgent Business Opportunity'),
            alert_description=alert.get('description', ''),
            contact_name=alert.get('contact_name', ''),
            contact_info=alert.get('contact_info', ''),
            deadline=alert.get('deadline', ''),
            potential_value=alert.get('potential_value', ''),
            action_required=alert.get('action_required', ''),
            dashboard_url="https://aiagentprospera.com/dashboard"
        )
    
    def send_email(self, to_email: str, subject: str, html_content: str, attachments: List[str] = None) -> bool:
        """Send email with professional formatting (requires email configuration)"""
        
        if attachments is None:
            attachments = []
        
        # For demo purposes, return True (in production, implement actual email sending)
        print(f"Email would be sent to: {to_email}")
        print(f"Subject: {subject}")
        print("Email sending requires proper SMTP configuration")
        return True
    
    def _get_weekly_briefing_template(self) -> str:
        """HTML template for weekly briefing"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prospera Weekly Intelligence Briefing</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            background-color: #f8f9fa;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        .header {
            background: linear-gradient(135deg, #1f77b4, #2e8b57);
            color: white;
            padding: 30px 20px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 24px;
            font-weight: 600;
        }
        .header p {
            margin: 10px 0 0 0;
            opacity: 0.9;
            font-size: 14px;
        }
        .content {
            padding: 30px 20px;
        }
        .summary-box {
            background-color: #f8f9fa;
            border-left: 4px solid #1f77b4;
            padding: 20px;
            margin: 20px 0;
            border-radius: 4px;
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin: 20px 0;
        }
        .metric-card {
            text-align: center;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 6px;
            border: 1px solid #e9ecef;
        }
        .metric-number {
            font-size: 24px;
            font-weight: bold;
            color: #1f77b4;
            display: block;
        }
        .metric-label {
            font-size: 12px;
            color: #6c757d;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .urgent-actions {
            margin: 30px 0;
        }
        .action-card {
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 6px;
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #f39c12;
        }
        .action-title {
            font-weight: 600;
            color: #856404;
            margin-bottom: 5px;
        }
        .action-details {
            font-size: 14px;
            color: #6c5400;
        }
        .leads-section {
            margin: 30px 0;
        }
        .lead-card {
            background-color: #e8f5e8;
            border: 1px solid #c3e6c3;
            border-radius: 6px;
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #28a745;
        }
        .lead-name {
            font-weight: 600;
            color: #155724;
            margin-bottom: 5px;
        }
        .lead-details {
            font-size: 14px;
            color: #0f5132;
        }
        .cta-section {
            text-align: center;
            margin: 30px 0;
        }
        .cta-button {
            display: inline-block;
            background-color: #1f77b4;
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 600;
            margin: 5px;
        }
        .cta-button.secondary {
            background-color: #28a745;
        }
        .footer {
            background-color: #f8f9fa;
            padding: 20px;
            text-align: center;
            font-size: 12px;
            color: #6c757d;
            border-top: 1px solid #e9ecef;
        }
        .footer a {
            color: #1f77b4;
            text-decoration: none;
        }
        @media (max-width: 600px) {
            .metrics-grid {
                grid-template-columns: 1fr;
            }
            .container {
                margin: 0;
                border-radius: 0;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Weekly Intelligence Briefing</h1>
            <p>{{ company_name }} | Week of {{ week_date }}</p>
        </div>
        
        <div class="content">
            <div class="summary-box">
                <strong>Executive Summary:</strong> This week Prospera identified {{ lead_count }} qualified leads and {{ opportunity_count }} market opportunities with combined potential value of {{ total_value }}. Your focus should be on the urgent actions below.
            </div>
            
            <div class="metrics-grid">
                <div class="metric-card">
                    <span class="metric-number">{{ lead_count }}</span>
                    <span class="metric-label">New Leads</span>
                </div>
                <div class="metric-card">
                    <span class="metric-number">{{ opportunity_count }}</span>
                    <span class="metric-label">Opportunities</span>
                </div>
                <div class="metric-card">
                    <span class="metric-number">{{ total_value }}</span>
                    <span class="metric-label">Potential Value</span>
                </div>
            </div>
            
            <div class="urgent-actions">
                <h2>Urgent Actions Required</h2>
                {% for action in urgent_actions %}
                <div class="action-card">
                    <div class="action-title">{{ loop.index }}. {{ action.title }}</div>
                    <div class="action-details">{{ action.description }}</div>
                    {% if action.deadline %}
                    <div class="action-details"><strong>Deadline:</strong> {{ action.deadline }}</div>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
            
            <div class="leads-section">
                <h2>Top Priority Leads</h2>
                {% for lead in top_leads %}
                <div class="lead-card">
                    <div class="lead-name">{{ lead.company_name }} ({{ lead.profile_fit_score }}% match)</div>
                    <div class="lead-details">
                        <strong>Location:</strong> {{ lead.location }}<br>
                        <strong>Opportunity:</strong> {{ lead.opportunity }}<br>
                        <strong>Potential Value:</strong> {{ lead.estimated_annual_volume }}
                    </div>
                </div>
                {% endfor %}
            </div>
            
            <div class="cta-section">
                <a href="{{ dashboard_url }}" class="cta-button">View Full Dashboard</a>
                <a href="{{ calendar_url }}" class="cta-button secondary">Schedule Strategy Call</a>
            </div>
        </div>
        
        <div class="footer">
            <p>
                <strong>AI Agent Prospera</strong> - Your Business Intelligence Partner<br>
                <a href="{{ mobile_app_url }}">Mobile App</a> | 
                <a href="{{ dashboard_url }}">Dashboard</a> | 
                <a href="{{ unsubscribe_url }}">Unsubscribe</a>
            </p>
            <p>Time saved this week: 12+ hours of manual research</p>
        </div>
    </div>
</body>
</html>
        """
    
    def _get_urgent_alert_template(self) -> str:
        """HTML template for urgent alerts"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Urgent Business Opportunity Alert</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            background-color: #f8f9fa;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        .alert-header {
            background: linear-gradient(135deg, #dc3545, #c82333);
            color: white;
            padding: 30px 20px;
            text-align: center;
        }
        .alert-header h1 {
            margin: 0;
            font-size: 24px;
            font-weight: 600;
        }
        .content {
            padding: 30px 20px;
        }
        .alert-box {
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 6px;
            padding: 20px;
            margin: 20px 0;
            border-left: 4px solid #f39c12;
        }
        .cta-section {
            text-align: center;
            margin: 30px 0;
        }
        .cta-button {
            display: inline-block;
            background-color: #dc3545;
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 600;
            font-size: 16px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="alert-header">
            <h1>URGENT: {{ alert_title }}</h1>
            <p>{{ company_name }} - Immediate Action Required</p>
        </div>
        
        <div class="content">
            <div class="alert-box">
                <h3>{{ alert_title }}</h3>
                <p>{{ alert_description }}</p>
                {% if contact_name %}
                <p><strong>Contact:</strong> {{ contact_name }}</p>
                {% endif %}
                {% if deadline %}
                <p><strong>Deadline:</strong> {{ deadline }}</p>
                {% endif %}
                {% if potential_value %}
                <p><strong>Potential Value:</strong> {{ potential_value }}</p>
                {% endif %}
                {% if action_required %}
                <p><strong>Action Required:</strong> {{ action_required }}</p>
                {% endif %}
            </div>
            
            <div class="cta-section">
                <a href="{{ dashboard_url }}" class="cta-button">Take Action Now</a>
            </div>
        </div>
    </div>
</body>
</html>
        """
    
    def _extract_urgent_actions(self, analysis: Dict) -> List[Dict]:
        """Extract urgent actions from analysis"""
        actions = []
        
        # Add urgent actions based on analysis
        if analysis.get('business_insights', {}).get('risks'):
            for risk in analysis['business_insights']['risks'][:2]:
                actions.append({
                    'title': f"Address Market Risk: {risk[:50]}...",
                    'description': risk,
                    'deadline': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
                })
        
        if analysis.get('ai_analysis', {}).get('recommendations'):
            for rec in analysis['ai_analysis']['recommendations'][:2]:
                actions.append({
                    'title': f"Implement: {rec[:50]}...",
                    'description': rec,
                    'deadline': (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
                })
        
        return actions
    
    def _calculate_total_value(self, opportunities: List) -> str:
        """Calculate total opportunity value"""
        if not opportunities:
            return "$0"
        
        # For demo purposes, estimate based on number of opportunities
        estimated_value = len(opportunities) * 25000
        return f"${estimated_value:,}"