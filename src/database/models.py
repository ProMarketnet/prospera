from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, JSON, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from datetime import datetime
import os

from ..utils.logger import setup_logger

logger = setup_logger(__name__)

Base = declarative_base()

class BusinessProfile(Base):
    """Business profile model for storing company information"""
    __tablename__ = 'business_profiles'
    
    id = Column(Integer, primary_key=True)
    company_name = Column(String(255), nullable=False, unique=True)
    industry = Column(String(100), nullable=False)
    sub_industry = Column(String(150))
    business_size = Column(String(50))
    annual_revenue = Column(String(50))
    location = Column(String(255))
    
    # Products & Services
    primary_products = Column(JSON)
    target_markets = Column(JSON)
    market_focus = Column(String(50))
    unique_selling_points = Column(JSON)
    
    # Goals & Challenges
    main_challenges = Column(JSON)
    growth_goals = Column(JSON)
    target_revenue_growth = Column(String(50))
    
    # Market Intelligence Preferences
    focus_regions = Column(JSON)
    competitor_companies = Column(JSON)
    key_keywords = Column(JSON)
    preferred_languages = Column(JSON)
    
    # Metadata
    profile_completeness = Column(Float, default=0.0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    data_collections = relationship("DataCollection", back_populates="profile")
    analyses = relationship("Analysis", back_populates="profile")

class DataCollection(Base):
    """Model for storing data collection sessions"""
    __tablename__ = 'data_collections'
    
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey('business_profiles.id'), nullable=False)
    industry = Column(String(100), nullable=False)
    collection_timestamp = Column(DateTime, server_default=func.now())
    
    # Collection metadata
    trends_count = Column(Integer, default=0)
    news_count = Column(Integer, default=0)
    leads_count = Column(Integer, default=0)
    competitors_count = Column(Integer, default=0)
    
    # Raw data storage
    raw_data = Column(JSON)
    collection_status = Column(String(50), default='completed')
    error_message = Column(Text)
    
    # Relationships
    profile = relationship("BusinessProfile", back_populates="data_collections")
    analyses = relationship("Analysis", back_populates="data_collection")

class Analysis(Base):
    """Model for storing AI analysis results"""
    __tablename__ = 'analyses'
    
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey('business_profiles.id'), nullable=False)
    data_collection_id = Column(Integer, ForeignKey('data_collections.id'), nullable=False)
    analysis_timestamp = Column(DateTime, server_default=func.now())
    
    # Analysis results
    market_summary = Column(Text)
    opportunities = Column(JSON)
    risks = Column(JSON)
    competitive_landscape = Column(Text)
    lead_insights = Column(Text)
    recommendations = Column(JSON)
    confidence_score = Column(Float)
    
    # Business intelligence metrics
    opportunity_score = Column(Float)
    competition_level = Column(String(50))
    lead_quality_score = Column(Float)
    trend_momentum = Column(String(50))
    
    # Full analysis data
    ai_analysis = Column(JSON)
    business_insights = Column(JSON)
    
    # Relationships
    profile = relationship("BusinessProfile", back_populates="analyses")
    data_collection = relationship("DataCollection", back_populates="analyses")

class MarketTrend(Base):
    """Model for storing individual market trends"""
    __tablename__ = 'market_trends'
    
    id = Column(Integer, primary_key=True)
    data_collection_id = Column(Integer, ForeignKey('data_collections.id'), nullable=False)
    
    keyword = Column(String(255))
    source = Column(String(255))
    trend_score = Column(Float)
    article_count = Column(Integer)
    headlines = Column(JSON)
    scraped_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    data_collection = relationship("DataCollection")

class NewsArticle(Base):
    """Model for storing news articles"""
    __tablename__ = 'news_articles'
    
    id = Column(Integer, primary_key=True)
    data_collection_id = Column(Integer, ForeignKey('data_collections.id'), nullable=False)
    
    title = Column(String(500), nullable=False)
    description = Column(Text)
    url = Column(String(1000))
    source = Column(String(255))
    published_at = Column(DateTime)
    relevance_score = Column(Float)
    
    # Relationships
    data_collection = relationship("DataCollection")

class Lead(Base):
    """Model for storing discovered leads"""
    __tablename__ = 'leads'
    
    id = Column(Integer, primary_key=True)
    data_collection_id = Column(Integer, ForeignKey('data_collections.id'), nullable=False)
    
    company_name = Column(String(255), nullable=False)
    source = Column(String(255))
    lead_score = Column(Float)
    industry_match = Column(Boolean, default=True)
    discovered_at = Column(DateTime, server_default=func.now())
    
    # Additional lead data
    contact_info = Column(JSON)
    notes = Column(Text)
    
    # Relationships
    data_collection = relationship("DataCollection")

class Competitor(Base):
    """Model for storing competitor information"""
    __tablename__ = 'competitors'
    
    id = Column(Integer, primary_key=True)
    data_collection_id = Column(Integer, ForeignKey('data_collections.id'), nullable=False)
    
    name = Column(String(255), nullable=False)
    market_position = Column(String(100))
    estimated_size = Column(String(50))
    focus_area = Column(String(255))
    competitive_score = Column(Float)
    discovered_via = Column(String(255))
    last_updated = Column(DateTime, server_default=func.now())
    
    # Relationships
    data_collection = relationship("DataCollection")

class DatabaseManager:
    """Database connection and session management"""
    
    def __init__(self):
        self.database_url = os.getenv('DATABASE_URL')
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable is required")
        
        self.engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
    def create_tables(self):
        """Create all database tables"""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating database tables: {str(e)}")
            raise
    
    def get_session(self):
        """Get database session"""
        return self.SessionLocal()
    
    def close_session(self, session):
        """Close database session"""
        session.close()

# Initialize database manager
db_manager = DatabaseManager()