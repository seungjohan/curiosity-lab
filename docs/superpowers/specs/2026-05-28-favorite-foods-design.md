# Design Spec: Favorite Foods Wiki & Michelin Wine List Scraper

## Overview
This project implements two connected components: a "Favorite Foods" registry in the brainstorming wiki and a data acquisition pipeline for Michelin Guide restaurants with the "Interesting Wine List" award. The goal is to provide a reference for favorite dishes that can be cross-referenced with high-quality restaurants.

## Goals
1. Create a structured registry of favorite foods categorized by country.
2. Interlink the favorite foods with the existing [[Michelin Filter]] idea.
3. Scrape Michelin Guide data for restaurants with "Interesting Wine List" awards into a CSV format.

## 1. Favorite Foods Wiki Page
- **File**: wiki/Favorite Foods.md
- **Structure**:
    - **Header**: Title and "Related" section (linking to [[Michelin Filter]]).
    - **Sections**: Organized by ## Country (e.g., Spain, Korea, Japan).
    - **Format**: Within each country, a table with:
        - Food Name (Bolded, potential for future pages)
        - Type (Main Dish, Appetizer, etc.)
        - Basic Ingredient (Main define ingredient)
        - Notes (Brief description or why it's a favorite)
- **First Entry**: [[Fideuá]] (Spain, Main Dish, Seafood/Noodles).

## 2. Michelin "Interesting Wine List" Scraper
- **Task**: Scrape the Michelin Guide website for restaurants featuring the "Interesting Wine List" award.
- **Output**: raw/michelin_wine_list.csv
- **CSV Schema**:
    - Name, Address, Location, Price, Cuisine, Longitude, Latitude, PhoneNumber, Url, WebsiteUrl, Award, GreenStar, FacilitiesAndServices, Description
- **Technical Approach**:
    - Use @generalist with web_fetch to crawl search result pages.
    - Filter for the specific award category.
    - Extract structured metadata from individual restaurant pages.

## 3. Integration & Updates
- **wiki/index.md**: Add [[Favorite Foods]] under a new Culinary & Dining category.
- **wiki/Michelin Filter.md**:
    - Add a "Reference" section linking to [[Favorite Foods]].
    - Update "Data Scope" to mention the new CSV.
- **wiki/Log.md**: Record the creation of the page and the data ingestion.
