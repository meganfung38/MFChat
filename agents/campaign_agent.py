"""
Campaign Clarity OpenAI Agent

This agent orchestrates the campaign analysis workflow:
1. Fetches campaign data from Salesforce
2. Enriches context using field mappings
3. Generates AI-powered sales descriptions
"""
import json
import os
from typing import Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv

from .tools.salesforce_tools import get_campaign_data, get_campaign_data_tool
from .tools.context_tools import enrich_campaign_context, enrich_campaign_context_tool
from .tools.description_tools import generate_campaign_description, generate_campaign_description_tool

load_dotenv()


class CampaignAgent:
    """
    OpenAI Agent for SFDC Campaign Clarity
    
    This agent is an expert at analyzing Salesforce campaigns and generating
    enhanced sales-friendly descriptions. It understands campaign metadata,
    prospect behavior, and sales enablement best practices.
    """
    
    def __init__(self):
        """Initialize the Campaign Clarity Agent"""
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = "gpt-4o"
        
        # Define available tools
        self.tools = [
            get_campaign_data_tool,
            enrich_campaign_context_tool,
            generate_campaign_description_tool
        ]
        
        # Map tool names to functions
        self.tool_functions = {
            "get_campaign_data": get_campaign_data,
            "enrich_campaign_context": enrich_campaign_context,
            "generate_campaign_description": generate_campaign_description
        }
        
        # Base system instructions (will be customized based on intent)
        self.base_system_instructions = """You are an expert SFDC Campaign Clarity assistant for RingCentral sales teams.

Your expertise includes:
- Analyzing Salesforce campaign data to understand prospect behavior
- Translating technical marketing metadata into actionable sales insights
- Generating channel-specific campaign descriptions tailored for sales reps
- Understanding 8 different prompt strategies based on campaign channels
- Providing context about buyer intent, engagement stage, and recommended follow-up approaches

IMPORTANT: Each tool returns a JSON object with "success" and other fields. You MUST extract the relevant data from each result before passing to the next tool.

ERROR HANDLING:
- If a tool returns "success": false, check the "error" field for details
- If the AI description generation fails, you can still provide useful information from the campaign data and enriched context
- Always inform the user clearly if something went wrong and what information you were able to retrieve
- If only one tool fails, provide the information from the successful tools

FORMATTING RULES FOR RINGCENTRAL CHAT:
- Use **bold** for section headers (NOT ### markdown headers)
- Use bullet points with • or -
- Use **bold** for emphasis
- Keep formatting simple and chat-friendly
- DO NOT use ### or #### markdown headers - RingCentral doesn't render them
- Example: "**Campaign Name:** SMB_RingEX_Nurture" instead of "### Campaign Name"

Your responses should be:
- Sales-focused and actionable
- Clear and concise
- Friendly and conversational
- Formatted for RingCentral chat (use **bold**, not ### headers)
- Transparent about any errors or limitations

Always be helpful and explain what you're doing. If something fails, explain the error clearly and provide what information you can."""
    
    def _get_intent_instructions(self, intent: str) -> str:
        """
        Get workflow instructions based on user intent
        
        Args:
            intent: One of 'basic_info', 'ai_description', 'full_analysis'
            
        Returns:
            Intent-specific instructions
        """
        if intent == 'basic_info':
            return """
WORKFLOW FOR BASIC INFO REQUEST:
The user wants raw Salesforce field data and enriched context - NO AI-generated sales description.

Step 1: Call get_campaign_data(campaign_id="{the_campaign_id}")
   - Extract the "data" object from the result
   - This contains all the raw Salesforce fields

Step 2: Call enrich_campaign_context(campaign_data={the_data_from_step1})
   - Extract the "enriched_context" string

Step 3: Present a response with BOTH sections:

SECTION 1 - RAW SALESFORCE DATA:
Display the actual raw field values from the campaign data object. Include fields like:
   - Campaign Name
   - Campaign ID
   - Channel (e.g., "Email", "EMSF", etc.)
   - Description
   - Sub Channel (e.g., "Nurture", "NURT", etc.)
   - Intended Country
   - Intended Product
   - TCP Program
   - TCP Theme
   - Vendor
   - Type
   - Status
   - Any other relevant fields from the data object

SECTION 2 - ENRICHED CONTEXT:
Display the full enriched_context string which translates technical fields into human-readable insights.

FORMAT EXAMPLE:
**Campaign:** [Name] ([ID])

**Raw Salesforce Fields:**
• Channel: [actual field value from data]
• Description: [actual field value from data]
• Intended Country: [actual field value from data]
• Intended Product: [actual field value from data]
• Sub Channel: [actual field value from data]
• TCP Program: [actual field value from data]
• TCP Theme: [actual field value from data]
• Vendor: [actual field value from data]

**Enriched Context:**
[Full enriched_context string goes here]

IMPORTANT: 
- Show the ACTUAL raw field values from the Salesforce data object
- Then show the enriched context which provides human-readable explanations
- Use **bold** for section headers, NOT ### markdown
- DO NOT call generate_campaign_description
- DO NOT provide AI-generated sales guidance"""

        elif intent == 'ai_description':
            return """
WORKFLOW FOR AI DESCRIPTION REQUEST:
The user wants AI-generated sales guidance - keep it focused and concise.

Step 1: Call get_campaign_data(campaign_id="{the_campaign_id}")
   - Extract the "data" object

Step 2: Call enrich_campaign_context(campaign_data={the_data_from_step1})
   - Extract the "enriched_context" string

Step 3: Call generate_campaign_description(campaign_data={the_data_from_step1}, enriched_context={the_string_from_step2})
   - Extract the "ai_description"

Step 4: Present a FOCUSED response emphasizing the AI sales description:
   - Brief campaign context (name, ID, channel)
   - **HIGHLIGHT the AI-generated sales description** (engagement, intent, next steps)
   - Keep it concise - user wants actionable sales guidance, not full details
   
FORMAT: Use **bold** for section headers, NOT ### markdown. Example:
**Campaign:** SMB_RingEX_Nurture (701Hr000001L82yIAC)
**Channel:** Email

**Sales Description:**
• **Engagement:** Prospects engaged via email...
• **Intent:** Interested in RingEX for SMB...
• **Next Steps:** Follow up with tailored messaging..."""

        else:  # full_analysis
            return """
WORKFLOW FOR FULL ANALYSIS REQUEST:
The user wants comprehensive information - provide everything.

Step 1: Call get_campaign_data(campaign_id="{the_campaign_id}")
   - Extract the "data" object

Step 2: Call enrich_campaign_context(campaign_data={the_data_from_step1})
   - Extract the "enriched_context" string

Step 3: Call generate_campaign_description(campaign_data={the_data_from_step1}, enriched_context={the_string_from_step2})
   - Extract the "ai_description"

Step 4: Present a COMPREHENSIVE response including:
   - Campaign name and ID
   - Channel and type details
   - Complete enriched context
   - Full AI-generated sales description
   - Any alerts or special handling instructions
   
FORMAT: Use **bold** for section headers, NOT ### markdown. Example:
**Campaign Overview**
• Campaign Name: SMB_RingEX_Nurture
• Campaign ID: 701Hr000001L82yIAC
• Channel: Email

**Enriched Context**
• Target Market: SMB (1-499 employees)
• Engagement Method: Email outreach

**AI Sales Description**
• **Engagement:** Prospects engaged via...
• **Intent:** Interested in...
   
Provide all available information in a well-organized, RingCentral-chat-friendly format."""

    def run(self, user_message: str, intent: str = 'full_analysis') -> Dict[str, Any]:
        """
        Run the agent with a user message
        
        Args:
            user_message: The user's input message
            intent: User intent - 'basic_info', 'ai_description', or 'full_analysis'
            
        Returns:
            Dictionary containing the agent's response and metadata
        """
        try:
            # Build system instructions based on intent
            intent_instructions = self._get_intent_instructions(intent)
            full_instructions = self.base_system_instructions + "\n\n" + intent_instructions
            
            messages = [
                {"role": "system", "content": full_instructions},
                {"role": "user", "content": user_message}
            ]
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )
            
            # Process the response
            return self._process_response(response, messages)
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Agent execution failed: {str(e)}",
                "response": f"I encountered an error: {str(e)}"
            }
    
    def _process_response(self, response, messages: list) -> Dict[str, Any]:
        """
        Process the agent response and handle tool calls
        
        Args:
            response: OpenAI chat completion response
            messages: Conversation messages
            
        Returns:
            Dictionary containing processed response
        """
        max_iterations = 10
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            message = response.choices[0].message
            
            # If no tool calls, we're done
            if not message.tool_calls:
                return {
                    "success": True,
                    "response": message.content,
                    "iterations": iteration
                }
            
            # Add assistant message to conversation
            messages.append(message)
            
            # Execute each tool call
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                
                print(f"  🔧 Calling tool: {tool_name}")
                
                # Execute the tool
                if tool_name in self.tool_functions:
                    tool_result = self.tool_functions[tool_name](**tool_args)
                else:
                    tool_result = {"error": f"Unknown tool: {tool_name}"}
                
                # Add tool result to messages
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(tool_result)
                })
            
            # Get next response from agent
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )
        
        return {
            "success": False,
            "error": "Maximum iterations reached",
            "response": "I've reached the maximum number of processing steps. Please try again."
        }
    
    def analyze_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """
        Analyze a campaign by ID (convenience method)
        
        Args:
            campaign_id: Salesforce campaign ID
            
        Returns:
            Dictionary containing analysis results
        """
        return self.run(f"Analyze campaign {campaign_id}")

