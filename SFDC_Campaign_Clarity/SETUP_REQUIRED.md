# SFDC Campaign Clarity - Setup Required

## ⚠️ Missing Files Required to Run

This directory contains the SFDC Campaign Clarity engine used by MFChat, but **some files are not included** in the repository for security reasons.

### Required Files (Not Included)

#### 1. **Field Mappings** (CRITICAL)
- **File**: `data/field_mappings.json`
- **Why**: Contains sensitive RingCentral business intelligence mappings
- **How to get**: Request from [megan.fung@ringcentral.com](mailto:megan.fung@ringcentral.com)
- **Required**: YES - System will not work without this file

#### 2. **Credentials** (CRITICAL)
- **File**: `.env`
- **Why**: Contains Salesforce and OpenAI API credentials
- **How to get**: Create from `.env.example` template
- **Required**: YES - System cannot connect without credentials

#### 3. **Sample Outputs** (Optional)
- **Directory**: `feedback_+_samples/`
- **Why**: Contains actual RingCentral campaign data and feedback
- **Required**: NO - Only for reference/testing

---

## Quick Setup

### 1. Get Required Files

Contact the project maintainer to obtain:
- `data/field_mappings.json`
- Salesforce credentials
- OpenAI API key

### 2. Create .env File

```bash
cd SFDC_Campaign_Clarity
cp .env.example .env
# Edit .env with your credentials
```

Required in `.env`:
```bash
SF_USERNAME=your.email@company.com
SF_PASSWORD=your_password
SF_SECURITY_TOKEN=your_token
SF_DOMAIN=login  # or 'test' for sandbox

OPENAI_API_KEY=sk-your-key-here
```

### 3. Install Dependencies

```bash
cd ..  # Back to project root
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Test Connection

```bash
# From project root
python -c "from agents import CampaignAgent; agent = CampaignAgent(); print('✅ Setup successful!')"
```

---

## What This Code Does

The SFDC Campaign Clarity engine provides:
- **Salesforce Integration** - Fetches campaign metadata
- **Context Enrichment** - Translates technical fields to sales insights
- **AI Description Generation** - Creates channel-specific descriptions
- **8 Prompt Strategies** - Tailored for different campaign types

This code is integrated into MFChat via the OpenAI Agents SDK.

---

## Security Note

The following are **excluded from git** for security:
- ✅ `.env` files (credentials)
- ✅ `data/field_mappings.json` (business intelligence)
- ✅ `feedback_+_samples/` (actual campaign data)
- ✅ `logs/` (may contain sensitive info)
- ✅ `cache/` (may contain campaign IDs)
- ✅ `*.xlsx` (output reports with campaign data)

These files are safe to have locally but should **never** be committed to git.

---

**For detailed usage, see the main [MFCHAT_USAGE.md](../MFCHAT_USAGE.md)**

