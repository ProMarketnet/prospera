import streamlit as st
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

from ..utils.logger import setup_logger
from .chat_utils import get_openai_client, generate_ai_response_safe

logger = setup_logger(__name__)

class AIChatInterface:
    """Sleek AI chat interface for business intelligence conversations"""
    
    def __init__(self):
        self.openai_client = get_openai_client()
        self.system_prompt = self._get_system_prompt()
    
    def render_chat_interface(self):
        """Render the modern AI chat interface"""
        
        # Initialize chat history in session state
        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = [
                {
                    "role": "assistant",
                    "content": "👋 Hello! I'm your AI Business Intelligence Assistant. I can help you analyze market trends, discover leads, understand competitors, and provide strategic insights for your business. What would you like to explore today?",
                    "timestamp": datetime.now().isoformat()
                }
            ]
        
        # Custom CSS for sleek chat design
        st.markdown("""
        <style>
        .chat-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            padding: 25px;
            margin: 20px 0;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .chat-header {
            text-align: center;
            color: white;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        
        .chat-message {
            margin: 15px 0;
            padding: 15px 20px;
            border-radius: 18px;
            max-width: 80%;
            word-wrap: break-word;
            animation: fadeIn 0.5s ease-in;
        }
        
        .user-message {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            margin-left: auto;
            text-align: right;
            box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3);
        }
        
        .assistant-message {
            background: white;
            color: #2c3e50;
            margin-right: auto;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border-left: 4px solid #667eea;
        }
        
        .chat-input-container {
            background: white;
            border-radius: 25px;
            padding: 10px 20px;
            margin-top: 20px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            border: 2px solid transparent;
            transition: all 0.3s ease;
        }
        
        .chat-input-container:focus-within {
            border-color: #667eea;
            box-shadow: 0 5px 25px rgba(102, 126, 234, 0.2);
        }
        
        .typing-indicator {
            display: flex;
            align-items: center;
            padding: 15px 20px;
            background: rgba(255,255,255,0.9);
            border-radius: 18px;
            margin: 10px 0;
            max-width: 150px;
        }
        
        .typing-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #667eea;
            margin: 0 2px;
            animation: typing 1.4s infinite ease-in-out;
        }
        
        .typing-dot:nth-child(1) { animation-delay: -0.32s; }
        .typing-dot:nth-child(2) { animation-delay: -0.16s; }
        
        @keyframes typing {
            0%, 80%, 100% { transform: scale(0); opacity: 0.5; }
            40% { transform: scale(1); opacity: 1; }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .chat-suggestions {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 20px 0;
        }
        
        .suggestion-chip {
            background: rgba(255,255,255,0.2);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            border: 1px solid rgba(255,255,255,0.3);
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 14px;
        }
        
        .suggestion-chip:hover {
            background: rgba(255,255,255,0.3);
            transform: translateY(-2px);
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Chat container
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Chat header
        st.markdown('<div class="chat-header">🤖 AI Business Intelligence Assistant</div>', unsafe_allow_html=True)
        
        # Display chat messages
        self._display_chat_messages()
        
        # Quick suggestions (only show if conversation is new)
        if len(st.session_state.chat_messages) <= 1:
            self._display_quick_suggestions()
        
        # Chat input
        self._render_chat_input()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def _display_chat_messages(self):
        """Display chat messages with styling"""
        
        for message in st.session_state.chat_messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
    
    def _display_quick_suggestions(self):
        """Display quick suggestion chips"""
        
        suggestions = [
            "Analyze my industry trends",
            "Find potential leads",
            "Research my competitors",
            "Market opportunity analysis",
            "Growth strategy recommendations"
        ]
        
        st.markdown('<div class="chat-suggestions">', unsafe_allow_html=True)
        
        cols = st.columns(len(suggestions))
        for i, suggestion in enumerate(suggestions):
            with cols[i]:
                if st.button(suggestion, key=f"suggestion_{i}", help="Click to ask this question"):
                    self._process_user_message(suggestion)
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def _render_chat_input(self):
        """Render the chat input field"""
        
        st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
        
        # Create columns for input and send button
        col1, col2 = st.columns([4, 1])
        
        with col1:
            user_input = st.text_input(
                "Type your message...",
                key="chat_input",
                placeholder="Ask me about market trends, competitors, leads, or strategic insights...",
                label_visibility="collapsed"
            )
        
        with col2:
            send_button = st.button("Send", key="send_button", type="primary")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Process message when send button is clicked or Enter is pressed
        if send_button and user_input.strip():
            self._process_user_message(user_input)
            st.rerun()
        
        # Handle Enter key press
        if user_input and st.session_state.get("chat_input_submitted", False):
            self._process_user_message(user_input)
            st.session_state.chat_input_submitted = False
            st.rerun()
    
    def _process_user_message(self, user_message: str):
        """Process user message and generate AI response"""
        
        # Add user message to chat history
        st.session_state.chat_messages.append({
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Generate AI response
        try:
            with st.spinner("🤔 Thinking..."):
                ai_response = self._generate_ai_response_safe(user_message)
                
                # Add AI response to chat history
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": ai_response,
                    "timestamp": datetime.now().isoformat()
                })
                
        except Exception as e:
            logger.error(f"Error generating AI response: {e}")
            error_response = "I apologize, but I'm having trouble processing your request right now. Please try again in a moment or contact support if the issue persists."
            
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": error_response,
                "timestamp": datetime.now().isoformat()
            })
        
        # Clear the input
        if "chat_input" in st.session_state:
            st.session_state.chat_input = ""
    
    def _generate_ai_response_safe(self, user_message: str) -> str:
        """Generate AI response using OpenAI with proper error handling"""
        
        # Prepare conversation history for context
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add recent chat history (last 10 messages for context)
        recent_messages = st.session_state.chat_messages[-10:]
        for msg in recent_messages:
            if msg["role"] in ["user", "assistant"]:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        # Get business context if available
        business_context = self._get_business_context()
        if business_context:
            messages.insert(1, {
                "role": "system", 
                "content": f"Current business context: {business_context}"
            })
        
        # Generate response using the utility function
        return generate_ai_response_safe(self.openai_client, messages)
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the AI assistant"""
        
        return """You are an expert AI Business Intelligence Assistant for AI Agent Prospera platform. 
        
        Your role is to help business owners and entrepreneurs with:
        
        1. **Market Analysis**: Analyze industry trends, market opportunities, and competitive landscapes
        2. **Lead Discovery**: Help identify potential customers and business opportunities
        3. **Competitive Intelligence**: Provide insights about competitors and market positioning
        4. **Strategic Planning**: Offer actionable recommendations for business growth
        5. **Data Interpretation**: Explain business intelligence findings in clear, actionable terms
        
        **Communication Style:**
        - Professional yet conversational
        - Focus on actionable insights
        - Use business terminology appropriately
        - Provide specific, practical recommendations
        - Ask clarifying questions when needed
        
        **Capabilities:**
        - Access to real-time market data and trends
        - Industry analysis and benchmarking
        - Lead scoring and qualification insights
        - Competitive positioning analysis
        - Growth strategy recommendations
        
        **Guidelines:**
        - Always provide practical, actionable advice
        - Support recommendations with data-driven insights
        - Ask for clarification when requests are vague
        - Offer next steps and follow-up actions
        - Maintain confidentiality of business information
        
        Be helpful, insightful, and focused on driving business results."""
    
    def _get_business_context(self) -> Optional[str]:
        """Get current business profile context if available"""
        
        try:
            if "current_profile" in st.session_state and st.session_state.current_profile:
                profile = st.session_state.current_profile
                context = f"""
                Company: {profile.get('company_name', 'N/A')}
                Industry: {profile.get('industry', 'N/A')}
                Business Size: {profile.get('business_size', 'N/A')}
                Location: {profile.get('location', 'N/A')}
                Products/Services: {', '.join(profile.get('primary_products', []))}
                Target Markets: {', '.join(profile.get('target_markets', []))}
                """
                return context
        except Exception as e:
            logger.error(f"Error getting business context: {e}")
        
        return None
    
    def clear_chat_history(self):
        """Clear the chat history"""
        if "chat_messages" in st.session_state:
            st.session_state.chat_messages = [
                {
                    "role": "assistant",
                    "content": "Chat history cleared. How can I help you today?",
                    "timestamp": datetime.now().isoformat()
                }
            ]
    
    def export_chat_history(self) -> str:
        """Export chat history as JSON"""
        try:
            return json.dumps(st.session_state.chat_messages, indent=2)
        except Exception as e:
            logger.error(f"Error exporting chat history: {e}")
            return "Error exporting chat history"