"""Utility functions for AI chat interface"""

from typing import Dict, List, Any
import streamlit as st
import os
from openai import OpenAI

def get_openai_client():
    """Get OpenAI client with proper error handling"""
    try:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found")
        return OpenAI(api_key=api_key)
    except Exception as e:
        st.error(f"OpenAI configuration error: {e}")
        return None

def format_messages_for_openai(messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Format messages for OpenAI API compatibility"""
    formatted_messages = []
    
    for msg in messages:
        if "role" in msg and "content" in msg:
            formatted_messages.append({
                "role": msg["role"],
                "content": str(msg["content"])
            })
    
    return formatted_messages

def generate_ai_response_safe(client, messages: List[Dict[str, str]]) -> str:
    """Generate AI response with proper error handling"""
    try:
        if not client:
            return "AI service is currently unavailable. Please check your configuration."
        
        formatted_messages = format_messages_for_openai(messages)
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=formatted_messages,
            max_tokens=1000,
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        return content if content else "I'm unable to provide a response at the moment."
        
    except Exception as e:
        return f"I'm experiencing technical difficulties: {str(e)}"