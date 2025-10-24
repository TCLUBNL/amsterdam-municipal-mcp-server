import requests
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

def get_public_reports(
    category: Optional[str] = None,
    status: Optional[str] = None,
    stadsdeel: Optional[str] = None,
    limit: int = 20
) -> Dict[str, Any]:
    """
    Get public space incident reports (SIA - Signalen Informatievoorziening Amsterdam).
    Citizens report issues like waste, road damage, nuisance, etc.
    
    Args:
        category: Category filter (e.g., "afval", "wegen", "overlast")
        status: Status filter (e.g., "open", "gesloten", "behandeling")
        stadsdeel: District filter (e.g., "Centrum", "West")
        limit: Maximum number of results (default 20)
    
    Returns:
        Dictionary containing public incident report data
    """
    api_key = os.getenv("AMSTERDAM_API_KEY")
    
    base_url = "https://api.data.amsterdam.nl/v1/meldingen/meldingen/"
    
    headers = {}
    if api_key:
        headers["X-Api-Key"] = api_key
    
    params = {
        "_pageSize": limit,
        "_sort": "-createdAt"
    }
    
    if category:
        params["hoofdcategorie"] = category
    if status:
        params["status"] = status
    if stadsdeel:
        params["stadsdeel"] = stadsdeel
    
    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        results = []
        items = data.get("_embedded", {}).get("meldingen", [])
        
        for item in items:
            results.append({
                "id": item.get("id"),
                "created_at": item.get("createdAt"),
                "updated_at": item.get("updatedAt"),
                "category": item.get("hoofdcategorie"),
                "subcategory": item.get("subcategorie"),
                "status": item.get("status", {}).get("state"),
                "priority": item.get("prioriteit", {}).get("priority"),
                "stadsdeel": item.get("locatie", {}).get("stadsdeel"),
                "buurt": item.get("locatie", {}).get("buurtCode"),
                "description": item.get("text"),
                "geometry": item.get("locatie", {}).get("geometrie")
            })
        
        return {
            "total_results": len(results),
            "results": results[:limit],
            "source": "Amsterdam Public Reports API (SIA)"
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to fetch public reports: {str(e)}",
            "note": "Ensure AMSTERDAM_API_KEY is set in .env file"
        }
