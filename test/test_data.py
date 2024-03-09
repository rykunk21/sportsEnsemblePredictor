from src.Lib import data
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
from src.Lib.util import Game
from datetime import datetime
import pickle

from scipy.optimize import curve_fit
from scipy.stats import poisson


def test_LineScraper():

    ls = data.LineScraper()
    if ls._teams_are_set():
        spread = ls.spread()
        home_ml_odds, away_ml_odds = ls.getMoneyLineOdds()
        home_spread_odds, away_spread_odds = ls.getSpreadOdds()

    games = ls.getTodaysGames()

def test_data():
    # Test with positive numbers
    assert True

def test_scraper():
    scraper = data.Scraper()
    
    
    urls = {
        'https://www.sports-reference.com/cbb/seasons/men/2024-school-stats.html': 'basic_school_stats',
        'https://www.sports-reference.com/cbb/players/tyson-walker-1/gamelog/2024/':'gamelog',
        'https://www.sports-reference.com/cbb/schools/michigan-state/men/2024-gamelogs.html': 'sgl-basic_NCAAM'
        


    }

    for url, tableID in list(urls.items())[1:]:

        scraper.visit(url)

        table = scraper.getTable(tableID)

        for row in table:
            assert not row is None

        assert not table.header is None

def test_NCAABTeamScraper():

    scraper = data.NCAABLeagueScraper(2024)
    teams = scraper.getTeamNames()

    assert all(not item.isdigit() and isinstance(item, str) for item in teams), "List contains numeric strings"
    db = data.DataBase('./test/resources/testSchool.db')
    db.clear()


    tableParams = {
        'School': 'VARCHAR(255)',
        'OverallG': 'INT',
        'OverallW': 'INT',
        'OverallL': 'INT',
        'OverallWL': 'DECIMAL(5, 2)',
        'OverallSRS': 'DECIMAL(5, 2)',
        'OverallSOS': 'DECIMAL(5, 2)',
        'ConfW': 'INT',
        'ConfL': 'INT',
        'HomeW': 'INT',
        'HomeL': 'INT',
        'AwayW': 'INT',
        'AwayL': 'INT',
        'PointsTm': 'DECIMAL(5, 2)',
        'PointsOpp': 'DECIMAL(5, 2)',
        'TotalsMP': 'DECIMAL(5, 2)',
        'TotalsFG': 'DECIMAL(5, 2)',
        'TotalsFGA': 'DECIMAL(5, 2)',
        'TotalsFG': 'DECIMAL(5, 2)',
        'Totals3P': 'DECIMAL(5, 2)',
        'Totals3PA': 'DECIMAL(5, 2)',
        'Totals3P': 'DECIMAL(5, 2)',
        'TotalsFT': 'DECIMAL(5, 2)',
        'TotalsFTA': 'DECIMAL(5, 2)',
        'TotalsFT': 'DECIMAL(5, 2)',
        'TotalsORB': 'DECIMAL(5, 2)',
        'TotalsTRB': 'DECIMAL(5, 2)',
        'TotalsAST': 'DECIMAL(5, 2)',
        'TotalsSTL': 'DECIMAL(5, 2)',
        'TotalsBLK': 'DECIMAL(5, 2)',
        'TotalsTOV': 'DECIMAL(5, 2)',
        'TotalsPF': 'DECIMAL(5, 2)'
    }
    schema = db.create('ncaabTest')
    table = schema.addTable('test', tableParams)

    assert db.exists('test')

def test_NCAABPlayerScraper():

    scraper = data.NCAABPlayerScraper('tyson-walker-1')
    table = scraper.getTable()
    points = [int(row[8]) for row in table.rows]

def test_NCAABRosterScraper():
    scraper = data.NCAABRosterScraper('michigan-state')
    roster = scraper.getRoster()
    links = scraper.getLinks()

def test_NCAABRosterScraperUpdate():

    teamName = 'florida'
    data.simHandler.updateTeam(teamName)

def test_DataBase():
    db = data.DataBase('./test/resources/testDB.db')
    db.clear()

def test_DataBaseSchema():
    db = data.DataBase('./test/resources/testDB.db')
    db.clear()

    tableParams = {
        'ID': 'INT PRIMARY KEY',
        'Name': 'VARCHAR(255) NOT NULL',
        'Age': 'INT NOT NULL'
    }
    
    schema = db.create('testSchema')

    schema.addview('testView')
    assert 'testView' in schema.views


    schema.addTable('test', tableParams)
    assert schema.dropTable('test')
    assert not schema.dropTable('Doesnt_Exist')


    schema = db.create('testSchema')
    
def test_DataBaseTable():
    db = data.DataBase('./test/resources/testDB.db')
    db.clear()

    tableParams = {
        'ID': 'INT PRIMARY KEY',
        'Name': 'VARCHAR(255) NOT NULL',
        'Age': 'INT NOT NULL'
    }
    
    schema = db.create('testSchema')

    schema.addview('testView')
    assert 'testView' in schema.views


    schema.addTable('test', tableParams)
    assert schema.dropTable('test')

    table = schema.addTable('test', tableParams)

    row = table.template()

    row['ID'] = 12
    row['Name'] = 'Example Location'
    row['Age'] = 50

    try:
        row['Doesnt_exist'] = None
        row['ID'] = 'Invalid type'
        assert False

    except:
        assert True

    table.add(row)

    row = table.get(12)

    assert row['Name'] == 'Example Location'
    assert row['Age'] == 50

