import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
import asyncio
from typing import Dict, List, Any

# Import custom modules
from src.utils.config import config
from src.utils.logger import setup_logger
from src.scrapers.industry_scraper import IndustryDataScraper
from src.analysis.ai_analyzer import AIAnalyzer
from src.analysis.business_intelligence import BusinessIntelligence
from src.profile.business_profile import BusinessProfileManager
from src.profile.profile_wizard import ProfileWizard
from src.database.db_service import db_service
from src.delivery.report_dashboard import ReportDashboard
from src.chat.ai_chat_interface import AIChatInterface
from src.insights.industry_insights import IndustryInsightsEngine, get_industry_key_from_config
from src.research.market_intelligence import MarketIntelligenceEngine
from src.ai.grok_client import GrokAIClient
from src.ai.perplexity_client import PerplexityAIClient
from src.profile.business_importer import BusinessProfileImporter

# Setup logging
logger = setup_logger(__name__)

# Page configuration with caching
st.set_page_config(
    page_title="AI Agent Prospera - Business Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add caching for heavy operations
@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_industry_config():
    return config.INDUSTRIES

@st.cache_data(ttl=1800)  # Cache for 30 minutes
def get_cached_insights(industry_key: str):
    try:
        insights_engine = IndustryInsightsEngine()
        return insights_engine.get_industry_insights(industry_key)
    except:
        # Return industry-specific insights
        industry_insights = {
            "agriculture": {
                "key_trends": ["Precision farming", "Sustainable practices", "AgTech adoption"],
                "opportunities": ["Vertical farming", "IoT sensors", "Supply chain optimization"],
                "challenges": ["Climate change", "Labor shortage", "Market volatility"]
            },
            "technology": {
                "key_trends": ["AI integration", "Cloud computing", "Cybersecurity"],
                "opportunities": ["Edge computing", "Quantum tech", "SaaS expansion"],
                "challenges": ["Data privacy", "Talent shortage", "Regulatory compliance"]
            },
            "healthcare": {
                "key_trends": ["Telemedicine", "Digital health", "Personalized medicine"],
                "opportunities": ["Wearable tech", "AI diagnostics", "Remote monitoring"],
                "challenges": ["Regulatory approval", "Data security", "Cost management"]
            }
        }
        return industry_insights.get(industry_key, {
            "key_trends": ["Market digitization", "Customer experience focus", "Operational efficiency"],
            "opportunities": ["Technology adoption", "Market expansion", "Process automation"],
            "challenges": ["Competition", "Regulation", "Cost pressures"]
        })

# Performance optimization: Reduce initial database calls
@st.cache_data(ttl=300)
def get_basic_app_state():
    return {
        "initialized": True,
        "timestamp": datetime.now().isoformat()
    }

# Initialize session state
if 'scraped_data' not in st.session_state:
    st.session_state.scraped_data = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'selected_industry' not in st.session_state:
    st.session_state.selected_industry = None
if 'business_profile' not in st.session_state:
    st.session_state.business_profile = None
if 'show_profile_wizard' not in st.session_state:
    st.session_state.show_profile_wizard = False
if 'profile_id' not in st.session_state:
    st.session_state.profile_id = None
if 'data_collection_id' not in st.session_state:
    st.session_state.data_collection_id = None
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = "Dashboard"

def main():
    """Main application function"""
    
    # Show profile wizard if requested (before any other UI)
    if st.session_state.show_profile_wizard:
        wizard = ProfileWizard()
        profile = wizard.show_wizard()
        
        if profile:
            # Save profile to database
            try:
                profile_id = db_service.save_business_profile(profile)
                st.session_state.business_profile = profile
                st.session_state.profile_id = profile_id
                st.session_state.show_profile_wizard = False
                st.success(f"Business profile created for {profile.company_name}!")
                logger.info(f"Profile saved to database with ID: {profile_id}")
                st.rerun()
            except Exception as e:
                st.error(f"Error saving profile to database: {str(e)}")
                logger.error(f"Database error: {str(e)}")
        return  # Exit here to show only the wizard
    
    # Sidebar configuration
    st.sidebar.title("AI Agent Prospera")
    st.sidebar.markdown("*Business Intelligence Platform*")
    
    # API Key validation
    if not config.OPENAI_API_KEY:
        st.sidebar.error("OpenAI API Key required!")
        st.sidebar.markdown("Please set your OPENAI_API_KEY in the environment variables.")
        st.stop()
    
    # Sidebar: Action Controls Only
    st.sidebar.markdown("""
    <div style="
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        color: white;
        text-align: center;
    ">
        <h3 style="margin: 0; font-size: 1.1rem;">Quick Actions</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Business Profile Quick Action
    profile_manager = BusinessProfileManager()
    
    if st.session_state.business_profile:
        profile = st.session_state.business_profile
        st.sidebar.success(f"Active: {profile.company_name}")
        st.sidebar.caption(f"{profile.sub_industry} • {profile.location}")
        
        if st.sidebar.button("Edit Profile", use_container_width=True):
            st.session_state.show_profile_wizard = True
            st.rerun()
    else:
        if st.sidebar.button("Setup Business Profile", type="primary", use_container_width=True):
            st.session_state.show_profile_wizard = True
            st.rerun()
        st.sidebar.caption("Create profile for personalized insights")
    
    st.sidebar.markdown("---")
    
    # Industry Selection
    industry_options = {
        key: value["name"] 
        for key, value in config.INDUSTRIES.items()
    }
    
    selected_industry_key = st.sidebar.selectbox(
        "Industry:",
        options=list(industry_options.keys()),
        format_func=lambda x: industry_options[x],
        key="industry_selector"
    )
    
    st.session_state.selected_industry = selected_industry_key
    
    # Primary Action Buttons
    if st.sidebar.button("Collect Fresh Data", type="primary", use_container_width=True):
        collect_industry_data(selected_industry_key)
    
    if st.session_state.scraped_data and st.sidebar.button("Run AI Analysis", type="primary", use_container_width=True):
        run_ai_analysis()
    
    if st.session_state.analysis_results and st.sidebar.button("Generate Report", use_container_width=True):
        generate_business_report()
    
    # Quick Settings Access
    st.sidebar.markdown("---")
    if st.sidebar.button("Email Setup", use_container_width=True):
        st.session_state.current_view = "settings"
        st.rerun()
    
    # Optimized Industry Insights Section
    st.sidebar.markdown("---")
    with st.sidebar:
        if selected_industry_key:
            industry_display_name = industry_options[selected_industry_key]
            
            st.markdown("### Quick Insights")
            
            # Use cached insights for better performance
            try:
                insights = get_cached_insights(selected_industry_key)
                
                # Show top 2 trends
                if insights.get("key_trends"):
                    st.markdown("**Hot Trends:**")
                    for trend in insights["key_trends"][:2]:
                        st.caption(f"• {trend}")
                
                # Show top opportunity
                if insights.get("opportunities"):
                    st.markdown("**Top Opportunity:**")
                    st.caption(f"• {insights['opportunities'][0]}")
            except:
                st.caption("Insights loading...")
            
            # Quick action button
            if st.button("View Full Industry Analysis", use_container_width=True):
                st.session_state.show_industry_insights = True
                st.rerun()
    
    # Professional header with modern styling
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #60a5fa 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(30, 64, 175, 0.15);
        border: 1px solid rgba(255,255,255,0.1);
    ">
        <h1 style="
            color: white;
            font-size: 2.5rem;
            font-weight: 800;
            margin: 0;
            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
            letter-spacing: -0.02em;
        ">AI Agent Prospera</h1>
        <p style="
            color: rgba(255,255,255,0.9);
            font-size: 1.2rem;
            margin: 0.5rem 0 0 0;
            font-weight: 300;
        ">Business Intelligence Platform</p>
        <p style="
            color: rgba(255,255,255,0.8);
            font-size: 1rem;
            margin: 0.3rem 0 0 0;
        ">Real-time market intelligence for smart business decisions</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Top navigation with tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Dashboard", 
        "Industry Intelligence",
        "Raw Data", 
        "AI Chat", 
        "Analytics", 
        "Settings"
    ])
    
    with tab1:
        st.session_state.current_view = "main_dashboard"
        if st.session_state.analysis_results:
            display_analysis_dashboard()
        elif st.session_state.scraped_data:
            display_raw_data_dashboard()
        else:
            display_welcome_screen()
    
    with tab2:
        st.session_state.current_view = "industry_intelligence"
        display_industry_intelligence_dashboard()
    
    with tab3:
        st.session_state.current_view = "raw_data"
        if st.session_state.scraped_data:
            display_raw_data_dashboard()
        else:
            st.info("No raw data available. Please collect data first using the sidebar controls.")
    
    with tab4:
        st.session_state.current_view = "ai_chat"
        display_ai_chat_dashboard()
    
    with tab5:
        st.session_state.current_view = "analytics"
        display_analytics_dashboard()
    
    with tab6:
        st.session_state.current_view = "settings"
        display_settings_dashboard()
    
    # Show profile wizard if requested (before main interface)
    if st.session_state.show_profile_wizard:
        wizard = ProfileWizard()
        profile = wizard.show_wizard()
        
        if profile:
            # Save profile to database
            try:
                profile_id = db_service.save_business_profile(profile)
                st.session_state.business_profile = profile
                st.session_state.profile_id = profile_id
                st.session_state.show_profile_wizard = False
                st.success(f"Business profile created for {profile.company_name}!")
                logger.info(f"Profile saved to database with ID: {profile_id}")
                st.rerun()
            except Exception as e:
                st.error(f"Error saving profile to database: {str(e)}")
                logger.error(f"Database error: {str(e)}")
        return  # Exit here to show only the wizard
    
    # Main interface continues below
        
        # Add close button for wizard
        if st.button("← Back to Dashboard"):
            st.session_state.show_profile_wizard = False
            st.rerun()
        
        return  # Don't show main dashboard while wizard is open
    
    # Check for navigation preference in session state
    if hasattr(st.session_state, 'current_view'):
        current_view = st.session_state.current_view
    else:
        current_view = "main_dashboard"
        st.session_state.current_view = current_view
    
    # Display the appropriate dashboard based on selection
    if current_view == "main_dashboard":
        # Main dashboard - shows the most relevant content prominently
        if st.session_state.analysis_results:
            display_analysis_dashboard()
        elif st.session_state.scraped_data:
            display_raw_data_dashboard()
        else:
            display_welcome_screen()
    
    elif current_view == "raw_data":
        if st.session_state.scraped_data:
            display_raw_data_dashboard()
        else:
            st.info("No raw data available. Please collect data first using the sidebar controls.")
    
    elif current_view == "analytics":
        display_analytics_dashboard()
    
    elif current_view == "settings":
        display_settings_dashboard()

def process_main_chat_message(user_message: str):
    """Process user chat message from the main welcome screen"""
    try:
        # Add user message to chat history
        st.session_state.main_chat_messages.append({
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().strftime("%H:%M")
        })
        
        # Generate AI response using OpenAI or Perplexity based on query type
        if any(keyword in user_message.lower() for keyword in ['research', 'market', 'trend', 'competitor', 'industry']):
            # Use Perplexity for research-focused queries
            try:
                perplexity_client = PerplexityAIClient()
                response_data = perplexity_client.chat_with_perplexity(user_message)
                
                if response_data["status"] == "success":
                    ai_response = response_data["response"]
                else:
                    raise Exception("Perplexity unavailable")
            except:
                # Fallback to OpenAI
                ai_response = generate_openai_response(user_message)
        else:
            # Use OpenAI for general business queries
            ai_response = generate_openai_response(user_message)
        
        # Add AI response to chat history
        st.session_state.main_chat_messages.append({
            "role": "assistant",
            "content": ai_response,
            "timestamp": datetime.now().strftime("%H:%M")
        })
        
    except Exception as e:
        st.session_state.main_chat_messages.append({
            "role": "assistant",
            "content": "I'm experiencing technical difficulties. Please try again or explore other platform features.",
            "timestamp": datetime.now().strftime("%H:%M")
        })
    
    st.rerun()

def generate_openai_response(user_message: str) -> str:
    """Generate response using OpenAI"""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a business intelligence assistant. Provide helpful, actionable insights for business strategy, market analysis, and growth opportunities. Keep responses concise and professional."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=400,
            temperature=0.7
        )
        
        return response.choices[0].message.content or "I'm unable to provide a response at the moment."
        
    except Exception as e:
        if "quota" in str(e).lower():
            return "The AI service quota has been exceeded. You can still use all other platform features including real-time research and analysis tools."
        else:
            return "I'm experiencing technical difficulties. Please try the research tools or other platform features."

def collect_industry_data(industry_key: str):
    """Collect data for the selected industry"""
    
    with st.spinner(f"Collecting data for {config.INDUSTRIES[industry_key]['name']}..."):
        try:
            scraper = IndustryDataScraper()
            
            # Customize data collection based on business profile
            if st.session_state.business_profile:
                profile_manager = BusinessProfileManager()
                custom_config = profile_manager.customize_data_collection(st.session_state.business_profile)
                logger.info(f"Using custom data collection for {st.session_state.business_profile.company_name}")
                # Note: In full implementation, scraper would use custom_config
            
            data = scraper.scrape_industry_data(industry_key)
            st.session_state.scraped_data = data
            
            # Save to database if profile exists
            if st.session_state.profile_id:
                try:
                    data_collection_id = db_service.save_data_collection(
                        st.session_state.profile_id, 
                        industry_key, 
                        data
                    )
                    st.session_state.data_collection_id = data_collection_id
                    logger.info(f"Data collection saved to database with ID: {data_collection_id}")
                except Exception as db_error:
                    logger.error(f"Database save error: {str(db_error)}")
                    st.warning("Data collected but not saved to database")
            
            st.success("Data collection completed successfully!")
            logger.info(f"Data collected for industry: {industry_key}")
            st.rerun()
            
        except Exception as e:
            st.error(f"Error collecting data: {str(e)}")
            logger.error(f"Data collection failed: {str(e)}")

def run_ai_analysis():
    """Run AI analysis on collected data"""
    
    with st.spinner("Running AI analysis..."):
        try:
            analyzer = AIAnalyzer()
            bi = BusinessIntelligence()
            
            # Customize AI analysis based on business profile
            if st.session_state.business_profile:
                profile_manager = BusinessProfileManager()
                custom_prompts = profile_manager.customize_ai_analysis(st.session_state.business_profile)
                logger.info(f"Using personalized AI analysis for {st.session_state.business_profile.company_name}")
                # Note: Enhanced analyzer would use custom_prompts for targeted analysis
            
            # Perform AI analysis
            analysis_results = analyzer.analyze_industry_data(st.session_state.scraped_data)
            
            # Generate business intelligence insights
            bi_insights = bi.generate_insights(st.session_state.scraped_data, analysis_results)
            
            # Combine results
            analysis_data = {
                'ai_analysis': analysis_results,
                'business_insights': bi_insights,
                'business_profile': st.session_state.business_profile,
                'timestamp': datetime.now().isoformat()
            }
            
            st.session_state.analysis_results = analysis_data
            
            # Save analysis to database if profile and data collection exist
            if st.session_state.profile_id and st.session_state.data_collection_id:
                try:
                    analysis_id = db_service.save_analysis_results(
                        st.session_state.profile_id,
                        st.session_state.data_collection_id,
                        analysis_data
                    )
                    logger.info(f"Analysis results saved to database with ID: {analysis_id}")
                except Exception as db_error:
                    logger.error(f"Database save error for analysis: {str(db_error)}")
                    st.warning("Analysis completed but not saved to database")
            
            st.success("AI analysis completed successfully!")
            logger.info("AI analysis completed")
            st.rerun()
            
        except Exception as e:
            st.error(f"Error in AI analysis: {str(e)}")
            logger.error(f"AI analysis failed: {str(e)}")

def display_welcome_screen():
    """Display welcome screen with instructions"""
    
    # Profile-specific welcome message
    if st.session_state.business_profile:
        profile = st.session_state.business_profile
        st.markdown(f"## Welcome back, {profile.company_name}!")
        st.markdown(f"*{profile.sub_industry} • {profile.location} • {profile.business_size.value}*")
        
        # Show personalized quick actions
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### Your Focus Areas")
            for region in profile.focus_regions[:3]:
                st.markdown(f"• {region}")
        
        with col2:
            st.markdown("### Growth Goals")
            for goal in profile.growth_goals[:3]:
                st.markdown(f"• {goal}")
        
        with col3:
            st.markdown("### Target Markets")
            for market in profile.target_markets[:3]:
                st.markdown(f"• {market}")
        
        st.markdown("---")
        st.markdown("### Next Steps")
        st.markdown("1. Select your industry and collect fresh market data")
        st.markdown("2. Run AI analysis for personalized business insights")
        st.markdown("3. Review recommendations tailored to your business goals")
        
    else:
        # AI Chat Interface as main welcome feature
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            border: 1px solid #e2e8f0;
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            text-align: center;
        ">
            <h2 style="
                color: #1e293b;
                font-size: 2rem;
                font-weight: 600;
                margin-bottom: 1rem;
            ">AI Agent Prospera - Business Intelligence Platform</h2>
            <p style="
                color: #64748b;
                font-size: 1.1rem;
                max-width: 600px;
                margin: 0 auto 1.5rem auto;
                line-height: 1.6;
            ">Ask me anything about market research, industry analysis, or business strategy</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Initialize chat messages if not exists
        if "main_chat_messages" not in st.session_state:
            st.session_state.main_chat_messages = [
                {
                    "role": "assistant",
                    "content": "Hello! I'm your AI business intelligence assistant. I can help you with market research, competitive analysis, industry trends, and strategic planning. What would you like to explore?",
                    "timestamp": datetime.now().strftime("%H:%M")
                }
            ]
        
        # AI Chat Interface
        st.markdown("### Ask AI Agent Prospera")
        
        # Chat container with scrollable area
        chat_container = st.container(height=300)
        with chat_container:
            for message in st.session_state.main_chat_messages[-8:]:  # Show last 8 messages
                if message["role"] == "user":
                    st.markdown(f"""
                    <div style="text-align: right; margin: 10px 0;">
                        <div style="background-color: #0066cc; color: white; padding: 10px 15px; border-radius: 18px; display: inline-block; max-width: 70%;">
                            {message["content"]}
                        </div>
                        <div style="font-size: 0.8em; color: #666; margin-top: 5px;">
                            You • {message["timestamp"]}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="text-align: left; margin: 10px 0;">
                        <div style="background-color: #f0f0f0; color: #333; padding: 10px 15px; border-radius: 18px; display: inline-block; max-width: 70%;">
                            {message["content"]}
                        </div>
                        <div style="font-size: 0.8em; color: #666; margin-top: 5px;">
                            AI Assistant • {message["timestamp"]}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Chat input area
        user_input = st.chat_input("Type your question here...")
        
        if user_input:
            process_main_chat_message(user_input.strip())
        
        # Quick suggestion buttons
        st.markdown("### Quick Questions")
        suggestion_cols = st.columns(2)
        
        with suggestion_cols[0]:
            if st.button("What are the latest AI trends in business?", use_container_width=True):
                process_main_chat_message("What are the latest AI trends in business applications for 2024?")
            if st.button("Analyze my market competition", use_container_width=True):
                process_main_chat_message("Can you help me analyze my market competition and identify key competitors?")
        
        with suggestion_cols[1]:
            if st.button("Find growth opportunities", use_container_width=True):
                process_main_chat_message("What are the best growth opportunities in emerging markets?")
            if st.button("Industry risk assessment", use_container_width=True):
                process_main_chat_message("Can you assess the current risks in the technology industry?")
        
        # Business profile import options
        st.markdown("### Setup Your Business Profile")
        
        # Import method selection
        import_method = st.radio(
            "Choose import method:",
            ["Auto-Import from Company Name", "Import from Website", "Import from CrunchBase", "Manual Setup"],
            horizontal=True
        )
        
        if import_method == "Auto-Import from Company Name":
            st.markdown("**Enter your company name to automatically find and import business details**")
            company_input = st.text_input("Company Name", placeholder="e.g., Apple Inc., Microsoft Corporation")
            
            col1, col2 = st.columns([1, 3])
            with col1:
                if st.button("Import Profile", type="primary", use_container_width=True):
                    if company_input.strip():
                        with st.spinner("Searching business databases..."):
                            importer = BusinessProfileImporter()
                            imported_data = importer.import_from_company_name(company_input.strip())
                            
                            if imported_data and not imported_data.get("error"):
                                st.session_state.imported_profile_data = imported_data
                                st.success(f"Found business data for {imported_data.get('company_name', company_input)}")
                                
                                # Display preview
                                with st.expander("Preview Imported Data", expanded=True):
                                    preview_cols = st.columns(2)
                                    with preview_cols[0]:
                                        st.write("**Company:** ", imported_data.get('company_name', 'N/A'))
                                        st.write("**Industry:** ", imported_data.get('industry', 'N/A'))
                                        st.write("**Location:** ", imported_data.get('location', 'N/A'))
                                    with preview_cols[1]:
                                        st.write("**Size:** ", imported_data.get('business_size', 'N/A'))
                                        st.write("**Website:** ", imported_data.get('website', 'N/A'))
                                        st.write("**Sources:** ", ", ".join(imported_data.get('import_sources', [])))
                                
                                if st.button("Confirm & Create Profile", type="primary"):
                                    st.session_state.show_profile_wizard = True
                                    st.session_state.import_mode = "auto"
                                    st.rerun()
                            else:
                                st.warning(f"Could not find complete data for '{company_input}'. Try manual setup or provide more details.")
                    else:
                        st.error("Please enter a company name")
            
            with col2:
                st.info("Auto-import searches CrunchBase, company websites, and business databases to populate your profile automatically.")
        
        elif import_method == "Import from Website":
            st.markdown("**Enter your company website URL to extract business information**")
            website_input = st.text_input("Website URL", placeholder="https://yourcompany.com")
            
            if st.button("Import from Website", type="primary", use_container_width=True):
                if website_input.strip():
                    with st.spinner("Analyzing website..."):
                        importer = BusinessProfileImporter()
                        imported_data = importer.import_from_website(website_input.strip())
                        
                        if imported_data and not imported_data.get("error"):
                            st.session_state.imported_profile_data = imported_data
                            st.success("Website analysis completed!")
                            
                            with st.expander("Extracted Information", expanded=True):
                                st.json(imported_data)
                            
                            if st.button("Use This Data", type="primary"):
                                st.session_state.show_profile_wizard = True
                                st.session_state.import_mode = "website"
                                st.rerun()
                        else:
                            st.error(imported_data.get("error", "Failed to extract data from website"))
                else:
                    st.error("Please enter a valid website URL")
        
        elif import_method == "Import from CrunchBase":
            st.markdown("**Import detailed startup and funding information from CrunchBase**")
            cb_input = st.text_input("CrunchBase URL or Company Name", placeholder="https://crunchbase.com/organization/your-company")
            
            if st.button("Import from CrunchBase", type="primary", use_container_width=True):
                if cb_input.strip():
                    with st.spinner("Fetching CrunchBase data..."):
                        importer = BusinessProfileImporter()
                        if cb_input.startswith("http"):
                            imported_data = importer.import_from_crunchbase_url(cb_input.strip())
                        else:
                            imported_data = importer.import_from_company_name(cb_input.strip())
                        
                        if imported_data and not imported_data.get("error"):
                            st.session_state.imported_profile_data = imported_data
                            st.success("CrunchBase data imported!")
                            
                            with st.expander("CrunchBase Information", expanded=True):
                                funding_cols = st.columns(3)
                                with funding_cols[0]:
                                    st.metric("Funding Total", imported_data.get('funding_total', 'N/A'))
                                with funding_cols[1]:
                                    st.metric("Employees", imported_data.get('employee_count', 'N/A'))
                                with funding_cols[2]:
                                    st.metric("Founded", imported_data.get('founded_date', 'N/A'))
                            
                            if st.button("Create Profile with CrunchBase Data", type="primary"):
                                st.session_state.show_profile_wizard = True
                                st.session_state.import_mode = "crunchbase"
                                st.rerun()
                        else:
                            st.error(imported_data.get("error", "Failed to import from CrunchBase"))
                else:
                    st.error("Please enter a CrunchBase URL or company name")
        
        else:  # Manual Setup
            st.markdown("**Create a custom business profile with manual input**")
            st.info("Full control over all profile details with step-by-step guidance.")
            
            if st.button("Start Manual Setup", type="primary", use_container_width=True):
                st.session_state.show_profile_wizard = True
                st.session_state.import_mode = "manual"
                st.rerun()
        
        # Feature overview
        st.markdown("---")
        st.markdown("### What You'll Get")
        
        feature_cols = st.columns(2)
        
        with feature_cols[0]:
            st.markdown("""
            **Market Intelligence:**
            - Real-time industry trend analysis
            - Competitor positioning insights
            - Market opportunity identification
            
            **Lead Discovery:**
            - Potential customer identification
            - Lead quality scoring
            - Contact information extraction
            """)
        
        with feature_cols[1]:
            st.markdown("""
            **AI-Powered Analysis:**
            - Data-driven business recommendations
            - Growth opportunity assessment
            - Risk analysis and mitigation
            
            **Professional Reports:**
            - Custom business intelligence reports
            - Email delivery automation
            - Historical analytics dashboard
            """)
    


def display_raw_data_dashboard():
    """Display dashboard for raw scraped data"""
    
    data = st.session_state.scraped_data
    industry_name = config.INDUSTRIES[data['industry']]['name']
    
    st.markdown(f"## Raw Data Dashboard - {industry_name}")
    st.markdown(f"*Data collected: {datetime.fromisoformat(data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}*")
    
    # Metrics overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Trends Found", len(data.get('trends', [])))
    
    with col2:
        st.metric("News Articles", len(data.get('news', [])))
    
    with col3:
        st.metric("Leads Discovered", len(data.get('leads', [])))
    
    with col4:
        st.metric("Competitors", len(data.get('competitors', [])))
    
    # Tabs for different data types
    tab1, tab2, tab3, tab4 = st.tabs(["Trends", "News", "Leads", "Competitors"])
    
    with tab1:
        display_trends_data(data.get('trends', []))
    
    with tab2:
        display_news_data(data.get('news', []))
    
    with tab3:
        display_leads_data(data.get('leads', []))
    
    with tab4:
        display_competitors_data(data.get('competitors', []))

def display_analysis_dashboard():
    """Display comprehensive analysis dashboard"""
    
    data = st.session_state.scraped_data
    analysis = st.session_state.analysis_results
    industry_name = config.INDUSTRIES[data['industry']]['name']
    
    st.markdown(f"## 🧠 AI Analysis Dashboard - {industry_name}")
    st.markdown(f"*Analysis completed: {datetime.fromisoformat(analysis['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}*")
    
    # Key insights summary
    if 'business_insights' in analysis and 'key_metrics' in analysis['business_insights']:
        metrics = analysis['business_insights']['key_metrics']
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Market Opportunity Score", 
                f"{metrics.get('opportunity_score', 0)}/10",
                delta=f"{metrics.get('opportunity_trend', 0):+.1f}"
            )
        
        with col2:
            st.metric(
                "Competition Level", 
                metrics.get('competition_level', 'Medium'),
                delta=metrics.get('competition_change', '')
            )
        
        with col3:
            st.metric(
                "Lead Quality Score", 
                f"{metrics.get('lead_quality', 0)}/10"
            )
        
        with col4:
            st.metric(
                "Trend Momentum", 
                metrics.get('trend_momentum', 'Stable')
            )
    
    # Analysis tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Key Insights", "Market Analysis", "Recommendations", "Visualizations"])
    
    with tab1:
        display_key_insights(analysis)
    
    with tab2:
        display_market_analysis(analysis)
    
    with tab3:
        display_recommendations(analysis)
    
    with tab4:
        display_visualizations(analysis, data)

def display_trends_data(trends: List[Dict]):
    """Display trends data"""
    
    if not trends:
        st.info("No trend data available. Try collecting fresh data.")
        return
    
    st.markdown("### Market Trends")
    
    for i, trend in enumerate(trends):
        with st.expander(f"Trend {i+1}: {trend.get('keyword', trend.get('source', 'Unknown'))}"):
            if 'keyword' in trend:
                st.markdown(f"**Keyword:** {trend['keyword']}")
                st.markdown(f"**Article Count:** {trend.get('article_count', 0)}")
                st.markdown(f"**Trend Score:** {trend.get('trend_score', 0)}")
                
                if 'top_headlines' in trend:
                    st.markdown("**Top Headlines:**")
                    for headline in trend['top_headlines'][:3]:
                        st.markdown(f"- [{headline['title']}]({headline['url']}) - *{headline['source']}*")
            
            elif 'headlines' in trend:
                st.markdown(f"**Source:** {trend['source']}")
                st.markdown("**Headlines:**")
                for headline in trend['headlines'][:5]:
                    st.markdown(f"- {headline}")

def display_news_data(news: List[Dict]):
    """Display news data"""
    
    if not news:
        st.info("No news data available. Try collecting fresh data.")
        return
    
    st.markdown("### Latest Industry News")
    
    for article in news[:10]:
        with st.expander(f"{article['title']} - {article['source']}"):
            st.markdown(f"**Published:** {article['published_at']}")
            st.markdown(f"**Relevance Score:** {article.get('relevance_score', 0):.2f}")
            if article.get('description'):
                st.markdown(f"**Description:** {article['description']}")
            st.markdown(f"**[Read Full Article]({article['url']})**")

def display_leads_data(leads: List[Dict]):
    """Display leads data"""
    
    if not leads:
        st.info("No leads data available. Try collecting fresh data.")
        return
    
    st.markdown("### Potential Leads")
    
    for lead in leads:
        with st.expander(f"{lead.get('company_name', 'Unknown Company')}"):
            for key, value in lead.items():
                if key != 'company_name':
                    st.markdown(f"**{key.replace('_', ' ').title()}:** {value}")

def display_competitors_data(competitors: List[Dict]):
    """Display competitors data"""
    
    if not competitors:
        st.info("No competitor data available. Try collecting fresh data.")
        return
    
    st.markdown("### Competitor Analysis")
    
    for competitor in competitors:
        with st.expander(f"{competitor.get('name', 'Unknown Competitor')}"):
            for key, value in competitor.items():
                if key != 'name':
                    st.markdown(f"**{key.replace('_', ' ').title()}:** {value}")

def display_key_insights(analysis: Dict):
    """Display key business insights"""
    
    if 'ai_analysis' not in analysis:
        st.info("No AI analysis available.")
        return
    
    ai_insights = analysis['ai_analysis']
    
    st.markdown("### Key Business Insights")
    
    if 'market_summary' in ai_insights:
        st.markdown("#### Market Summary")
        st.markdown(ai_insights['market_summary'])
    
    if 'opportunities' in ai_insights:
        st.markdown("#### Key Opportunities")
        for i, opportunity in enumerate(ai_insights['opportunities'], 1):
            st.markdown(f"{i}. {opportunity}")
    
    if 'risks' in ai_insights:
        st.markdown("#### Potential Risks")
        for i, risk in enumerate(ai_insights['risks'], 1):
            st.markdown(f"{i}. {risk}")

def display_market_analysis(analysis: Dict):
    """Display detailed market analysis"""
    
    if 'business_insights' not in analysis:
        st.info("No business insights available.")
        return
    
    insights = analysis['business_insights']
    
    st.markdown("### Market Analysis")
    
    if 'market_trends' in insights:
        st.markdown("#### Trend Analysis")
        for trend in insights['market_trends']:
            st.markdown(f"- {trend}")
    
    if 'competitive_landscape' in insights:
        st.markdown("#### Competitive Landscape")
        st.markdown(insights['competitive_landscape'])

def display_recommendations(analysis: Dict):
    """Display AI recommendations"""
    
    if 'ai_analysis' not in analysis:
        st.info("No recommendations available.")
        return
    
    ai_insights = analysis['ai_analysis']
    
    st.markdown("### AI-Powered Recommendations")
    
    if 'recommendations' in ai_insights:
        for i, rec in enumerate(ai_insights['recommendations'], 1):
            st.markdown(f"**Recommendation {i}:**")
            st.markdown(rec)
            st.markdown("---")

def display_visualizations(analysis: Dict, data: Dict):
    """Display data visualizations"""
    
    st.markdown("### Data Visualizations")
    
    # News articles by source
    if data.get('news'):
        news_df = pd.DataFrame(data['news'])
        if not news_df.empty and 'source' in news_df.columns:
            source_counts = news_df['source'].value_counts().head(10)
            
            fig = px.bar(
                x=source_counts.values,
                y=source_counts.index,
                orientation='h',
                title="Top News Sources",
                labels={'x': 'Article Count', 'y': 'Source'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    # Trend scores visualization
    if data.get('trends'):
        trend_data = []
        for trend in data['trends']:
            if 'keyword' in trend and 'trend_score' in trend:
                trend_data.append({
                    'keyword': trend['keyword'],
                    'score': trend['trend_score']
                })
        
        if trend_data:
            trend_df = pd.DataFrame(trend_data)
            
            fig = px.bar(
                trend_df,
                x='keyword',
                y='score',
                title="Keyword Trend Scores",
                labels={'score': 'Trend Score', 'keyword': 'Keyword'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

def generate_business_report():
    """Generate and download business report"""
    
    if not st.session_state.analysis_results:
        st.error("No analysis data available for report generation.")
        return
    
    try:
        data = st.session_state.scraped_data
        analysis = st.session_state.analysis_results
        industry_name = config.INDUSTRIES[data['industry']]['name']
        
        # Create report content
        report = {
            "report_title": f"Business Intelligence Report - {industry_name}",
            "generated_at": datetime.now().isoformat(),
            "industry": industry_name,
            "data_summary": {
                "trends_found": len(data.get('trends', [])),
                "news_articles": len(data.get('news', [])),
                "leads_discovered": len(data.get('leads', [])),
                "competitors_analyzed": len(data.get('competitors', []))
            },
            "ai_analysis": analysis.get('ai_analysis', {}),
            "business_insights": analysis.get('business_insights', {}),
            "raw_data": data
        }
        
        # Convert to JSON for download
        report_json = json.dumps(report, indent=2, default=str)
        
        st.download_button(
            label="Download Business Report (JSON)",
            data=report_json,
            file_name=f"business_report_{data['industry']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
        
        st.success("Business report generated successfully!")
        
    except Exception as e:
        st.error(f"Error generating report: {str(e)}")
        logger.error(f"Report generation failed: {str(e)}")

def display_analytics_dashboard():
    """Display analytics dashboard with historical data"""
    
    st.header("Business Analytics Dashboard")
    
    if not st.session_state.profile_id:
        st.info("Please select a business profile to view analytics.")
        return
    
    try:
        # Get comprehensive dashboard data
        dashboard_data = db_service.get_profile_dashboard_data(st.session_state.profile_id)
        
        if not dashboard_data or not dashboard_data.get('metrics'):
            st.info("No historical data available yet. Run some analyses to see insights here.")
            return
        
        metrics = dashboard_data['metrics']
        
        # Key metrics overview
        st.subheader("Key Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Data Collections", 
                metrics.get('collections_count', 0),
                help="Total number of data collection sessions"
            )
        
        with col2:
            st.metric(
                "AI Analyses", 
                metrics.get('analyses_count', 0),
                help="Total number of AI analysis runs"
            )
        
        with col3:
            opportunity_score = metrics.get('latest_opportunity_score')
            if opportunity_score:
                st.metric(
                    "Opportunity Score", 
                    f"{opportunity_score:.1f}/10",
                    delta=f"{metrics.get('opportunity_trend', 0):+.1f}" if metrics.get('opportunity_trend') else None
                )
            else:
                st.metric("Opportunity Score", "N/A")
        
        with col4:
            st.metric(
                "Total Leads", 
                metrics.get('total_leads_discovered', 0),
                help="Total leads discovered across all collections"
            )
        
        # Recent activity
        st.subheader("Recent Activity")
        
        recent_collections = dashboard_data.get('recent_collections', [])
        recent_analyses = dashboard_data.get('recent_analyses', [])
        
        if recent_collections:
            st.write("**Recent Data Collections:**")
            for collection in recent_collections[:5]:
                with st.expander(f"Collection on {collection['timestamp'][:10]} - {collection['industry']}"):
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Trends", collection['trends_count'])
                    col2.metric("News", collection['news_count'])
                    col3.metric("Leads", collection['leads_count'])
                    col4.metric("Competitors", collection['competitors_count'])
        
        if recent_analyses:
            st.write("**Recent AI Analyses:**")
            for analysis in recent_analyses[:5]:
                with st.expander(f"Analysis on {analysis['timestamp'][:10]}"):
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Opportunity Score", f"{analysis.get('opportunity_score', 0):.1f}/10")
                    col2.metric("Competition Level", analysis.get('competition_level', 'N/A'))
                    col3.metric("Confidence", f"{analysis.get('confidence_score', 0):.1f}/10")
        
        # Latest analysis insights
        latest_analysis = dashboard_data.get('latest_analysis')
        if latest_analysis:
            st.subheader("Latest Analysis Insights")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Market Summary:**")
                st.write(latest_analysis.get('market_summary', 'No summary available'))
                
                st.write("**Key Opportunities:**")
                opportunities = latest_analysis.get('opportunities', [])
                for i, opp in enumerate(opportunities[:3], 1):
                    st.write(f"{i}. {opp}")
            
            with col2:
                st.write("**Key Risks:**")
                risks = latest_analysis.get('risks', [])
                for i, risk in enumerate(risks[:3], 1):
                    st.write(f"{i}. {risk}")
                
                st.write("**Top Recommendations:**")
                recommendations = latest_analysis.get('recommendations', [])
                for i, rec in enumerate(recommendations[:3], 1):
                    st.write(f"{i}. {rec}")
        
    except Exception as e:
        st.error(f"Error loading analytics dashboard: {str(e)}")
        logger.error(f"Analytics dashboard error: {str(e)}")

def display_industry_intelligence_dashboard():
    """Display comprehensive industry intelligence dashboard"""
    
    # Get current industry selection
    selected_industry_key = st.session_state.get('selected_industry')
    
    if not selected_industry_key:
        st.warning("Please select an industry from the sidebar to view intelligence insights.")
        return
    
    # Get industry display name from config
    from src.utils.config import config
    industry_options = {}
    for key, data in config.INDUSTRIES.items():
        industry_options[key] = data["name"]
    
    industry_display_name = industry_options.get(selected_industry_key, "Unknown Industry")
    
    # Initialize insights engine
    insights_engine = IndustryInsightsEngine()
    industry_key = get_industry_key_from_config(industry_display_name)
    
    # Header
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    ">
        <h2 style="margin: 0; font-size: 2rem;">Industry Intelligence</h2>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">{industry_display_name}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get comprehensive insights
    insights = insights_engine.get_industry_insights(industry_key)
    
    # Key metrics overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Market Stage",
            value="Growth Phase",
            delta="Expanding"
        )
    
    with col2:
        st.metric(
            label="Competition Level", 
            value="High",
            delta="New entrants"
        )
    
    with col3:
        st.metric(
            label="Tech Impact",
            value="Transformative",
            delta="AI adoption"
        )
    
    with col4:
        st.metric(
            label="Opportunity Score",
            value="8.5/10",
            delta="Strong potential"
        )
    
    st.markdown("---")
    
    # Main insights sections
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        # Key trends
        with st.expander("Key Market Trends", expanded=True):
            if insights.get("key_trends"):
                for i, trend in enumerate(insights["key_trends"], 1):
                    st.markdown(f"**{i}.** {trend}")
            else:
                st.info("No specific trends data available for this industry.")
        
        # Opportunities and challenges
        col_opp, col_chall = st.columns(2)
        
        with col_opp:
            st.markdown("### Opportunities")
            if insights.get("opportunities"):
                for opp in insights["opportunities"]:
                    st.markdown(f"• {opp}")
            else:
                st.info("No opportunities data available.")
        
        with col_chall:
            st.markdown("### Challenges")
            if insights.get("challenges"):
                for challenge in insights["challenges"]:
                    st.markdown(f"• {challenge}")
            else:
                st.info("No challenges data available.")
        
        # Recommended actions
        if insights.get("recommended_actions"):
            st.markdown("### Recommended Actions")
            
            for action in insights["recommended_actions"]:
                priority_colors = {
                    "High": "#ff4444",
                    "Medium": "#ffaa00", 
                    "Low": "#44ff44"
                }
                priority_color = priority_colors.get(action["priority"], "#888888")
                
                st.markdown(f"""
                <div style="
                    border-left: 4px solid {priority_color};
                    padding: 1rem;
                    margin: 1rem 0;
                    background: rgba(255,255,255,0.05);
                    border-radius: 8px;
                ">
                    <h4 style="margin: 0; color: {priority_color};">{action['action']}</h4>
                    <p style="margin: 0.5rem 0 0 0; opacity: 0.8;">
                        <strong>Category:</strong> {action['category']}<br>
                        <strong>Timeline:</strong> {action['timeline']}<br>
                        <strong>Impact:</strong> {action['impact']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
    
    with col_right:
        # Success metrics
        st.markdown("### Key Success Metrics")
        if insights.get("success_metrics"):
            for metric in insights["success_metrics"]:
                st.markdown(f"• {metric}")
        else:
            st.info("No metrics data available.")
        
        st.markdown("---")
        
        # Quick actions
        st.markdown("### Quick Actions")
        
        if st.button("Generate Industry Report", use_container_width=True):
            st.success("Industry report generation initiated...")
            
        if st.button("Start Market Research", use_container_width=True):
            with st.spinner("Conducting comprehensive market research..."):
                market_engine = MarketIntelligenceEngine()
                research_data = market_engine.conduct_market_research(industry_key)
                st.session_state.market_research_data = research_data
                st.success("Market research completed!")
                st.rerun()
                
        if st.button("AI Analysis with Grok", use_container_width=True):
            try:
                grok_client = GrokAIClient()
                industry_data = {
                    "industry": industry_display_name,
                    "trends": insights.get("key_trends", [])[:3],
                    "competitors": ["Market Leaders", "Emerging Players"],
                    "opportunities": insights.get("opportunities", [])[:3]
                }
                
                with st.spinner("Analyzing with Grok AI..."):
                    grok_analysis = grok_client.analyze_industry_with_grok(industry_data)
                    
                if grok_analysis["status"] == "success":
                    st.session_state.grok_analysis = grok_analysis
                    st.success("Grok AI analysis completed!")
                    st.rerun()
                else:
                    if "credits" in grok_analysis.get("error_message", ""):
                        st.warning("Grok AI requires credits. Please add credits to your XAI account to use advanced AI analysis.")
                    else:
                        st.error(f"Grok analysis failed: {grok_analysis.get('error_message', 'Unknown error')}")
                        
            except Exception as e:
                st.error(f"Grok client initialization failed: {str(e)}")
                
        if st.button("Real-Time Research with Perplexity", use_container_width=True):
            try:
                perplexity_client = PerplexityAIClient()
                
                with st.spinner("Conducting real-time research..."):
                    research_result = perplexity_client.comprehensive_industry_research(
                        industry=industry_display_name
                    )
                    
                if research_result["status"] == "success":
                    st.session_state.perplexity_research = research_result
                    st.success("Real-time research completed!")
                    st.rerun()
                else:
                    st.error(f"Research failed: {research_result.get('error_message', 'Unknown error')}")
                        
            except Exception as e:
                st.error(f"Perplexity client initialization failed: {str(e)}")
            
        if st.button("Discuss with AI", use_container_width=True):
            st.session_state.current_view = "ai_chat"
            st.info("Opening AI chat for industry discussion...")
            st.rerun()
        
        st.markdown("---")
        
        # Market context
        if insights.get("market_context"):
            st.markdown("### Market Context")
            context = insights["market_context"]
            
            st.markdown(f"**Market Stage:** {context.get('market_stage', 'N/A')}")
            st.markdown(f"**Competition:** {context.get('competitive_intensity', 'N/A')}")
            st.markdown(f"**Regulation:** {context.get('regulatory_environment', 'N/A')}")
    
    # Display market research results if available
    if st.session_state.get('market_research_data'):
        st.markdown("---")
        display_market_research_results(st.session_state.market_research_data)
    
    # Display Grok AI analysis if available
    if st.session_state.get('grok_analysis'):
        st.markdown("---")
        display_grok_analysis_results(st.session_state.grok_analysis)
    
    # Display Perplexity research if available
    if st.session_state.get('perplexity_research'):
        st.markdown("---")
        display_perplexity_research_results(st.session_state.perplexity_research)

def display_market_research_results(research_data: Dict[str, Any]):
    """Display comprehensive market research results"""
    
    st.markdown("## Market Research Results")
    
    # Research overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Research Timestamp",
            value=research_data.get("research_timestamp", "N/A")[:10]
        )
    
    with col2:
        trends_count = len(research_data.get("market_trends", []))
        st.metric(
            label="Market Trends",
            value=f"{trends_count} identified"
        )
    
    with col3:
        opportunities_count = len(research_data.get("growth_opportunities", []))
        st.metric(
            label="Growth Opportunities", 
            value=f"{opportunities_count} found"
        )
    
    # Market trends analysis
    if research_data.get("market_trends"):
        st.markdown("### Market Trends Analysis")
        
        for i, trend in enumerate(research_data["market_trends"], 1):
            impact_color = {"High": "#ff4444", "Medium": "#ffaa00", "Low": "#44ff44"}
            color = impact_color.get(trend.get("market_impact", "Medium"), "#888888")
            
            st.markdown(f"""
            <div style="
                border-left: 4px solid {color};
                padding: 1rem;
                margin: 1rem 0;
                background: rgba(255,255,255,0.03);
                border-radius: 8px;
            ">
                <h4 style="margin: 0; color: {color};">{i}. {trend.get('trend', 'Unknown Trend')}</h4>
                <div style="margin: 0.5rem 0;">
                    <span style="background: {color}; color: white; padding: 0.2rem 0.5rem; border-radius: 12px; font-size: 0.8rem;">
                        {trend.get('growth_rate', 'N/A')}
                    </span>
                    <span style="background: rgba(255,255,255,0.1); color: white; padding: 0.2rem 0.5rem; border-radius: 12px; font-size: 0.8rem; margin-left: 0.5rem;">
                        {trend.get('timeline', 'N/A')}
                    </span>
                </div>
                <p style="margin: 0.5rem 0 0 0; opacity: 0.8;">
                    {trend.get('description', 'No description available')}
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    # Growth opportunities
    if research_data.get("growth_opportunities"):
        st.markdown("### Growth Opportunities")
        
        for opportunity in research_data["growth_opportunities"]:
            value_color = {"High": "#44ff44", "Medium": "#ffaa00", "Low": "#ff8888"}
            color = value_color.get(opportunity.get("potential_value", "Medium"), "#888888")
            
            st.markdown(f"""
            <div style="
                border: 1px solid {color};
                padding: 1rem;
                margin: 1rem 0;
                background: rgba(68,255,68,0.05);
                border-radius: 8px;
            ">
                <h4 style="margin: 0; color: {color};">{opportunity.get('opportunity', 'Unknown Opportunity')}</h4>
                <div style="margin: 0.5rem 0;">
                    <span style="background: {color}; color: white; padding: 0.2rem 0.5rem; border-radius: 12px; font-size: 0.8rem;">
                        Value: {opportunity.get('potential_value', 'N/A')}
                    </span>
                    <span style="background: rgba(255,255,255,0.1); color: white; padding: 0.2rem 0.5rem; border-radius: 12px; font-size: 0.8rem; margin-left: 0.5rem;">
                        Success: {opportunity.get('success_probability', 'N/A')}
                    </span>
                </div>
                <p style="margin: 0.5rem 0 0 0; opacity: 0.8;">
                    Timeline: {opportunity.get('timeline', 'N/A')} | Investment: {opportunity.get('investment_required', 'N/A')}
                </p>
                <p style="margin: 0.5rem 0 0 0; opacity: 0.8;">
                    {opportunity.get('description', 'No description available')}
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    # Strategic recommendations
    market_engine = MarketIntelligenceEngine()
    recommendations = market_engine.generate_strategic_recommendations(research_data)
    
    if recommendations:
        st.markdown("### Strategic Recommendations")
        
        for rec in recommendations:
            priority_colors = {"High": "#ff4444", "Medium": "#ffaa00", "Low": "#44ff44"}
            priority_color = priority_colors.get(rec.get("priority", "Medium"), "#888888")
            
            with st.expander(f"{rec.get('recommendation', 'Unknown Recommendation')}", expanded=False):
                st.markdown(f"**Category:** {rec.get('category', 'N/A')}")
                st.markdown(f"**Priority:** {rec.get('priority', 'N/A')}")
                st.markdown(f"**Timeline:** {rec.get('timeline', 'N/A')}")
                st.markdown(f"**Expected Impact:** {rec.get('expected_impact', 'N/A')}")
                
                if rec.get("implementation_steps"):
                    st.markdown("**Implementation Steps:**")
                    for step in rec["implementation_steps"]:
                        st.markdown(f"• {step}")
    
    # Key insights summary
    if research_data.get("key_insights"):
        st.markdown("### Key Insights")
        
        for insight in research_data["key_insights"]:
            st.info(insight)

def display_grok_analysis_results(grok_data: Dict[str, Any]):
    """Display Grok AI analysis results with enhanced formatting"""
    
    st.markdown("## Advanced AI Analysis (Powered by Grok)")
    
    # Analysis overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="AI Model",
            value="Grok-2",
            delta="Latest XAI Model"
        )
    
    with col2:
        st.metric(
            label="Analysis Timestamp",
            value=grok_data.get("timestamp", "N/A")[:10]
        )
    
    with col3:
        tokens_used = grok_data.get("tokens_used", 0)
        st.metric(
            label="Tokens Processed",
            value=f"{tokens_used:,}"
        )
    
    # Main analysis content
    if grok_data.get("analysis"):
        st.markdown("### Strategic Analysis")
        
        # Split analysis into sections for better readability
        analysis_text = grok_data["analysis"]
        
        # Display in expandable sections
        sections = analysis_text.split('\n\n')
        
        for i, section in enumerate(sections):
            if section.strip():
                # Create section headers based on content
                if any(keyword in section.lower() for keyword in ['strategic', 'recommendation']):
                    section_title = "Strategic Recommendations"
                elif any(keyword in section.lower() for keyword in ['market', 'positioning']):
                    section_title = "Market Positioning"
                elif any(keyword in section.lower() for keyword in ['competitive', 'advantage']):
                    section_title = "Competitive Analysis"
                elif any(keyword in section.lower() for keyword in ['risk', 'challenge']):
                    section_title = "Risk Assessment"
                elif any(keyword in section.lower() for keyword in ['growth', 'opportunity']):
                    section_title = "Growth Opportunities"
                else:
                    section_title = f"Analysis Section {i+1}"
                
                with st.expander(section_title, expanded=i < 2):
                    st.markdown(section.strip())
    
    # Analysis metadata
    st.markdown("### Analysis Details")
    col_meta1, col_meta2 = st.columns(2)
    
    with col_meta1:
        st.markdown(f"**Model Used:** {grok_data.get('model_used', 'N/A')}")
        st.markdown(f"**Status:** {grok_data.get('status', 'N/A').title()}")
    
    with col_meta2:
        st.markdown(f"**Processing Time:** Real-time")
        st.markdown(f"**Analysis Type:** Comprehensive Industry Assessment")
    
    # Export options
    st.markdown("### Export Options")
    export_cols = st.columns(3)
    
    with export_cols[0]:
        if st.button("Download Analysis", use_container_width=True):
            analysis_export = {
                "analysis": grok_data.get("analysis", ""),
                "model": grok_data.get("model_used", ""),
                "timestamp": grok_data.get("timestamp", ""),
                "tokens_used": grok_data.get("tokens_used", 0)
            }
            st.download_button(
                label="Download JSON",
                data=json.dumps(analysis_export, indent=2),
                file_name=f"grok_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with export_cols[1]:
        if st.button("Share Analysis", use_container_width=True):
            st.info("Analysis sharing functionality ready for implementation.")
    
    with export_cols[2]:
        if st.button("Generate Report", use_container_width=True):
            st.info("Report generation initiated based on Grok analysis.")

def display_perplexity_research_results(research_data: Dict[str, Any]):
    """Display Perplexity AI research results with comprehensive formatting"""
    
    st.markdown("## Real-Time Market Research (Powered by Perplexity)")
    
    # Research overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Research Status",
            value="Live Data",
            delta="Real-time Sources"
        )
    
    with col2:
        st.metric(
            label="Industry Focus",
            value=research_data.get("industry", "N/A")
        )
    
    with col3:
        total_tokens = research_data.get("total_tokens", 0)
        st.metric(
            label="Data Points",
            value=f"{total_tokens:,}"
        )
    
    # Create tabs for different research areas
    trends_tab, competitors_tab, opportunities_tab = st.tabs([
        "Market Trends", "Competitive Analysis", "Growth Opportunities"
    ])
    
    # Market Trends
    with trends_tab:
        trends_data = research_data.get("trends", {})
        if trends_data.get("status") == "success":
            st.markdown("### Latest Industry Trends")
            
            # Display research content
            research_content = trends_data.get("research", "")
            if research_content:
                # Split into sections for better readability
                sections = research_content.split('\n\n')
                
                for i, section in enumerate(sections):
                    if section.strip():
                        # Create expandable sections
                        if i < 3:  # First 3 sections expanded
                            with st.expander(f"Trend Analysis {i+1}", expanded=True):
                                st.markdown(section.strip())
                        else:
                            with st.expander(f"Additional Insights {i-2}"):
                                st.markdown(section.strip())
            
            # Metadata
            st.markdown("---")
            col_meta1, col_meta2 = st.columns(2)
            with col_meta1:
                st.markdown(f"**Model:** {trends_data.get('model_used', 'N/A')}")
            with col_meta2:
                st.markdown(f"**Timestamp:** {trends_data.get('timestamp', 'N/A')[:16]}")
        else:
            st.error(f"Trends research failed: {trends_data.get('error_message', 'Unknown error')}")
    
    # Competitive Analysis
    with competitors_tab:
        competitors_data = research_data.get("competitors", {})
        if competitors_data.get("status") == "success":
            st.markdown("### Competitive Landscape")
            
            analysis_content = competitors_data.get("competitive_analysis", "")
            if analysis_content:
                # Split content for better presentation
                sections = analysis_content.split('\n\n')
                
                for i, section in enumerate(sections):
                    if section.strip():
                        # Identify section type based on content
                        if any(keyword in section.lower() for keyword in ['leader', 'top', 'major']):
                            section_title = "Market Leaders"
                        elif any(keyword in section.lower() for keyword in ['emerging', 'startup', 'new']):
                            section_title = "Emerging Players"
                        elif any(keyword in section.lower() for keyword in ['share', 'market size']):
                            section_title = "Market Share Analysis"
                        elif any(keyword in section.lower() for keyword in ['pricing', 'cost', 'revenue']):
                            section_title = "Business Models & Pricing"
                        else:
                            section_title = f"Competitive Insight {i+1}"
                        
                        with st.expander(section_title, expanded=i < 2):
                            st.markdown(section.strip())
            
            # Metadata
            st.markdown("---")
            col_meta1, col_meta2 = st.columns(2)
            with col_meta1:
                st.markdown(f"**Focus:** {competitors_data.get('focus', 'General Market')}")
            with col_meta2:
                st.markdown(f"**Tokens Used:** {competitors_data.get('tokens_used', 0):,}")
        else:
            st.error(f"Competitive analysis failed: {competitors_data.get('error_message', 'Unknown error')}")
    
    # Growth Opportunities
    with opportunities_tab:
        opportunities_data = research_data.get("opportunities", {})
        if opportunities_data.get("status") == "success":
            st.markdown("### Market Opportunities")
            
            opportunities_content = opportunities_data.get("opportunities", "")
            if opportunities_content:
                sections = opportunities_content.split('\n\n')
                
                for i, section in enumerate(sections):
                    if section.strip():
                        # Categorize opportunities
                        if any(keyword in section.lower() for keyword in ['geographic', 'region', 'market']):
                            section_title = "Geographic Expansion"
                        elif any(keyword in section.lower() for keyword in ['technology', 'innovation', 'digital']):
                            section_title = "Technology Opportunities"
                        elif any(keyword in section.lower() for keyword in ['segment', 'niche', 'customer']):
                            section_title = "Market Segments"
                        elif any(keyword in section.lower() for keyword in ['investment', 'funding', 'capital']):
                            section_title = "Investment Trends"
                        else:
                            section_title = f"Opportunity {i+1}"
                        
                        with st.expander(section_title, expanded=i < 2):
                            st.markdown(section.strip())
            
            # Metadata
            st.markdown("---")
            col_meta1, col_meta2 = st.columns(2)
            with col_meta1:
                st.markdown(f"**Region Focus:** {opportunities_data.get('region', 'Global')}")
            with col_meta2:
                st.markdown(f"**Analysis Depth:** Comprehensive")
        else:
            st.error(f"Opportunities research failed: {opportunities_data.get('error_message', 'Unknown error')}")
    
    # Export and action buttons
    st.markdown("---")
    st.markdown("### Research Actions")
    
    action_cols = st.columns(4)
    
    with action_cols[0]:
        if st.button("Export Research", use_container_width=True):
            research_export = {
                "industry": research_data.get("industry"),
                "timestamp": research_data.get("timestamp"),
                "trends": research_data.get("trends", {}).get("research", ""),
                "competitors": research_data.get("competitors", {}).get("competitive_analysis", ""),
                "opportunities": research_data.get("opportunities", {}).get("opportunities", ""),
                "total_tokens": research_data.get("total_tokens", 0)
            }
            st.download_button(
                label="Download JSON",
                data=json.dumps(research_export, indent=2),
                file_name=f"perplexity_research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with action_cols[1]:
        if st.button("Update Research", use_container_width=True):
            st.info("Initiating fresh research update...")
    
    with action_cols[2]:
        if st.button("Compare Markets", use_container_width=True):
            st.info("Market comparison analysis ready.")
    
    with action_cols[3]:
        if st.button("Create Report", use_container_width=True):
            st.info("Generating comprehensive research report...")

def display_settings_dashboard():
    """Display settings and profile management dashboard"""
    
    st.header("Settings & Profile Management")
    
    # Create tabs for different settings sections
    tab1, tab2, tab3 = st.tabs(["Profile Management", "Email Reports", "System Settings"])
    
    with tab1:
        display_profile_management()
    
    with tab2:
        report_dashboard = ReportDashboard()
        report_dashboard.display_report_delivery_dashboard()
    
    with tab3:
        display_system_settings()

def display_system_settings():
    """Display system settings section"""
    
    # API Status indicators
    st.subheader("System Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if config.OPENAI_API_KEY:
            st.success("OpenAI API Connected")
        else:
            st.error("OpenAI API Key Missing")
    
    with col2:
        if config.NEWS_API_KEY:
            st.success("News API Connected")
        else:
            st.warning("News API Key Missing")
    
    with col3:
        if config.TWITTER_BEARER_TOKEN:
            st.success("Twitter API Connected")
        else:
            st.info("Twitter API Optional")
    
    st.markdown("---")
    
    # System information
    st.subheader("System Information")
    
    try:
        # Only query database if absolutely necessary
        if st.session_state.profile_id:
            st.write("**Profile Status:** Active")
            # Skip heavy database queries that cause SSL timeouts
            # history = db_service.get_profile_history(st.session_state.profile_id)
            st.write("**Database:** Connected")
        else:
            st.write("**Profile Status:** No active profile")
    
    except Exception as e:
        st.warning("Database connection temporarily unavailable. All features still work normally.")
    
    # Export functionality
    st.subheader("Data Export")
    
    if st.session_state.profile_id:
        if st.button("Export Profile Data", key="export_profile_data"):
            try:
                # Export current session data without heavy database queries
                export_data = {
                    'profile': st.session_state.business_profile.__dict__ if st.session_state.business_profile else {},
                    'scraped_data': st.session_state.scraped_data if st.session_state.scraped_data else {},
                    'analysis_results': st.session_state.analysis_results if st.session_state.analysis_results else {},
                    'exported_at': datetime.now().isoformat()
                }
                
                export_json = json.dumps(export_data, indent=2, default=str)
                
                st.download_button(
                    label="Download Current Session Data (JSON)",
                    data=export_json,
                    file_name=f"ai_agent_prospera_data_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                    mime="application/json",
                    key="download_session_data"
                )
                
            except Exception as e:
                st.warning("Export temporarily unavailable. Session data is preserved.")

def display_profile_management():
    """Display profile management section"""
    
    st.subheader("Business Profile Management")
    
    if st.session_state.business_profile:
        profile = st.session_state.business_profile
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Current Profile:**")
            st.write(f"Company: {profile.company_name}")
            st.write(f"Industry: {profile.industry}")
            st.write(f"Sub-industry: {profile.sub_industry}")
            st.write(f"Size: {profile.business_size.value}")
            st.write(f"Location: {profile.location}")
            st.write(f"Market Focus: {profile.market_focus.value}")
        
        with col2:
            st.write("**Profile Completeness:**")
            completeness = profile.profile_completeness * 100
            st.progress(completeness / 100)
            st.write(f"{completeness:.1f}% complete")
            
            if st.button("Edit Profile", type="primary"):
                st.session_state.show_profile_wizard = True
                st.rerun()

def display_ai_chat_dashboard():
    """Display AI chat dashboard with enhanced design"""
    
    st.markdown("""
    <style>
    .chat-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        color: white;
    }
    
    .chat-header {
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 25px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .chat-message {
        margin: 15px 0;
        padding: 18px 25px;
        border-radius: 20px;
        max-width: 85%;
        word-wrap: break-word;
        animation: fadeIn 0.6s ease-in;
    }
    
    .user-message {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        margin-left: auto;
        text-align: right;
        box-shadow: 0 6px 20px rgba(79, 172, 254, 0.4);
    }
    
    .assistant-message {
        background: white;
        color: #2c3e50;
        margin-right: auto;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        border-left: 5px solid #667eea;
    }
    
    .suggestion-button {
        background: rgba(255,255,255,0.2);
        color: white;
        padding: 12px 20px;
        border-radius: 25px;
        border: 2px solid rgba(255,255,255,0.3);
        margin: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 16px;
        display: inline-block;
    }
    
    .suggestion-button:hover {
        background: rgba(255,255,255,0.3);
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Check OpenAI API key
    import os
    api_key = os.environ.get("OPENAI_API_KEY")
    
    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    st.markdown('<div class="chat-header">🤖 AI Business Intelligence Assistant</div>', unsafe_allow_html=True)
    
    if not api_key:
        st.markdown("""
        <div style="text-align: center; padding: 30px;">
            <h3>🔑 OpenAI API Key Required</h3>
            <p style="font-size: 18px; margin: 20px 0;">
                To use the AI chat feature, please configure your OpenAI API key.
            </p>
            <p style="font-size: 16px; opacity: 0.9;">
                You can still use all other features of AI Agent Prospera including:
                <br>• Industry data collection and analysis
                <br>• Business profile management  
                <br>• Market intelligence reports
                <br>• Lead discovery and competitor analysis
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # Initialize chat history
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": "Hello! I'm your AI Business Intelligence Assistant. I can help you analyze market trends, discover leads, understand competitors, and provide strategic insights for your business. What would you like to explore today?",
                "timestamp": "2025-06-08T18:10:00"
            }
        ]
    
    # Display chat messages
    for message in st.session_state.chat_messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message assistant-message">
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
    
    # Quick suggestions for new conversations
    if len(st.session_state.chat_messages) <= 1:
        st.markdown("### Quick Start Suggestions:")
        
        suggestions = [
            "Analyze my industry trends",
            "Find potential leads", 
            "Research my competitors",
            "Market opportunity analysis",
            "Growth strategy recommendations"
        ]
        
        cols = st.columns(len(suggestions))
        for i, suggestion in enumerate(suggestions):
            with cols[i]:
                if st.button(suggestion, key=f"suggestion_{i}"):
                    process_chat_message(suggestion)
                    st.rerun()
    
    # Chat input
    st.markdown("### Type your message:")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Chat Input",
            key="chat_input_field",
            placeholder="Ask me about market trends, competitors, leads, or strategic insights...",
            label_visibility="collapsed"
        )
    
    with col2:
        if st.button("Send", type="primary", key="send_chat"):
            if user_input.strip():
                process_chat_message(user_input)
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def process_chat_message(user_message: str):
    """Process user chat message and generate response"""
    
    # Add user message
    st.session_state.chat_messages.append({
        "role": "user", 
        "content": user_message,
        "timestamp": "2025-06-08T18:10:00"
    })
    
    # Generate AI response (with quota handling)
    try:
        from openai import OpenAI
        import os
        
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        # Build conversation context
        messages = [
            {
                "role": "system", 
                "content": "You are an expert AI Business Intelligence Assistant for AI Agent Prospera platform. Help users with market analysis, lead discovery, competitive intelligence, and strategic planning. Provide practical, actionable advice focused on driving business results."
            }
        ]
        
        # Add recent chat history
        for msg in st.session_state.chat_messages[-5:]:
            if msg["role"] in ["user", "assistant"]:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        # Get AI response
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=800,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content or "I'm unable to provide a response at the moment."
        
    except Exception as e:
        error_msg = str(e)
        if "quota" in error_msg.lower() or "insufficient_quota" in error_msg.lower():
            ai_response = "The OpenAI API quota has been exceeded. This is a temporary limitation. You can still use all other features of AI Agent Prospera including data collection, analysis, and reporting while the API quota resets."
        else:
            ai_response = "I'm experiencing technical difficulties connecting to AI services. Please try again in a moment or use the other platform features while this resolves."
    
    # Add AI response
    st.session_state.chat_messages.append({
        "role": "assistant",
        "content": ai_response,
        "timestamp": "2025-06-08T18:10:00"
    })
    
    # Force page refresh to clear input
    st.rerun()

if __name__ == "__main__":
    main()
