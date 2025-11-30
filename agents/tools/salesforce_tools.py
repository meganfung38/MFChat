"""
Salesforce tools for fetching campaign data
"""
import os
import sys
import json
from pathlib import Path
from typing import Dict, Any

# Add SFDC_Campaign_Clarity src to path
project_root = Path(__file__).parent.parent.parent
sfdc_src = project_root / "SFDC_Campaign_Clarity" / "src"
sys.path.insert(0, str(sfdc_src))

from salesforce_client import SalesforceClient


def get_campaign_data(campaign_id: str) -> Dict[str, Any]:
    """
    Fetch campaign data from Salesforce for a given campaign ID.
    
    This tool connects to Salesforce and retrieves complete campaign metadata
    including all fields needed for analysis and description generation.
    
    Args:
        campaign_id: Salesforce campaign ID (15 or 18 characters)
    
    Returns:
        Dictionary containing campaign data with all relevant fields
        
    Raises:
        ValueError: If campaign ID is invalid or campaign not found
        Exception: If Salesforce connection fails
    """
    # Validate campaign ID
    campaign_id = campaign_id.strip()
    if len(campaign_id) not in [15, 18]:
        raise ValueError(f"Invalid campaign ID length: {len(campaign_id)}. Must be 15 or 18 characters.")
    
    if not campaign_id.isalnum():
        raise ValueError("Campaign ID must contain only alphanumeric characters")
    
    try:
        # Initialize Salesforce client
        sf_client = SalesforceClient()
        
        # Extract campaign data
        df = sf_client.extract_campaigns([campaign_id])
        
        if df.empty:
            raise ValueError(f"No campaign found with ID: {campaign_id}")
        
        # Convert to dictionary
        campaign_data = df.iloc[0].to_dict()
        
        # Convert NaN and None values to empty strings for better JSON serialization
        for key, value in campaign_data.items():
            if value is None or (isinstance(value, float) and str(value) == 'nan'):
                campaign_data[key] = ''
        
        return {
            "success": True,
            "campaign_id": campaign_id,
            "campaign_name": campaign_data.get('Name', 'Unknown'),
            "data": campaign_data
        }
        
    except ValueError as e:
        return {
            "success": False,
            "error": str(e),
            "campaign_id": campaign_id
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Salesforce query failed: {str(e)}",
            "campaign_id": campaign_id
        }


# Tool definition for OpenAI function calling
get_campaign_data_tool = {
    "type": "function",
    "function": {
        "name": "get_campaign_data",
        "description": "Fetch complete campaign data from Salesforce including all metadata fields needed for analysis. Use this when you need raw campaign information from Salesforce.",
        "parameters": {
            "type": "object",
            "properties": {
                "campaign_id": {
                    "type": "string",
                    "description": "The Salesforce campaign ID (15 or 18 character alphanumeric string)",
                }
            },
            "required": ["campaign_id"],
            "additionalProperties": False
        }
    }
}

