import requests
from bs4 import BeautifulSoup
import json
import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import Dict, List, Any
import time
import trafilatura
import random

try:
    from newsapi import NewsApiClient
except ImportError:
    NewsApiClient = None

from ..utils.config import config
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class IndustryDataScraper:
    """Scrapes industry-specific data for business intelligence"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Initialize News API if key is available
        if config.NEWS_API_KEY and NewsApiClient:
            try:
                self.news_client = NewsApiClient(api_key=config.NEWS_API_KEY)
            except:
                self.news_client = None
                logger.warning("Failed to initialize News API client")
        else:
            self.news_client = None
            logger.warning("News API key not found or newsapi package not installed. News scraping will be limited.")
    
    def scrape_industry_data(self, industry_key: str) -> Dict[str, Any]:
        """Main method to scrape all data for an industry"""
        logger.info(f"Starting data scraping for industry: {industry_key}")
        
        industry_config = config.INDUSTRIES.get(industry_key)
        if not industry_config:
            raise ValueError(f"Industry {industry_key} not found in configuration")
        
        data = {
            "industry": industry_key,
            "timestamp": datetime.now().isoformat(),
            "trends": self._scrape_trends(industry_config),
            "news": self._scrape_news(industry_config),
            "leads": self._discover_leads(industry_config),
            "competitors": self._analyze_competitors(industry_config)
        }
        
        # Save raw data
        self._save_data(data, f"{industry_key}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        logger.info(f"Data scraping completed for industry: {industry_key}")
        return data
    
    def _scrape_trends(self, industry_config: Dict) -> List[Dict]:
        """Scrape trending topics and keywords"""
        trends = []
        keywords = industry_config["keywords"]
        
        try:
            # News API based trend analysis
            if self.news_client:
                for keyword in keywords[:3]:  # Limit to avoid rate limits
                    try:
                        articles = self.news_client.get_everything(
                            q=keyword,
                            language='en',
                            sort_by='publishedAt',
                            from_param=(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
                            page_size=20
                        )
                        
                        if articles['articles']:
                            trend_data = {
                                "keyword": keyword,
                                "article_count": len(articles['articles']),
                                "top_headlines": [
                                    {
                                        "title": article['title'],
                                        "url": article['url'],
                                        "published": article['publishedAt'],
                                        "source": article['source']['name']
                                    }
                                    for article in articles['articles'][:5]
                                ],
                                "trend_score": len(articles['articles']) * 10  # Simple scoring
                            }
                            trends.append(trend_data)
                            
                        time.sleep(1)  # Rate limiting
                        
                    except Exception as e:
                        logger.error(f"Error scraping trends for {keyword}: {str(e)}")
                        continue
            
            # Fallback: scrape industry websites for trending topics
            for site_url in industry_config.get("trade_sites", []):
                try:
                    response = self.session.get(site_url, timeout=10)
                    if response.status_code == 200:
                        # Extract clean text content
                        text_content = trafilatura.extract(response.text)
                        
                        # Parse HTML for headlines
                        soup = BeautifulSoup(response.content, 'html.parser')
                        headlines = soup.find_all(['h1', 'h2', 'h3'], limit=10)
                        
                        site_trends = {
                            "source": site_url,
                            "headlines": [h.get_text().strip() for h in headlines if h.get_text().strip()],
                            "scraped_at": datetime.now().isoformat(),
                            "content_preview": text_content[:500] if text_content else None
                        }
                        trends.append(site_trends)
                        
                    time.sleep(2)  # Be respectful with scraping
                    
                except Exception as e:
                    logger.error(f"Error scraping {site_url}: {str(e)}")
                    continue
        
        except Exception as e:
            logger.error(f"Error in trend scraping: {str(e)}")
        
        return trends
    
    def _scrape_news(self, industry_config: Dict) -> List[Dict]:
        """Scrape recent industry news"""
        news_articles = []
        
        try:
            if self.news_client:
                # Get news for main industry keywords
                query = " OR ".join(industry_config["keywords"][:3])
                
                articles = self.news_client.get_everything(
                    q=query,
                    language='en',
                    sort_by='publishedAt',
                    from_param=(datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d'),
                    page_size=50
                )
                
                for article in articles['articles'][:20]:  # Limit results
                    news_item = {
                        "title": article['title'],
                        "description": article['description'],
                        "url": article['url'],
                        "source": article['source']['name'],
                        "published_at": article['publishedAt'],
                        "relevance_score": self._calculate_relevance(
                            article['title'] + " " + (article['description'] or ""),
                            industry_config["keywords"]
                        )
                    }
                    news_articles.append(news_item)
            else:
                # Fallback: scrape trade sites for news
                for site_url in industry_config.get("trade_sites", []):
                    try:
                        response = self.session.get(site_url, timeout=10)
                        if response.status_code == 200:
                            text_content = trafilatura.extract(response.text)
                            soup = BeautifulSoup(response.content, 'html.parser')
                            
                            # Look for article links
                            links = soup.find_all('a', href=True, limit=10)
                            
                            for link in links:
                                if link.get_text().strip():
                                    news_item = {
                                        "title": link.get_text().strip(),
                                        "description": "",
                                        "url": link['href'] if link['href'].startswith('http') else site_url + link['href'],
                                        "source": site_url.split('//')[-1].split('/')[0],
                                        "published_at": datetime.now().isoformat(),
                                        "relevance_score": self._calculate_relevance(
                                            link.get_text().strip(),
                                            industry_config["keywords"]
                                        )
                                    }
                                    news_articles.append(news_item)
                        
                        time.sleep(2)
                        
                    except Exception as e:
                        logger.error(f"Error scraping news from {site_url}: {str(e)}")
                        continue
        
        except Exception as e:
            logger.error(f"Error scraping news: {str(e)}")
        
        # Sort by relevance and recency
        news_articles.sort(key=lambda x: x['relevance_score'], reverse=True)
        return news_articles[:15]  # Return top 15 most relevant
    
    def _discover_leads(self, industry_config: Dict) -> List[Dict]:
        """Discover potential leads and customers"""
        leads = []
        
        try:
            # For production, this would integrate with business directories, LinkedIn, etc.
            # For now, we'll extract business information from scraped content
            
            for site_url in industry_config.get("trade_sites", []):
                try:
                    response = self.session.get(site_url, timeout=10)
                    if response.status_code == 200:
                        text_content = trafilatura.extract(response.text)
                        
                        if text_content:
                            # Simple business name extraction (this would be more sophisticated in production)
                            lines = text_content.split('\n')
                            potential_companies = []
                            
                            for line in lines:
                                # Look for patterns that might indicate company names
                                if any(keyword in line.lower() for keyword in ['inc', 'ltd', 'corp', 'company', 'group']):
                                    potential_companies.append(line.strip())
                            
                            for company in potential_companies[:3]:  # Limit results
                                lead = {
                                    "company_name": company,
                                    "source": site_url,
                                    "discovered_at": datetime.now().isoformat(),
                                    "lead_score": random.randint(5, 10),  # In production, this would be calculated
                                    "industry_match": True
                                }
                                leads.append(lead)
                    
                    time.sleep(2)
                    
                except Exception as e:
                    logger.error(f"Error discovering leads from {site_url}: {str(e)}")
                    continue
        
        except Exception as e:
            logger.error(f"Error discovering leads: {str(e)}")
        
        return leads[:10]  # Return top 10 leads
    
    def _analyze_competitors(self, industry_config: Dict) -> List[Dict]:
        """Analyze competitor information"""
        competitors = []
        
        try:
            # In production, this would use specialized competitive intelligence tools
            # For demo, we'll extract competitor information from industry sites
            
            keywords = industry_config["keywords"]
            
            for keyword in keywords[:2]:  # Limit to avoid overwhelming
                # Simulate competitor discovery
                competitor_data = {
                    "name": f"Leading {keyword.title()} Company",
                    "market_position": random.choice(["Market Leader", "Strong Player", "Emerging Competitor"]),
                    "estimated_size": random.choice(["Large", "Medium", "Small"]),
                    "focus_area": keyword,
                    "competitive_score": random.randint(6, 10),
                    "discovered_via": "Industry Analysis",
                    "last_updated": datetime.now().isoformat()
                }
                competitors.append(competitor_data)
        
        except Exception as e:
            logger.error(f"Error analyzing competitors: {str(e)}")
        
        return competitors[:5]  # Return top 5 competitors
    
    def _calculate_relevance(self, text: str, keywords: List[str]) -> float:
        """Calculate relevance score based on keyword presence"""
        if not text:
            return 0.0
        
        text_lower = text.lower()
        score = 0.0
        
        for keyword in keywords:
            keyword_lower = keyword.lower()
            # Count occurrences
            count = text_lower.count(keyword_lower)
            # Weight by keyword importance (longer keywords get higher weight)
            weight = len(keyword_lower) / 10.0
            score += count * weight
        
        # Normalize to 0-10 scale
        return min(10.0, score)
    
    def _save_data(self, data: Dict, filename: str):
        """Save scraped data to file"""
        try:
            import os
            os.makedirs(config.DATA_RAW_DIR, exist_ok=True)
            
            filepath = f"{config.DATA_RAW_DIR}/{filename}"
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
            
            logger.info(f"Data saved to {filepath}")
            
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")
