import requests
import sqlite3

url = "http://overpass-api.de/api/interpreter"
query = """
[out:json];
node["amenity"="clinic"](41.0,69.0,42.0,70.0);  // Toshkentning lat/long diapazoni
out body;
"""

response = requests.get(url, params={"data": query})
data = response.json()

conn = sqlite3.connect('base.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS clinics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    latitude REAL,
    longitude REAL,
    address TEXT,
    phone TEXT,
    website TEXT,
    opening_hours TEXT,
    operator TEXT
)
''')
clinics = data.get("elements", [])
if clinics:
    for clinic in clinics:
        name = clinic.get("tags", {}).get("name", "Клиника")
        lat = clinic.get("lat")
        lon = clinic.get("lon")
        address = clinic.get("tags", {}).get("address", "None")
        phone = clinic.get("tags", {}).get("phone", "None")
        website = clinic.get("tags", {}).get("website", "None")
        opening_hours = clinic.get("tags", {}).get("opening_hours", "None")
        operator = clinic.get("tags", {}).get("operator", "None")

        try:
            cursor.execute('''
            INSERT INTO clinics (name, latitude, longitude, address, phone, website, opening_hours, operator)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, lat, lon, address, phone, website, opening_hours, operator))
        except Exception as e: print(f"error: {e}")
    
    conn.commit()

else:print("Klinikalar topilmadi.")


conn.close()
