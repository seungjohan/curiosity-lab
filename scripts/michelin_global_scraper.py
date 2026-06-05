import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os
import json

BASE_URL = "https://guide.michelin.com"
LIST_URL = f"{BASE_URL}/en/restaurants/page/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
COLUMNS = [
    "Name", "Address", "Location", "Price", "Cuisine", 
    "Longitude", "Latitude", "PhoneNumber", "Url", 
    "WebsiteUrl", "Award", "GreenStar", "FacilitiesAndServices", "Description"
]
OUTPUT_CSV = "raw/michelin_global_restaurants.csv"
URL_LOG = "raw/michelin_urls.json"

def main():
    print("Michelin Global Scraper Initialized")

if __name__ == "__main__":
    main()
