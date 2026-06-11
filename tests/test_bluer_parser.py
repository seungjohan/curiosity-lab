import pytest
from bs4 import BeautifulSoup

def parse_ribbons(soup):
    # Placeholder for logic
    return 0

def test_parse_ribbons():
    html = '<div class="ribbon-2"></div>'
    soup = BeautifulSoup(html, "html.parser")
    assert parse_ribbons(soup) == 2
