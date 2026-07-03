import requests
from bs4 import BeautifulSoup

URL = "https://guide.michelin.com/en/hong-kong-region/hong-kong/restaurant/amber569032"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(response.content, "html.parser")

# Print some snippets to identify selectors
print("--- Name ---")
print(soup.select_one("h1.restaurant-details__name"))

print("\n--- Address ---")
print(soup.select_one("ul.restaurant-details__address-list"))

print("\n--- Price & Cuisine ---")
print(soup.select_one("li.restaurant-details__heading-price"))

print("\n--- Award ---")
# Look for stars
print(soup.select("div.restaurant-details__classification--list img"))

print("\n--- Description ---")
print(soup.select_one("div.restaurant-details__description--content"))

print("\n--- Facilities ---")
print(soup.select("div.restaurant-details__facilities li"))

print("\n--- Phone ---")
print(soup.select_one("a[href^='tel:']"))

print("\n--- Website ---")
print(soup.select_one("a[aria-label='View the website']"))

print("\n--- Coordinates ---")
# Often in google maps link
print(soup.select_one("a[href*='maps.google.com']"))
