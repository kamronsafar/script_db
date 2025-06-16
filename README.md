# 🏥 OSM Clinic Scraper (Tashkent)

This project queries OpenStreetMap (OSM) data using the Overpass API to find clinics located in Tashkent, Uzbekistan. The script extracts information about these clinics and stores it in a local SQLite database.

## 📌 Features

- Fetches clinics tagged with `amenity=clinic` from OSM
- Retrieves clinic metadata (name, location, phone, website, opening hours, etc.)
- Saves the data to a local SQLite database (`base.db`)

## ⚙️ Technologies

- Python 3.x
- `requests` – For HTTP communication
- `sqlite3` – For lightweight database handling

## 📦 Installation & Usage

```bash
git clone https://github.com/kamronsafar/clinic-scraper.git
cd clinic-scraper
pip install requests sqlite3
python scraper.py
