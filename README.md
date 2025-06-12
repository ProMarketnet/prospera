# AI Agent Prospera

A comprehensive Business Intelligence Platform that empowers Small and Medium Enterprises (SMEs) with advanced market intelligence and strategic insights using cutting-edge AI technologies.

## Features

### Core Capabilities
- **Multi-Source Business Profile Import**: Automatically import business data from CrunchBase, company websites, and business databases
- **Real-Time Market Intelligence**: Live market research powered by Perplexity AI with web search capabilities
- **Advanced AI Analysis**: Comprehensive business insights using OpenAI GPT-4o and XAI Grok-2
- **Interactive AI Chat**: Smart business intelligence assistant with query routing
- **Automated Report Generation**: Professional business intelligence reports with email delivery
- **Industry Classification**: NAICS-based industry analysis and insights

### AI Integrations
- **OpenAI GPT-4o**: Strategic analysis and business recommendations
- **XAI Grok-2**: Advanced market research and competitive intelligence
- **Perplexity AI**: Real-time web research and trend analysis

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL database
- API keys for OpenAI, XAI Grok, and Perplexity

### Installation

1. Clone the repository:
```bash
git clone https://github.com/ProMarketnet/prospera.git
cd prospera
```

2. Install dependencies:
```bash
pip install -r REQUIREMENTS.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. Run the application:
```bash
streamlit run app.py --server.port 5000
```

## Configuration

### Environment Variables
```
OPENAI_API_KEY=your_openai_api_key
XAI_API_KEY=your_xai_grok_api_key
PERPLEXITY_API_KEY=your_perplexity_api_key
DATABASE_URL=postgresql://user:password@host:port/database
```

### API Key Setup
- **OpenAI**: Get from https://platform.openai.com/api-keys
- **XAI Grok**: Get from https://console.x.ai/
- **Perplexity**: Get from https://www.perplexity.ai/settings/api

## Usage

### Business Profile Setup
1. Click "Setup Business Profile" in the sidebar
2. Choose import method:
   - Auto-import from company name
   - Import from website URL
   - Import from CrunchBase
   - Manual setup

### Market Research
1. Navigate to "Industry Intelligence" tab
2. Select your industry or use business profile
3. Generate real-time market insights

### AI Chat Interface
1. Use the main chat interface for business questions
2. Smart routing automatically selects the best AI model
3. Access quick suggestions for common queries

## Architecture

### Project Structure
```
src/
├── ai/                 # AI client integrations
├── analysis/           # Business intelligence analysis
├── chat/              # AI chat interfaces
├── database/          # Database models and services
├── delivery/          # Report generation and email
├── insights/          # Industry insights engine
├── profile/           # Business profile management
├── research/          # Market intelligence
├── scraping/          # Data collection
└── utils/             # Utilities and configuration
```

### Database Schema
- **business_profiles**: Company information and settings
- **data_collections**: Raw market data and research
- **analysis_results**: AI-generated insights and recommendations

## Development

### Running Tests
```bash
python -m pytest tests/
```

### API Testing
```bash
python test_grok_api.py
python test_perplexity_api.py
```

## Deployment

### Streamlit Cloud
1. Connect your GitHub repository
2. Set environment variables in Streamlit Cloud settings
3. Deploy automatically

### Docker (Optional)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["streamlit", "run", "app.py", "--server.port", "5000"]
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Check the documentation in the `docs/` folder
- Review API setup guide in `docs/API_SETUP.md`

## Acknowledgments

- OpenAI for GPT-4o language model
- XAI for Grok-2 advanced AI capabilities
- Perplexity AI for real-time web research
- Streamlit for the web application framework