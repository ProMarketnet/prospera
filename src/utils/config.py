import os
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

class Config:
    """Configuration management for the application"""
    
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    NEWS_API_KEY = os.getenv('NEWS_API_KEY')
    TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
    GOOGLE_CSE_ID = os.getenv('GOOGLE_CSE_ID')
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    
    # Data Directories
    DATA_RAW_DIR = "data/raw"
    DATA_PROCESSED_DIR = "data/processed"
    REPORTS_DIR = "data/reports"
    
    # NAICS-Based Industries Configuration - Complete 20 Sector Classification
    INDUSTRIES = {
        # Goods-Producing Industries (5 sectors)
        "agriculture": {
            "name": "Agriculture, Forestry, Fishing & Hunting",
            "naics_code": "11",
            "description": "Crop Production, Animal Production, Forestry and Logging, Fishing and Hunting",
            "keywords": ["agriculture", "farming", "crop", "livestock", "forestry", "fishing", "hunting", "organic farming", "aquaculture"],
            "trade_sites": [
                "https://www.agriculture.com/",
                "https://www.farm-equipment.com/",
                "https://www.farmprogress.com/"
            ]
        },
        "mining_extraction": {
            "name": "Mining, Quarrying & Oil/Gas Extraction", 
            "naics_code": "21",
            "description": "Oil and Gas Extraction, Mining (except Oil and Gas), Support Activities for Mining",
            "keywords": ["mining", "oil", "gas", "extraction", "quarrying", "petroleum", "coal", "mineral extraction"],
            "trade_sites": [
                "https://www.mining.com/",
                "https://www.rigzone.com/",
                "https://www.oilandgasjournal.com/"
            ]
        },
        "utilities": {
            "name": "Utilities",
            "naics_code": "22", 
            "description": "Electric Power Generation, Natural Gas Distribution, Water and Sewer Systems",
            "keywords": ["utilities", "electric", "power", "gas", "water", "sewer", "renewable energy", "solar", "wind"],
            "trade_sites": [
                "https://www.utilitydive.com/",
                "https://www.powermag.com/",
                "https://www.renewableenergyworld.com/"
            ]
        },
        "construction": {
            "name": "Construction",
            "naics_code": "23",
            "description": "Construction of Buildings, Heavy and Civil Engineering, Specialty Trade Contractors",
            "keywords": ["construction", "building", "contractor", "renovation", "civil engineering", "residential", "commercial"],
            "trade_sites": [
                "https://www.constructiondive.com/",
                "https://www.constructionequipment.com/",
                "https://www.enr.com/"
            ]
        },
        "manufacturing": {
            "name": "Manufacturing",
            "naics_code": "31-33",
            "description": "Food, Textile, Apparel, Leather, Wood, Paper, Chemical, Plastics, Metal, Machinery, Electronics, Transportation Equipment",
            "keywords": ["manufacturing", "industrial", "machinery", "equipment", "automation", "industry 4.0", "supply chain", "fabrication"],
            "subcategories": {
                "food_manufacturing": "Food Manufacturing (NAICS 311)",
                "textile_apparel": "Textile & Apparel Manufacturing (NAICS 313-315)", 
                "leather_products": "Leather & Allied Products (NAICS 316)",
                "wood_products": "Wood Product Manufacturing (NAICS 321)",
                "chemical_manufacturing": "Chemical Manufacturing (NAICS 325)",
                "plastics_rubber": "Plastics & Rubber Products (NAICS 326)",
                "metal_fabrication": "Fabricated Metal Products (NAICS 332)",
                "machinery": "Machinery Manufacturing (NAICS 333)",
                "electronics": "Computer & Electronic Products (NAICS 334)",
                "transportation_equipment": "Transportation Equipment (NAICS 336)",
                "furniture": "Furniture & Related Products (NAICS 337)"
            },
            "trade_sites": [
                "https://www.manufacturingnews.com/",
                "https://www.industryweek.com/",
                "https://www.manufacturing.net/"
            ]
        },
        
        # Service-Providing Industries (15 sectors)
        "wholesale_trade": {
            "name": "Wholesale Trade",
            "naics_code": "42",
            "description": "Merchant Wholesalers, Electronic Markets and Agents",
            "keywords": ["wholesale", "distribution", "supply chain", "B2B", "merchant", "distributor"],
            "trade_sites": [
                "https://www.wholesaler.com/",
                "https://www.inboundlogistics.com/"
            ]
        },
        "retail_trade": {
            "name": "Retail Trade", 
            "naics_code": "44-45",
            "description": "Motor Vehicle Dealers, Electronics Stores, Clothing Stores, Food Stores, General Merchandise",
            "keywords": ["retail", "store", "shopping", "e-commerce", "consumer", "merchandise", "omnichannel"],
            "trade_sites": [
                "https://www.retaildive.com/",
                "https://nrf.com/",
                "https://www.retailwire.com/"
            ]
        },
        "transportation_warehousing": {
            "name": "Transportation & Warehousing",
            "naics_code": "48-49", 
            "description": "Air, Water, Truck, Rail Transportation, Pipeline, Warehousing and Storage",
            "keywords": ["transportation", "logistics", "shipping", "freight", "warehousing", "supply chain", "delivery"],
            "trade_sites": [
                "https://www.supplychaindive.com/",
                "https://www.freightwaves.com/",
                "https://www.logisticsmgmt.com/"
            ]
        },
        "information": {
            "name": "Information",
            "naics_code": "51",
            "description": "Publishing, Motion Picture, Broadcasting, Telecommunications, Data Processing",
            "keywords": ["media", "publishing", "broadcasting", "telecommunications", "data processing", "internet"],
            "trade_sites": [
                "https://www.broadcastingcable.com/",
                "https://www.fiercetelecom.com/"
            ]
        },
        "finance_insurance": {
            "name": "Finance & Insurance", 
            "naics_code": "52",
            "description": "Credit Intermediation, Securities, Insurance Carriers and Related Activities",
            "keywords": ["finance", "banking", "insurance", "investment", "fintech", "credit", "securities"],
            "trade_sites": [
                "https://www.americanbanker.com/",
                "https://www.insurancejournal.com/",
                "https://www.finextra.com/"
            ]
        },
        "real_estate": {
            "name": "Real Estate & Rental/Leasing",
            "naics_code": "53", 
            "description": "Real Estate, Rental and Leasing Services",
            "keywords": ["real estate", "property", "rental", "leasing", "commercial property", "residential"],
            "trade_sites": [
                "https://www.realtor.com/news/",
                "https://www.multihousingnews.com/"
            ]
        },
        "professional_services": {
            "name": "Professional, Scientific & Technical Services",
            "naics_code": "54",
            "description": "Legal, Accounting, Engineering, Computer Systems Design, Management Consulting, Research",
            "keywords": ["consulting", "legal", "accounting", "engineering", "architecture", "research", "professional services"],
            "trade_sites": [
                "https://www.consultingmag.com/",
                "https://www.computerworld.com/"
            ]
        },
        "management_enterprises": {
            "name": "Management of Companies & Enterprises",
            "naics_code": "55",
            "description": "Management of Companies and Enterprises", 
            "keywords": ["management", "holding companies", "corporate headquarters"],
            "trade_sites": []
        },
        "administrative_support": {
            "name": "Administrative & Support Services",
            "naics_code": "56",
            "description": "Administrative and Support Services, Waste Management",
            "keywords": ["administrative", "support services", "waste management", "business support"],
            "trade_sites": []
        },
        "educational_services": {
            "name": "Educational Services",
            "naics_code": "61",
            "description": "Educational Services",
            "keywords": ["education", "school", "university", "training", "learning", "academic"],
            "trade_sites": [
                "https://www.educationdive.com/",
                "https://www.insidehighered.com/"
            ]
        },
        "healthcare": {
            "name": "Health Care & Social Assistance", 
            "naics_code": "62",
            "description": "Ambulatory Health Care, Hospitals, Nursing Care, Social Assistance",
            "keywords": ["healthcare", "medical", "hospital", "nursing", "social assistance", "health services"],
            "trade_sites": [
                "https://www.healthcaredive.com/",
                "https://www.modernhealthcare.com/"
            ]
        },
        "arts_entertainment": {
            "name": "Arts, Entertainment & Recreation",
            "naics_code": "71", 
            "description": "Performing Arts, Sports, Museums, Amusement and Recreation",
            "keywords": ["entertainment", "arts", "sports", "recreation", "gaming", "amusement", "cultural"],
            "trade_sites": [
                "https://variety.com/",
                "https://www.sportsbusinessjournal.com/"
            ]
        },
        "accommodation_food": {
            "name": "Accommodation & Food Services",
            "naics_code": "72",
            "description": "Accommodation, Food Services and Drinking Places", 
            "keywords": ["hospitality", "hotel", "restaurant", "food service", "accommodation", "tourism"],
            "trade_sites": [
                "https://www.hotel-online.com/",
                "https://www.restaurantbusinessonline.com/"
            ]
        },
        "other_services": {
            "name": "Other Services (except Public Administration)",
            "naics_code": "81",
            "description": "Repair and Maintenance, Personal Services, Religious Organizations",
            "keywords": ["repair", "maintenance", "personal services", "religious", "automotive repair"],
            "trade_sites": []
        },
        "public_administration": {
            "name": "Public Administration", 
            "naics_code": "92",
            "description": "Government, Justice, Public Order, National Security",
            "keywords": ["government", "public", "administration", "justice", "security", "municipal"],
            "trade_sites": [
                "https://www.governing.com/",
                "https://www.govtech.com/"
            ]
        },
        
        # High-Priority SME Focus Industries
        "fashion_apparel": {
            "name": "Fashion & Apparel (SME Focus)",
            "naics_code": "315-316",
            "description": "Cut and Sew Apparel, Leather Products, Footwear, Fashion Accessories",
            "keywords": ["fashion", "apparel", "clothing", "textile", "garment", "luxury fashion", "fast fashion", "sustainable fashion", "leather", "footwear"],
            "regional_strength": {
                "italy": 0.95,
                "france": 0.90, 
                "usa": 0.85
            },
            "trade_sites": [
                "https://www.fashionbiz.com.au/news",
                "https://wwd.com/",
                "https://www.fibre2fashion.com/news/",
                "https://fashionunited.com/news"
            ]
        },
        "technology_software": {
            "name": "Technology & Software", 
            "naics_code": "54+51",
            "description": "Software Development, IT Services, Computer Systems Design, Digital Services",
            "keywords": ["technology", "software", "IT", "digital", "app development", "SaaS", "cloud", "AI", "machine learning"],
            "regional_strength": {
                "usa": 0.95,
                "india": 0.90,
                "china": 0.85
            },
            "trade_sites": [
                "https://techcrunch.com/",
                "https://www.computerworld.com/",
                "https://www.infoworld.com/"
            ]
        },
        "consumer_electronics": {
            "name": "Consumer Electronics",
            "naics_code": "334-335", 
            "description": "Electronic Equipment, Appliances, Consumer Devices",
            "keywords": ["electronics", "consumer devices", "appliances", "smartphones", "computers", "wearables"],
            "regional_strength": {
                "korea": 0.95,
                "china": 0.90,
                "japan": 0.90
            },
            "trade_sites": [
                "https://www.electronicdesign.com/",
                "https://www.eetimes.com/"
            ]
        }
    }
    
    # SME Priority Rankings (1-3, where 1 is highest priority)
    SME_PRIORITY_INDUSTRIES = {
        # Tier 1: Primary SME Focus
        "fashion_apparel": 1,
        "manufacturing": 1, 
        "consumer_electronics": 1,
        "technology_software": 1,
        
        # Tier 2: Secondary SME Focus
        "professional_services": 2,
        "retail_trade": 2,
        "accommodation_food": 2,
        "arts_entertainment": 2,
        
        # Tier 3: Broader Business Categories
        "wholesale_trade": 3,
        "construction": 3,
        "healthcare": 3,
        "finance_insurance": 3,
        "real_estate": 3,
        "transportation_warehousing": 3,
        "information": 3,
        "educational_services": 3,
        "administrative_support": 3,
        "other_services": 3,
        "utilities": 3,
        "mining_extraction": 3,
        "agriculture": 3,
        "management_enterprises": 3,
        "public_administration": 3
    }
    
    # OpenAI Configuration
    # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
    # do not change this unless explicitly requested by the user
    OPENAI_MODEL = "gpt-4o"
    MAX_TOKENS = 2000
    TEMPERATURE = 0.7
    
    @classmethod
    def get_industry_options(cls):
        """Get formatted industry options for dropdown"""
        return {key: data["name"] for key, data in cls.INDUSTRIES.items()}

config = Config()
