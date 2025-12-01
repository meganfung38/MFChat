# MFChat Intent Classification Guide

## Overview

MFChat now intelligently determines what information the user wants and provides focused, non-verbose responses.

---

## Three Response Types

### 1. **Basic Info** (Salesforce Metadata Only)
**What it returns:** Campaign name, ID, channel, type, and enriched context  
**What it DOESN'T return:** AI-generated sales description  
**Tools called:** `get_campaign_data` + `enrich_campaign_context`

**Example Prompts:**
- "Give me the Salesforce information about campaign 701Hr000001L82yIAC"
- "What's the channel and type for 701Hr000001L9q4IAC?"
- "Show me the metadata for campaign 701TU00000ad4whYAA"
- "SFDC info for 701Hr000001L8QHIA0"

---

### 2. **AI Description** (Sales Guidance Only) - DEFAULT
**What it returns:** Brief context + AI-generated sales description (engagement, intent, next steps)  
**What it emphasizes:** Actionable sales guidance  
**Tools called:** All three tools, but response focuses on AI description

**Example Prompts:**
- "What is 701Hr000001L82yIAC?" ✅ **This should now give AI description only**
- "Tell me about campaign 701Hr000001L9q4IAC"
- "What can you tell me about 701TU00000ad4whYAA?"
- "Give me a description of 701Hr000001L8QHIA0"
- "Describe this campaign: 701TU00000ayWTJYA2"
- "Quick summary of 701Hr000001L82yIAC"
- "Enhance campaign 701Hr000001L9q4IAC"

**This is the default** if user intent is unclear - it's the most useful for sales reps!

---

### 3. **Full Analysis** (Everything)
**What it returns:** Complete analysis with all details  
**Tools called:** All three tools, comprehensive output

**Example Prompts:**
- "Give me a full analysis of campaign 701Hr000001L82yIAC"
- "I need complete information on 701Hr000001L9q4IAC"
- "Full details for 701TU00000ad4whYAA"
- "Comprehensive analysis of campaign 701Hr000001L8QHIA0"
- "Give me everything about 701TU00000ayWTJYA2"

---

## Bot Identity Questions

When users ask "what are you" or similar questions:

**Example Prompts:**
- "MFChat what are you"
- "What do you do?"
- "What is this bot?"
- "Tell me about yourself"
- "What are your capabilities?"

**Response:** Detailed explanation of bot's purpose, three types of requests, requirements, and examples.

---

## Help Requests

**Example Prompts:**
- "help"
- "how to use"
- "what can you do"
- "commands"

**Response:** Comprehensive help with examples for all three request types.

---

## No Campaign ID Provided

**Response:** Friendly message explaining:
- What MFChat does
- Three types of information available
- Requirement for campaign ID
- Examples of each request type
- Invitation to say "help" or "what are you"

---

## Out of Scope Requests

If a user asks something the bot can't do (e.g., "search for campaigns about healthcare"), the bot will:
1. Politely explain it can't do that
2. Inform them of available capabilities
3. Provide examples of valid requests

---

## Intent Classification Logic

The bot classifies intent by looking for keywords:

### Full Analysis Keywords:
- "full analysis", "complete analysis", "full contextual"
- "everything", "all information", "comprehensive"

### Basic Info Keywords:
- "salesforce information", "sfdc info", "campaign type"
- "channel", "enriched context", "metadata"

### AI Description Keywords (Default):
- "what is", "what can you tell me", "describe"
- "summary", "enhance", "tell me about", "explain"

**Default:** If unclear, assume AI description (most useful for sales)

---

## Testing Examples

### Test 1: Basic Info
```
User: "Give me the Salesforce information for 701Hr000001L82yIAC"
Expected: Campaign name, ID, channel, type, enriched context ONLY
Should NOT include: AI description
```

### Test 2: AI Description (The Fixed Case!)
```
User: "What is 701Hr000001L82yIAC?"
Expected: Brief context + focused AI sales description
Should NOT include: Verbose full analysis
```

### Test 3: Full Analysis
```
User: "Give me a full analysis of 701Hr000001L82yIAC"
Expected: Everything - metadata, context, and AI description
```

### Test 4: Bot Identity
```
User: "MFChat what are you"
Expected: Detailed description of purpose and capabilities
Should NOT: Try to extract campaign ID
```

### Test 5: No Campaign ID
```
User: "MFChat hello"
Expected: Friendly explanation of capabilities and examples
Should NOT: Return error
```

---

## Key Improvements

✅ **Less Verbose** - Returns only what user asks for  
✅ **Smarter** - Understands user intent from natural language  
✅ **Better Identity** - Properly introduces itself when asked  
✅ **Clearer Help** - Shows all three types of requests  
✅ **No False Positives** - Won't try to analyze non-campaign ID messages  

---

**Status:** Ready to test! 🚀

