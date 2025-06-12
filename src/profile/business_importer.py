"""
Business Profile Importer
Automatically imports business information from multiple data sources
"""

import os
import json
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime
import trafilatura
from bs4 import BeautifulSoup

class BusinessProfileImporter:
    """Import business profiles from various sources"""
    
    def __init__(self):
        self.crunchbase_api_key = os.getenv("CRUNCHBASE_API_KEY")
        self.linkedin_api_key = os.getenv("LINKEDIN_API_KEY")
        self.clearbit_api_key = os.getenv("CLEARBIT_API_KEY")
        
    def import_from_company_name(self, company_name: str) -> Dict[str, Any]:
        """Import business profile using company name"""
        profile_data = {
            "company_name": company_name,
            "data_sources": [],
            "import_timestamp": datetime.now().isoformat()
        }
        
        # Try multiple sources
        sources = [
            self._import_from_crunchbase,
            self._import_from_clearbit,
            self._import_from_web_search
        ]
        
        for source_func in sources:
            try:
                source_data = source_func(company_name)
                if source_data:
                    profile_data.update(source_data)
                    profile_data["data_sources"].append(source_func.__name__)
            except Exception as e:
                print(f"Error importing from {source_func.__name__}: {str(e)}")
        
        return self._standardize_profile(profile_data)
    
    def import_from_website(self, website_url: str) -> Dict[str, Any]:
        """Import business profile from company website"""
        try:
            # Extract company information from website
            downloaded = trafilatura.fetch_url(website_url)
            text_content = trafilatura.extract(downloaded)
            
            # Get structured data
            response = requests.get(website_url, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(response.content, 'html.parser')
            
            profile_data = {
                "website": website_url,
                "import_method": "website_scraping",
                "import_timestamp": datetime.now().isoformat()
            }
            
            # Extract company name
            title = soup.find('title')
            if title:
                profile_data["company_name"] = title.text.strip().split('|')[0].strip()
            
            # Extract description from meta tags
            description = soup.find('meta', attrs={'name': 'description'})
            if description:
                profile_data["description"] = description.get('content', '')
            
            # Extract structured data (JSON-LD)
            scripts = soup.find_all('script', type='application/ld+json')
            for script in scripts:
                try:
                    data = json.loads(script.string)
                    if data.get('@type') == 'Organization':
                        profile_data.update(self._extract_org_data(data))
                except:
                    continue
            
            # Analyze content for business information
            if text_content:
                profile_data.update(self._analyze_website_content(text_content))
            
            return self._standardize_profile(profile_data)
            
        except Exception as e:
            return {"error": f"Failed to import from website: {str(e)}"}
    
    def import_from_crunchbase_url(self, crunchbase_url: str) -> Dict[str, Any]:
        """Import from CrunchBase profile URL"""
        try:
            # Extract company identifier from URL
            company_id = crunchbase_url.split('/')[-1]
            
            if self.crunchbase_api_key:
                return self._import_from_crunchbase_api(company_id)
            else:
                return self._scrape_crunchbase_public(crunchbase_url)
                
        except Exception as e:
            return {"error": f"Failed to import from CrunchBase: {str(e)}"}
    
    def import_from_linkedin_url(self, linkedin_url: str) -> Dict[str, Any]:
        """Import from LinkedIn company page"""
        try:
            # Extract basic information from LinkedIn public page
            response = requests.get(linkedin_url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            soup = BeautifulSoup(response.content, 'html.parser')
            
            profile_data = {
                "linkedin_url": linkedin_url,
                "import_method": "linkedin_scraping",
                "import_timestamp": datetime.now().isoformat()
            }
            
            # Extract company name
            title = soup.find('title')
            if title:
                profile_data["company_name"] = title.text.replace('| LinkedIn', '').strip()
            
            # Extract company info from page
            company_info = soup.find('section', class_='artdeco-card')
            if company_info:
                # Extract industry, size, location etc.
                details = company_info.find_all('dd')
                for detail in details:
                    text = detail.get_text(strip=True)
                    if 'employees' in text.lower():
                        profile_data["employee_count"] = text
                    elif any(industry in text.lower() for industry in ['technology', 'healthcare', 'finance']):
                        profile_data["industry"] = text
            
            return self._standardize_profile(profile_data)
            
        except Exception as e:
            return {"error": f"Failed to import from LinkedIn: {str(e)}"}
    
    def _import_from_crunchbase(self, company_name: str) -> Dict[str, Any]:
        """Import from CrunchBase API or public data"""
        if not self.crunchbase_api_key:
            return {}
            
        try:
            # CrunchBase API call
            headers = {"X-cb-user-key": self.crunchbase_api_key}
            url = f"https://api.crunchbase.com/api/v4/entities/organizations"
            params = {"name": company_name}
            
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                return self._process_crunchbase_data(data)
                
        except Exception as e:
            print(f"CrunchBase API error: {str(e)}")
        
        return {}
    
    def _import_from_clearbit(self, company_name: str) -> Dict[str, Any]:
        """Import from Clearbit API"""
        if not self.clearbit_api_key:
            return {}
            
        try:
            headers = {"Authorization": f"Bearer {self.clearbit_api_key}"}
            url = f"https://company.clearbit.com/v2/companies/find"
            params = {"name": company_name}
            
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                return self._process_clearbit_data(data)
                
        except Exception as e:
            print(f"Clearbit API error: {str(e)}")
        
        return {}
    
    def _import_from_web_search(self, company_name: str) -> Dict[str, Any]:
        """Import basic information from web search"""
        try:
            # Search for company website
            search_query = f"{company_name} company official website"
            # Implementation would use search API or web scraping
            # For now, return basic structure
            
            return {
                "search_attempted": True,
                "search_query": search_query
            }
            
        except Exception as e:
            return {}
    
    def _analyze_website_content(self, content: str) -> Dict[str, Any]:
        """Analyze website content to extract business information"""
        analysis = {}
        content_lower = content.lower()
        
        # Industry detection
        industries = {
            "technology": ["software", "tech", "ai", "saas", "platform", "digital"],
            "healthcare": ["health", "medical", "hospital", "pharma", "biotech"],
            "finance": ["financial", "banking", "fintech", "investment", "insurance"],
            "retail": ["retail", "ecommerce", "shopping", "store", "marketplace"],
            "manufacturing": ["manufacturing", "factory", "production", "industrial"]
        }
        
        for industry, keywords in industries.items():
            if any(keyword in content_lower for keyword in keywords):
                analysis["detected_industry"] = industry
                break
        
        # Size indicators
        if any(term in content_lower for term in ["enterprise", "corporation", "multinational"]):
            analysis["estimated_size"] = "Large"
        elif any(term in content_lower for term in ["startup", "small business", "sme"]):
            analysis["estimated_size"] = "Small"
        else:
            analysis["estimated_size"] = "Medium"
        
        return analysis
    
    def _extract_org_data(self, json_ld_data: Dict) -> Dict[str, Any]:
        """Extract organization data from JSON-LD structured data"""
        extracted = {}
        
        if json_ld_data.get('name'):
            extracted['company_name'] = json_ld_data['name']
        
        if json_ld_data.get('description'):
            extracted['description'] = json_ld_data['description']
        
        if json_ld_data.get('url'):
            extracted['website'] = json_ld_data['url']
        
        if json_ld_data.get('address'):
            address = json_ld_data['address']
            if isinstance(address, dict):
                location_parts = []
                if address.get('addressLocality'):
                    location_parts.append(address['addressLocality'])
                if address.get('addressCountry'):
                    location_parts.append(address['addressCountry'])
                if location_parts:
                    extracted['location'] = ', '.join(location_parts)
        
        return extracted
    
    def _process_crunchbase_data(self, data: Dict) -> Dict[str, Any]:
        """Process CrunchBase API response"""
        processed = {}
        
        if data.get('entities'):
            entity = data['entities'][0]
            properties = entity.get('properties', {})
            
            processed.update({
                "company_name": properties.get('name', ''),
                "description": properties.get('short_description', ''),
                "website": properties.get('website', ''),
                "founded_date": properties.get('founded_on', ''),
                "employee_count": properties.get('num_employees_enum', ''),
                "funding_total": properties.get('total_funding_usd', 0),
                "source": "crunchbase"
            })
        
        return processed
    
    def _process_clearbit_data(self, data: Dict) -> Dict[str, Any]:
        """Process Clearbit API response"""
        processed = {}
        
        if data:
            processed.update({
                "company_name": data.get('name', ''),
                "description": data.get('description', ''),
                "website": data.get('domain', ''),
                "industry": data.get('category', {}).get('industry', ''),
                "employee_count": data.get('metrics', {}).get('employees', ''),
                "annual_revenue": data.get('metrics', {}).get('annualRevenue', ''),
                "location": data.get('geo', {}).get('city', ''),
                "source": "clearbit"
            })
        
        return processed
    
    def _standardize_profile(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Standardize imported profile data to match BusinessProfile format"""
        standardized = {
            "company_name": raw_data.get("company_name", ""),
            "industry": self._standardize_industry(raw_data.get("industry", "")),
            "sub_industry": raw_data.get("detected_industry", ""),
            "business_size": self._standardize_size(raw_data.get("employee_count", "")),
            "location": raw_data.get("location", ""),
            "website": raw_data.get("website", ""),
            "description": raw_data.get("description", ""),
            "founded_date": raw_data.get("founded_date", ""),
            "annual_revenue": raw_data.get("annual_revenue", ""),
            "import_sources": raw_data.get("data_sources", []),
            "import_timestamp": raw_data.get("import_timestamp", ""),
            "confidence_score": self._calculate_confidence(raw_data)
        }
        
        return {k: v for k, v in standardized.items() if v}  # Remove empty values
    
    def _standardize_industry(self, industry: str) -> str:
        """Map industry to standard categories"""
        industry_lower = industry.lower()
        
        mappings = {
            "technology": ["tech", "software", "saas", "ai", "digital"],
            "healthcare": ["health", "medical", "pharma", "biotech"],
            "finance": ["financial", "banking", "fintech", "investment"],
            "retail": ["retail", "ecommerce", "consumer"],
            "manufacturing": ["manufacturing", "industrial", "production"],
            "agriculture": ["agriculture", "farming", "agtech"],
            "education": ["education", "edtech", "learning"],
            "real_estate": ["real estate", "property", "construction"],
            "transportation": ["transportation", "logistics", "shipping"],
            "energy": ["energy", "renewable", "oil", "gas"]
        }
        
        for standard_industry, keywords in mappings.items():
            if any(keyword in industry_lower for keyword in keywords):
                return standard_industry
        
        return industry
    
    def _standardize_size(self, employee_info: str) -> str:
        """Standardize business size based on employee count"""
        if not employee_info:
            return ""
        
        employee_lower = str(employee_info).lower()
        
        if any(term in employee_lower for term in ["1-10", "startup", "small"]):
            return "Small (1-50 employees)"
        elif any(term in employee_lower for term in ["11-50", "51-200", "medium"]):
            return "Medium (51-200 employees)"
        elif any(term in employee_lower for term in ["201-1000", "large"]):
            return "Large (201-1000 employees)"
        elif any(term in employee_lower for term in ["1000+", "enterprise"]):
            return "Enterprise (1000+ employees)"
        
        return employee_info
    
    def _calculate_confidence(self, data: Dict[str, Any]) -> float:
        """Calculate confidence score based on data completeness"""
        required_fields = ["company_name", "industry", "location", "description"]
        filled_fields = sum(1 for field in required_fields if data.get(field))
        
        base_score = filled_fields / len(required_fields)
        
        # Bonus for multiple sources
        sources_bonus = min(len(data.get("data_sources", [])) * 0.1, 0.2)
        
        return min(base_score + sources_bonus, 1.0)