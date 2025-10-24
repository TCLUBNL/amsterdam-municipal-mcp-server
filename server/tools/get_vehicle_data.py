import requests
from typing import Dict, Any, Optional

def get_vehicle_data(kenteken: Optional[str] = None,
                     postcode: Optional[str] = None,
                     merk: Optional[str] = None) -> Dict[str, Any]:
    """
    Get vehicle registration data from RDW (Rijksdienst voor het Wegverkeer).
    
    Args:
        kenteken: License plate number (e.g., 'XX-123-X')
        postcode: Postal code for registered vehicles
        merk: Vehicle brand/make filter
    
    Returns:
        Dictionary containing vehicle registration data
    """
    base_url = "https://opendata.rdw.nl/resource/m9d7-ebf2.json"
    
    params = {}
    if kenteken:
        params["kenteken"] = kenteken.replace("-", "").upper()
    if postcode:
        params["postcode"] = postcode
    if merk:
        params["merk"] = merk.upper()
    
    params["$limit"] = 100
    
    try:
        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data if isinstance(data, list) else []:
            results.append({
                "kenteken": item.get("kenteken"),
                "merk": item.get("merk"),
                "handelsbenaming": item.get("handelsbenaming"),
                "datum_eerste_toelating": item.get("datum_eerste_toelating"),
                "datum_eerste_tenaamstelling": item.get("datum_eerste_tenaamstelling_in_nederland"),
                "voertuigsoort": item.get("voertuigsoort"),
                "inrichting": item.get("inrichting"),
                "aantal_zitplaatsen": item.get("aantal_zitplaatsen"),
                "brandstof": item.get("brandstof_omschrijving"),
                "co2_uitstoot": item.get("co2_uitstoot_gecombineerd"),
                "catalogusprijs": item.get("catalogusprijs"),
                "zuinigheidslabel": item.get("zuinigheidslabel")
            })
        
        return {
            "kenteken": kenteken,
            "postcode": postcode,
            "merk": merk,
            "vehicles_found": len(results),
            "results": results,
            "source": "RDW Open Data - Gekentekende voertuigen",
            "note": "Dutch vehicle registration database"
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to fetch RDW vehicle data: {str(e)}",
            "kenteken": kenteken,
            "note": "Ensure license plate format is correct (XX-123-X)"
        }
