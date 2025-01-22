import requests
import sqlite3

# OSM Overpass API URL
url = "http://overpass-api.de/api/interpreter"

# Toshkentdagi klinikalarni qidirish so'rovi
query = """
[out:json];
node["amenity"="clinic"](41.0,69.0,42.0,70.0);  // Toshkentning lat/long diapazoni
out body;
"""

response = requests.get(url, params={"data": query})
data = response.json()

# SQLite ma'lumotlar bazasiga ulanish va jadval yaratish
conn = sqlite3.connect('base.db')
cursor = conn.cursor()

# Jadvalni yaratish (agar mavjud bo'lmasa)
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

# Klinikalar ro'yxatini bazaga joylash
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

        # Ma'lumotlarni bazaga kiritish
        try:
            cursor.execute('''
            INSERT INTO clinics (name, latitude, longitude, address, phone, website, opening_hours, operator)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, lat, lon, address, phone, website, opening_hours, operator))
        except Exception as e:
            print(f"Xatolik: {e}")

    # O'zgartirishlarni saqlash
    conn.commit()

else:
    print("Klinikalar topilmadi.")

# Ma'lumotlar bazasini yopish
conn.close()
