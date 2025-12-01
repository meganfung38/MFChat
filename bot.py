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

# Store last campaign ID per group for context
last_campaign_by_group = {}

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


def is_bot_identity_question(text):
    """Check if the user is asking what the bot is"""
    identity_patterns = [
        'what are you', 'who are you', 'what do you do', 
        'what is this bot', 'what is mfchat', 'tell me about yourself',
        'what can you help with', 'what are your capabilities'
    ]
    text_lower = text.lower()
    return any(pattern in text_lower for pattern in identity_patterns)


def is_follow_up_question(text):
    """Check if the message is a follow-up question about a previous campaign"""
    follow_up_patterns = [
        'that campaign', 'this campaign', 'the campaign', 'same campaign',
        'it', 'that one', 'this one', 'the same one', 'that', 'this'
    ]
    text_lower = text.lower()
    return any(pattern in text_lower for pattern in follow_up_patterns)


def classify_user_intent(text, campaign_id):
    """
    Classify what the user wants to know about the campaign.
    
    Returns:
        - 'basic_info': User wants basic Salesforce information (channel, type, context)
        - 'ai_description': User wants AI-generated sales description
        - 'full_analysis': User wants complete analysis
    """
    text_lower = text.lower()
    
    # Full analysis keywords
    full_analysis_keywords = [
        'full analysis', 'complete analysis', 'full contextual', 
        'everything', 'all information', 'full details',
        'comprehensive', 'detailed analysis'
    ]
    
    # Basic info keywords
    basic_info_keywords = [
        'salesforce information', 'salesforce data', 'sfdc info', 'sfdc metadata', 
        'sfdc data', 'campaign type', 'channel', 'enriched context', 'basic info',
        'metadata', 'campaign details', 'raw data', 'campaign data'
    ]
    
    # AI description keywords
    ai_description_keywords = [
        'what can you tell me', 'describe', 'description',
        'summary', 'quick summary', 'enhance', 'what is',
        'tell me about', 'explain'
    ]
    
    # Check for full analysis
    if any(keyword in text_lower for keyword in full_analysis_keywords):
        return 'full_analysis'
    
    # Check for basic info
    if any(keyword in text_lower for keyword in basic_info_keywords):
        return 'basic_info'
    
    # Check for AI description - this is the most common, so it's the default
    if any(keyword in text_lower for keyword in ai_description_keywords):
        return 'ai_description'
    
    # Default: if just campaign ID or unclear, give AI description (most useful)
    return 'ai_description'


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
    
    # Handle "what are you" / bot identity questions
    if is_bot_identity_question(clean_text):
        identity_text = """👋 **Hi! I'm MFChat - Your Campaign Clarity Assistant**

**Purpose:** I help sales teams understand Salesforce campaigns by translating technical marketing data into actionable sales insights.

**What I Can Do:**

🔍 **Basic Campaign Info** - Get Salesforce metadata (channel, type, enriched context)
  • _Example:_ "Give me the Salesforce information about campaign 701Hr000001L82yIAC"

💡 **AI Sales Description** - Get AI-generated sales guidance (buyer intent, next steps, outreach)
  • _Example:_ "What can you tell me about 701Hr000001L82yIAC?"
  • _Example:_ "Give me a summary of campaign 701Hr000001L9q4IAC"
  • _Example:_ "Describe this campaign: 701TU00000ad4whYAA"

📊 **Full Campaign Analysis** - Get everything (metadata + AI description + context)
  • _Example:_ "Give me a full analysis of 701Hr000001L82yIAC"
  • _Example:_ "I need complete information on 701TU00000ayWTJYA2"

**Requirements:**
✅ Must provide a Salesforce Campaign ID (15-18 characters, usually starts with '701')
❌ Cannot search by campaign name (ID required)

**Need more help?** Just say "help" for more examples!"""
        
        bot.sendMessage(groupId, {'text': identity_text})
        return
    
    # Handle help requests
    if is_help_request(clean_text):
        help_text = """📚 **MFChat - Campaign Clarity Help**

**I can analyze Salesforce campaigns!** Just give me a campaign ID and I'll provide the information you need.

**Three Ways to Use Me:**

1️⃣ **Basic Info** - Salesforce metadata only
   • `Give me the Salesforce information about 701Hr000001L82yIAC`

2️⃣ **AI Description** - Sales guidance only (default)
   • `What is 701Hr000001L82yIAC?`
   • `Describe campaign 701Hr000001L9q4IAC`
   • `Give me a summary of 701TU00000ad4whYAA`

3️⃣ **Full Analysis** - Everything combined
   • `Full analysis of 701Hr000001L82yIAC`
   • `Give me complete information on 701Hr000001L8QHIA0`

**Sample Campaign IDs:**
• `701Hr000001L82yIAC` - SMB RingEX Nurture
• `701Hr000001L8QHIA0` - Healthcare Nurture
• `701Hr000001L9q4IAC` - Partner Referral
• `701TU00000ad4whYAA` - Content Syndication

Just mention me with ![:Person]({bot.id}) and your request!"""
        
        bot.sendMessage(groupId, {'text': help_text})
        return
    
    # Try to extract campaign ID from current message
    campaign_id = extract_campaign_id(clean_text)
    is_follow_up = False
    
    # If no campaign ID found, check if this is a follow-up question
    if not campaign_id and is_follow_up_question(clean_text):
        # Try to use the last campaign ID from this group
        campaign_id = last_campaign_by_group.get(groupId)
        if campaign_id:
            print(f"  💬 Using previous campaign ID from context: {campaign_id}")
            is_follow_up = True
    
    if campaign_id:
        # Store this campaign ID for future follow-up questions
        last_campaign_by_group[groupId] = campaign_id
        # Classify user intent
        intent = classify_user_intent(clean_text, campaign_id)
        
        # Send appropriate "thinking" message based on intent
        thinking_messages = {
            'basic_info': f'🔍 Fetching Salesforce information for campaign `{campaign_id}`...',
            'ai_description': f'🤖 Generating sales description for campaign `{campaign_id}`...',
            'full_analysis': f'📊 Performing full analysis of campaign `{campaign_id}`...\n\nThis may take a few seconds.'
        }
        
        bot.sendMessage(
            groupId,
            {
                'text': thinking_messages.get(intent, f'🔍 Analyzing campaign `{campaign_id}`...')
            }
        )
        
        try:
            # If this is a follow-up, inject the campaign ID into the message for the agent
            agent_message = clean_text
            if is_follow_up:
                # Replace references like "that", "it", etc. with the actual campaign ID
                agent_message = clean_text.replace('that campaign', f'campaign {campaign_id}')
                agent_message = agent_message.replace('this campaign', f'campaign {campaign_id}')
                agent_message = agent_message.replace('the campaign', f'campaign {campaign_id}')
                agent_message = agent_message.replace('same campaign', f'campaign {campaign_id}')
                agent_message = agent_message.replace('that one', f'campaign {campaign_id}')
                agent_message = agent_message.replace('this one', f'campaign {campaign_id}')
                agent_message = agent_message.replace(' it', f' campaign {campaign_id}')
                agent_message = agent_message.replace(' that', f' {campaign_id}')
                agent_message = agent_message.replace(' this', f' {campaign_id}')
                
                print(f"  💬 Transformed message: '{clean_text}' → '{agent_message}'")
            
            # Call the agent with intent
            result = campaign_agent.run(agent_message, intent=intent)
            
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
                'text': f"""👋 Hi ![:Person]({creatorId})! I'm **MFChat**, your Campaign Clarity assistant.

I help sales teams understand Salesforce campaigns by providing:
• **Basic campaign info** (channel, type, context)
• **AI-generated sales descriptions** (buyer intent, next steps)
• **Full campaign analysis** (everything combined)

**I need a campaign ID to help you!** 
Please provide a Salesforce campaign ID (15-18 characters, usually starts with 701).

**Examples:**
• `What is 701Hr000001L82yIAC?` - Get AI description
• `Full analysis of 701Hr000001L8QHIA0` - Get everything
• `Salesforce info for 701Hr000001L9q4IAC` - Get basic info

Say **help** for more details or **what are you** to learn about my capabilities!"""
            }
        )
