import requests
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_brk2_parcel(
    cadastral_id: Optional[str] = None,
    postcode: Optional[str] = None,
    huisnummer: Optional[int] = None,
    limit: int = 20
) -> Dict[str, Any]:
    """
    Get cadastral parcel information from BRK2 (Basisregistratie Kadaster).
    Includes ownership, mortgages, leasehold, building rights, and usufruct data.
    
    Args:
        cadastral_id: Cadastral object ID (e.g., "NL.IMKAD.KadastraalObject.11460687970000")
        postcode: Postal code to search parcels
        huisnummer: House number (use with postcode)
        limit: Maximum number of results (default 20)
    
    Returns:
        Dictionary containing cadastral parcel data with ownership information
    """
    api_key = os.getenv("AMSTERDAM_API_KEY")
    
    base_url = "https://api.data.amsterdam.nl/v1/brk2/kadastraleobjecten/"
    
    headers = {}
    if api_key:
        headers["X-Api-Key"] = api_key
    
    params = {
        "_pageSize": limit
    }
    
    if cadastral_id:
        params["identificatie"] = cadastral_id
    if postcode:
        params["postcode"] = postcode.upper().replace(' ', '')
    if huisnummer:
        params["huisnummer"] = huisnummer
    
    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        results = []
        items = data.get("_embedded", {}).get("kadastraleobjecten", [])
        
        for item in items:
            results.append({
                "id": item.get("identificatie"),
                "kadastrale_aanduiding": item.get("kadastraleAanduiding"),
                "perceelnummer": item.get("perceelnummer"),
                "sectie": item.get("sectie"),
                "oppervlakte": item.get("grootte", {}).get("waarde"),
                "register9_nummer": item.get("register9Nummer"),
                "soort_grootte": item.get("grootte", {}).get("soortGrootte"),
                "cultuurcode": item.get("cultuurcodeOnbebouwd", {}).get("code"),
                "geometry": item.get("geometrie")
            })
        
        return {
            "total_results": len(results),
            "results": results[:limit],
            "source": "Amsterdam BRK2 API v1 (Cadastral Registry)"
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to fetch BRK2 cadastral data: {str(e)}",
            "note": "Ensure AMSTERDAM_API_KEY is set in .env file"
        }