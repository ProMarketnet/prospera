"""
Comprehensive Industry Classification System for Business Directory Import
Based on NAICS (North American Industry Classification System)
"""

from typing import Dict, List, Tuple, Optional
from enum import Enum
import re

class NAICSMapping:
    """NAICS-based industry classification and mapping system"""
    
    # Primary industry mappings for Google Places/Clearbit import
    INDUSTRY_KEYWORD_MAPPING = {
        # Fashion & Apparel (NAICS 315-316)
        'apparel': 'Fashion & Apparel',
        'clothing': 'Fashion & Apparel', 
        'fashion': 'Fashion & Apparel',
        'leather': 'Fashion & Apparel',
        'footwear': 'Fashion & Apparel',
        'shoes': 'Fashion & Apparel',
        'textile': 'Fashion & Apparel',
        'garment': 'Fashion & Apparel',
        'accessories': 'Fashion & Apparel',
        'jewelry': 'Fashion & Apparel',
        'handbag': 'Fashion & Apparel',
        'belt': 'Fashion & Apparel',
        
        # Manufacturing (NAICS 331-339)
        'manufacturing': 'Manufacturing',
        'fabrication': 'Manufacturing',
        'machinery': 'Manufacturing',
        'metal': 'Manufacturing',
        'steel': 'Manufacturing',
        'aluminum': 'Manufacturing',
        'welding': 'Manufacturing',
        'machining': 'Manufacturing',
        'industrial': 'Manufacturing',
        'equipment': 'Manufacturing',
        'tools': 'Manufacturing',
        'automotive parts': 'Manufacturing',
        'precision': 'Manufacturing',
        
        # Home & Lifestyle (NAICS 321, 337)
        'furniture': 'Home & Lifestyle',
        'wood': 'Home & Lifestyle',
        'cabinet': 'Home & Lifestyle',
        'millwork': 'Home & Lifestyle',
        'home decor': 'Home & Lifestyle',
        'kitchen': 'Home & Lifestyle',
        'interior': 'Home & Lifestyle',
        'design': 'Home & Lifestyle',
        
        # Consumer Electronics (NAICS 334-335)
        'electronics': 'Consumer Electronics',
        'appliance': 'Consumer Electronics',
        'computer': 'Consumer Electronics',
        'smartphone': 'Consumer Electronics',
        'device': 'Consumer Electronics',
        'semiconductor': 'Consumer Electronics',
        'electrical': 'Consumer Electronics',
        'audio': 'Consumer Electronics',
        'video': 'Consumer Electronics',
        
        # Food & Beverage (NAICS 311-312)
        'food': 'Food & Beverage',
        'beverage': 'Food & Beverage',
        'restaurant': 'Food & Beverage',
        'catering': 'Food & Beverage',
        'bakery': 'Food & Beverage',
        'brewery': 'Food & Beverage',
        'coffee': 'Food & Beverage',
        'organic': 'Food & Beverage',
        'specialty food': 'Food & Beverage',
        'nutrition': 'Food & Beverage',
        
        # Automotive (NAICS 336)
        'automotive': 'Automotive',
        'car': 'Automotive',
        'vehicle': 'Automotive',
        'truck': 'Automotive',
        'motorcycle': 'Automotive',
        'auto parts': 'Automotive',
        'repair': 'Automotive',
        'dealership': 'Automotive',
        
        # Medical Devices (NAICS 339)
        'medical': 'Medical Devices',
        'healthcare': 'Medical Devices',
        'pharmaceutical': 'Medical Devices',
        'surgical': 'Medical Devices',
        'dental': 'Medical Devices',
        'laboratory': 'Medical Devices',
        'diagnostic': 'Medical Devices',
        'biotechnology': 'Medical Devices',
        
        # Professional Services (NAICS 54)
        'consulting': 'Professional Services',
        'legal': 'Professional Services',
        'accounting': 'Professional Services',
        'engineering': 'Professional Services',
        'architecture': 'Professional Services',
        'marketing': 'Professional Services',
        'advertising': 'Professional Services',
        'design services': 'Professional Services',
        
        # Technology (NAICS 51, 54)
        'software': 'Technology',
        'technology': 'Technology',
        'IT': 'Technology',
        'development': 'Technology',
        'programming': 'Technology',
        'digital': 'Technology',
        'app': 'Technology',
        'web': 'Technology',
        'cloud': 'Technology',
        'AI': 'Technology',
        'data': 'Technology',
        
        # Construction (NAICS 23)
        'construction': 'Construction',
        'building': 'Construction',
        'contractor': 'Construction',
        'renovation': 'Construction',
        'plumbing': 'Construction',
        'electrical contractor': 'Construction',
        'roofing': 'Construction',
        
        # Retail (NAICS 44-45)
        'retail': 'Retail',
        'store': 'Retail',
        'shop': 'Retail',
        'boutique': 'Retail',
        'e-commerce': 'Retail',
        'online store': 'Retail',
        'marketplace': 'Retail',
        
        # Wholesale Trade (NAICS 42)
        'wholesale': 'Wholesale Trade',
        'distribution': 'Wholesale Trade',
        'distributor': 'Wholesale Trade',
        'supply': 'Wholesale Trade',
        'import': 'Wholesale Trade',
        'export': 'Wholesale Trade',
        
        # Transportation (NAICS 48-49)
        'transportation': 'Transportation',
        'logistics': 'Transportation',
        'shipping': 'Transportation',
        'freight': 'Transportation',
        'delivery': 'Transportation',
        'trucking': 'Transportation',
        
        # Energy (NAICS 21-22)
        'energy': 'Energy',
        'oil': 'Energy',
        'gas': 'Energy',
        'renewable': 'Energy',
        'solar': 'Energy',
        'wind': 'Energy',
        'utility': 'Energy',
        
        # Agriculture (NAICS 11)
        'agriculture': 'Agriculture',
        'farming': 'Agriculture',
        'crop': 'Agriculture',
        'livestock': 'Agriculture',
        'organic farming': 'Agriculture',
        'aquaculture': 'Agriculture',
        
        # Finance (NAICS 52)
        'finance': 'Finance',
        'banking': 'Finance',
        'insurance': 'Finance',
        'investment': 'Finance',
        'fintech': 'Finance',
        'accounting': 'Finance',
        
        # Real Estate (NAICS 53)
        'real estate': 'Real Estate',
        'property': 'Real Estate',
        'development': 'Real Estate',
        'property management': 'Real Estate',
        
        # Education (NAICS 61)
        'education': 'Education',
        'school': 'Education',
        'training': 'Education',
        'university': 'Education',
        'learning': 'Education',
        
        # Entertainment (NAICS 71)
        'entertainment': 'Entertainment',
        'media': 'Entertainment',
        'gaming': 'Entertainment',
        'sports': 'Entertainment',
        'event': 'Entertainment',
        
        # Personal Services (NAICS 81)
        'beauty': 'Personal Services',
        'wellness': 'Personal Services',
        'fitness': 'Personal Services',
        'spa': 'Personal Services',
        'salon': 'Personal Services'
    }
    
    # Standardized industry categories for Prospera profiles
    PROSPERA_INDUSTRIES = [
        'Fashion & Apparel',
        'Manufacturing', 
        'Consumer Electronics',
        'Home & Lifestyle',
        'Food & Beverage',
        'Automotive',
        'Medical Devices',
        'Professional Services',
        'Technology',
        'Construction',
        'Retail',
        'Wholesale Trade',
        'Transportation',
        'Energy',
        'Agriculture',
        'Finance',
        'Real Estate',
        'Education',
        'Entertainment',
        'Personal Services',
        'Other'
    ]
    
    # Geographic industry strengths
    REGIONAL_INDUSTRY_STRENGTHS = {
        'italy': {
            'Fashion & Apparel': 0.95,
            'Home & Lifestyle': 0.90,
            'Food & Beverage': 0.90,
            'Manufacturing': 0.85,
            'Automotive': 0.80
        },
        'germany': {
            'Manufacturing': 0.95,
            'Automotive': 0.95,
            'Technology': 0.85,
            'Energy': 0.80,
            'Medical Devices': 0.80
        },
        'korea': {
            'Consumer Electronics': 0.95,
            'Technology': 0.90,
            'Automotive': 0.85,
            'Manufacturing': 0.80
        },
        'united states': {
            'Technology': 0.95,
            'Consumer Electronics': 0.90,
            'Food & Beverage': 0.85,
            'Entertainment': 0.90,
            'Finance': 0.90
        },
        'china': {
            'Manufacturing': 0.95,
            'Consumer Electronics': 0.90,
            'Technology': 0.85,
            'Fashion & Apparel': 0.80
        },
        'japan': {
            'Consumer Electronics': 0.95,
            'Automotive': 0.95,
            'Technology': 0.90,
            'Manufacturing': 0.85
        }
    }

class IndustryClassifier:
    """Advanced industry classification system for business directory import"""
    
    def __init__(self):
        self.mapping = NAICSMapping()
    
    def classify_business(self, business_data: Dict) -> Tuple[str, float]:
        """
        Classify business into industry category with confidence score
        
        Args:
            business_data: Dictionary containing business information
            
        Returns:
            Tuple of (industry_category, confidence_score)
        """
        
        # Extract text content for analysis
        text_content = self._extract_classification_text(business_data)
        
        # Multi-level classification approach
        classifications = []
        
        # 1. Direct industry field matching
        if 'industry' in business_data and business_data['industry']:
            industry_match = self._match_industry_field(business_data['industry'])
            if industry_match:
                classifications.append((industry_match, 0.9))
        
        # 2. Business category/type matching
        if 'category' in business_data or 'business_type' in business_data:
            category = business_data.get('category', business_data.get('business_type', ''))
            category_match = self._match_keywords(category)
            if category_match:
                classifications.append((category_match, 0.8))
        
        # 3. Company name analysis
        if 'company_name' in business_data:
            name_match = self._match_keywords(business_data['company_name'])
            if name_match:
                classifications.append((name_match, 0.6))
        
        # 4. Description/content analysis
        description_match = self._match_keywords(text_content)
        if description_match:
            classifications.append((description_match, 0.7))
        
        # 5. Products/services analysis
        if 'products' in business_data or 'services' in business_data:
            products = ' '.join(business_data.get('products', []) + business_data.get('services', []))
            product_match = self._match_keywords(products)
            if product_match:
                classifications.append((product_match, 0.8))
        
        # Select best classification
        if classifications:
            # Group by industry and sum confidence scores
            industry_scores = {}
            for industry, confidence in classifications:
                if industry in industry_scores:
                    industry_scores[industry] += confidence
                else:
                    industry_scores[industry] = confidence
            
            # Get highest scoring industry
            best_industry = max(industry_scores.items(), key=lambda x: x[1])
            
            # Normalize confidence score
            max_possible_score = len(classifications)
            normalized_confidence = min(best_industry[1] / max_possible_score, 1.0)
            
            return best_industry[0], normalized_confidence
        
        return 'Other', 0.1
    
    def _extract_classification_text(self, business_data: Dict) -> str:
        """Extract all relevant text content for classification"""
        
        text_parts = []
        
        # Add various text fields
        text_fields = ['description', 'about', 'overview', 'services', 'products', 'specialties']
        
        for field in text_fields:
            if field in business_data and business_data[field]:
                if isinstance(business_data[field], list):
                    text_parts.extend(business_data[field])
                else:
                    text_parts.append(str(business_data[field]))
        
        return ' '.join(text_parts).lower()
    
    def _match_industry_field(self, industry_text: str) -> Optional[str]:
        """Match direct industry field to standardized categories"""
        
        industry_lower = industry_text.lower()
        
        # Direct mapping for common industry descriptions
        direct_mappings = {
            'manufacturing': 'Manufacturing',
            'technology': 'Technology',
            'software': 'Technology',
            'retail': 'Retail',
            'food service': 'Food & Beverage',
            'apparel': 'Fashion & Apparel',
            'construction': 'Construction',
            'healthcare': 'Medical Devices',
            'automotive': 'Automotive',
            'finance': 'Finance',
            'real estate': 'Real Estate',
            'consulting': 'Professional Services'
        }
        
        for key, value in direct_mappings.items():
            if key in industry_lower:
                return value
        
        # Fallback to keyword matching
        return self._match_keywords(industry_text)
    
    def _match_keywords(self, text: str) -> Optional[str]:
        """Match keywords in text to industry categories"""
        
        if not text:
            return None
        
        text_lower = text.lower()
        
        # Count matches for each industry
        industry_matches = {}
        
        for keyword, industry in self.mapping.INDUSTRY_KEYWORD_MAPPING.items():
            if keyword in text_lower:
                if industry in industry_matches:
                    industry_matches[industry] += 1
                else:
                    industry_matches[industry] = 1
        
        if industry_matches:
            # Return industry with most matches
            return max(industry_matches.items(), key=lambda x: x[1])[0]
        
        return None
    
    def enhance_with_regional_context(self, industry: str, confidence: float, location: str) -> Tuple[str, float]:
        """Enhance classification with regional industry strengths"""
        
        if not location:
            return industry, confidence
        
        location_lower = location.lower()
        
        # Find matching region
        region_multiplier = 1.0
        for region, strengths in self.mapping.REGIONAL_INDUSTRY_STRENGTHS.items():
            if region in location_lower:
                if industry in strengths:
                    region_multiplier = strengths[industry]
                break
        
        # Adjust confidence based on regional strength
        enhanced_confidence = min(confidence * region_multiplier, 1.0)
        
        return industry, enhanced_confidence
    
    def get_industry_suggestions(self, partial_text: str) -> List[str]:
        """Get industry suggestions for autocomplete/search"""
        
        if not partial_text:
            return self.mapping.PROSPERA_INDUSTRIES[:10]
        
        partial_lower = partial_text.lower()
        
        # Find matching industries
        matches = []
        for industry in self.mapping.PROSPERA_INDUSTRIES:
            if partial_lower in industry.lower():
                matches.append(industry)
        
        # Find matching keywords
        keyword_matches = set()
        for keyword, industry in self.mapping.INDUSTRY_KEYWORD_MAPPING.items():
            if partial_lower in keyword:
                keyword_matches.add(industry)
        
        # Combine and deduplicate
        all_matches = list(set(matches + list(keyword_matches)))
        
        return all_matches[:10]
    
    def get_sub_industries(self, main_industry: str) -> List[str]:
        """Get sub-industry categories for detailed classification"""
        
        sub_industries = {
            'Fashion & Apparel': [
                'Clothing Manufacturing',
                'Footwear & Leather Goods',
                'Textile Manufacturing', 
                'Jewelry & Accessories',
                'Fashion Design'
            ],
            'Manufacturing': [
                'Metal Fabrication',
                'Machinery Manufacturing',
                'Industrial Equipment',
                'Precision Manufacturing',
                'Custom Manufacturing'
            ],
            'Technology': [
                'Software Development',
                'IT Services',
                'Digital Marketing',
                'Mobile Apps',
                'AI & Machine Learning'
            ],
            'Food & Beverage': [
                'Food Manufacturing',
                'Restaurants',
                'Catering Services',
                'Specialty Foods',
                'Beverage Production'
            ],
            'Professional Services': [
                'Consulting',
                'Legal Services',
                'Accounting',
                'Marketing & Advertising',
                'Engineering Services'
            ]
        }
        
        return sub_industries.get(main_industry, [])
    
    def validate_industry_classification(self, industry: str, business_data: Dict) -> bool:
        """Validate if industry classification makes sense for the business"""
        
        if industry not in self.mapping.PROSPERA_INDUSTRIES:
            return False
        
        # Re-classify and check if results are consistent
        classified_industry, confidence = self.classify_business(business_data)
        
        # Accept if same industry or confidence is low (ambiguous case)
        return classified_industry == industry or confidence < 0.5