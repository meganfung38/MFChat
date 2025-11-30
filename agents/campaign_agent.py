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
        
        # System instructions
        self.system_instructions = """You are an expert SFDC Campaign Clarity assistant for RingCentral sales teams.

Your expertise includes:
- Analyzing Salesforce campaign data to understand prospect behavior
- Translating technical marketing metadata into actionable sales insights
- Generating channel-specific campaign descriptions tailored for sales reps
- Understanding 8 different prompt strategies based on campaign channels
- Providing context about buyer intent, engagement stage, and recommended follow-up approaches

CRITICAL WORKFLOW:
When a user provides a campaign ID, follow these steps EXACTLY:

Step 1: Call get_campaign_data(campaign_id="{the_campaign_id}")
   - This returns: {"success": True, "data": {campaign_fields...}, "campaign_name": "..."}
   - Extract the "data" object from this result

Step 2: Call enrich_campaign_context(campaign_data={the_data_object_from_step1})
   - Pass ONLY the "data" object, NOT the entire result from step 1
   - This returns: {"success": True, "enriched_context": "...", ...}
   - Extract the "enriched_context" string from this result

Step 3: Call generate_campaign_description(campaign_data={the_data_from_step1}, enriched_context={the_string_from_step2})
   - Pass the "data" object from step 1 AND the "enriched_context" string from step 2
   - This returns: {"success": True, "ai_description": "...", ...}

Step 4: Present the results in a friendly, formatted response that includes:
   - Campaign name and ID
   - Channel and type
   - The enriched context (formatted nicely)
   - The AI-generated sales description
   - Any alerts or special handling instructions

IMPORTANT: Each tool returns a JSON object with "success" and other fields. You MUST extract the relevant data from each result before passing to the next tool.

Your responses should be:
- Sales-focused and actionable
- Clear and concise
- Friendly and conversational
- Formatted for easy readability in chat

Always be helpful and explain what you're doing. If something fails, explain the error clearly and suggest next steps."""
    
    def run(self, user_message: str) -> Dict[str, Any]:
        """
        Run the agent with a user message
        
        Args:
            user_message: The user's input message
            
        Returns:
            Dictionary containing the agent's response and metadata
        """
        try:
            messages = [
                {"role": "system", "content": self.system_instructions},
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

