from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from datetime import datetime, timedelta

from .models import (
    BusinessProfile, DataCollection, Analysis, MarketTrend, 
    NewsArticle, Lead, Competitor, db_manager
)
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class BusinessProfileRepository:
    """Repository for business profile operations"""
    
    def __init__(self):
        self.db_manager = db_manager
    
    def create_profile(self, profile_data: Dict[str, Any]) -> BusinessProfile:
        """Create a new business profile"""
        session = self.db_manager.get_session()
        try:
            profile = BusinessProfile(**profile_data)
            session.add(profile)
            session.commit()
            session.refresh(profile)
            logger.info(f"Created business profile: {profile.company_name}")
            return profile
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating business profile: {str(e)}")
            raise
        finally:
            self.db_manager.close_session(session)
    
    def get_profile_by_id(self, profile_id: int) -> Optional[BusinessProfile]:
        """Get business profile by ID"""
        session = self.db_manager.get_session()
        try:
            profile = session.query(BusinessProfile).filter(BusinessProfile.id == profile_id).first()
            return profile
        except Exception as e:
            logger.error(f"Error getting business profile: {str(e)}")
            return None
        finally:
            self.db_manager.close_session(session)
    
    def get_profile_by_company_name(self, company_name: str) -> Optional[BusinessProfile]:
        """Get business profile by company name"""
        session = self.db_manager.get_session()
        try:
            profile = session.query(BusinessProfile).filter(
                BusinessProfile.company_name == company_name
            ).first()
            return profile
        except Exception as e:
            logger.error(f"Error getting business profile by name: {str(e)}")
            return None
        finally:
            self.db_manager.close_session(session)
    
    def update_profile(self, profile_id: int, update_data: Dict[str, Any]) -> Optional[BusinessProfile]:
        """Update business profile"""
        session = self.db_manager.get_session()
        try:
            profile = session.query(BusinessProfile).filter(BusinessProfile.id == profile_id).first()
            if profile:
                for key, value in update_data.items():
                    if hasattr(profile, key):
                        setattr(profile, key, value)
                session.commit()
                session.refresh(profile)
                logger.info(f"Updated business profile: {profile.company_name}")
                return profile
            return None
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating business profile: {str(e)}")
            raise
        finally:
            self.db_manager.close_session(session)
    
    def list_profiles(self) -> List[BusinessProfile]:
        """List all business profiles"""
        session = self.db_manager.get_session()
        try:
            profiles = session.query(BusinessProfile).order_by(BusinessProfile.created_at.desc()).all()
            return profiles
        except Exception as e:
            logger.error(f"Error listing business profiles: {str(e)}")
            return []
        finally:
            self.db_manager.close_session(session)

class DataCollectionRepository:
    """Repository for data collection operations"""
    
    def __init__(self):
        self.db_manager = db_manager
    
    def create_collection(self, collection_data: Dict[str, Any]) -> DataCollection:
        """Create a new data collection record"""
        session = self.db_manager.get_session()
        try:
            collection = DataCollection(**collection_data)
            session.add(collection)
            session.commit()
            session.refresh(collection)
            logger.info(f"Created data collection for profile {collection.profile_id}")
            return collection
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating data collection: {str(e)}")
            raise
        finally:
            self.db_manager.close_session(session)
    
    def save_collection_data(self, profile_id: int, industry: str, raw_data: Dict[str, Any]) -> DataCollection:
        """Save complete data collection session"""
        session = self.db_manager.get_session()
        try:
            # Create main collection record
            collection_data = {
                'profile_id': profile_id,
                'industry': industry,
                'raw_data': raw_data,
                'trends_count': len(raw_data.get('trends', [])),
                'news_count': len(raw_data.get('news', [])),
                'leads_count': len(raw_data.get('leads', [])),
                'competitors_count': len(raw_data.get('competitors', [])),
                'collection_status': 'completed'
            }
            
            collection = DataCollection(**collection_data)
            session.add(collection)
            session.flush()  # Get the ID
            
            # Save detailed trend data
            for trend in raw_data.get('trends', []):
                trend_record = MarketTrend(
                    data_collection_id=collection.id,
                    keyword=trend.get('keyword'),
                    source=trend.get('source'),
                    trend_score=trend.get('trend_score'),
                    article_count=trend.get('article_count'),
                    headlines=trend.get('top_headlines', trend.get('headlines', []))
                )
                session.add(trend_record)
            
            # Save news articles
            for article in raw_data.get('news', []):
                news_record = NewsArticle(
                    data_collection_id=collection.id,
                    title=article.get('title', ''),
                    description=article.get('description'),
                    url=article.get('url'),
                    source=article.get('source'),
                    published_at=datetime.fromisoformat(article.get('published_at', datetime.now().isoformat()).replace('Z', '+00:00')),
                    relevance_score=article.get('relevance_score')
                )
                session.add(news_record)
            
            # Save leads
            for lead in raw_data.get('leads', []):
                lead_record = Lead(
                    data_collection_id=collection.id,
                    company_name=lead.get('company_name', ''),
                    source=lead.get('source'),
                    lead_score=lead.get('lead_score'),
                    industry_match=lead.get('industry_match', True)
                )
                session.add(lead_record)
            
            # Save competitors
            for competitor in raw_data.get('competitors', []):
                competitor_record = Competitor(
                    data_collection_id=collection.id,
                    name=competitor.get('name', ''),
                    market_position=competitor.get('market_position'),
                    estimated_size=competitor.get('estimated_size'),
                    focus_area=competitor.get('focus_area'),
                    competitive_score=competitor.get('competitive_score'),
                    discovered_via=competitor.get('discovered_via')
                )
                session.add(competitor_record)
            
            session.commit()
            session.refresh(collection)
            logger.info(f"Saved complete data collection with {collection.trends_count} trends, {collection.news_count} news, {collection.leads_count} leads, {collection.competitors_count} competitors")
            return collection
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving data collection: {str(e)}")
            raise
        finally:
            self.db_manager.close_session(session)
    
    def get_latest_collection(self, profile_id: int) -> Optional[DataCollection]:
        """Get the latest data collection for a profile"""
        session = self.db_manager.get_session()
        try:
            collection = session.query(DataCollection).filter(
                DataCollection.profile_id == profile_id
            ).order_by(desc(DataCollection.collection_timestamp)).first()
            return collection
        except Exception as e:
            logger.error(f"Error getting latest collection: {str(e)}")
            return None
        finally:
            self.db_manager.close_session(session)
    
    def get_collections_history(self, profile_id: int, limit: int = 10) -> List[DataCollection]:
        """Get collection history for a profile"""
        session = self.db_manager.get_session()
        try:
            collections = session.query(DataCollection).filter(
                DataCollection.profile_id == profile_id
            ).order_by(desc(DataCollection.collection_timestamp)).limit(limit).all()
            return collections
        except Exception as e:
            logger.error(f"Error getting collection history: {str(e)}")
            return []
        finally:
            self.db_manager.close_session(session)

class AnalysisRepository:
    """Repository for analysis operations"""
    
    def __init__(self):
        self.db_manager = db_manager
    
    def save_analysis(self, profile_id: int, data_collection_id: int, analysis_data: Dict[str, Any]) -> Analysis:
        """Save AI analysis results"""
        session = self.db_manager.get_session()
        try:
            ai_analysis = analysis_data.get('ai_analysis', {})
            business_insights = analysis_data.get('business_insights', {})
            key_metrics = business_insights.get('key_metrics', {})
            
            analysis = Analysis(
                profile_id=profile_id,
                data_collection_id=data_collection_id,
                market_summary=ai_analysis.get('market_summary'),
                opportunities=ai_analysis.get('opportunities', []),
                risks=ai_analysis.get('risks', []),
                competitive_landscape=ai_analysis.get('competitive_landscape'),
                lead_insights=ai_analysis.get('lead_insights'),
                recommendations=ai_analysis.get('recommendations', []),
                confidence_score=ai_analysis.get('confidence_score'),
                opportunity_score=key_metrics.get('opportunity_score'),
                competition_level=key_metrics.get('competition_level'),
                lead_quality_score=key_metrics.get('lead_quality'),
                trend_momentum=key_metrics.get('trend_momentum'),
                ai_analysis=ai_analysis,
                business_insights=business_insights
            )
            
            session.add(analysis)
            session.commit()
            session.refresh(analysis)
            logger.info(f"Saved analysis for profile {profile_id}")
            return analysis
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving analysis: {str(e)}")
            raise
        finally:
            self.db_manager.close_session(session)
    
    def get_latest_analysis(self, profile_id: int) -> Optional[Analysis]:
        """Get the latest analysis for a profile"""
        session = self.db_manager.get_session()
        try:
            analysis = session.query(Analysis).filter(
                Analysis.profile_id == profile_id
            ).order_by(desc(Analysis.analysis_timestamp)).first()
            return analysis
        except Exception as e:
            logger.error(f"Error getting latest analysis: {str(e)}")
            return None
        finally:
            self.db_manager.close_session(session)
    
    def get_analysis_history(self, profile_id: int, days: int = 30) -> List[Analysis]:
        """Get analysis history for a profile"""
        session = self.db_manager.get_session()
        try:
            since_date = datetime.now() - timedelta(days=days)
            analyses = session.query(Analysis).filter(
                and_(
                    Analysis.profile_id == profile_id,
                    Analysis.analysis_timestamp >= since_date
                )
            ).order_by(desc(Analysis.analysis_timestamp)).all()
            return analyses
        except Exception as e:
            logger.error(f"Error getting analysis history: {str(e)}")
            return []
        finally:
            self.db_manager.close_session(session)

class MetricsRepository:
    """Repository for metrics and analytics"""
    
    def __init__(self):
        self.db_manager = db_manager
    
    def get_profile_metrics(self, profile_id: int) -> Dict[str, Any]:
        """Get comprehensive metrics for a profile"""
        session = self.db_manager.get_session()
        try:
            # Get counts
            collections_count = session.query(DataCollection).filter(
                DataCollection.profile_id == profile_id
            ).count()
            
            analyses_count = session.query(Analysis).filter(
                Analysis.profile_id == profile_id
            ).count()
            
            # Get latest data
            latest_collection = session.query(DataCollection).filter(
                DataCollection.profile_id == profile_id
            ).order_by(desc(DataCollection.collection_timestamp)).first()
            
            latest_analysis = session.query(Analysis).filter(
                Analysis.profile_id == profile_id
            ).order_by(desc(Analysis.analysis_timestamp)).first()
            
            # Calculate trends
            recent_analyses = session.query(Analysis).filter(
                and_(
                    Analysis.profile_id == profile_id,
                    Analysis.analysis_timestamp >= datetime.now() - timedelta(days=30)
                )
            ).order_by(desc(Analysis.analysis_timestamp)).limit(5).all()
            
            opportunity_trend = 0
            if len(recent_analyses) >= 2:
                latest_score = recent_analyses[0].opportunity_score or 0
                previous_score = recent_analyses[1].opportunity_score or 0
                opportunity_trend = latest_score - previous_score
            
            return {
                'collections_count': collections_count,
                'analyses_count': analyses_count,
                'latest_collection_date': latest_collection.collection_timestamp if latest_collection else None,
                'latest_analysis_date': latest_analysis.analysis_timestamp if latest_analysis else None,
                'latest_opportunity_score': latest_analysis.opportunity_score if latest_analysis else None,
                'latest_competition_level': latest_analysis.competition_level if latest_analysis else None,
                'opportunity_trend': opportunity_trend,
                'total_leads_discovered': sum([c.leads_count for c in session.query(DataCollection).filter(DataCollection.profile_id == profile_id).all()]),
                'total_news_analyzed': sum([c.news_count for c in session.query(DataCollection).filter(DataCollection.profile_id == profile_id).all()])
            }
            
        except Exception as e:
            logger.error(f"Error getting profile metrics: {str(e)}")
            return {}
        finally:
            self.db_manager.close_session(session)