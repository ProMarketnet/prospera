import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class BusinessSize(Enum):
    MICRO = "1-10 employees"
    SMALL = "11-50 employees" 
    MEDIUM = "51-250 employees"
    LARGE = "250+ employees"

class MarketFocus(Enum):
    LOCAL = "Local/Regional"
    NATIONAL = "National"
    INTERNATIONAL = "International"
    GLOBAL = "Global"

@dataclass
class BusinessProfile:
    # Company Details
    company_name: str
    industry: str
    sub_industry: str
    business_size: BusinessSize
    annual_revenue: str
    location: str
    
    # Products & Services
    primary_products: List[str]
    target_markets: List[str]
    market_focus: MarketFocus
    unique_selling_points: List[str]
    
    # Current Challenges & Goals
    main_challenges: List[str]
    growth_goals: List[str]
    target_revenue_growth: str
    
    # Market Intelligence Preferences
    focus_regions: List[str]
    competitor_companies: List[str]
    key_keywords: List[str]
    preferred_languages: List[str]
    
    # Profile Metadata
    created_at: str
    updated_at: str
    profile_completeness: float

class BusinessProfileManager:
    """Manages business profiles and customizes AI analysis accordingly"""
    
    def __init__(self):
        self.profiles_dir = "data/profiles"
        os.makedirs(self.profiles_dir, exist_ok=True)
    
    def create_profile_from_wizard(self, responses: Dict[str, Any]) -> BusinessProfile:
        """Create business profile from onboarding wizard responses"""
        
        # Extract and process wizard responses
        profile = BusinessProfile(
            company_name=responses.get("company_name", ""),
            industry=responses.get("industry", ""),
            sub_industry=responses.get("sub_industry", ""),
            business_size=BusinessSize(responses.get("business_size", BusinessSize.SMALL.value)),
            annual_revenue=responses.get("annual_revenue", ""),
            location=responses.get("location", ""),
            
            primary_products=self._parse_list_input(responses.get("primary_products", "")),
            target_markets=self._parse_list_input(responses.get("target_markets", "")),
            market_focus=MarketFocus(responses.get("market_focus", MarketFocus.LOCAL.value)),
            unique_selling_points=self._parse_list_input(responses.get("unique_selling_points", "")),
            
            main_challenges=self._parse_list_input(responses.get("main_challenges", "")),
            growth_goals=self._parse_list_input(responses.get("growth_goals", "")),
            target_revenue_growth=responses.get("target_revenue_growth", ""),
            
            focus_regions=self._parse_list_input(responses.get("focus_regions", "")),
            competitor_companies=self._parse_list_input(responses.get("competitor_companies", "")),
            key_keywords=self._generate_keywords(responses),
            preferred_languages=["English"],  # Default
            
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            profile_completeness=self._calculate_completeness(responses)
        )
        
        return profile
    
    def create_profile_from_data(self, profile_data: Dict[str, Any]) -> BusinessProfile:
        """Create business profile from imported data dictionary"""
        
        # Map string values to enum types
        business_size_map = {
            'startup': BusinessSize.MICRO,
            'small': BusinessSize.SMALL,
            'medium': BusinessSize.MEDIUM,
            'large': BusinessSize.LARGE
        }
        
        market_focus_map = {
            'local': MarketFocus.LOCAL,
            'regional': MarketFocus.LOCAL,
            'national': MarketFocus.NATIONAL,
            'international': MarketFocus.INTERNATIONAL
        }
        
        profile = BusinessProfile(
            company_name=profile_data.get("company_name", ""),
            industry=profile_data.get("industry", "consulting"),
            sub_industry=profile_data.get("sub_industry", ""),
            business_size=business_size_map.get(profile_data.get("business_size", "small"), BusinessSize.SMALL),
            annual_revenue=profile_data.get("annual_revenue", "undisclosed"),
            location=profile_data.get("location", ""),
            
            primary_products=profile_data.get("primary_products", []),
            target_markets=profile_data.get("target_markets", ["General Market"]),
            market_focus=market_focus_map.get(profile_data.get("market_focus", "national"), MarketFocus.NATIONAL),
            unique_selling_points=profile_data.get("unique_selling_points", []),
            
            main_challenges=profile_data.get("main_challenges", []),
            growth_goals=profile_data.get("growth_goals", []),
            target_revenue_growth=profile_data.get("target_revenue_growth", "steady_growth"),
            
            focus_regions=profile_data.get("focus_regions", []),
            competitor_companies=profile_data.get("competitor_companies", []),
            key_keywords=profile_data.get("key_keywords", []),
            preferred_languages=profile_data.get("preferred_languages", ["English"]),
            
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            profile_completeness=self._calculate_completeness_from_data(profile_data)
        )
        
        return profile
    
    def save_profile(self, profile: BusinessProfile) -> str:
        """Save business profile to file"""
        try:
            profile_id = profile.company_name.lower().replace(" ", "_").replace(",", "")
            filename = f"{profile_id}_profile.json"
            filepath = os.path.join(self.profiles_dir, filename)
            
            # Convert dataclass to dict, handling Enum values
            profile_dict = asdict(profile)
            profile_dict['business_size'] = profile.business_size.value
            profile_dict['market_focus'] = profile.market_focus.value
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(profile_dict, f, indent=2, default=str)
            
            logger.info(f"Profile saved for {profile.company_name}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error saving profile: {str(e)}")
            raise
    
    def load_profile(self, company_name: str) -> Optional[BusinessProfile]:
        """Load business profile from file"""
        try:
            profile_id = company_name.lower().replace(" ", "_").replace(",", "")
            filename = f"{profile_id}_profile.json"
            filepath = os.path.join(self.profiles_dir, filename)
            
            if not os.path.exists(filepath):
                return None
            
            with open(filepath, 'r', encoding='utf-8') as f:
                profile_dict = json.load(f)
            
            # Convert back to dataclass, handling Enum values
            profile_dict['business_size'] = BusinessSize(profile_dict['business_size'])
            profile_dict['market_focus'] = MarketFocus(profile_dict['market_focus'])
            
            return BusinessProfile(**profile_dict)
            
        except Exception as e:
            logger.error(f"Error loading profile: {str(e)}")
            return None
    
    def get_demo_profiles(self) -> Dict[str, Dict[str, Any]]:
        """Get pre-configured demo profiles for different business types"""
        return {
            "italian_shoe_manufacturer": {
                "company_name": "Artisan Leather Works",
                "industry": "fashion_apparel",
                "sub_industry": "Leather Goods & Footwear",
                "business_size": BusinessSize.SMALL.value,
                "annual_revenue": "$1-5M annually",
                "location": "Milan, Italy",
                
                "primary_products": "Premium leather shoes, Custom footwear, Artisan boots",
                "target_markets": "Luxury retail, Boutique stores, International buyers",
                "market_focus": MarketFocus.INTERNATIONAL.value,
                "unique_selling_points": "Traditional craftsmanship, Premium Italian leather, Custom sizing",
                
                "main_challenges": "Finding new international customers, Seasonal demand fluctuations, Material cost increases",
                "growth_goals": "Expand to Asian markets, Increase online sales, Develop sustainable product line",
                "target_revenue_growth": "25-30% annually",
                
                "focus_regions": "Europe, Asia, North America",
                "competitor_companies": "Santoni, Church's, Berluti",
                "preferred_languages": ["English", "Italian"]
            },
            "tech_startup": {
                "company_name": "InnovateTech Solutions",
                "industry": "manufacturing",
                "sub_industry": "Technology & Software",
                "business_size": BusinessSize.MICRO.value,
                "annual_revenue": "$100K-500K annually",
                "location": "Austin, Texas",
                
                "primary_products": "SaaS platform, Mobile apps, AI consulting",
                "target_markets": "Small businesses, Healthcare providers, E-commerce companies",
                "market_focus": MarketFocus.NATIONAL.value,
                "unique_selling_points": "AI-powered solutions, Rapid deployment, Cost-effective pricing",
                
                "main_challenges": "Customer acquisition, Competition from large players, Scaling operations",
                "growth_goals": "Reach 1000 customers, Launch enterprise tier, Expand to Canada",
                "target_revenue_growth": "200% annually",
                
                "focus_regions": "United States, Canada",
                "competitor_companies": "Salesforce, HubSpot, Slack",
                "preferred_languages": ["English"]
            },
            "organic_food_distributor": {
                "company_name": "Green Valley Organics",
                "industry": "consumer_goods",
                "sub_industry": "Food & Beverage",
                "business_size": BusinessSize.MEDIUM.value,
                "annual_revenue": "$5-20M annually",
                "location": "Portland, Oregon",
                
                "primary_products": "Organic produce, Natural supplements, Eco-friendly packaging",
                "target_markets": "Health food stores, Restaurants, Grocery chains",
                "market_focus": MarketFocus.NATIONAL.value,
                "unique_selling_points": "USDA Organic certified, Local sourcing, Sustainable practices",
                
                "main_challenges": "Supply chain disruptions, Price competition, Regulatory compliance",
                "growth_goals": "Enter European markets, Launch direct-to-consumer, Acquire smaller competitors",
                "target_revenue_growth": "40% annually",
                
                "focus_regions": "United States, Europe",
                "competitor_companies": "Whole Foods Market, Thrive Market, Vitacost",
                "preferred_languages": ["English"]
            }
        }
    
    def customize_data_collection(self, profile: BusinessProfile) -> Dict[str, Any]:
        """Customize data collection strategy based on business profile"""
        
        # Generate custom search keywords
        keywords = self._generate_comprehensive_keywords(profile)
        
        # Determine relevant data sources
        data_sources = self._select_data_sources(profile)
        
        # Define search parameters
        search_config = {
            "keywords": keywords,
            "data_sources": data_sources,
            "geographic_focus": profile.focus_regions,
            "competitor_tracking": profile.competitor_companies,
            "market_segments": profile.target_markets,
            "product_categories": profile.primary_products,
            "languages": profile.preferred_languages
        }
        
        return search_config
    
    def customize_ai_analysis(self, profile: BusinessProfile) -> Dict[str, str]:
        """Generate custom AI prompts based on business profile"""
        
        company_context = f"""
        Company Profile:
        - Name: {profile.company_name}
        - Industry: {profile.industry} - {profile.sub_industry}
        - Size: {profile.business_size.value}
        - Location: {profile.location}
        - Revenue: {profile.annual_revenue}
        
        Products: {', '.join(profile.primary_products)}
        Target Markets: {', '.join(profile.target_markets)}
        Market Focus: {profile.market_focus.value}
        
        Current Challenges: {', '.join(profile.main_challenges)}
        Growth Goals: {', '.join(profile.growth_goals)}
        Target Growth: {profile.target_revenue_growth}
        """
        
        custom_prompts = {
            "trend_analysis": f"""
            Analyze market trends specifically for this business profile:
            {company_context}
            
            Focus on trends that directly impact their products, target markets, and growth goals.
            Consider their geographic focus and current challenges.
            Provide actionable insights for their specific situation.
            """,
            
            "opportunity_identification": f"""
            Identify business opportunities specifically relevant to:
            {company_context}
            
            Consider:
            - Their unique selling points and competitive advantages
            - Target markets they want to expand into
            - Product categories that align with their expertise
            - Geographic regions they're targeting
            - Revenue growth goals
            """,
            
            "lead_qualification": f"""
            Evaluate and score leads based on fit for this specific business:
            {company_context}
            
            Prioritize leads that:
            - Match their target market profile
            - Are in their focus geographic regions
            - Would value their unique selling points
            - Align with their growth goals and capacity
            """,
            
            "competitive_analysis": f"""
            Analyze competition specifically for:
            {company_context}
            
            Compare against their known competitors: {', '.join(profile.competitor_companies)}
            Focus on competitive positioning in their target markets.
            Identify competitive advantages and threats specific to their situation.
            """
        }
        
        return custom_prompts
    
    def generate_custom_report_sections(self, profile: BusinessProfile) -> List[Dict[str, str]]:
        """Generate custom report sections based on business profile"""
        
        sections = [
            {
                "title": f"Executive Summary for {profile.company_name}",
                "focus": "Tailored insights for your specific business situation"
            },
            {
                "title": "Market Opportunities in Your Focus Regions",
                "focus": f"Specific opportunities in: {', '.join(profile.focus_regions)}"
            },
            {
                "title": "Qualified Leads for Your Products",
                "focus": f"Prospects specifically seeking: {', '.join(profile.primary_products)}"
            },
            {
                "title": "Competitive Intelligence",
                "focus": f"Analysis of {', '.join(profile.competitor_companies)} and market positioning"
            },
            {
                "title": "Growth Strategy Recommendations",
                "focus": f"Specific actions to achieve {profile.target_revenue_growth} growth"
            }
        ]
        
        # Add custom sections based on specific challenges
        if "international expansion" in ' '.join(profile.growth_goals).lower():
            sections.append({
                "title": "International Expansion Strategy",
                "focus": "Market entry recommendations for your target regions"
            })
        
        if "sustainable" in ' '.join(profile.growth_goals).lower():
            sections.append({
                "title": "Sustainability Opportunities",
                "focus": "Sustainable product development and market trends"
            })
        
        return sections
    
    def _generate_comprehensive_keywords(self, profile: BusinessProfile) -> List[str]:
        """Generate comprehensive keyword list based on profile"""
        keywords = []
        
        # Product-based keywords
        for product in profile.primary_products:
            keywords.extend([
                product.strip(),
                f"{product.strip()} manufacturer",
                f"{product.strip()} supplier",
                f"custom {product.strip()}",
                f"premium {product.strip()}"
            ])
        
        # Location-based keywords
        location_parts = profile.location.split(", ")
        for part in location_parts:
            keywords.extend([
                f"{part.strip()} {profile.sub_industry}",
                f"{part.strip()} manufacturing"
            ])
        
        # Market-based keywords
        for market in profile.target_markets:
            keywords.extend([
                market.strip(),
                f"{market.strip()} trends",
                f"{market.strip()} demand"
            ])
        
        # Challenge-based keywords
        for challenge in profile.main_challenges:
            if "international" in challenge.lower():
                keywords.extend(["export opportunities", "international trade", "global markets"])
            if "seasonal" in challenge.lower():
                keywords.extend(["seasonal demand", "inventory management", "demand forecasting"])
        
        # Goal-based keywords
        for goal in profile.growth_goals:
            if "asian" in goal.lower() or "asia" in goal.lower():
                keywords.extend(["asian market", "korea", "japan", "china", "singapore"])
            if "online" in goal.lower():
                keywords.extend(["e-commerce", "online retail", "digital sales"])
            if "sustainable" in goal.lower():
                keywords.extend(["sustainable fashion", "eco-friendly", "green manufacturing"])
        
        return list(set(keywords))  # Remove duplicates
    
    def _select_data_sources(self, profile: BusinessProfile) -> Dict[str, List[str]]:
        """Select relevant data sources based on profile"""
        sources = {
            "trade_publications": [],
            "social_media": ["LinkedIn", "Instagram"],
            "business_directories": ["Google Places", "Industry directories"],
            "news_sources": ["Industry news", "Local business news"],
            "market_research": ["Trade associations", "Industry reports"]
        }
        
        # Industry-specific sources
        if "fashion" in profile.industry.lower():
            sources["trade_publications"].extend([
                "WWD", "Fashion Business", "Drapers", "Fashion Network"
            ])
        elif "manufacturing" in profile.industry.lower():
            sources["trade_publications"].extend([
                "Manufacturing News", "Industry Week", "Plant Engineering"
            ])
        elif "consumer" in profile.industry.lower():
            sources["trade_publications"].extend([
                "Consumer Goods", "Retail Dive", "Food Business Magazine"
            ])
        
        return sources
    
    def _parse_list_input(self, input_str: str) -> List[str]:
        """Parse comma-separated string into list"""
        if not input_str:
            return []
        return [item.strip() for item in input_str.split(",") if item.strip()]
    
    def _generate_keywords(self, responses: Dict[str, Any]) -> List[str]:
        """Generate keywords from responses"""
        keywords = []
        
        # Add products as keywords
        products = self._parse_list_input(responses.get("primary_products", ""))
        keywords.extend(products)
        
        # Add industry terms
        if responses.get("sub_industry"):
            keywords.append(responses["sub_industry"])
        
        # Add location terms
        if responses.get("location"):
            location_parts = responses["location"].split(", ")
            keywords.extend(location_parts)
        
        return list(set(keywords))
    
    def _calculate_completeness(self, responses: Dict[str, Any]) -> float:
        """Calculate profile completeness percentage"""
        required_fields = [
            "company_name", "industry", "primary_products", "target_markets",
            "main_challenges", "growth_goals"
        ]
        
        completed_fields = sum(1 for field in required_fields if responses.get(field))
        return (completed_fields / len(required_fields)) * 100
    
    def _calculate_completeness_from_data(self, profile_data: Dict[str, Any]) -> float:
        """Calculate profile completeness from imported data"""
        total_fields = 15
        completed_fields = 0
        
        # Check required fields
        if profile_data.get("company_name"):
            completed_fields += 1
        if profile_data.get("industry"):
            completed_fields += 1
        if profile_data.get("location"):
            completed_fields += 1
        if profile_data.get("business_size"):
            completed_fields += 1
        if profile_data.get("description"):
            completed_fields += 1
        if profile_data.get("website"):
            completed_fields += 1
        if profile_data.get("primary_products"):
            completed_fields += 1
        if profile_data.get("target_markets"):
            completed_fields += 1
        if profile_data.get("market_focus"):
            completed_fields += 1
        if profile_data.get("annual_revenue"):
            completed_fields += 1
        if profile_data.get("phone"):
            completed_fields += 1
        if profile_data.get("email"):
            completed_fields += 1
        if profile_data.get("focus_regions"):
            completed_fields += 1
        if profile_data.get("key_keywords"):
            completed_fields += 1
        if profile_data.get("preferred_languages"):
            completed_fields += 1
        
        return completed_fields / total_fields