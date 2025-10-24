"""Get Amsterdam waste container locations"""
import os
import requests
from typing import Optional, Dict, Any

try:
    from pyproj import Transformer
    # Create transformer from WGS84 to RD New (EPSG:28992)
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:28992", always_xy=True)
    HAS_PYPROJ = True
except ImportError:
    HAS_PYPROJ = False

def wgs84_to_rd(lat: float, lon: float) -> tuple:
    """Convert WGS84 (GPS) to RD New (Dutch grid) coordinates"""
    if HAS_PYPROJ:
        x, y = transformer.transform(lon, lat)
        return (x, y)
    else:
        # Fallback approximation for Amsterdam
        x = (lon - 3.31) * 190000
        y = (lat - 50.46) * 111000
        return (x, y)

def get_waste_containers(
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    radius: int = 500,
    container_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Amsterdam waste container locations
    
    Args:
        lat: Latitude (WGS84) - converted to RD automatically
        lon: Longitude (WGS84) - converted to RD automatically
        radius: Search radius in meters (default: 500)
        container_type: Filter by type (Rest, Glas, Papier, Textiel, Plastic)
    
    Returns:
        Dictionary with container data
    """
    api_key = os.getenv('AMSTERDAM_API_KEY')
    if not api_key:
        return {"error": "AMSTERDAM_API_KEY not found in environment"}
    
    base_url = "https://api.data.amsterdam.nl/v1/huishoudelijkafval/container/"
    headers = {'X-Api-Key': api_key}
    params = {'_pageSize': 100}
    
    rd_x, rd_y = None, None
    
    # Convert WGS84 to RD if coordinates provided
    if lat and lon:
        rd_x, rd_y = wgs84_to_rd(lat, lon)
        params['location'] = f'{rd_x},{rd_y}'
        params['radius'] = radius
    
    if container_type:
        params['fractie'] = container_type
    
    try:
        response = requests.get(base_url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        containers = data.get('_embedded', {}).get('container', [])
        
        return {
            "location": {
                "lat": lat, 
                "lon": lon, 
                "rd_x": round(rd_x, 2) if rd_x else None, 
                "rd_y": round(rd_y, 2) if rd_y else None
            } if lat and lon else None,
            "radius_m": radius if lat and lon else None,
            "container_type": container_type,
            "containers_found": len(containers),
            "results": [
                {
                    "id": c.get('id'),
                    "serienummer": c.get('serienummer'),
                    "fractie": c.get('fractieOmschrijving'),
                    "eigenaar": c.get('eigenaarNaam'),
                    "status": c.get('status'),
                    "datum_creatie": c.get('datumCreatie'),
                    "geometry": c.get('geometry')
                }
                for c in containers
            ],
            "source": "Amsterdam Waste Container API v1 (Authenticated)",
            "coordinate_system": "RD New (EPSG:28992)" if rd_x else "None"
        }
    
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to fetch waste container data: {e}",
            "location": {"lat": lat, "lon": lon, "rd_x": rd_x, "rd_y": rd_y} if lat and lon else None
        }
