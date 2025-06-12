# API Setup Guide

This guide explains how to obtain and configure the required API keys for AI Agent Prospera.

## Required API Keys

### 1. OpenAI API Key
**Purpose**: Strategic analysis, business recommendations, and AI chat interface

**Setup Steps**:
1. Visit https://platform.openai.com/api-keys
2. Sign in or create an OpenAI account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. Add to your `.env` file: `OPENAI_API_KEY=sk-your-key-here`

**Pricing**: Pay-per-use, approximately $0.01-0.03 per 1K tokens

### 2. XAI Grok API Key
**Purpose**: Advanced market research and competitive intelligence

**Setup Steps**:
1. Visit https://console.x.ai/
2. Create an account or sign in
3. Navigate to API Keys section
4. Generate a new API key
5. Add to your `.env` file: `XAI_API_KEY=xai-your-key-here`

**Note**: XAI Grok requires credits purchase for full functionality

### 3. Perplexity AI API Key
**Purpose**: Real-time web research and trend analysis

**Setup Steps**:
1. Visit https://www.perplexity.ai/settings/api
2. Sign up for a Perplexity account
3. Subscribe to Pro plan (required for API access)
4. Generate API key in settings
5. Add to your `.env` file: `PERPLEXITY_API_KEY=pplx-your-key-here`

**Pricing**: $20/month for Pro plan includes API access

## Optional API Keys

### CrunchBase API (Optional)
**Purpose**: Enhanced business profile import functionality

1. Visit https://data.crunchbase.com/docs
2. Apply for API access
3. Add to `.env`: `CRUNCHBASE_API_KEY=your-key-here`

### Clearbit API (Optional)
**Purpose**: Company data enrichment

1. Visit https://clearbit.com/docs/enrichment
2. Sign up for account
3. Add to `.env`: `CLEARBIT_API_KEY=your-key-here`

## Database Setup

### PostgreSQL Database
**Purpose**: Store business profiles, analysis results, and historical data

**Option 1: Local PostgreSQL**
1. Install PostgreSQL locally
2. Create database: `createdb ai_agent_prospera`
3. Set `DATABASE_URL=postgresql://username:password@localhost:5432/ai_agent_prospera`

**Option 2: Cloud Database (Recommended)**
- **Neon**: https://neon.tech (Free tier available)
- **Supabase**: https://supabase.com (Free tier available)
- **Railway**: https://railway.app (PostgreSQL addon)

## Environment Configuration

Create `.env` file in project root:

```bash
# Required API Keys
OPENAI_API_KEY=sk-your-openai-key-here
XAI_API_KEY=xai-your-xai-key-here
PERPLEXITY_API_KEY=pplx-your-perplexity-key-here

# Database
DATABASE_URL=postgresql://user:password@host:port/database

# Optional API Keys
CRUNCHBASE_API_KEY=your-crunchbase-key-here
CLEARBIT_API_KEY=your-clearbit-key-here
LINKEDIN_API_KEY=your-linkedin-key-here

# Application Settings
DEBUG=False
LOG_LEVEL=INFO
```

## Testing API Keys

Run the test scripts to verify your API keys:

```bash
# Test OpenAI
python -c "from openai import OpenAI; client = OpenAI(); print('OpenAI: OK')"

# Test XAI Grok
python test_grok_api.py

# Test Perplexity
python test_perplexity_api.py
```

## Cost Estimation

**Monthly costs for typical SME usage**:
- OpenAI: $10-50 (depending on usage)
- XAI Grok: $25+ (credit-based)
- Perplexity: $20 (Pro subscription)
- Database: $0-10 (free tiers available)

**Total estimated monthly cost**: $55-105

## Security Best Practices

1. **Never commit API keys to Git**
   - Use `.env` files (added to `.gitignore`)
   - Use environment variables in production

2. **Rotate keys regularly**
   - Generate new keys monthly
   - Revoke old keys immediately

3. **Set usage limits**
   - Configure spending limits in API dashboards
   - Monitor usage regularly

4. **Use least privilege**
   - Only grant necessary permissions
   - Use separate keys for development/production

## Troubleshooting

### Common Issues

**OpenAI "Invalid API Key"**
- Verify key starts with `sk-`
- Check for extra spaces or characters
- Ensure account has billing enabled

**XAI Grok "Insufficient Credits"**
- Purchase credits at https://console.x.ai/
- Check credit balance in dashboard

**Perplexity "Unauthorized"**
- Verify Pro subscription is active
- Check API key in account settings

**Database Connection Error**
- Verify DATABASE_URL format
- Check network connectivity
- Ensure database exists and is accessible

### Getting Help

1. Check API provider documentation
2. Verify account status and billing
3. Test with minimal examples
4. Contact API provider support if needed

## Production Deployment

For production deployment:

1. Use secure secret management (AWS Secrets Manager, etc.)
2. Set up monitoring and alerting
3. Configure backup strategies
4. Implement proper logging
5. Set up CI/CD pipelines