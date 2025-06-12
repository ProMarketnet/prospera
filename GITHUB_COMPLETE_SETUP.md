# AI Agent Prospera - Complete GitHub Repository

## Repository Structure

```
ai-agent-prospera/
├── README.md                          # Main project documentation
├── REQUIREMENTS.txt                   # Python dependencies
├── .gitignore                        # Git ignore rules
├── .env.example                      # Environment variables template
├── app.py                           # Main Streamlit application
├── test_grok_api.py                 # XAI Grok API testing
├── test_perplexity_api.py           # Perplexity API testing
├── .streamlit/
│   └── config.toml                  # Streamlit configuration
├── src/
│   ├── __init__.py
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── grok_client.py           # XAI Grok integration
│   │   └── perplexity_client.py     # Perplexity AI integration
│   ├── analysis/
│   │   ├── __init__.py
│   │   ├── ai_analyzer.py           # AI-powered analysis
│   │   └── business_intelligence.py # Business insights generation
│   ├── chat/
│   │   ├── __init__.py
│   │   ├── ai_chat_interface.py     # Main chat interface
│   │   ├── chat_utils.py            # Chat utilities
│   │   └── simple_chat.py           # Simple chat implementation
│   ├── database/
│   │   ├── __init__.py
│   │   ├── db_service.py            # Database operations
│   │   ├── models.py                # SQLAlchemy models
│   │   └── repository.py            # Data repository pattern
│   ├── delivery/
│   │   ├── __init__.py
│   │   ├── email_templates.py       # Email template system
│   │   └── report_dashboard.py      # Report delivery interface
│   ├── insights/
│   │   └── industry_insights.py     # Industry intelligence engine
│   ├── profile/
│   │   ├── __init__.py
│   │   ├── business_importer.py     # Multi-source data import
│   │   ├── business_profile.py      # Business profile models
│   │   ├── directory_importer.py    # Directory data import
│   │   ├── industry_classifier.py   # NAICS classification
│   │   └── profile_wizard.py        # Profile creation wizard
│   ├── research/
│   │   └── market_intelligence.py   # Market research engine
│   ├── scrapers/
│   │   ├── __init__.py
│   │   └── industry_scraper.py      # Web scraping utilities
│   └── utils/
│       ├── __init__.py
│       ├── config.py                # Configuration management
│       ├── industry_config.py       # Industry definitions
│       ├── logger.py                # Logging utilities
│       └── web_scraper.py           # Web scraping tools
├── data/
│   └── industry_config.json         # Industry configuration data
├── docs/
│   └── API_SETUP.md                 # API setup documentation
└── logs/                            # Application logs (auto-created)
```

## Setup Instructions

### 1. Clone and Setup
```bash
git clone https://github.com/ProMarketnet/prospera.git
cd prospera
pip install -r REQUIREMENTS.txt
```

### 2. Environment Configuration
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Run Application
```bash
streamlit run app.py --server.port 5000
```

## Required API Keys

1. **OpenAI API Key**: https://platform.openai.com/api-keys
2. **XAI Grok API Key**: https://console.x.ai/
3. **Perplexity AI API Key**: https://www.perplexity.ai/settings/api
4. **Database URL**: PostgreSQL connection string

## Key Features

- **Multi-Source Business Import**: CrunchBase, websites, business databases
- **Real-Time Market Intelligence**: Perplexity AI web research
- **Advanced AI Analysis**: OpenAI GPT-4o + XAI Grok-2
- **Interactive Chat Interface**: Smart query routing
- **Automated Reporting**: Email delivery system
- **Industry Intelligence**: NAICS-based classification

## Files Already in Current Directory

All source files are already present in your current Replit workspace:
- `app.py` - Main application (2,196 lines)
- `src/` directory with all modules
- `.streamlit/config.toml` - Streamlit configuration
- Database models and services
- AI client integrations
- Business profile import system

## GitHub Commands

```bash
# Initialize repository
git init

# Add all files
git add .

# Initial commit
git commit -m "Initial commit: AI Agent Prospera Business Intelligence Platform"

# Add remote repository
git remote add origin https://github.com/ProMarketnet/prospera.git

# Push to GitHub
git push -u origin main
```

## Production Deployment Options

1. **Streamlit Cloud** (Recommended)
   - Connect GitHub repository
   - Set environment variables
   - Auto-deploy on push

2. **Railway**
   - One-click deployment
   - Automatic PostgreSQL addon
   - Custom domain support

3. **Heroku**
   - Traditional PaaS deployment
   - Add PostgreSQL addon
   - Configure environment variables

Your complete business intelligence platform is ready for GitHub deployment with professional documentation, proper file organization, and production-ready configuration.