import streamlit as st
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
from .email_templates import EmailTemplateSystem

class ReportDashboard:
    """Dashboard for managing and sending business intelligence reports"""
    
    def __init__(self):
        self.email_system = EmailTemplateSystem()
    
    def display_report_delivery_dashboard(self):
        """Display the complete report delivery dashboard"""
        
        st.markdown("## 📧 Report Delivery & Email System")
        st.markdown("Configure automated reports and email alerts for your business intelligence insights.")
        
        # Quick setup banner
        if not hasattr(st.session_state, 'email_configured'):
            st.info("Set up email delivery to receive automated weekly business intelligence reports and urgent opportunity alerts directly in your inbox!")
            if st.button("Quick Setup Guide", key=f"email_setup_guide_{id(self)}"):
                st.session_state.show_email_guide = True
        
        # Quick status overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Email Config", "Not Set", delta="Setup Required", delta_color="inverse")
        with col2:
            st.metric("Weekly Reports", "Disabled", delta="Configure Now", delta_color="inverse")
        with col3:
            st.metric("Urgent Alerts", "Disabled", delta="Enable", delta_color="inverse")
        with col4:
            st.metric("Last Delivery", "Never", delta="Send Test", delta_color="inverse")
        
        st.markdown("---")
        
        # Email Configuration Section
        with st.expander("1. Email Configuration", expanded=True):
            self._display_email_config()
        
        # Report Scheduling Section
        with st.expander("2. Report Scheduling"):
            self._display_report_scheduling()
        
        # Email Preview Section
        with st.expander("3. Email Preview & Testing"):
            self._display_email_preview()
        
        # Delivery History
        with st.expander("4. Delivery History & Analytics"):
            self._display_delivery_history()
    
    def _display_email_config(self):
        """Display email configuration settings"""
        
        st.markdown("### Email Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            smtp_server = st.text_input("SMTP Server", value="smtp.gmail.com", help="Your email provider's SMTP server", key=f"smtp_server_{id(self)}")
            smtp_port = st.number_input("SMTP Port", value=587, help="Usually 587 for TLS or 465 for SSL", key=f"smtp_port_{id(self)}")
            from_email = st.text_input("From Email", placeholder="your-email@company.com", key=f"from_email_{id(self)}")
        
        with col2:
            email_user = st.text_input("Email Username", placeholder="your-email@gmail.com", key=f"email_user_{id(self)}")
            email_password = st.text_input("Email Password", type="password", help="Use app password for Gmail", key=f"email_password_{id(self)}")
            company_name = st.text_input("Company Name", value="AI Agent Prospera", key=f"company_name_{id(self)}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Test Email Configuration", type="primary", key=f"test_email_config_{id(self)}"):
                if email_user and email_password:
                    test_result = self._test_email_config(smtp_server, smtp_port, email_user, email_password)
                    if test_result:
                        st.success("Email configuration is working correctly!")
                        st.session_state.email_configured = True
                    else:
                        st.error("Email configuration failed. Please check your settings.")
                else:
                    st.warning("Please provide email username and password to test configuration.")
        
        with col2:
            if st.button("Save Configuration", key=f"save_email_config_{id(self)}"):
                st.session_state.email_config = {
                    'smtp_server': smtp_server,
                    'smtp_port': smtp_port,
                    'email_user': email_user,
                    'from_email': from_email,
                    'company_name': company_name
                }
                st.success("Email configuration saved!")
    
    def _display_report_scheduling(self):
        """Display report scheduling options"""
        
        st.markdown("### Automated Report Scheduling")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Weekly Executive Briefing")
            weekly_enabled = st.checkbox("Enable Weekly Reports", value=True, key=f"weekly_enabled_{id(self)}")
            weekly_day = st.selectbox("Send on", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], index=0, key=f"weekly_day_{id(self)}")
            weekly_time = st.time_input("At time", value=datetime.strptime("09:00", "%H:%M").time(), key=f"weekly_time_{id(self)}")
            weekly_recipients = st.text_area("Recipients (one per line)", placeholder="ceo@company.com\nmanager@company.com", key=f"weekly_recipients_{id(self)}")
        
        with col2:
            st.markdown("#### Urgent Alerts")
            alerts_enabled = st.checkbox("Enable Urgent Alerts", value=True, key=f"alerts_enabled_{id(self)}")
            alert_threshold = st.slider("Alert Threshold (Opportunity Value)", 0, 100000, 25000, step=5000, key=f"alert_threshold_{id(self)}")
            alert_recipients = st.text_area("Alert Recipients", placeholder="sales@company.com\nalerts@company.com", key=f"alert_recipients_{id(self)}")
        
        # Save scheduling settings
        if st.button("Save Scheduling Settings", key=f"save_schedule_settings_{id(self)}"):
            schedule_config = {
                "weekly_reports": {
                    "enabled": weekly_enabled,
                    "day": weekly_day,
                    "time": weekly_time.strftime("%H:%M"),
                    "recipients": [email.strip() for email in weekly_recipients.split('\n') if email.strip()]
                },
                "urgent_alerts": {
                    "enabled": alerts_enabled,
                    "threshold": alert_threshold,
                    "recipients": [email.strip() for email in alert_recipients.split('\n') if email.strip()]
                }
            }
            
            # Save to session state (in production, save to database)
            st.session_state.schedule_config = schedule_config
            st.success("Scheduling settings saved successfully!")
    
    def _display_email_preview(self):
        """Display email preview and testing"""
        
        st.markdown("### Email Preview & Testing")
        
        email_type = st.selectbox("Email Type", ["Weekly Briefing", "Urgent Alert"], key=f"email_type_{id(self)}")
        
        # Initialize variables at function scope
        sample_profile = {"company_name": "Sample Company Inc.", "industry": "technology"}
        week_date = datetime.now().strftime("%Y-%m-%d")
        
        sample_analysis = {
            "qualified_leads": {"leads": [
                {"company_name": "TechCorp", "profile_fit_score": 85, "location": "San Francisco", 
                 "opportunity": "Digital transformation", "estimated_annual_volume": "$150,000"},
                {"company_name": "DataSoft", "profile_fit_score": 92, "location": "New York", 
                 "opportunity": "AI implementation", "estimated_annual_volume": "$200,000"}
            ]},
            "targeted_opportunities": [{"value": 25000}, {"value": 35000}],
            "business_insights": {
                "risks": ["Market saturation in primary region", "Increased competition from new entrants"],
            },
            "ai_analysis": {
                "recommendations": ["Expand to European markets", "Develop mobile-first strategy"]
            }
        }
        
        sample_alert = {
            "title": "High-Value Lead Requires Immediate Attention",
            "description": "A potential client with $500K annual contract value has shown strong interest and is making decisions this week.",
            "contact_name": "John Smith, CEO",
            "contact_info": "john@bigclient.com",
            "deadline": "2024-12-15",
            "potential_value": "$500,000",
            "action_required": "Schedule meeting within 48 hours"
        }
        
        if email_type == "Weekly Briefing":
            html_content = self.email_system.generate_weekly_briefing_email(
                sample_profile, sample_analysis, week_date
            )
            
            st.markdown("#### Weekly Briefing Preview:")
            st.code(html_content[:500] + "..." if len(html_content) > 500 else html_content, language="html")
        
        elif email_type == "Urgent Alert":
            html_content = self.email_system.generate_urgent_alert_email(sample_profile, sample_alert)
            
            st.markdown("#### Urgent Alert Preview:")
            st.code(html_content[:500] + "..." if len(html_content) > 500 else html_content, language="html")
        
        # Test email sending
        col1, col2 = st.columns(2)
        with col1:
            test_email = st.text_input("Test Email Address", placeholder="test@example.com", key=f"test_email_{id(self)}")
        with col2:
            if st.button("Send Test Email", key=f"send_test_email_{id(self)}"):
                if test_email:
                    # Generate content based on email type
                    if email_type == "Weekly Briefing":
                        test_html_content = self.email_system.generate_weekly_briefing_email(
                            sample_profile, sample_analysis, week_date
                        )
                    else:
                        test_html_content = self.email_system.generate_urgent_alert_email(sample_profile, sample_alert)
                    
                    success = self._send_test_email(test_email, email_type, test_html_content)
                    if success:
                        st.success(f"Test {email_type.lower()} sent to {test_email}")
                    else:
                        st.error("Failed to send test email. Check your email configuration.")
                else:
                    st.warning("Please enter a test email address.")
    
    def _display_delivery_history(self):
        """Display email delivery history"""
        
        st.markdown("### Recent Deliveries")
        
        # Sample delivery history (in production, fetch from database)
        delivery_history = [
            {
                "date": "2024-12-08 09:00",
                "type": "Weekly Briefing",
                "recipients": ["ceo@company.com", "sales@company.com"],
                "status": "Delivered",
                "open_rate": "85%"
            },
            {
                "date": "2024-12-06 14:30",
                "type": "Urgent Alert",
                "recipients": ["sales@company.com"],
                "status": "Delivered",
                "open_rate": "100%"
            },
            {
                "date": "2024-12-01 09:00",
                "type": "Weekly Briefing",
                "recipients": ["ceo@company.com", "sales@company.com"],
                "status": "Delivered",
                "open_rate": "90%"
            }
        ]
        
        # Display as table
        import pandas as pd
        df = pd.DataFrame(delivery_history)
        st.dataframe(df, use_container_width=True)
        
        # Delivery statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Sent", "24")
        with col2:
            st.metric("Delivery Rate", "98%")
        with col3:
            st.metric("Average Open Rate", "88%")
        with col4:
            st.metric("Click Rate", "42%")
    
    def _test_email_config(self, smtp_server: str, smtp_port: int, email_user: str, email_password: str) -> bool:
        """Test email configuration"""
        try:
            import smtplib
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(email_user, email_password)
            server.quit()
            return True
        except Exception:
            return False
    
    def _send_test_email(self, test_email: str, email_type: str, html_content: str) -> bool:
        """Send test email"""
        try:
            subject = f"Test {email_type} from AI Agent Prospera"
            return self.email_system.send_email(test_email, subject, html_content)
        except Exception:
            return False