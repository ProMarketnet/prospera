"""
Credits management system for Prospera
Handles user credits, transactions, and usage tracking for the pay-per-use model
"""
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class TransactionType(Enum):
    PURCHASE = "purchase"
    USAGE = "usage"
    REFUND = "refund"
    BONUS = "bonus"

class SubscriptionTier(Enum):
    FREE = "free"
    BASIC = "basic"
    PRO = "pro"
    ENTERPRISE = "enterprise"

@dataclass
class CreditTransaction:
    """Credit transaction record"""
    id: str
    user_id: str
    transaction_type: TransactionType
    amount: int  # Positive for credits added, negative for credits used
    description: str
    created_at: datetime
    payment_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class UserCredits:
    """User credit account information"""
    user_id: str
    email: str
    credits_balance: int
    total_credits_purchased: int
    total_credits_used: int
    subscription_tier: SubscriptionTier
    created_at: datetime
    last_activity: datetime

class CreditManager:
    """Manages user credits and transactions"""
    
    # Credit costs for different actions
    CREDIT_COSTS = {
        'opportunity_report_download': 1,
        'detailed_match_analysis': 2,
        'contact_reveal': 3,
        'custom_research_report': 5,
        'competitor_intelligence': 3,
        'market_trend_analysis': 2,
        'supplier_contact_info': 2,
        'event_networking_list': 1
    }
    
    # Credit packages available for purchase
    CREDIT_PACKAGES = {
        'starter': {'credits': 10, 'price': 9.99, 'bonus': 0},
        'professional': {'credits': 50, 'price': 39.99, 'bonus': 5},
        'business': {'credits': 150, 'price': 99.99, 'bonus': 25},
        'enterprise': {'credits': 500, 'price': 299.99, 'bonus': 100}
    }
    
    def __init__(self):
        self.user_accounts = {}  # In production, this would be database storage
        
    def create_user_account(self, email: str, company_name: Optional[str] = None) -> UserCredits:
        """Create a new user credit account with free starter credits"""
        
        user_id = f"user_{hash(email)}"
        
        user_credits = UserCredits(
            user_id=user_id,
            email=email,
            credits_balance=3,  # Free starter credits
            total_credits_purchased=3,
            total_credits_used=0,
            subscription_tier=SubscriptionTier.FREE,
            created_at=datetime.now(),
            last_activity=datetime.now()
        )
        
        # Store user account
        self.user_accounts[user_id] = user_credits
        
        # Log account creation for company
        company_name_str = company_name if company_name is not None else "Unknown Company"
        logger.info(f"Credit account created for {company_name_str} ({email})")
        
        return user_credits
    
    def get_user_credits(self, user_id: str) -> Optional[UserCredits]:
        """Get user credit account information"""
        return self.user_accounts.get(user_id)
    
    def check_sufficient_credits(self, user_id: str, action: str) -> bool:
        """Check if user has sufficient credits for an action"""
        
        user_credits = self.get_user_credits(user_id)
        if not user_credits:
            return False
        
        required_credits = self.CREDIT_COSTS.get(action, 1)
        return user_credits.credits_balance >= required_credits
    
    def consume_credits(self, user_id: str, action: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Consume credits for a user action"""
        
        user_credits = self.get_user_credits(user_id)
        if not user_credits:
            return False
        
        required_credits = self.CREDIT_COSTS.get(action, 1)
        
        if user_credits.credits_balance < required_credits:
            logger.warning(f"Insufficient credits for {user_id}: need {required_credits}, have {user_credits.credits_balance}")
            return False
        
        # Deduct credits
        user_credits.credits_balance -= required_credits
        user_credits.total_credits_used += required_credits
        user_credits.last_activity = datetime.now()
        
        # Record transaction
        self._record_transaction(user_id, TransactionType.USAGE, -required_credits, 
                               f"Credits used for {action}", metadata=metadata or {})
        
        logger.info(f"Consumed {required_credits} credits for {action} (user: {user_id})")
        return True
    
    def get_available_actions(self) -> Dict[str, Dict[str, Any]]:
        """Get available actions and their credit costs"""
        
        actions = {}
        for action, cost in self.CREDIT_COSTS.items():
            actions[action] = {
                'cost': cost,
                'description': self._get_action_description(action),
                'category': self._get_action_category(action)
            }
        
        return actions
    
    def _record_transaction(self, user_id: str, transaction_type: TransactionType, 
                          amount: int, description: str, payment_id: Optional[str] = None, 
                          metadata: Optional[Dict[str, Any]] = None):
        """Record a credit transaction"""
        
        transaction = CreditTransaction(
            id=f"txn_{datetime.now().timestamp()}_{user_id}",
            user_id=user_id,
            transaction_type=transaction_type,
            amount=amount,
            description=description,
            created_at=datetime.now(),
            payment_id=payment_id,
            metadata=metadata or {}
        )
        
        # In production, save to database
        logger.info(f"Transaction recorded: {transaction.description} ({amount} credits)")
    
    def _get_action_description(self, action: str) -> str:
        """Get human-readable description for action"""
        
        descriptions = {
            'opportunity_report_download': 'Download detailed opportunity report',
            'detailed_match_analysis': 'Get detailed AI analysis of opportunity match',
            'contact_reveal': 'Reveal contact information for opportunity',
            'custom_research_report': 'Generate custom market research report',
            'competitor_intelligence': 'Access competitor analysis and insights',
            'market_trend_analysis': 'Get market trend analysis and forecasts',
            'supplier_contact_info': 'Access supplier contact information',
            'event_networking_list': 'Get networking list for business events'
        }
        
        return descriptions.get(action, action.replace('_', ' ').title())
    
    def _get_action_category(self, action: str) -> str:
        """Get category for action"""
        
        if action in ['opportunity_report_download', 'custom_research_report']:
            return 'reports'
        elif action in ['detailed_match_analysis', 'competitor_intelligence', 'market_trend_analysis']:
            return 'research'
        elif action in ['contact_reveal', 'supplier_contact_info', 'event_networking_list']:
            return 'contact'
        else:
            return 'general'
