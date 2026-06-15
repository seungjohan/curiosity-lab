# Design Spec: Guia Repsol 2026 Scraper

## Goal
Scrape the complete list of 2026 "Soles" from Guia Repsol and update the local `raw/guia_repsol_full.csv`.

## Approach
1. **Scraping Engine:** Use `requests` and `BeautifulSoup` to parse the 2026 edition page.
2. **Data Mapping:**
   - **Name:** Restaurant title.
   - **Location:** City and Province.
   - **Award:** 1, 2, or 3 Soles (based on the section header).
   - **Description:** Brief text summary from the restaurant listing or profile.
   - **Website:** Extracted from the restaurant profile link if possible, otherwise empty.
3. **Execution:** Update `scripts/guia_repsol_scraper.py` to move from hardcoded data to a dynamic scraper.
4. **Validation:** Ensure the final CSV contains the ~700+ restaurants expected from the 2026 edition.

## Data Schema
| Column | Description |
| --- | --- |
| Name | Restaurant name |
| Location | City, Province |
| Award | "3 Soles", "2 Soles", or "1 Sol" |
| Description | Summary/Review snippet |
| Website | URL (if available) |
