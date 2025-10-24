import requests
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def search_bag_address(query: str, limit: int = 20) -> Dict[str, Any]:
    """
    Search Amsterdam BAG (Basisregistratie Adressen en Gebouwen) for buildings and addresses.
    
    Args:
        query: Search query (address, postal code, or building name)
        limit: Maximum number of results (default 20)
    
    Returns:
        Dictionary containing BAG address/building data
    """
    api_key = os.getenv("AMSTERDAM_API_KEY")
    
    # Updated to plural endpoint
    base_url = "https://api.data.amsterdam.nl/v1/bag/nummeraanduidingen/"
    
    headers = {}
    if api_key:
        headers["X-Api-Key"] = api_key
    
    # Use _pageSize for pagination
    params = {
        "_pageSize": limit
    }
    
    # Try to parse query - if it contains numbers, might be postcode
    if any(char.isdigit() for char in query):
        # Might be postcode or house number
        parts = query.split()
        for part in parts:
            if part.replace('-', '').replace(' ', '').isalnum() and len(part) >= 4:
                params["postcode"] = part.upper().replace(' ', '')
                break
    
    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        results = []
        items = data.get("_embedded", {}).get("nummeraanduidingen", [])
        
        for item in items:
            # Extract openbare ruimte name if available
            openbare_ruimte = item.get("ligtAan", {})
            straat_naam = openbare_ruimte.get("naam") if isinstance(openbare_ruimte, dict) else None
            
            results.append({
                "id": item.get("identificatie"),
                "postcode": item.get("postcode"),
                "huisnummer": item.get("huisnummer"),
                "huisletter": item.get("huisletter"),
                "toevoeging": item.get("huisnummertoevoeging"),
                "straat": straat_naam,
                "status": item.get("status"),
                "type_adres": item.get("typeAdresseerbaarObject"),
                "geometry": item.get("geometrie")
            })
        
        return {
            "query": query,
            "total_results": len(results),
            "results": results[:limit],
            "source": "Amsterdam BAG API v1 (Authenticated)"
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to search BAG addresses: {str(e)}",
            "query": query,
            "note": "Ensure AMSTERDAM_API_KEY is set in .env file"
        }
