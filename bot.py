"""
MFChat Bot - Campaign Clarity Assistant

This bot analyzes Salesforce campaigns and generates AI-powered descriptions
to help sales reps understand prospect behavior and campaign intent.
"""
__name__ = 'localConfig'
__package__ = 'ringcentral_bot_framework'

import copy
import re
from agents import CampaignAgent

# Initialize the Campaign Clarity Agent
campaign_agent = CampaignAgent()

def botJoinPrivateChatAction(bot, groupId, user, dbAction):
    """
    This is invoked when the bot is added to a private group.
    """
    welcome_message = f"""👋 Hello! I'm **MFChat**, your Campaign Clarity assistant!

I can analyze Salesforce campaigns and provide AI-powered insights to help you understand prospect behavior.

**How to use me:**
• Send me a campaign ID: `701Hr000001L82yIAC`
• Ask me to analyze: `analyze 701Hr000001L82yIAC`
• Ask about a campaign: `what is campaign 701Hr000001L82yIAC?`
• Get help: `help`

Just mention me with ![:Person]({bot.id}) and your request!"""
    
    bot.sendMessage(
        groupId,
        {
            'text': welcome_message
        }
    )

def extract_campaign_id(text):
    """
    Extract Salesforce campaign ID from text.
    Campaign IDs are 15 or 18 characters, alphanumeric, often starting with 701
    """
    # Pattern for Salesforce campaign ID (usually starts with 701)
    patterns = [
        r'\b(701[a-zA-Z0-9]{12,15})\b',  # Starts with 701
        r'\b([a-zA-Z0-9]{15})\b',         # Any 15-char alphanumeric
        r'\b([a-zA-Z0-9]{18})\b'          # Any 18-char alphanumeric
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            campaign_id = match.group(1)
            # Validate it looks like a campaign ID
            if len(campaign_id) in [15, 18] and campaign_id.isalnum():
                return campaign_id
    return None


def is_help_request(text):
    """Check if the user is asking for help"""
    help_keywords = ['help', 'how to use', 'how do i', 'commands', 'what can you do']
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in help_keywords)


def format_agent_response_for_chat(agent_response):
    """
    Format the agent's response for RingCentral chat.
    Add formatting, emojis, and structure for better readability.
    """
    # The agent already formats nicely, just ensure it's clean
    response = agent_response.get('response', '')
    
    # Add a header if the response is successful
    if agent_response.get('success'):
        return f"🎯 **Campaign Analysis Complete!**\n\n{response}"
    else:
        return f"⚠️ **Analysis Issue**\n\n{response}"


def botGotPostAddAction(
    bot,
    groupId,
    creatorId,
    user,
    text,
    dbAction,
    handledByExtension,
    event
):
    """
    This is invoked when the user sends a message to the bot.
    
    Handles:
    - Campaign analysis requests
    - Help requests
    - General conversation
    """
    if handledByExtension:
        return

    # Only respond if bot is mentioned
    if f'![:Person]({bot.id})' not in text:
        return
    
    # Remove bot mention to get clean text
    clean_text = text.replace(f'![:Person]({bot.id})', '').strip()
    
    # Handle help requests
    if is_help_request(clean_text):
        help_text = """📚 **MFChat - Campaign Clarity Help**

**I can analyze Salesforce campaigns!** Just give me a campaign ID and I'll provide:
✅ Campaign metadata and context
✅ AI-generated sales description
✅ Buyer intent analysis
✅ Recommended follow-up approach

**How to use:**
1. **Direct ID**: `701Hr000001L82yIAC`
2. **With command**: `analyze 701Hr000001L82yIAC`
3. **Ask naturally**: `what's campaign 701Hr000001L82yIAC?`

**Example campaign IDs:**
• `701Hr000001L82yIAC` - SMB RingEX Nurture
• `701Hr000001L8QHIA0` - Healthcare Nurture
• `701Hr000001L9q4IAC` - Partner Referral

Just mention me with ![:Person]({bot.id}) and send your request!"""
        
        bot.sendMessage(groupId, {'text': help_text})
        return
    
    # Try to extract campaign ID
    campaign_id = extract_campaign_id(clean_text)
    
    if campaign_id:
        # Send "thinking" message
        bot.sendMessage(
            groupId,
            {
                'text': f'🔍 Analyzing campaign `{campaign_id}`...\n\nThis may take a few seconds while I:\n1️⃣ Fetch data from Salesforce\n2️⃣ Enrich the context\n3️⃣ Generate AI description'
            }
        )
        
        try:
            # Call the agent
            result = campaign_agent.run(f"Analyze campaign {campaign_id}")
            
            # Format and send response
            formatted_response = format_agent_response_for_chat(result)
            bot.sendMessage(
                groupId,
                {
                    'text': formatted_response
                }
            )
            
        except Exception as e:
            error_message = f"❌ **Error analyzing campaign**\n\nSomething went wrong: {str(e)}\n\nPlease check the campaign ID and try again, or contact support if the issue persists."
            bot.sendMessage(groupId, {'text': error_message})
    
    else:
        # No campaign ID found - provide guidance
        bot.sendMessage(
            groupId,
            {
                'text': f"👋 Hi ![:Person]({creatorId})! I'm MFChat, your Campaign Clarity assistant.\n\nI didn't find a campaign ID in your message. Please provide a Salesforce campaign ID (15-18 characters, usually starts with 701).\n\n**Examples:**\n• `analyze 701Hr000001L82yIAC`\n• `701Hr000001L8QHIA0`\n\nOr say **help** for more information!"
            }
        )
