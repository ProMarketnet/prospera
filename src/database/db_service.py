from typing import Optional, Dict, Any, List
from datetime import datetime

from .models import db_manager, BusinessProfile as DBBusinessProfile
from .repository import BusinessProfileRepository, DataCollectionRepository, AnalysisRepository, MetricsRepository
from ..profile.business_profile import BusinessProfile, BusinessSize, MarketFocus
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class DatabaseService:
    """Service layer for database operations"""
    
    def __init__(self):
        self.profile_repo = BusinessProfileRepository()
        self.collection_repo = DataCollectionRepository()
        self.analysis_repo = AnalysisRepository()
        self.metrics_repo = MetricsRepository()
        
        # Initialize database tables
        try:
            db_manager.create_tables()
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")
    
    def save_business_profile(self, profile: BusinessProfile) -> int:
        """Save business profile to database and return ID"""
        try:
            profile_data = {
                'company_name': profile.company_name,
                'industry': profile.industry,
                'sub_industry': profile.sub_industry,
                'business_size': profile.business_size.value,
                'annual_revenue': profile.annual_revenue,
                'location': profile.location,
                'primary_products': profile.primary_products,
                'target_markets': profile.target_markets,
                'market_focus': profile.market_focus.value,
                'unique_selling_points': profile.unique_selling_points,
                'main_challenges': profile.main_challenges,
                'growth_goals': profile.growth_goals,
                'target_revenue_growth': profile.target_revenue_growth,
                'focus_regions': profile.focus_regions,
                'competitor_companies': profile.competitor_companies,
                'key_keywords': profile.key_keywords,
                'preferred_languages': profile.preferred_languages,
                'profile_completeness': profile.profile_completeness
            }
            
            # Check if profile already exists
            existing_profile = self.profile_repo.get_profile_by_company_name(profile.company_name)
            if existing_profile:
                # Update existing profile
                updated_profile = self.profile_repo.update_profile(existing_profile.id, profile_data)
                return updated_profile.id if updated_profile else existing_profile.id
            else:
                # Create new profile
                db_profile = self.profile_repo.create_profile(profile_data)
                return db_profile.id
                
        except Exception as e:
            logger.error(f"Error saving business profile: {str(e)}")
            raise
    
    def load_business_profile(self, company_name: str) -> Optional[BusinessProfile]:
        """Load business profile from database"""
        try:
            db_profile = self.profile_repo.get_profile_by_company_name(company_name)
            if not db_profile:
                return None
            
            # Convert database model to business profile
            profile = BusinessProfile(
                company_name=db_profile.company_name,
                industry=db_profile.industry,
                sub_industry=db_profile.sub_industry or '',
                business_size=BusinessSize(db_profile.business_size),
                annual_revenue=db_profile.annual_revenue or '',
                location=db_profile.location or '',
                primary_products=db_profile.primary_products or [],
                target_markets=db_profile.target_markets or [],
                market_focus=MarketFocus(db_profile.market_focus),
                unique_selling_points=db_profile.unique_selling_points or [],
                main_challenges=db_profile.main_challenges or [],
                growth_goals=db_profile.growth_goals or [],
                target_revenue_growth=db_profile.target_revenue_growth or '',
                focus_regions=db_profile.focus_regions or [],
                competitor_companies=db_profile.competitor_companies or [],
                key_keywords=db_profile.key_keywords or [],
                preferred_languages=db_profile.preferred_languages or ['English'],
                created_at=db_profile.created_at.isoformat(),
                updated_at=db_profile.updated_at.isoformat(),
                profile_completeness=db_profile.profile_completeness or 0.0
            )
            
            return profile
            
        except Exception as e:
            logger.error(f"Error loading business profile: {str(e)}")
            return None
    
    def save_data_collection(self, profile_id: int, industry: str, raw_data: Dict[str, Any]) -> int:
        """Save data collection session to database"""
        try:
            collection = self.collection_repo.save_collection_data(profile_id, industry, raw_data)
            return collection.id
        except Exception as e:
            logger.error(f"Error saving data collection: {str(e)}")
            raise
    
    def save_analysis_results(self, profile_id: int, data_collection_id: int, analysis_data: Dict[str, Any]) -> int:
        """Save analysis results to database"""
        try:
            analysis = self.analysis_repo.save_analysis(profile_id, data_collection_id, analysis_data)
            return analysis.id
        except Exception as e:
            logger.error(f"Error saving analysis results: {str(e)}")
            raise
    
    def get_profile_dashboard_data(self, profile_id: int) -> Dict[str, Any]:
        """Get comprehensive dashboard data for a profile"""
        try:
            # Get basic metrics
            metrics = self.metrics_repo.get_profile_metrics(profile_id)
            
            # Get recent collections and analyses
            recent_collections = self.collection_repo.get_collections_history(profile_id, limit=5)
            recent_analyses = self.analysis_repo.get_analysis_history(profile_id, days=30)
            
            # Get latest analysis data
            latest_analysis = self.analysis_repo.get_latest_analysis(profile_id)
            
            dashboard_data = {
                'metrics': metrics,
                'recent_collections': [
                    {
                        'id': c.id,
                        'industry': c.industry,
                        'timestamp': c.collection_timestamp.isoformat(),
                        'trends_count': c.trends_count,
                        'news_count': c.news_count,
                        'leads_count': c.leads_count,
                        'competitors_count': c.competitors_count
                    } for c in recent_collections
                ],
                'recent_analyses': [
                    {
                        'id': a.id,
                        'timestamp': a.analysis_timestamp.isoformat(),
                        'opportunity_score': a.opportunity_score,
                        'competition_level': a.competition_level,
                        'confidence_score': a.confidence_score
                    } for a in recent_analyses
                ],
                'latest_analysis': {
                    'id': latest_analysis.id,
                    'timestamp': latest_analysis.analysis_timestamp.isoformat(),
                    'market_summary': latest_analysis.market_summary,
                    'opportunities': latest_analysis.opportunities,
                    'risks': latest_analysis.risks,
                    'recommendations': latest_analysis.recommendations,
                    'opportunity_score': latest_analysis.opportunity_score,
                    'competition_level': latest_analysis.competition_level,
                    'lead_quality_score': latest_analysis.lead_quality_score,
                    'trend_momentum': latest_analysis.trend_momentum
                } if latest_analysis else None
            }
            
            return dashboard_data
            
        except Exception as e:
            logger.error(f"Error getting dashboard data: {str(e)}")
            return {}
    
    def get_all_profiles(self) -> List[Dict[str, Any]]:
        """Get all business profiles summary"""
        try:
            profiles = self.profile_repo.list_profiles()
            return [
                {
                    'id': p.id,
                    'company_name': p.company_name,
                    'industry': p.industry,
                    'sub_industry': p.sub_industry,
                    'location': p.location,
                    'created_at': p.created_at.isoformat(),
                    'profile_completeness': p.profile_completeness
                } for p in profiles
            ]
        except Exception as e:
            logger.error(f"Error getting all profiles: {str(e)}")
            return []
    
    def get_profile_history(self, profile_id: int) -> Dict[str, Any]:
        """Get detailed history for a profile"""
        try:
            collections = self.collection_repo.get_collections_history(profile_id, limit=20)
            analyses = self.analysis_repo.get_analysis_history(profile_id, days=90)
            
            return {
                'collections': [
                    {
                        'id': c.id,
                        'industry': c.industry,
                        'timestamp': c.collection_timestamp.isoformat(),
                        'status': c.collection_status,
                        'data_summary': {
                            'trends': c.trends_count,
                            'news': c.news_count,
                            'leads': c.leads_count,
                            'competitors': c.competitors_count
                        }
                    } for c in collections
                ],
                'analyses': [
                    {
                        'id': a.id,
                        'timestamp': a.analysis_timestamp.isoformat(),
                        'opportunity_score': a.opportunity_score,
                        'competition_level': a.competition_level,
                        'lead_quality_score': a.lead_quality_score,
                        'confidence_score': a.confidence_score,
                        'recommendations_count': len(a.recommendations) if a.recommendations else 0
                    } for a in analyses
                ]
            }
            
        except Exception as e:
            logger.error(f"Error getting profile history: {str(e)}")
            return {'collections': [], 'analyses': []}

# Global database service instance
db_service = DatabaseService()