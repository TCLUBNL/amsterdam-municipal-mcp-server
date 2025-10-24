import requests
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

def get_waste_containers(lat: Optional[float] = None, 
                         lon: Optional[float] = None,
                         radius: int = 500,
                         container_type: Optional[str] = None) -> Dict[str, Any]:
    """
    Get waste container locations and weight data in Amsterdam.
    
    Args:
        lat: Latitude (WGS84)
        lon: Longitude (WGS84)
        radius: Search radius in meters (default 500)
        container_type: Type filter ('Rest', 'Glas', 'Papier', 'Textiel', 'Plastic')
    
    Returns:
        Dictionary containing waste container locations and data
    """
    api_key = os.getenv("AMSTERDAM_API_KEY")
    base_url = "https://api.data.amsterdam.nl/v1/huishoudelijkafval/container/"
    
    headers = {}
    if api_key:
        headers["X-Api-Key"] = api_key
    
    params = {"_pageSize": 100}
    
    if lat and lon:
        params["location"] = f"{lat},{lon}"
        params["radius"] = radius
    
    if container_type:
        params["fractieOmschrijving"] = container_type
    
    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get("_embedded", {}).get("container", []):
            results.append({
                "id": item.get("id"),
                "serienummer": item.get("serienummer"),
                "fractie": item.get("fractieOmschrijving"),
                "eigenaar": item.get("eigenaarNaam"),
                "status": item.get("status"),
                "datum_creatie": item.get("datumCreatie"),
                "geometry": item.get("geometrie")
            })
        
        return {
            "location": {"lat": lat, "lon": lon} if lat and lon else None,
            "radius_m": radius if lat and lon else None,
            "container_type": container_type,
            "containers_found": len(results),
            "results": results,
            "source": "Amsterdam Waste Container API v1 (Authenticated)"
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to fetch waste container data: {str(e)}",
            "location": {"lat": lat, "lon": lon}
        }
