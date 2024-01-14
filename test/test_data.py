from src.Lib import data
from bs4 import BeautifulSoup

def test_data():
    # Test with positive numbers
    assert True

def test_scraper():
    scraper = data.Scraper()
    
    
    urls = {
        'https://www.sports-reference.com/cbb/schools/michigan-state/men/2024-gamelogs.html': 'sgl-basic_NCAAM',
        'https://www.sports-reference.com/cbb/seasons/men/2024-school-stats.html': 'basic_school_stats'

    }

    for url, tableID in list(urls.items())[1:]:

        scraper.visit(url)

        table = scraper.getTable(tableID)

        for row in table:
            assert not row is None

        assert not table.header is None

def test_NCAABTeamScraper():
    scraper = data.NCAABTeamScraper(2024)
    teams = scraper.getTeamNames()
    assert all(not item.isdigit() and isinstance(item, str) for item in teams), "List contains numeric strings"

