import requests
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

def get_infrastructure(
    object_type: str = "verhardingen",
    stadsdeel: Optional[str] = None,
    limit: int = 20
) -> Dict[str, Any]:
    """
    Get public space infrastructure objects (pavements, green objects, terrain parts).
    
    Args:
        object_type: Type of infrastructure object:
            - "verhardingen" (pavements/road surfaces)
            - "groenobjecten" (green objects/vegetation)
            - "terreindeel" (terrain parts/land parcels)
        stadsdeel: District filter (e.g., "Centrum", "West")
        limit: Maximum number of results (default 20)
    
    Returns:
        Dictionary containing public infrastructure object data
    """
    api_key = os.getenv("AMSTERDAM_API_KEY")
    
    endpoint_map = {
        "verhardingen": "verhardingen",
        "groenobjecten": "groenobjecten",
        "terreindeel": "terreindelen"
    }
    
    endpoint = endpoint_map.get(object_type, "verhardingen")
    base_url = f"https://api.data.amsterdam.nl/v1/objectenopenbareruimte/{endpoint}/"
    
    headers = {}
    if api_key:
        headers["X-Api-Key"] = api_key
    
    params = {
        "_pageSize": limit
    }
    
    if stadsdeel:
        params["ligtInStadsdeel"] = stadsdeel
    
    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        results = []
        items = data.get("_embedded", {}).get(endpoint, [])
        
        for item in items:
            result = {
                "id": item.get("identificatie"),
                "object_type": object_type,
                "stadsdeel": item.get("ligtInStadsdeel"),
                "buurt": item.get("ligtInBuurt"),
                "geometry": item.get("geometrie")
            }
            
            if object_type == "verhardingen":
                result.update({
                    "verhardingstype": item.get("verhardingstype"),
                    "oppervlakte": item.get("oppervlakte"),
                    "wegdeel": item.get("plusTypeVerharding")
                })
            elif object_type == "groenobjecten":
                result.update({
                    "groentype": item.get("plusType"),
                    "oppervlakte": item.get("oppervlakte")
                })
            elif object_type == "terreindeel":
                result.update({
                    "terreintype": item.get("plusType"),
                    "oppervlakte": item.get("oppervlakte")
                })
            
            results.append(result)
        
        return {
            "object_type": object_type,
            "total_results": len(results),
            "results": results[:limit],
            "source": "Amsterdam Public Infrastructure API"
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to fetch infrastructure objects: {str(e)}",
            "note": "Ensure AMSTERDAM_API_KEY is set in .env file"
        }
