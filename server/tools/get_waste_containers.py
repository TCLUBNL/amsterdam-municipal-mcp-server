"""Get Amsterdam waste container locations with client-side distance filtering"""
import os
import requests
import math
from typing import Optional, Dict, Any, List

try:
    from pyproj import Transformer
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:28992", always_xy=True)
    HAS_PYPROJ = True
except ImportError:
    HAS_PYPROJ = False

def wgs84_to_rd(lat: float, lon: float) -> tuple:
    """Convert WGS84 to RD New coordinates"""
    if HAS_PYPROJ:
        x, y = transformer.transform(lon, lat)
        return (x, y)
    else:
        x = (lon - 3.31) * 190000
        y = (lat - 50.46) * 111000
        return (x, y)

def calculate_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """Calculate Euclidean distance between two RD points (in meters)"""
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def get_waste_containers(
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    radius: int = 500,
    container_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Amsterdam waste container locations
    
    Note: API doesn't support spatial queries, so we fetch all containers
    and filter by distance in Python (limited to first 500 results).
    
    Args:
        lat: Latitude (WGS84)
        lon: Longitude (WGS84)
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
    params = {'_pageSize': 500}  # Fetch more containers for filtering
    
    # Filter by container type if specified
    if container_type:
        params['fractieOmschrijving'] = container_type
    
    rd_x, rd_y = None, None
    if lat and lon:
        rd_x, rd_y = wgs84_to_rd(lat, lon)
    
    try:
        response = requests.get(base_url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        containers = data.get('_embedded', {}).get('container', [])
        
        # Filter by distance if coordinates provided
        filtered_containers = []
        if lat and lon and rd_x and rd_y:
            for c in containers:
                geom = c.get('geometry')
                if geom and geom.get('coordinates'):
                    cx, cy = geom['coordinates']
                    distance = calculate_distance(rd_x, rd_y, cx, cy)
                    if distance <= radius:
                        filtered_containers.append({
                            "id": c.get('id'),
                            "serienummer": c.get('serienummer'),
                            "fractie": c.get('fractieOmschrijving'),
                            "eigenaar": c.get('eigenaarNaam'),
                            "status": c.get('status'),
                            "datum_creatie": c.get('datumCreatie'),
                            "geometry": geom,
                            "distance_m": round(distance, 1)
                        })
            # Sort by distance
            filtered_containers.sort(key=lambda x: x['distance_m'])
        else:
            # No location filter, return all
            filtered_containers = [
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
            ]
        
        return {
            "location": {
                "lat": lat, 
                "lon": lon, 
                "rd_x": round(rd_x, 2) if rd_x else None, 
                "rd_y": round(rd_y, 2) if rd_y else None
            } if lat and lon else None,
            "radius_m": radius if lat and lon else None,
            "container_type": container_type,
            "containers_found": len(filtered_containers),
            "total_fetched": len(containers),
            "results": filtered_containers,
            "source": "Amsterdam Waste Container API v1 (client-side distance filter)",
            "note": "API fetches max 500 containers, then filters by distance in Python"
        }
    
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to fetch waste container data: {e}",
            "location": {"lat": lat, "lon": lon} if lat and lon else None
        }
