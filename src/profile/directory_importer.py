import requests
import json
from typing import Dict, List, Any, Optional
import os
from dataclasses import dataclass
import re
from urllib.parse import urlparse
import trafilatura

from ..utils.logger import setup_logger
from .business_profile import BusinessProfileManager
from .industry_classifier import IndustryClassifier

logger = setup_logger(__name__)

@dataclass
class BusinessDirectoryData:
    """Standardized business data from multiple directory sources"""
    company_name: str
    website: str
    industry: str
    description: str
    location: str
    employee_count: str
    annual_revenue: str
    phone: str
    email: str
    social_media: Dict[str, str]
    products_services: List[str]
    target_markets: List[str]
    company_logo: str
    founded_year: str
    company_size: str
    business_type: str
    confidence_score: float
    data_sources: List[str]

class BusinessDirectoryImporter:
    """Import and aggregate business data from multiple directory sources"""
    
    def __init__(self):
        self.industry_classifier = IndustryClassifier()
        self.profile_manager = BusinessProfileManager()
    
    def search_business_by_name(self, company_name: str, location: str = "") -> List[BusinessDirectoryData]:
        """Search for business using web scraping and public sources"""
        results = []
        
        # Search using website discovery
        website_results = self._discover_company_website(company_name, location)
        if website_results:
            results.extend(website_results)
        
        # Sort by confidence score
        results.sort(key=lambda x: x.confidence_score, reverse=True)
        
        return results[:3]  # Return top 3 matches
    
    def search_business_by_website(self, website: str) -> Optional[BusinessDirectoryData]:
        """Search for business by website URL"""
        
        # Clean website URL
        cleaned_url = self._clean_website_url(website)
        
        # Extract business data from website
        result = self._extract_website_data(cleaned_url)
        
        return result
    
    def import_business_profile(self, search_query: str, location: str = "") -> Dict[str, Any]:
        """Main method to import business profile data"""
        
        # Determine if search query is a website or company name
        if self._is_website_url(search_query):
            business_data = self.search_business_by_website(search_query)
            candidates = [business_data] if business_data else []
        else:
            candidates = self.search_business_by_name(search_query, location)
        
        if not candidates:
            return {"status": "not_found", "message": "No business found matching your search"}
        
        # Return formatted profile data
        best_match = candidates[0]
        profile_data = self._convert_to_profile_format(best_match)
        
        return {
            "status": "found",
            "profile_data": profile_data,
            "alternatives": [self._convert_to_profile_format(c) for c in candidates[1:3]],
            "confidence": best_match.confidence_score,
            "data_sources": best_match.data_sources
        }
    
    def _discover_company_website(self, company_name: str, location: str = "") -> List[BusinessDirectoryData]:
        """Discover company website using web search simulation"""
        results = []
        
        try:
            # Common website patterns
            domain_variations = [
                f"{company_name.lower().replace(' ', '')}.com",
                f"{company_name.lower().replace(' ', '-')}.com",
                f"{company_name.lower().replace(' ', '')}.net",
                f"www.{company_name.lower().replace(' ', '')}.com"
            ]
            
            for domain in domain_variations:
                try:
                    # Test if domain exists and extract data
                    url = f"https://{domain}"
                    business_data = self._extract_website_data(url)
                    if business_data and business_data.company_name:
                        results.append(business_data)
                        break  # Stop at first successful match
                except:
                    continue
                    
        except Exception as e:
            print(f"Error discovering website: {str(e)}")
        
        return results
    
    def _extract_website_data(self, website_url: str) -> Optional[BusinessDirectoryData]:
        """Extract business data from company website"""
        
        try:
            # Clean URL
            if not website_url.startswith(('http://', 'https://')):
                website_url = f"https://{website_url}"
            
            # Fetch website content
            downloaded = trafilatura.fetch_url(website_url)
            if not downloaded:
                return None
                
            # Extract main text content
            text_content = trafilatura.extract(downloaded)
            if not text_content:
                return None
            
            # Parse business information from content
            business_data = self._parse_website_content(text_content, website_url)
            
            return business_data
            
        except Exception as e:
            print(f"Error extracting website data: {str(e)}")
            return None
    
    def _parse_website_content(self, content: str, website_url: str) -> Optional[BusinessDirectoryData]:
        """Parse business information from website content"""
        
        try:
            # Extract company name from URL domain
            domain = urlparse(website_url).netloc.replace('www.', '')
            company_name = domain.split('.')[0].replace('-', ' ').title()
            
            # Extract description (first meaningful paragraph)
            description = self._extract_description(content)
            
            # Extract contact information
            phone = self._extract_phone(content)
            email = self._extract_email(content)
            location = self._extract_location(content)
            
            # Extract products/services
            products_services = self._extract_products_services(content)
            
            # Determine industry using advanced classification
            business_data_for_classification = {
                'description': description,
                'content': content,
                'company_name': company_name,
                'website': website_url,
                'location': location,
                'products': products_services
            }
            industry, confidence = self.industry_classifier.classify_business(business_data_for_classification)
            
            # Enhance with regional context if location is available
            if location and location != "Location not specified":
                industry, confidence = self.industry_classifier.enhance_with_regional_context(
                    industry, confidence, location
                )
            
            return BusinessDirectoryData(
                company_name=company_name,
                website=website_url,
                industry=industry,
                description=description,
                location=location,
                employee_count="Not specified",
                annual_revenue="Not available",
                phone=phone,
                email=email,
                social_media={},
                products_services=products_services,
                target_markets=[],
                company_logo="",
                founded_year="",
                company_size="Small Business",
                business_type="Company",
                confidence_score=0.8,
                data_sources=["Company Website"]
            )
            
        except Exception as e:
            print(f"Error parsing website content: {str(e)}")
            return None
    
    def _extract_description(self, content: str) -> str:
        """Extract company description from content"""
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if len(line) > 50 and len(line) < 300:
                # Check if it's a descriptive sentence
                if any(keyword in line.lower() for keyword in ['company', 'business', 'we are', 'we provide', 'leading', 'specializes']):
                    return line
        return "Business description not available"
    
    def _determine_industry_from_content(self, content: str) -> str:
        """Determine industry based on content keywords"""
        # Use the advanced industry classifier
        business_data = {
            'description': content,
            'content': content
        }
        
        industry, confidence = self.industry_classifier.classify_business(business_data)
        logger.info(f"Industry classified as '{industry}' with confidence {confidence:.2f}")
        
        return industry
    
    def _extract_phone(self, content: str) -> str:
        """Extract phone number from content"""
        phone_pattern = r'[\+]?[1-9]?[0-9]{7,15}'
        matches = re.findall(phone_pattern, content)
        return matches[0] if matches else ""
    
    def _extract_email(self, content: str) -> str:
        """Extract email from content"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.findall(email_pattern, content)
        return matches[0] if matches else ""
    
    def _extract_location(self, content: str) -> str:
        """Extract location from content"""
        # Look for address patterns
        location_keywords = ['address', 'location', 'based in', 'headquarters', 'office']
        lines = content.split('\n')
        
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in location_keywords):
                # Extract the line and clean it
                location = line.strip()
                if len(location) > 10 and len(location) < 100:
                    return location
        
        return "Location not specified"
    
    def _extract_products_services(self, content: str) -> List[str]:
        """Extract products and services from content"""
        service_keywords = ['services', 'products', 'solutions', 'offerings']
        products = []
        
        lines = content.split('\n')
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in service_keywords):
                # Look for list items or comma-separated services
                if ',' in line:
                    items = [item.strip() for item in line.split(',')]
                    products.extend(items[:3])  # Limit to 3 items
                    break
        
        return products[:5]  # Limit to 5 products/services
    
    def _clean_website_url(self, url: str) -> str:
        """Clean and validate website URL"""
        url = url.strip().lower()
        if not url.startswith(('http://', 'https://')):
            url = f"https://{url}"
        return url
    
    def _is_website_url(self, query: str) -> bool:
        """Check if query is a website URL"""
        return '.' in query and ' ' not in query
    
    def _convert_to_profile_format(self, business_data: BusinessDirectoryData) -> Dict[str, Any]:
        """Convert BusinessDirectoryData to profile format"""
        return {
            'company_name': business_data.company_name,
            'industry': self._map_to_standard_industry(business_data.industry),
            'sub_industry': business_data.industry,
            'business_size': self._map_to_business_size(business_data.employee_count),
            'annual_revenue': self._map_to_revenue_range(business_data.annual_revenue),
            'location': business_data.location,
            'website': business_data.website,
            'phone': business_data.phone,
            'email': business_data.email,
            'description': business_data.description,
            'primary_products': business_data.products_services,
            'target_markets': business_data.target_markets or ['General Market'],
            'market_focus': 'Local' if 'local' in business_data.description.lower() else 'National',
            'unique_selling_points': [],
            'main_challenges': [],
            'growth_goals': [],
            'target_revenue_growth': 'Steady Growth',
            'focus_regions': [business_data.location] if business_data.location else [],
            'competitor_companies': [],
            'key_keywords': business_data.products_services,
            'preferred_languages': ['English']
        }
    
    def _map_to_standard_industry(self, industry: str) -> str:
        """Map industry to standard options using NAICS classification"""
        # Use the NAICS industry classifier to get standardized mapping
        industry_map = {
            'Fashion & Apparel': 'fashion_apparel',
            'Manufacturing': 'manufacturing',
            'Consumer Electronics': 'technology',
            'Technology': 'tech_software',
            'Home & Lifestyle': 'home_lifestyle',
            'Food & Beverage': 'food_beverage',
            'Automotive': 'automotive',
            'Medical Devices': 'healthcare',
            'Professional Services': 'consulting',
            'Construction': 'construction',
            'Retail': 'retail',
            'Wholesale Trade': 'wholesale',
            'Transportation': 'transportation',
            'Energy': 'energy',
            'Agriculture': 'agriculture',
            'Finance': 'finance',
            'Real Estate': 'real_estate',
            'Education': 'education',
            'Entertainment': 'entertainment',
            'Personal Services': 'personal_services'
        }
        return industry_map.get(industry, 'consulting')
    
    def _map_to_business_size(self, employee_count: str) -> str:
        """Map employee count to business size enum"""
        if not employee_count or employee_count == "Not specified":
            return 'small'
        
        try:
            count = int(employee_count.split('-')[0])
            if count < 10:
                return 'startup'
            elif count < 50:
                return 'small'
            elif count < 250:
                return 'medium'
            else:
                return 'large'
        except:
            return 'small'
    
    def _map_to_revenue_range(self, revenue: str) -> str:
        """Map revenue to standard ranges"""
        if not revenue or revenue == "Not available":
            return 'undisclosed'
        
        revenue_lower = revenue.lower()
        if 'million' in revenue_lower:
            return 'million_plus'
        elif 'thousand' in revenue_lower or 'k' in revenue_lower:
            return 'hundred_thousand'
        else:
            return 'undisclosed'