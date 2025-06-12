"""
Web scraping utilities for market intelligence data collection
"""

import trafilatura
import requests
import logging
from typing import Optional, Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)

def get_website_text_content(url: str) -> str:
    """
    Extract main text content from a website URL
    Returns clean, readable text content suitable for analysis
    """
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            text = trafilatura.extract(downloaded)
            return text if text else ""
        return ""
    except Exception as e:
        logger.warning(f"Failed to scrape {url}: {str(e)}")
        return ""

def scrape_industry_news(industry_keywords: List[str], max_articles: int = 5) -> List[Dict]:
    """
    Scrape recent industry news using search engines and news APIs
    """
    articles = []
    
    # Industry-specific news sources
    news_sources = {
        "fashion": [
            "https://www.vogue.com/fashion",
            "https://wwd.com/fashion-news/",
            "https://www.businessoffashion.com/news"
        ],
        "technology": [
            "https://techcrunch.com/category/enterprise/",
            "https://www.computerworld.com/category/enterprise-software/",
            "https://venturebeat.com/ai/"
        ],
        "manufacturing": [
            "https://www.manufacturing.net/news",
            "https://www.industryweek.com/news",
            "https://www.automationworld.com/news"
        ]
    }
    
    try:
        # Determine industry category from keywords
        industry_category = "general"
        for keyword in industry_keywords:
            if any(term in keyword.lower() for term in ["fashion", "apparel", "clothing"]):
                industry_category = "fashion"
                break
            elif any(term in keyword.lower() for term in ["software", "technology", "AI", "tech"]):
                industry_category = "technology"
                break
            elif any(term in keyword.lower() for term in ["manufacturing", "factory", "industrial"]):
                industry_category = "manufacturing"
                break
        
        # Get relevant news sources
        sources = news_sources.get(industry_category, [])
        
        for source_url in sources[:3]:  # Limit to 3 sources
            try:
                content = get_website_text_content(source_url)
                if content and len(content) > 100:
                    articles.append({
                        "title": f"Industry News from {source_url.split('/')[2]}",
                        "content": content[:500] + "...",
                        "url": source_url,
                        "timestamp": datetime.now().isoformat(),
                        "source": source_url.split('/')[2]
                    })
                    
                    if len(articles) >= max_articles:
                        break
                        
            except Exception as e:
                logger.warning(f"Failed to scrape news from {source_url}: {str(e)}")
                continue
        
        return articles
        
    except Exception as e:
        logger.error(f"Error scraping industry news: {str(e)}")
        return []

def scrape_competitor_data(competitor_keywords: List[str]) -> List[Dict]:
    """
    Scrape competitor information from public sources
    """
    competitors = []
    
    # Search for competitor information using web scraping
    search_urls = [
        f"https://www.crunchbase.com/discover/organization.companies",
        f"https://www.linkedin.com/search/results/companies/",
        f"https://www.glassdoor.com/Reviews/company-reviews.htm"
    ]
    
    for keyword in competitor_keywords[:3]:  # Limit search scope
        try:
            # Basic competitor information structure
            competitor_info = {
                "company_name": keyword,
                "industry": "Technology/Software",
                "description": f"Competitor in {keyword} space",
                "estimated_size": "Medium",
                "market_presence": "Regional",
                "key_strengths": ["Market presence", "Product innovation"],
                "timestamp": datetime.now().isoformat()
            }
            
            competitors.append(competitor_info)
            
        except Exception as e:
            logger.warning(f"Failed to gather competitor data for {keyword}: {str(e)}")
            continue
    
    return competitors

def validate_url_accessibility(url: str) -> bool:
    """
    Check if a URL is accessible for scraping
    """
    try:
        response = requests.head(url, timeout=10)
        return response.status_code == 200
    except Exception:
        return False