# -*- coding: utf-8 -*-
"""English → Korean labels for the cuisine/category columns.

Sources are mixed: `all-cities-full.csv` uses Michelin's `Cuisine` vocabulary
("Modern Cuisine", "Meats and Grills"), `bcbm-lisboa-porto.csv` falls back to
Google's `Google_Category` ("Seafood restaurant"). Both map here. Anything not
in the table passes through unchanged, so an unmapped term is visible in the
output rather than silently dropped.
"""
KO = {
    # Michelin / Repsol `Cuisine`
    'Contemporary': '컨템퍼러리',
    'Creative': '크리에이티브',
    'Modern Cuisine': '모던',
    'Farm to table': '팜투테이블',
    'Traditional Cuisine': '전통 요리',
    'Seafood': '해산물',
    'Meats and Grills': '고기·그릴',
    'Fusion': '퓨전',
    'Mediterranean Cuisine': '지중해',
    'Regional Cuisine': '향토 요리',
    'Portuguese': '포르투갈 요리',
    'Italian': '이탈리안',
    'Seasonal Cuisine': '제철 요리',
    'Mexican': '멕시칸',
    # Google `Google_Category`
    'African restaurant': '아프리카 요리',
    'Argentinian restaurant': '아르헨티나 요리',
    'Armenian restaurant': '아르메니아 요리',
    'Asian restaurant': '아시아 요리',
    'Basque restaurant': '바스크 요리',
    'Bistro': '비스트로',
    'Brazilian restaurant': '브라질 요리',
    'Chinese restaurant': '중식',
    'European restaurant': '유럽 요리',
    'Event venue': '행사 공간',
    'Fine dining restaurant': '파인다이닝',
    'Fusion restaurant': '퓨전',
    'Goan restaurant': '고아 요리',
    'Indian restaurant': '인도 요리',
    'Italian restaurant': '이탈리안',
    'Japanese restaurant': '일식',
    'Mediterranean restaurant': '지중해 요리',
    'Mexican restaurant': '멕시칸',
    'Middle Eastern restaurant': '중동 요리',
    'Pan-Asian restaurant': '아시안',
    'Portuguese restaurant': '포르투갈 요리',
    'Restaurant': '레스토랑',
    'Seafood restaurant': '해산물',
    'Spanish restaurant': '스페인 요리',
    'Steak house': '스테이크',
    'Sushi restaurant': '스시',
    'Vegetarian restaurant': '채식',
}


def ko(s):
    s = (s or '').strip()
    return KO.get(s, s)
