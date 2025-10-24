import requests
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_gas_consumption(
    postcode: Optional[str] = None,
    year: Optional[int] = None,
    limit: int = 20
) -> Dict[str, Any]:
    """
    Get gas consumption statistics per postal code range in Amsterdam Metropolitan Area.
    Data provided by Liander (energy network operator).
    
    Args:
        postcode: Postal code (4 digits) to filter results
        year: Year for consumption data (e.g., 2023)
        limit: Maximum number of results (default 20)
    
    Returns:
        Dictionary containing gas consumption data per postal code area
    """
    api_key = os.getenv("AMSTERDAM_API_KEY")
    
    base_url = "https://api.data.amsterdam.nl/v1/aardgasverbruik/mrastatistiekenpcranges/"
    
    headers = {}
    if api_key:
        headers["X-Api-Key"] = api_key
    
    params = {
        "_pageSize": limit
    }
    
    if postcode:
        # Extract numeric part of postcode (first 4 digits)
        postcode_clean = ''.join(filter(str.isdigit, postcode))[:4]
        params["postcodeVan"] = postcode_clean
    
    if year:
        params["jaar"] = year
    
    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        results = []
        items = data.get("_embedded", {}).get("mrastatistiekenpcranges", [])
        
        for item in items:
            results.append({
                "postcode_range": f"{item.get('postcodeVan')}-{item.get('postcodeTot')}",
                "year": item.get("jaar"),
                "connections_total": item.get("totaalAansluitingen"),
                "connections_business": item.get("aansluitingenZakelijk"),
                "consumption_avg": item.get("gemiddeldVerbruikM3PerAansluiting"),
                "consumption_total_m3": item.get("totaalVerbruikM3"),
                "percentage_delivery": item.get("percentageLevering"),
                "geometry": item.get("geometrie")
            })
        
        return {
            "total_results": len(results),
            "results": results[:limit],
            "source": "Amsterdam Gas Consumption API (Liander MRA)"
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to fetch gas consumption data: {str(e)}",
            "note": "Ensure AMSTERDAM_API_KEY is set in .env file"
        }