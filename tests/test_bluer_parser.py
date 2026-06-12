import pytest
from bs4 import BeautifulSoup
from scripts.bluer_extractor import BlueRibbonParser

def test_parse_ribbons():
    # Test ribbon 2
    html2 = '<img src="/images/common/ribbon2.png">'
    soup2 = BeautifulSoup(html2, "html.parser")
    assert BlueRibbonParser.parse_ribbons(soup2) == 2
    
    # Test ribbon 3
    html3 = '<img src="/images/common/ribbon3.png">'
    soup3 = BeautifulSoup(html3, "html.parser")
    assert BlueRibbonParser.parse_ribbons(soup3) == 3
    
    # Test 0 ribbons
    html0 = '<div>No ribbons</div>'
    soup0 = BeautifulSoup(html0, "html.parser")
    assert BlueRibbonParser.parse_ribbons(soup0) == 0

def test_price_mapping():
    assert BlueRibbonParser.map_price_to_tier("₩11,500 ~ ₩16,000") == 1
    assert BlueRibbonParser.map_price_to_tier("₩45,000 ~ ₩60,000") == 2
    assert BlueRibbonParser.map_price_to_tier("₩90,000 ~ ₩120,000") == 3
    assert BlueRibbonParser.map_price_to_tier("₩250,000") == 4
    assert BlueRibbonParser.map_price_to_tier("10,000원 이하") == 1
    assert BlueRibbonParser.map_price_to_tier("") == 0

def test_parse_page_basic():
    html = """
    <html>
        <h1 class="restaurant-name">올라라</h1>
        <div class="info-list">
            <li>주소: 서울특별시 강남구 압구정로10길 30-8</li>
            <li>전화: 0507-1380-1151</li>
            <li>가격: ₩11,500 ~ ₩16,000</li>
        </div>
        <div class="description">마라탕 전문점</div>
    </html>
    """
    url = "https://www.bluer.co.kr/restaurants/51682"
    data = BlueRibbonParser.parse_page(html, url)
    
    assert data["Name"] == "올라라"
    assert data["Address"] == "서울특별시 강남구 압구정로10길 30-8"
    assert data["Region"] == "서울"
    assert data["Phone"] == "0507-1380-1151"
    assert data["Price_Tier"] == 1
    assert data["Description"] == "마라탕 전문점"
