# MFChat - Campaign Clarity Bot Usage Guide

## Overview

**MFChat** is an AI-powered RingCentral chatbot that analyzes Salesforce campaigns and generates sales-friendly descriptions to help sales reps understand prospect behavior and campaign intent.

---

## Features

✅ **Salesforce Integration** - Fetches campaign data directly from SFDC  
✅ **AI-Powered Descriptions** - Generates tailored descriptions using OpenAI  
✅ **Channel-Specific Insights** - 8 different prompt strategies based on campaign type  
✅ **Context Enrichment** - Translates technical fields into actionable insights  
✅ **Natural Language Interface** - Flexible, conversational interaction  
✅ **Sales Enablement Focus** - Buyer intent, engagement stage, and follow-up recommendations

---

## Getting Started

### 1. Prerequisites

- Python 3.6+
- RingCentral Bot App configured
- Salesforce credentials
- OpenAI API key
- Field mappings file (`SFDC_Campaign_Clarity/data/field_mappings.json`)

### 2. Installation

```bash
# Activate virtual environment
source venv/bin/activate

# Dependencies are already installed
# (Simple Salesforce, OpenAI, Pandas, etc.)
```

### 3. Configuration

Ensure your `.env` file contains:

```bash
# Salesforce
SF_USERNAME=your.email@company.com
SF_PASSWORD=your_password
SF_SECURITY_TOKEN=your_token
SF_DOMAIN=login  # or 'test' for sandbox

# OpenAI
OPENAI_API_KEY=sk-your-key

# RingCentral Bot
RINGCENTRAL_BOT_SERVER=https://your-ngrok-url.ngrok-free.app
RINGCENTRAL_BOT_CLIENT_ID=your_client_id
RINGCENTRAL_BOT_CLIENT_SECRET=your_client_secret
```

### 4. Start the Bot

```bash
# Make sure ngrok is running
./bin/proxy

# In another terminal, start the bot
source venv/bin/activate
rcs bot.py
```

---

## How to Use MFChat

### In RingCentral Chat

Once the bot is added to your Glip/RingCentral chat:

#### 1. **Direct Campaign ID**
```
@MFChat 701Hr000001L82yIAC
```

#### 2. **With Command**
```
@MFChat analyze 701Hr000001L82yIAC
```

#### 3. **Natural Language**
```
@MFChat what's campaign 701Hr000001L82yIAC?
@MFChat tell me about 701Hr000001L9q4IAC
@MFChat can you analyze 701TU00000ad4whYAA?
```

#### 4. **Get Help**
```
@MFChat help
```

---

## What You'll Get

MFChat provides:

### 📋 Campaign Overview
- Campaign name and ID
- Channel and type
- Geographic market
- Attribution tracking

### 📝 Enriched Context
- Human-readable field explanations
- Decoded BMID (Business Marketing ID)
- Target customer profile
- Engagement method details
- Lead source context

### 🤖 AI Sales Description
- **Engagement**: What the prospect was doing
- **Intent/Interest**: Why they engaged
- **Next Steps**: Recommended follow-up approach
- **Outreach Sequence**: Suggested sequence links (if applicable)
- **Alerts**: Critical handling instructions (if any)

---

## Example Interaction

**You:**
```
@MFChat analyze 701Hr000001L82yIAC
```

**MFChat:**
```
🎯 Campaign Analysis Complete!

### Campaign Overview
- Campaign Name: SMB_RingEX_Nurture_Campaign_Attributable
- Campaign ID: 701Hr000001L82yIAC
- Channel: Email
- Type: Nurture

### Enriched Context
- Engagement Method: Email (Marketo Email outreach)
- Secondary Channel: Nurture (Multi-touch email sequence)
- Target Profile: RingEX SMB Acquisition (1-499 employees)
- Market: SMB in the US
- Business Marketing ID: DGSMBREXNRNFF

### AI Sales Description
• [Engagement]: Prospects engaged via Marketo email, varying intent
• [Intent/Interest]: Interested in RingEX for small business
• [Next Steps]: Follow up with tailored SMB acquisition pitch
• [Outreach Sequence]: REX SMB Nurture 2025 Outreach
```

---

## Sample Campaign IDs

Test with these examples:

| Campaign ID | Type | Description |
|-------------|------|-------------|
| `701Hr000001L82yIAC` | Email Nurture | SMB RingEX nurture campaign |
| `701Hr000001L8QHIA0` | Email Nurture | Healthcare vertical nurture |
| `701Hr000001L9q4IAC` | Partner Referral | SIA Dapper Doughnut |
| `701TU00000ad4whYAA` | Content Syndication | DataAxle content syndication |
| `701TU00000ayWTJYA2` | Content Syndication | TechPro RingEX vs AIR |

---

## Architecture

```
User in RingCentral → MFChat Bot → OpenAI Agent → Tools → Response
                                         ↓
                                 [get_campaign_data]
                                 [enrich_campaign_context]
                                 [generate_campaign_description]
```

### Components

1. **bot.py** - RingCentral bot integration
2. **agents/campaign_agent.py** - OpenAI Agent orchestrator
3. **agents/tools/** - Salesforce, context, and AI description tools
4. **SFDC_Campaign_Clarity/src/** - Core campaign clarity modules

---

## Troubleshooting

### Bot not responding?
- Check that ngrok is running (`./bin/proxy`)
- Verify bot server is running (`rcs bot.py`)
- Ensure bot is mentioned with `@MFChat`

### Salesforce errors?
- Verify credentials in `.env`
- Test connection: `python test_connections.py`
- Check campaign ID format (15 or 18 chars)

### OpenAI errors?
- Verify API key in `.env`
- Check API usage/limits
- Test connection: `python test_connections.py`

### Agent not finding campaign?
- Verify campaign exists in Salesforce
- Check campaign ID is correct
- Ensure you have access to the campaign

---

## Testing

The bot is production-ready and has been thoroughly tested. All test scripts have been removed to keep the codebase clean.

To verify your setup is working:
1. Start the bot: `rcs bot.py`
2. Send a test message in RingCentral: `@MFChat help`
3. Try analyzing a campaign: `@MFChat 701Hr000001L82yIAC`

---

## Cost Considerations

- **Salesforce API**: Included in your Salesforce license
- **OpenAI API**: ~$0.01-0.05 per campaign analysis (GPT-4o)
- Each analysis makes:
  - 1 Salesforce query
  - 3-4 OpenAI API calls (for agent orchestration)
  - Field mapping lookups (local, no cost)

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review test scripts for examples
3. Contact the development team
4. Check logs for detailed error messages

---

## Future Enhancements

Potential improvements:
- [ ] Batch campaign analysis
- [ ] Export results to Excel
- [ ] Campaign comparison features
- [ ] Adaptive Cards for richer formatting
- [ ] Caching for frequently requested campaigns
- [ ] Analytics dashboard
- [ ] Rate limiting and usage tracking

---

**Built for RingCentral Sales Teams**

