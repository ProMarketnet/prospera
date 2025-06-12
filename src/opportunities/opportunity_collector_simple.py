"""
Simplified opportunity collector for Prospera
Uses demo data to showcase opportunity matching functionality
"""
import os
from typing import List, Dict, Any
from datetime import datetime, timedelta

from ..utils.logger import setup_logger
from ..matching.opportunity_matcher import Opportunity
from .demo_opportunities import DemoOpportunityProvider

logger = setup_logger(__name__)

class OpportunityCollector:
    """Simplified opportunity collector using demo data"""
    
    def __init__(self):
        self.demo_provider = DemoOpportunityProvider()
        self.collected_opportunities = []
        
    def collect_all_opportunities(self) -> List[Opportunity]:
        """Collect opportunities from demo data source"""
        
        all_opportunities = self.demo_provider.get_opportunities()
        
        # Store collected opportunities
        self.collected_opportunities = all_opportunities
        
        logger.info(f"Collected {len(all_opportunities)} demo opportunities")
        return all_opportunities
        
    def collect_by_industry(self, industry: str) -> List[Opportunity]:
        """Collect opportunities filtered by industry"""
        
        opportunities = self.demo_provider.get_opportunities(industry)
        
        logger.info(f"Collected {len(opportunities)} opportunities for {industry} industry")
        return opportunities
