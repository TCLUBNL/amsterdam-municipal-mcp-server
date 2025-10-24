import requests
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

def get_gebieden(gebied_type: str = "buurt", naam: Optional[str] = None) -> Dict[str, Any]:
    """
    Get Amsterdam district/neighborhood boundaries and information.
    
    Args:
        gebied_type: Type of area ('stadsdeel', 'wijk', 'buurt', 'bouwblok')
        naam: Optional name filter
    
    Returns:
        Dictionary containing area boundaries and metadata
    """
    api_key = os.getenv("AMSTERDAM_API_KEY")
    
    type_mapping = {
        "stadsdeel": "stadsdelen",
        "wijk": "wijken",
        "buurt": "buurten",
        "bouwblok": "bouwblokken"
    }
    
    endpoint = type_mapping.get(gebied_type, "buurten")
    base_url = f"https://api.data.amsterdam.nl/v1/gebieden/{endpoint}/"
    
    headers = {}
    if api_key:
        headers["X-Api-Key"] = api_key
    
    params = {"_pageSize": 100}
    if naam:
        params["naam"] = naam
    
    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        results = []
        items = data.get("_embedded", {}).get(endpoint, [])
        
        for item in items:
            results.append({
                "id": item.get("identificatie"),
                "code": item.get("code"),
                "naam": item.get("naam"),
                "vollcode": item.get("vollcode"),
                "begin_geldigheid": item.get("beginGeldigheid"),
                "einde_geldigheid": item.get("eindeGeldigheid"),
                "geometry": item.get("geometrie"),
                "type": gebied_type
            })
        
        return {
            "gebied_type": gebied_type,
            "naam_filter": naam,
            "results": results,
            "count": len(results),
            "source": "Amsterdam Gebieden API v1 (Authenticated)"
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to fetch gebieden data: {str(e)}",
            "gebied_type": gebied_type,
            "note": "Ensure AMSTERDAM_API_KEY is set in .env file"
        }
