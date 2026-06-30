# geolocation_utils.py
import requests
from math import radians, cos, sin, sqrt, atan2

API_KEY = "AIzaSyAKmXqHHc8_vOP30aKSKvV2C3sH2c67fqY"


# =========================
# פונקציה 1: כתובת -> lat,lng
# =========================
def geocode_address(address: str):
    """
    מקבלת כתובת בעברית או באנגלית
    מחזירה מילון עם latitude ו-longitude
    """
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={API_KEY}&language=iw"
    response = requests.get(url)
    data = response.json()

    if data.get("status") != "OK" or not data['results']:
        return {"error": "כתובת לא נמצאה"}

    location = data['results'][0]['geometry']['location']
    return {"lat": location['lat'], "lng": location['lng']}


# =========================
# פונקציה 2: מרחק בין שתי נקודות (Haversine)
# =========================
def distance_between_points(lat1, lng1, lat2, lng2):
    """
    מחשב מרחק בקילומטרים בין שתי נקודות
    """
    R = 6371  # רדיוס כדור הארץ בק"מ
    dlat = radians(lat2 - lat1)
    dlng = radians(lng2 - lng1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlng / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance


# =========================
# פונקציה 3: זמן נסיעה בין שתי נקודות (Google Distance Matrix)
# =========================
import requests

def travel_time_between_points(lat1, lng1, lat2, lng2, mode="driving"):
    import requests

    print("CALLING GOOGLE MAPS")

    origins = f"{lat1},{lng1}"
    destinations = f"{lat2},{lng2}"

    url = (
        "https://maps.googleapis.com/maps/api/distancematrix/json"
        f"?origins={origins}&destinations={destinations}"
        f"&mode={mode}&key={API_KEY}"
    )

    response = requests.get(url)
    data = response.json()

    print("GOOGLE STATUS:", data.get("status"))
    print("FULL RESPONSE:", data)

    if data.get('status') != 'OK':
        return 0   # ⚠️ לא 999999!

    element = data['rows'][0]['elements'][0]

    print("ELEMENT STATUS:", element.get("status"))

    if element.get('status') != 'OK':
        return 0

    return element['duration']['value'] / 60

# =========================
# פונקציה 4: קבלת אזור/יישוב/מחוז
# =========================
def get_region_from_address(address: str):
    """
    מחזיר את העיר/יישוב/מחוז של כתובת
    """
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={API_KEY}&language=iw"
    response = requests.get(url)
    data = response.json()

    if data['status'] != 'OK' or not data['results']:
        return {"error": "כתובת לא נמצאה"}

    components = data['results'][0]['address_components']
    region = {"city": None, "administrative_area": None, "country": None}

    for comp in components:
        if "locality" in comp['types']:
            region['city'] = comp['long_name']
        elif "administrative_area_level_1" in comp['types']:
            region['administrative_area'] = comp['long_name']
        elif "country" in comp['types']:
            region['country'] = comp['long_name']

    return region

def safe_travel_time(lat1, lng1, lat2, lng2, google_maps_service):
    try:
        result = google_maps_service(lat1, lng1, lat2, lng2)

        if isinstance(result, dict):
            return result.get("duration_min", 999)

        if isinstance(result, (int, float)):
            return float(result)

        return 999

    except:
        return 999