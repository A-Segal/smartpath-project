# geolocation_utils.py
import requests
from math import radians, cos, sin, sqrt, atan2

# הכנס את המפתח שלך כאן
API_KEY = "YOUR_GOOGLE_API_KEY_HERE"

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

    if data['status'] != 'OK' or not data['results']:
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
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlng/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c
    return distance

# =========================
# פונקציה 3: זמן נסיעה בין שתי נקודות (Google Distance Matrix)
# =========================
def travel_time_between_points(lat1, lng1, lat2, lng2, mode="driving"):
    """
    מחזיר זמן נסיעה בדקות בין שתי נקודות
    mode: driving, walking, bicycling, transit
    """
    origins = f"{lat1},{lng1}"
    destinations = f"{lat2},{lng2}"
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origins}&destinations={destinations}&mode={mode}&key={API_KEY}&language=iw"
    response = requests.get(url)
    data = response.json()

    if data['status'] != 'OK':
        return {"error": "בעיה בבקשה"}

    element = data['rows'][0]['elements'][0]
    if element['status'] != 'OK':
        return {"error": "נתיב לא נמצא"}

    distance_km = element['distance']['value'] / 1000  # מטר -> ק"מ
    duration_min = element['duration']['value'] / 60   # שניות -> דקות
    return {"distance_km": distance_km, "duration_min": duration_min}

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