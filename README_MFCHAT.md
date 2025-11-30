# MFChat - Campaign Clarity Bot

AI-powered RingCentral chatbot that analyzes Salesforce campaigns and generates sales-friendly descriptions using OpenAI Agents SDK.

## 🚀 Quick Start

```bash
# Install dependencies
source venv/bin/activate
pip install -r requirements.txt

# Configure credentials
cp .env.example .env
# Edit .env with your credentials

# Start the bot
./bin/proxy          # Terminal 1: Start ngrok
rcs bot.py           # Terminal 2: Start bot
```

## 📚 Documentation

- **[Usage Guide](MFCHAT_USAGE.md)** - Complete usage instructions
- **[Project Summary](MFCHAT_PROJECT_SUMMARY.md)** - Technical overview

## ✨ Features

- 🔍 **Salesforce Integration** - Direct campaign data fetching
- 🤖 **OpenAI Agents** - GPT-4o powered analysis
- 📊 **8 Prompt Strategies** - Channel-specific descriptions
- 💬 **Natural Language** - Flexible, conversational interface
- 🎯 **Sales Enablement** - Buyer intent & follow-up guidance

## 🛠️ Architecture

```
RingCentral Chat → MFChat Bot → OpenAI Agent → [3 Tools] → Response
                                                      ↓
                                          [Salesforce | Context | AI]
```

## 📋 Example Usage

```
@MFChat 701Hr000001L82yIAC
@MFChat analyze campaign 701Hr000001L9q4IAC
@MFChat help
```

## 🔒 Security Note

This repository does NOT include:
- `.env` files (credentials)
- `field_mappings.json` (sensitive RingCentral business data)
- Sample campaign feedback files
- Any customer or prospect data

**To run this bot, you need:**
1. Salesforce credentials (SF_USERNAME, SF_PASSWORD, SF_SECURITY_TOKEN)
2. OpenAI API key
3. RingCentral bot credentials
4. Field mappings file (request from project maintainer)

## 📁 Project Structure

```
MFChat/
├── bot.py                    # Main bot with Campaign Clarity
├── agents/                   # OpenAI Agent system
│   ├── campaign_agent.py     # Agent orchestrator
│   └── tools/               # Salesforce, Context, AI tools
├── SFDC_Campaign_Clarity/   # Campaign analysis engine
├── requirements.txt         # Python dependencies
└── docs/                    # Documentation
```

## 🧪 Testing

Start the bot and test with:
```
@MFChat help
@MFChat 701Hr000001L82yIAC
```

## 💡 Built With

- **Python 3.12+**
- **OpenAI GPT-4o** - AI agent orchestration
- **Salesforce API** - Campaign data retrieval
- **RingCentral Bot Framework** - Chat integration
- **Pandas** - Data processing

## 📄 License

Internal RingCentral tool - Not for public distribution

## 👤 Author

**Megan Fung** - Summer Intern 2025

---

**For detailed setup and usage instructions, see [MFCHAT_USAGE.md](MFCHAT_USAGE.md)**

