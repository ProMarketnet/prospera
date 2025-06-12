#!/bin/bash

# AI Agent Prospera - GitHub Deployment Script
# Run this script after downloading the repository files locally

echo "🚀 Deploying AI Agent Prospera to GitHub..."

# Initialize Git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: AI Agent Prospera Business Intelligence Platform

- Multi-source business profile import (CrunchBase, websites, databases)
- Real-time market intelligence with Perplexity AI
- Advanced AI analysis using OpenAI GPT-4o and XAI Grok-2
- Interactive chat interface with smart query routing
- Automated report generation and email delivery
- PostgreSQL database integration
- NAICS industry classification system
- Professional Streamlit web interface"

# Add remote repository
git remote add origin https://github.com/ProMarketnet/prospera.git

# Push to GitHub
git push -u origin main

echo "✅ Deployment complete! Your repository is live at:"
echo "https://github.com/ProMarketnet/prospera"

echo ""
echo "📋 Next Steps:"
echo "1. Set up API keys in your deployment platform"
echo "2. Configure PostgreSQL database"
echo "3. Deploy to Streamlit Cloud or Railway"
echo "4. Update README with your specific setup instructions"