import requests
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_gas_free_neighborhoods(
    buurt_code: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 20
) -> Dict[str, Any]:
    """
    Get gas-free neighborhood zones and initiatives in Amsterdam.
    Shows realized or planned gas-free areas for energy transition.
    
    Args:
        buurt_code: Neighborhood code to filter results
        status: Status filter (e.g., "gerealiseerd", "gepland")
        limit: Maximum number of results (default 20)
    
    Returns:
        Dictionary containing gas-free neighborhood data
    """
    api_key = os.getenv("AMSTERDAM_API_KEY")
    
    base_url = "https://api.data.amsterdam.nl/v1/aardgasvrijezones/buurt/"
    
    headers = {}
    if api_key:
        headers["X-Api-Key"] = api_key
    
    params = {
        "_pageSize": limit
    }
    
    if buurt_code:
        params["buurtCode"] = buurt_code
    if status:
        params["status"] = status
    
    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        results = []
        items = data.get("_embedded", {}).get("buurt", [])
        
        for item in items:
            results.append({
                "buurt_code": item.get("buurtCode"),
                "buurt_naam": item.get("buurtNaam"),
                "stadsdeel": item.get("stadsdeel"),
                "status": item.get("status"),
                "prioriteit": item.get("prioriteit"),
                "jaar_gasloos": item.get("jaarGasloos"),
                "aantal_woningen": item.get("aantalWoningen"),
                "type_bebouwing": item.get("typeBebouwing"),
                "geometry": item.get("geometrie")
            })
        
        return {
            "total_results": len(results),
            "results": results[:limit],
            "source": "Amsterdam Gas-Free Zones API"
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to fetch gas-free neighborhood data: {str(e)}",
            "note": "Ensure AMSTERDAM_API_KEY is set in .env file"
        }
