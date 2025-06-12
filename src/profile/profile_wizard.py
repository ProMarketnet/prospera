import streamlit as st
from typing import Dict, Any, Optional
from .business_profile import BusinessProfileManager, BusinessProfile, BusinessSize, MarketFocus
from .directory_importer import BusinessDirectoryImporter
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class ProfileWizard:
    """Interactive business profile creation wizard"""
    
    def __init__(self):
        self.profile_manager = BusinessProfileManager()
        self.directory_importer = BusinessDirectoryImporter()
    
    def show_wizard(self) -> Optional[BusinessProfile]:
        """Display the profile creation wizard"""
        
        st.markdown("## Business Profile Setup")
        st.markdown("Let's customize the AI agent for your specific business needs.")
        
        # Enhanced setup options
        setup_option = st.selectbox(
            "Choose setup option:",
            ["Import from Company Info", "Create Custom Profile", "Use Demo Profile"]
        )
        
        if setup_option == "Import from Company Info":
            return self._show_import_wizard()
        elif setup_option == "Use Demo Profile":
            return self._show_demo_profiles()
        else:
            return self._show_custom_wizard()
    
    def _show_import_wizard(self) -> Optional[BusinessProfile]:
        """Show business data import wizard"""
        
        st.markdown("### Import Business Information")
        st.markdown("Enter your company name or website to automatically populate your profile.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            search_query = st.text_input(
                "Company Name or Website:",
                placeholder="e.g., 'Acme Corp' or 'www.acmecorp.com'"
            )
        
        with col2:
            location = st.text_input(
                "Location (optional):",
                placeholder="e.g., 'New York, NY'"
            )
        
        if st.button("Import Business Data", type="primary"):
            if search_query:
                with st.spinner("Searching for business information..."):
                    try:
                        import_result = self.directory_importer.import_business_profile(
                            search_query, location
                        )
                        
                        if import_result["status"] == "found":
                            return self._show_import_results(import_result)
                        else:
                            st.error("No business information found. Please try manual setup.")
                            return self._show_custom_wizard()
                            
                    except Exception as e:
                        st.error(f"Error importing business data: {str(e)}")
                        return self._show_custom_wizard()
            else:
                st.warning("Please enter a company name or website.")
        
        return None
    
    def _show_import_results(self, import_result: Dict[str, Any]) -> Optional[BusinessProfile]:
        """Display imported business data for confirmation"""
        
        profile_data = import_result["profile_data"]
        confidence = import_result["confidence"]
        
        st.success(f"Business information found (Confidence: {confidence:.0%})")
        
        st.markdown("### Review and Confirm Business Profile")
        
        # Display found information in editable form
        col1, col2 = st.columns(2)
        
        with col1:
            company_name = st.text_input("Company Name", value=profile_data.get("company_name", ""))
            industry = st.selectbox(
                "Industry",
                ["fashion_apparel", "tech_software", "food_beverage", "healthcare", 
                 "finance", "automotive", "real_estate", "education", "retail", "consulting"],
                index=0 if profile_data.get("industry") == "fashion_apparel" else 0
            )
            business_size = st.selectbox(
                "Business Size",
                ["startup", "small", "medium", "large"],
                index=["startup", "small", "medium", "large"].index(profile_data.get("business_size", "small"))
            )
            location = st.text_input("Location", value=profile_data.get("location", ""))
        
        with col2:
            website = st.text_input("Website", value=profile_data.get("website", ""))
            phone = st.text_input("Phone", value=profile_data.get("phone", ""))
            email = st.text_input("Email", value=profile_data.get("email", ""))
            description = st.text_area("Description", value=profile_data.get("description", ""))
        
        # Additional profile details
        st.markdown("### Additional Details")
        
        primary_products = st.text_area(
            "Primary Products/Services (one per line)",
            value="\n".join(profile_data.get("primary_products", []))
        )
        
        col3, col4 = st.columns(2)
        
        with col3:
            market_focus = st.selectbox(
                "Market Focus",
                ["local", "regional", "national", "international"],
                index=["local", "regional", "national", "international"].index(
                    profile_data.get("market_focus", "national").lower()
                )
            )
            
        with col4:
            annual_revenue = st.selectbox(
                "Annual Revenue",
                ["startup", "hundred_thousand", "million_plus", "undisclosed"],
                index=["startup", "hundred_thousand", "million_plus", "undisclosed"].index(
                    profile_data.get("annual_revenue", "undisclosed")
                )
            )
        
        # Confirmation buttons
        col5, col6 = st.columns(2)
        
        with col5:
            if st.button("Create Profile", type="primary"):
                # Create profile with confirmed data
                updated_profile_data = {
                    "company_name": company_name,
                    "industry": industry,
                    "sub_industry": profile_data.get("sub_industry", ""),
                    "business_size": business_size,
                    "annual_revenue": annual_revenue,
                    "location": location,
                    "website": website,
                    "phone": phone,
                    "email": email,
                    "description": description,
                    "primary_products": [p.strip() for p in primary_products.split('\n') if p.strip()],
                    "target_markets": profile_data.get("target_markets", ["General Market"]),
                    "market_focus": market_focus,
                    "unique_selling_points": [],
                    "main_challenges": [],
                    "growth_goals": [],
                    "target_revenue_growth": "steady_growth",
                    "focus_regions": [location] if location else [],
                    "competitor_companies": [],
                    "key_keywords": [p.strip() for p in primary_products.split('\n') if p.strip()],
                    "preferred_languages": ["English"]
                }
                
                try:
                    profile = self.profile_manager.create_profile_from_data(updated_profile_data)
                    st.success("Business profile created successfully!")
                    return profile
                except Exception as e:
                    st.error(f"Error creating profile: {str(e)}")
        
        with col6:
            if st.button("Manual Setup Instead"):
                return self._show_custom_wizard()
        
        return None
    
    def _show_demo_profiles(self) -> Optional[BusinessProfile]:
        """Show demo profile selection"""
        
        demo_profiles = self.profile_manager.get_demo_profiles()
        
        st.markdown("### Select a Demo Business Profile")
        
        profile_options = {
            "Italian Shoe Manufacturer": "italian_shoe_manufacturer",
            "Tech Startup": "tech_startup", 
            "Organic Food Distributor": "organic_food_distributor"
        }
        
        selected_profile_name = st.selectbox(
            "Choose a demo profile:",
            list(profile_options.keys())
        )
        
        selected_profile_key = profile_options[selected_profile_name]
        profile_data = demo_profiles[selected_profile_key]
        
        # Show profile preview
        st.markdown("### Profile Preview")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Company:** {profile_data['company_name']}")
            st.markdown(f"**Industry:** {profile_data['sub_industry']}")
            st.markdown(f"**Location:** {profile_data['location']}")
            st.markdown(f"**Size:** {profile_data['business_size']}")
        
        with col2:
            st.markdown(f"**Products:** {profile_data['primary_products']}")
            st.markdown(f"**Target Growth:** {profile_data['target_revenue_growth']}")
            st.markdown(f"**Focus Regions:** {profile_data['focus_regions']}")
        
        if st.button("Use This Profile", type="primary"):
            profile = self.profile_manager.create_profile_from_wizard(profile_data)
            self.profile_manager.save_profile(profile)
            st.success(f"Profile created for {profile.company_name}!")
            return profile
        
        return None
    
    def _show_custom_wizard(self) -> Optional[BusinessProfile]:
        """Show custom profile creation wizard"""
        
        with st.form("business_profile_form"):
            st.markdown("### Company Information")
            
            col1, col2 = st.columns(2)
            
            with col1:
                company_name = st.text_input("Company Name*", help="Your business name")
                industry = st.selectbox(
                    "Industry*",
                    ["fashion_apparel", "consumer_goods", "manufacturing"],
                    format_func=lambda x: {
                        "fashion_apparel": "Fashion & Apparel",
                        "consumer_goods": "Consumer Goods", 
                        "manufacturing": "Manufacturing"
                    }[x]
                )
                sub_industry = st.text_input("Sub-Industry*", help="e.g., Leather Goods, Software, Food & Beverage")
                business_size = st.selectbox(
                    "Business Size*",
                    [size.value for size in BusinessSize]
                )
            
            with col2:
                annual_revenue = st.selectbox(
                    "Annual Revenue",
                    ["Under $100K", "$100K-500K", "$500K-1M", "$1M-5M", "$5M-20M", "Over $20M"]
                )
                location = st.text_input("Location*", help="City, Country")
                market_focus = st.selectbox(
                    "Market Focus",
                    [focus.value for focus in MarketFocus]
                )
            
            st.markdown("### Products & Services")
            
            primary_products = st.text_area(
                "Primary Products/Services*",
                help="Comma-separated list of your main products or services"
            )
            
            target_markets = st.text_area(
                "Target Markets*",
                help="Comma-separated list of your target customer segments"
            )
            
            unique_selling_points = st.text_area(
                "Unique Selling Points",
                help="What makes your business different from competitors?"
            )
            
            st.markdown("### Business Goals & Challenges")
            
            col1, col2 = st.columns(2)
            
            with col1:
                main_challenges = st.text_area(
                    "Main Business Challenges*",
                    help="Current challenges you're facing"
                )
                
                target_revenue_growth = st.selectbox(
                    "Target Revenue Growth",
                    ["10-20% annually", "20-30% annually", "30-50% annually", "50%+ annually"]
                )
            
            with col2:
                growth_goals = st.text_area(
                    "Growth Goals*",
                    help="Your main business growth objectives"
                )
                
                focus_regions = st.text_area(
                    "Focus Regions",
                    help="Geographic regions you want to target"
                )
            
            st.markdown("### Competitive Intelligence")
            
            competitor_companies = st.text_area(
                "Known Competitors",
                help="Companies you consider direct competitors"
            )
            
            # Form submission
            submitted = st.form_submit_button("Create Profile", type="primary")
            
            if submitted:
                # Validate required fields
                required_fields = {
                    "company_name": company_name,
                    "industry": industry,
                    "sub_industry": sub_industry,
                    "primary_products": primary_products,
                    "target_markets": target_markets,
                    "main_challenges": main_challenges,
                    "growth_goals": growth_goals,
                    "location": location
                }
                
                missing_fields = [field for field, value in required_fields.items() if not value.strip()]
                
                if missing_fields:
                    st.error(f"Please fill in required fields: {', '.join(missing_fields)}")
                    return None
                
                # Create profile
                responses = {
                    "company_name": company_name,
                    "industry": industry,
                    "sub_industry": sub_industry,
                    "business_size": business_size,
                    "annual_revenue": annual_revenue,
                    "location": location,
                    "primary_products": primary_products,
                    "target_markets": target_markets,
                    "market_focus": market_focus,
                    "unique_selling_points": unique_selling_points,
                    "main_challenges": main_challenges,
                    "growth_goals": growth_goals,
                    "target_revenue_growth": target_revenue_growth,
                    "focus_regions": focus_regions,
                    "competitor_companies": competitor_companies
                }
                
                try:
                    profile = self.profile_manager.create_profile_from_wizard(responses)
                    self.profile_manager.save_profile(profile)
                    st.success(f"Profile created for {profile.company_name}!")
                    logger.info(f"Created profile for {profile.company_name}")
                    return profile
                    
                except Exception as e:
                    st.error(f"Error creating profile: {str(e)}")
                    logger.error(f"Error creating profile: {str(e)}")
                    return None
        
        return None
    
    def show_profile_summary(self, profile: BusinessProfile):
        """Display profile summary"""
        
        st.markdown(f"## Profile: {profile.company_name}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### Company Details")
            st.markdown(f"**Industry:** {profile.sub_industry}")
            st.markdown(f"**Size:** {profile.business_size.value}")
            st.markdown(f"**Location:** {profile.location}")
            st.markdown(f"**Revenue:** {profile.annual_revenue}")
        
        with col2:
            st.markdown("### Products & Markets")
            st.markdown(f"**Products:** {', '.join(profile.primary_products[:3])}...")
            st.markdown(f"**Target Markets:** {', '.join(profile.target_markets[:2])}...")
            st.markdown(f"**Market Focus:** {profile.market_focus.value}")
        
        with col3:
            st.markdown("### Goals & Focus")
            st.markdown(f"**Target Growth:** {profile.target_revenue_growth}")
            st.markdown(f"**Focus Regions:** {', '.join(profile.focus_regions[:2])}...")
            st.markdown(f"**Profile Completeness:** {profile.profile_completeness:.0f}%")
        
        # Show key challenges and goals
        if profile.main_challenges:
            with st.expander("Current Challenges"):
                for challenge in profile.main_challenges:
                    st.markdown(f"• {challenge}")
        
        if profile.growth_goals:
            with st.expander("Growth Goals"):
                for goal in profile.growth_goals:
                    st.markdown(f"• {goal}")