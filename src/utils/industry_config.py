"""
Industry configuration and mapping utilities for AI Agent Prospera
Integrates NAICS classification with the existing profile system
"""

from typing import Dict, List, Tuple
from enum import Enum

class IndustryCategory(Enum):
    """Standard industry categories for AI Agent Prospera"""
    FASHION_APPAREL = "fashion_apparel"
    MANUFACTURING = "manufacturing"
    TECHNOLOGY = "technology"
    CONSUMER_ELECTRONICS = "consumer_electronics"
    HOME_LIFESTYLE = "home_lifestyle"
    FOOD_BEVERAGE = "food_beverage"
    AUTOMOTIVE = "automotive"
    MEDICAL_DEVICES = "medical_devices"
    PROFESSIONAL_SERVICES = "professional_services"
    CONSTRUCTION = "construction"
    RETAIL = "retail"
    WHOLESALE_TRADE = "wholesale"
    TRANSPORTATION = "transportation"
    ENERGY = "energy"
    AGRICULTURE = "agriculture"
    FINANCE = "finance"
    REAL_ESTATE = "real_estate"
    EDUCATION = "education"
    ENTERTAINMENT = "entertainment"
    PERSONAL_SERVICES = "personal_services"
    CONSULTING = "consulting"
    OTHER = "other"

# Mapping from NAICS classifications to Prospera industry categories
NAICS_TO_PROSPERA_MAPPING = {
    'Fashion & Apparel': IndustryCategory.FASHION_APPAREL,
    'Manufacturing': IndustryCategory.MANUFACTURING,
    'Consumer Electronics': IndustryCategory.CONSUMER_ELECTRONICS,
    'Technology': IndustryCategory.TECHNOLOGY,
    'Home & Lifestyle': IndustryCategory.HOME_LIFESTYLE,
    'Food & Beverage': IndustryCategory.FOOD_BEVERAGE,
    'Automotive': IndustryCategory.AUTOMOTIVE,
    'Medical Devices': IndustryCategory.MEDICAL_DEVICES,
    'Professional Services': IndustryCategory.PROFESSIONAL_SERVICES,
    'Construction': IndustryCategory.CONSTRUCTION,
    'Retail': IndustryCategory.RETAIL,
    'Wholesale Trade': IndustryCategory.WHOLESALE_TRADE,
    'Transportation': IndustryCategory.TRANSPORTATION,
    'Energy': IndustryCategory.ENERGY,
    'Agriculture': IndustryCategory.AGRICULTURE,
    'Finance': IndustryCategory.FINANCE,
    'Real Estate': IndustryCategory.REAL_ESTATE,
    'Education': IndustryCategory.EDUCATION,
    'Entertainment': IndustryCategory.ENTERTAINMENT,
    'Personal Services': IndustryCategory.PERSONAL_SERVICES
}

# Display names for industry categories
INDUSTRY_DISPLAY_NAMES = {
    IndustryCategory.FASHION_APPAREL: "Fashion & Apparel",
    IndustryCategory.MANUFACTURING: "Manufacturing",
    IndustryCategory.CONSUMER_ELECTRONICS: "Consumer Electronics",
    IndustryCategory.TECHNOLOGY: "Technology & Software",
    IndustryCategory.HOME_LIFESTYLE: "Home & Lifestyle",
    IndustryCategory.FOOD_BEVERAGE: "Food & Beverage",
    IndustryCategory.AUTOMOTIVE: "Automotive",
    IndustryCategory.MEDICAL_DEVICES: "Medical Devices",
    IndustryCategory.PROFESSIONAL_SERVICES: "Professional Services",
    IndustryCategory.CONSTRUCTION: "Construction",
    IndustryCategory.RETAIL: "Retail & E-commerce",
    IndustryCategory.WHOLESALE_TRADE: "Wholesale Trade",
    IndustryCategory.TRANSPORTATION: "Transportation & Logistics",
    IndustryCategory.ENERGY: "Energy & Utilities",
    IndustryCategory.AGRICULTURE: "Agriculture",
    IndustryCategory.FINANCE: "Finance & Banking",
    IndustryCategory.REAL_ESTATE: "Real Estate",
    IndustryCategory.EDUCATION: "Education & Training",
    IndustryCategory.ENTERTAINMENT: "Entertainment & Media",
    IndustryCategory.PERSONAL_SERVICES: "Personal Services",
    IndustryCategory.CONSULTING: "Consulting Services",
    IndustryCategory.OTHER: "Other"
}

def get_industry_display_name(industry_code: str) -> str:
    """Get display name for industry code"""
    try:
        category = IndustryCategory(industry_code)
        return INDUSTRY_DISPLAY_NAMES.get(category, industry_code)
    except ValueError:
        return industry_code

def get_industry_options() -> Dict[str, str]:
    """Get all industry options for dropdowns"""
    return {
        category.value: display_name 
        for category, display_name in INDUSTRY_DISPLAY_NAMES.items()
    }

def map_naics_to_prospera(naics_industry: str) -> str:
    """Map NAICS industry classification to Prospera category"""
    category = NAICS_TO_PROSPERA_MAPPING.get(naics_industry, IndustryCategory.OTHER)
    return category.value

def get_industry_keywords(industry_category: IndustryCategory) -> List[str]:
    """Get relevant keywords for an industry category"""
    keyword_mapping = {
        IndustryCategory.FASHION_APPAREL: [
            "fashion", "apparel", "clothing", "textile", "leather", "footwear", 
            "accessories", "jewelry", "handbag", "shoes"
        ],
        IndustryCategory.MANUFACTURING: [
            "manufacturing", "fabrication", "machinery", "metal", "industrial", 
            "equipment", "tools", "precision", "welding", "machining"
        ],
        IndustryCategory.TECHNOLOGY: [
            "software", "technology", "IT", "development", "programming", 
            "digital", "app", "web", "cloud", "AI", "data"
        ],
        IndustryCategory.FOOD_BEVERAGE: [
            "food", "beverage", "restaurant", "catering", "bakery", "brewery", 
            "coffee", "organic", "nutrition", "culinary"
        ],
        IndustryCategory.AUTOMOTIVE: [
            "automotive", "car", "vehicle", "truck", "motorcycle", "auto parts", 
            "repair", "dealership", "transportation"
        ]
    }
    
    return keyword_mapping.get(industry_category, [])

def get_regional_industry_strengths(location: str) -> Dict[str, float]:
    """Get regional industry strength multipliers"""
    location_lower = location.lower()
    
    regional_strengths = {
        'italy': {
            IndustryCategory.FASHION_APPAREL: 1.2,
            IndustryCategory.HOME_LIFESTYLE: 1.15,
            IndustryCategory.FOOD_BEVERAGE: 1.15,
            IndustryCategory.MANUFACTURING: 1.1
        },
        'germany': {
            IndustryCategory.MANUFACTURING: 1.2,
            IndustryCategory.AUTOMOTIVE: 1.2,
            IndustryCategory.TECHNOLOGY: 1.1,
            IndustryCategory.ENERGY: 1.1
        },
        'korea': {
            IndustryCategory.CONSUMER_ELECTRONICS: 1.2,
            IndustryCategory.TECHNOLOGY: 1.15,
            IndustryCategory.AUTOMOTIVE: 1.1
        },
        'united states': {
            IndustryCategory.TECHNOLOGY: 1.2,
            IndustryCategory.ENTERTAINMENT: 1.15,
            IndustryCategory.FINANCE: 1.15
        }
    }
    
    # Find matching region
    for region, strengths in regional_strengths.items():
        if region in location_lower:
            return {cat.value: multiplier for cat, multiplier in strengths.items()}
    
    return {}