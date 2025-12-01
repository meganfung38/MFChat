"""
AI description generation tools for campaigns
"""
import os
import sys
import json
from pathlib import Path
from typing import Dict, Any, Optional
import pandas as pd

# Add SFDC_Campaign_Clarity src to path
project_root = Path(__file__).parent.parent.parent
sfdc_src = project_root / "SFDC_Campaign_Clarity" / "src"
sys.path.insert(0, str(sfdc_src))

from openai_client import OpenAIClient


def generate_campaign_description(
    campaign_data: Dict[str, Any] = None,
    enriched_context: str = "",
    **kwargs
) -> Dict[str, Any]:
    """
    Generate AI-powered sales-friendly campaign description.
    
    This tool uses OpenAI to create tailored campaign descriptions based on
    channel type, using 8 different prompt strategies to provide the most
    relevant guidance for sales reps.
    
    Args:
        campaign_data: Dictionary containing raw campaign data from Salesforce
        enriched_context: Human-readable context string from context enrichment
        **kwargs: Additional arguments (for flexibility)
    
    Returns:
        Dictionary containing AI-generated description and metadata
        
    Raises:
        Exception: If AI generation fails
    """
    try:
        # Handle None campaign_data
        if campaign_data is None:
            return {
                "success": False,
                "error": "No campaign data provided",
                "ai_description": ""
            }
        
        # If campaign_data has a 'data' field (from get_campaign_data result), extract it
        if isinstance(campaign_data, dict) and 'data' in campaign_data:
            campaign_data = campaign_data['data']
        
        # If enriched_context is a dict with 'enriched_context' field, extract it
        if isinstance(enriched_context, dict) and 'enriched_context' in enriched_context:
            enriched_context = enriched_context['enriched_context']
        
        # Initialize OpenAI client
        openai_client = OpenAIClient(use_openai=True)
        
        # Convert dict to pandas Series if needed
        if isinstance(campaign_data, dict):
            campaign_series = pd.Series(campaign_data)
        else:
            campaign_series = campaign_data
        
        # Generate AI description
        description, prompt_used = openai_client.generate_description(
            campaign_series,
            enriched_context
        )
        
        # Check if description generation failed
        if description.startswith("Error generating"):
            return {
                "success": False,
                "error": f"AI description generation failed: {description}",
                "ai_description": "",
                "campaign_name": campaign_data.get('Name', 'Unknown') if isinstance(campaign_data, dict) else 'Unknown',
                "channel": campaign_data.get('Channel__c', 'Unknown') if isinstance(campaign_data, dict) else 'Unknown'
            }
        
        # Determine prompt type
        prompt_type = openai_client._get_prompt_type(campaign_series)
        
        return {
            "success": True,
            "ai_description": description,
            "description_length": len(description),
            "prompt_type": prompt_type,
            "campaign_name": campaign_data.get('Name', 'Unknown') if isinstance(campaign_data, dict) else 'Unknown',
            "channel": campaign_data.get('Channel__c', 'Unknown') if isinstance(campaign_data, dict) else 'Unknown'
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"AI description generation failed: {str(e)}",
            "ai_description": ""
        }


# Tool definition for OpenAI function calling
generate_campaign_description_tool = {
    "type": "function",
    "function": {
        "name": "generate_campaign_description",
        "description": "Generate an AI-powered sales-friendly campaign description using OpenAI. The description is tailored based on campaign channel (Email, Events, Partner Referral, etc.) and provides actionable guidance for sales reps on how to approach prospects.",
        "parameters": {
            "type": "object",
            "properties": {
                "campaign_data": {
                    "type": "object",
                    "description": "The raw campaign data dictionary from Salesforce",
                    "additionalProperties": True
                },
                "enriched_context": {
                    "type": "string",
                    "description": "The human-readable enriched context string that was generated from the campaign data"
                }
            },
            "required": ["campaign_data", "enriched_context"],
            "additionalProperties": False
        }
    }
}

