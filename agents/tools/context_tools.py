"""
Context enrichment tools for campaign data
"""
import os
import sys
import json
from pathlib import Path
from typing import Dict, Any
import pandas as pd

# Add SFDC_Campaign_Clarity src to path
project_root = Path(__file__).parent.parent.parent
sfdc_src = project_root / "SFDC_Campaign_Clarity" / "src"
sys.path.insert(0, str(sfdc_src))

from context_manager import ContextManager


def enrich_campaign_context(campaign_data: Dict[str, Any] = None, **kwargs) -> Dict[str, Any]:
    """
    Enrich campaign data with human-readable context using field mappings.
    
    This tool transforms raw Salesforce field values into clear, sales-friendly
    explanations using the field_mappings.json file. It decodes technical values
    into actionable insights.
    
    Args:
        campaign_data: Dictionary containing raw campaign data from Salesforce
        **kwargs: Additional arguments (for flexibility)
    
    Returns:
        Dictionary containing enriched context string and metadata
        
    Raises:
        Exception: If context enrichment fails
    """
    try:
        # Handle None campaign_data
        if campaign_data is None:
            return {
                "success": False,
                "error": "No campaign data provided",
                "enriched_context": ""
            }
        
        # If campaign_data has a 'data' field (from get_campaign_data result), extract it
        if isinstance(campaign_data, dict) and 'data' in campaign_data:
            campaign_data = campaign_data['data']
        
        # Initialize context manager
        context_mgr = ContextManager()
        
        # Convert dict to pandas Series if needed
        if isinstance(campaign_data, dict):
            campaign_series = pd.Series(campaign_data)
        else:
            campaign_series = campaign_data
        
        # Generate enriched context
        enriched_context = context_mgr.enrich_campaign_context(campaign_series)
        
        return {
            "success": True,
            "enriched_context": enriched_context,
            "context_length": len(enriched_context),
            "campaign_name": campaign_data.get('Name', 'Unknown') if isinstance(campaign_data, dict) else 'Unknown'
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Context enrichment failed: {str(e)}",
            "enriched_context": ""
        }


# Tool definition for OpenAI function calling
enrich_campaign_context_tool = {
    "type": "function",
    "function": {
        "name": "enrich_campaign_context",
        "description": "Transform raw Salesforce campaign data into human-readable, sales-friendly context. This decodes technical field values (like Channel, Type, BMID) into clear explanations that help sales reps understand prospect behavior and campaign intent.",
        "parameters": {
            "type": "object",
            "properties": {
                "campaign_data": {
                    "type": "object",
                    "description": "The raw campaign data dictionary from Salesforce containing fields like Name, Channel__c, Type, BMID__c, etc.",
                    "additionalProperties": True
                }
            },
            "required": ["campaign_data"],
            "additionalProperties": False
        }
    }
}

