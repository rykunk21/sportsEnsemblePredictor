"""
GENERAL

"""

import sqlite3
import requests
from collections import UserDict
from bs4 import BeautifulSoup
from typing import Any, Iterator, TypeVar, Dict
from datetime import datetime

from . import util

import pickle
import os
import json
import numpy as np


class Scraper:

    class Table:
        def __init__(self, htmlContent: Any = None) -> None:
            """
            Initializes the object with HTML content, parses it, and prepares row iteration.
            """
            self.soup = BeautifulSoup(str(htmlContent), 'html.parser')
            self.rows = self.soup.find_all('tr')
            self.currentRow = 0
        
        def __iter__(self) -> Iterator:
            """Returns an iterator for the class instance."""
            return self

        def __next__(self) -> BeautifulSoup:
            """
            Advances to the next row in the iterator. 
            Raises StopIteration when there are no more rows.
            """
            if self.currentRow >= len(self.rows):
                raise StopIteration
            row = self.rows[self.currentRow]
            self.currentRow += 1
            return row

        @property
        def header(self):
            """
            Extracts and combines the over headers and main headers from the table,
            handling 'colspan' and excluding headers with 'over_header' class or 'DUMMY' data-stat.
            """

            def _extract_over_headers(table_header):
                """Extracts over headers and replicates them based on 'colspan' attribute."""
                return [
                    [elem.text] * int(elem.get('colspan', 1))
                    for elem in table_header.find_all('th')
                    if 'over_header' in elem.get('class', [])
                ]
            
            def _extract_main_headers(table_header):
                """Extracts main headers, excluding those with 'over_header' class or 'DUMMY' data-stat."""

                return [
                    elem.text
                    for elem in table_header.find_all('th')
                    if 'over_header' not in elem.get('class', []) and elem.get('data-stat') not in ["DUMMY", 'x'] and elem.text
                ]

            def _combine_headers(over_headers, main_header):
                """Combines over headers and main headers, appending over header text to main headers."""
                if not over_headers:
                    return [
                        (f'{main_header}' if main_header else '')
                        for i, main_header in enumerate(main_header)
                    ]

                return [
                    over_headers + (f'_{main_header[i]}' if main_header[i] else '')
                    for i, over_headers in enumerate(over_headers)
                ]

            def _clean_header_values(header):
                illegal_characters = [
                    '.', '-', ' ', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', 
                    '+', '=', '{', '}', '[', ']', '|', '\\', '/', '?', '<', '>', "'", '¥', 
                    '¢', '£', '¬'
                ]
                for i, _ in enumerate(header):
                    for char in illegal_characters:
                        header[i] = header[i].replace(char, '')
                return header

            table_header = self.soup.find('thead')
            if not table_header:
                return None

            over_headers = _extract_over_headers(table_header)

            # flatten over headers
            over_headers = [item for sublist in over_headers for item in sublist]

            main_headers = _extract_main_headers(table_header)

            combined_headers = _combine_headers(over_headers, main_headers) # eliminate id at position 0

            return _clean_header_values(combined_headers)

        def drop(self, pattern):
            self.rows = [
                row for row in self.rows
                if not pattern(row)
            ]

        def format(self, pattern):
            self.rows = [
                pattern(row) for row in self.rows
            ]

        def get(self, col):

            index = self.header.index(col)

            return [
                row[index] for row in self.rows
            ]

        def __str__(self):
            return '\n'.join([str(self.header), '\n'.join([str(row) for row in self.rows])])

        def __repr__(self):
            return self.__str__()


    def __init__(self):
        """
        Initializes the class instance with default properties.
        """
        self.soup = None

    def visit(self, url: str) -> None:
        """
        Makes a GET request to the specified URL and initializes the BeautifulSoup object if successful.
        """
        try:
            response = requests.get(url)

            if not 200 <= response.status_code < 300:
                if response.status_code == 429:
                    retryAfter = response.headers.get('Retry-After')
                    dt = datetime.datetime.fromtimestamp(int(retryAfter))
                    raise Exception(f'Visiting url raised error {response.status_code}: {response.reason}. Try after {dt.hour}:{dt.minute}')

                raise Exception(f'Visiting url raised error {response.status_code}: {response.reason}')
            
            


            response.raise_for_status()
            self.soup = BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            print(f"Failed to retrieve content: {e}")

    def getTable(self, table_id: str) -> Table:
        """
        Retrieves a table by its ID and returns a Table object.
        """
        if self.soup is None:
            print("Soup object is not initialized. Please visit a URL first.")
            return None

        table_html = self.soup.find(id=table_id)
        return self.Table(table_html) if table_html else None


class DataBase: # TODO
    """
    Interface for interacting with and manipulating a database
    """
    class Schema:

        views = []
        tables = []
        
        def __init__(self, conn: sqlite3.Connection) -> None:
            self.conn = conn
            self.cursor = self.conn.cursor()
        
        def addview(self, name: str) -> bool:
            self.cursor.execute(f'''
                CREATE VIEW IF NOT EXISTS {name} AS
                SELECT * FROM my_table WHERE 1=0;
            ''')

            if not name in self.views:
                self.views.append(name)
            self.conn.commit()
        
        def addTable(self, name: str, params: dict) -> 'DataBase.Table':
            
            table = DataBase.Table(name, params, self.conn)

            self.cursor.execute(f'CREATE TABLE {table};')
            
            if not name in self.tables:
                self.tables.append(name)

            return table

        def dropTable(self, name: str) -> bool:
            
            if not name in self.tables:
                return False
            
            self.cursor.execute(f'DROP TABLE {name};')
            return True

    class Table:

        T = TypeVar('T', bound=Dict[str, Any])

        class Row(dict):
            def __init__(self, params: dict):
                super().__init__(params)

            def __setitem__(self, key: str, value: Any):
                if key not in self.keys():
                    raise KeyError(f"Key '{key}' not found in table definition.")

                sql_type = self[key]
                if not isinstance(value, (int, str)):
                    raise TypeError(f"Value for key '{key}' must be an int or str, not {type(value)}.")

                if sql_type.startswith('INT'):
                    if not isinstance(value, int):
                        raise TypeError(f"Value for key '{key}' must be an int, not {type(value)}.")
                elif sql_type.startswith('VARCHAR'):
                    if not isinstance(value, str):
                        raise TypeError(f"Value for key '{key}' must be a str, not {type(value)}.")

                super().__setitem__(key, value)
            
            def __str__(self) -> str:
                out = ', '.join([f"'{value}'" if isinstance(value, str) else str(value) for value in self.values()])
                return out.lstrip()
                                    


        def __init__(self, name: str, cols: dict, conn: sqlite3.Connection) -> None:
            self.name = name
            self.cols = cols
            self.conn = conn
            self.cursor = conn.cursor()

        def __str__(self) -> str:
            col_str =  ', '.join([f'{key} {value}' for key, value in self.cols.items()])
            return f'{self.name} ({col_str})'

        def __repr__(self) -> str:
            return self.__str__()
        

        def template(self) -> dict:
            """
            returns a template for the specific table
            useful for when you dont know the values of the header
            """
            return self.Row(self.cols)

        def add(self, row: Row) -> None:
            """
            
            """
            self.cursor.execute(f'INSERT INTO {self.name} VALUES ({row});')


        def get(self, ID: int) -> Row:

            row = self.Row(self.cols)

            self.cursor.execute(f'SELECT * FROM {self.name} WHERE ID = \'{ID}\';')
            data = self.cursor.fetchone()

            row.update({k: v for k, v in zip(row.keys(), data)})
            
            return row

        def getAny(self, condition: str) -> Row:
            pass

    def __init__(self, database: str) -> None:
        self.conn = sqlite3.connect(database)
        self.cursor = self.conn.cursor()


    def clear(self) -> None:
        for table in self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall():
            self.cursor.execute(f"DROP TABLE {table[0]};")
        self.conn.commit()

    def exists(self, table):
        return table in self.tableNames()

    def create(self, schema: str) -> Schema:
        """
        Creates a new schema
        """
        return self.Schema(self.conn)

    def retreive(self, query=None):
        if query is None:
            query = 'SELECT * FROM sqlite_master WHERE type="table"'
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

    def tableNames(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return [row[0] for row in self.cursor.fetchall()]
    
    def tables(self):
        from collections import OrderedDict
        
        tables = dict()
        def format(entry):
            """
            cid: The column ID, which is an integer representing the position of the column in the table (starting from 0).
            name: The name of the column.
            type: The declared data type of the column.
            notnull: A flag indicating whether the column has a NOT NULL constraint (1 for true, 0 for false).
            dflt_value: The default value for the column, if one is specified.
            pk: A flag indicating whether the column is part of the primary key (1 for true, 0 for false).
            """
            column_name = entry[1]
            column_type = entry[2]
            not_null = ' NOT NULL' if entry[3] else ''
            primary_key = ' PRIMARY KEY' if entry[5] else ''

            column_dict = {column_name: f'{column_type}{not_null}{primary_key}'}

            return column_dict

        for i, row in enumerate(self.tableNames()):
            self.cursor.execute(f'PRAGMA table_info(\'{row}\');')
            dicts = [format(row) for row in self.cursor.fetchall()]

            # Use OrderedDict to preserve the order of the columns
            cols = OrderedDict()
            for d in dicts:
                for k, v in d.items():
                    cols[k] = v

            tables[i] = self.Table(row, cols)

        return tables


class Preprocessor:
    """
    Class to provide general preprocessing tasks
    """
    def __init__(self):
        pass


class Handler:
    """
    Class to provide general data handling tasks
    """
    def __init__(self, db):
        self.db = DataBase(db)



"""
Special Scrapers
"""

class NCAABLeagueScraper(Scraper):

    def __init__(self, year):
        """
        Initializes the NCAABTeamScraper with a specific year.
        Sets up the scraper to point to the NCAAB teams URL for the given year
        and retrieves the team statistics table.
        """
        self.ncaabTeamsUrl = f'https://www.sports-reference.com/cbb/seasons/men/{year}-school-stats.html'
        self.tableId = 'basic_school_stats'

        super().__init__()
        self.visit(self.ncaabTeamsUrl)
        self.table = self.getTable(self.tableId)
    
    def getTable(self, tableID: str) -> Scraper.Table:
        """
        Retrieves and returns a table by its ID after applying specific filtering.
        """
        table = super().getTable(tableID)

        # drop empty rows
        pattern = lambda x: x.th.get('scope') != 'row'
        table.drop(pattern)

        # format table data
        pattern = lambda x: [str(data.text) for data in x.find_all('td') if data.text]
        table.format(pattern)

        return table
    
    def getTeamNames(self):
        return [
            row[0] for row in self.table.rows
        ]

class NCAABTeamScraper(Scraper):
    def __init__(self, teamName):
        super().__init__()
        self.url = f'https://www.sports-reference.com/cbb/schools/{teamName}/men/2024-gamelogs.html'
        self.teamName = teamName
        self.table_id = 'sgl-basic_NCAAM'
        self.visit(self.url)
        self.table = self.getTable()
        self.links = self.gameLinks()

    def getTable(self) -> Scraper.Table:
        table = super().getTable(self.table_id)

        pattern = lambda x: x.th.get('scope') != 'row'
        table.drop(pattern)
        

        pattern = lambda x: [str(data.text) for data in x.find_all('td')]
        table.format(pattern)

        pattern = lambda x: ["H" if not data else data for data in x]
        table.format(pattern)

        return table

    def gameLinks(self):
        baseUrl = 'https://www.sports-reference.com'

        table = super().getTable(self.table_id)

        pattern = lambda x: x.th.get('scope') != 'row'
        table.drop(pattern)

        stats = ['date', 'opp_team_id']

        pattern = lambda x: [data for data in x.find_all('td') if data['data-stat'] in stats]
        table.format(pattern)

        pattern = lambda x: x[0].find('a') is None
        table.drop(pattern)

        pattern = lambda x: [
            (datetime.strptime(data.text, '%Y-%m-%d').date(), baseUrl + data.find('a')['href']) 
            if data['data-stat'] == 'date' else data.text for data in x
        ]
        table.format(pattern)
    
        return table

    def getSchedule(self):

        current_date = datetime.now().date()
        past = []
        future = []
        for row in self.table.rows:

            date_str = row[0]
            # Convert the date string to a datetime object
            date_object = datetime.strptime(date_str, '%Y-%m-%d').date()

            # Check if the date has already happened
            if date_object <= current_date:
                past.append(row)
                # Add your code here for the dates that have already happened
            else:
                future.append(row)

        return (past, future)


    def getNumGames(self):
        return len(self.getSchedule()[0]) 
    

    def getGame(self, date, game):
        pass

class NCAABPlayerScraper(Scraper):
        def __init__(self, playerName, link=None):
            self.playerName = playerName
            super().__init__()

            if link is None:
                self.playerUrl = f'https://www.sports-reference.com/cbb/players/{playerName}/gamelog/2024/'

            else:
                self.playerUrl = link

            self.tableID = 'gamelog'
            
            self.visit(self.playerUrl)
        

        def getTable(self) -> Scraper.Table:

            table = super().getTable(self.tableID)

            if not table:
                return Scraper.Table()
            # drop empty rows
            pattern = lambda x: x.th.get('scope') != 'row'
            table.drop(pattern)


            pattern = lambda x: [str(data.text) for data in x.find_all('td')]
            table.format(pattern)

            pattern = lambda x: ["H" if not data else data for data in x]
            table.format(pattern)
            # format table data
            
            pattern = lambda x: ["" if data=='H' and i == len(x) - 1 else data for i, data in enumerate(x)]
            table.format(pattern)

            return table

class NCAABRosterScraper(Scraper):
    def __init__(self, teamName):
        self.teamName = teamName
        super().__init__()
        self.rosterURL = f'https://www.sports-reference.com/cbb/schools/{self.teamName}/men/2024.html'
        self.tableID = 'roster'

        self.visit(self.rosterURL) 

        self.table = self.getTable()

    def getTable(self) -> Scraper.Table:

        table = super().getTable(self.tableID)

        if not table:
            return Scraper.Table()
        # drop empty rows
        pattern = lambda x: x.th.get('scope') != 'row'
        table.drop(pattern)

        pattern = lambda x: [str(data.text) for data in x.find_all(['th', 'td'])]
        table.format(pattern) 

        return table
    
    def getLinks(self) -> Scraper.Table:
        table = super().getTable(self.tableID)

        if not table:
            return Scraper.Table()
        # drop empty rows
        pattern = lambda x: x.th.get('scope') != 'row'
        table.drop(pattern)

        pattern = lambda x: [(str(data.text), 'https://www.sports-reference.com{}/gamelog/2024'.format(data['href'].split('.')[0])) for data in x.find_all('a', limit=1)]
        table.format(pattern) 

        return table
    
    def getPlayerPrefix(self) -> Scraper.Table:
        links = self.getLinks()

        pattern = lambda x: [data[1]  for data in x]
        links.format(pattern)

        pattern = lambda x: [data.split('/')[-1] for data in x]
        links.format(pattern)

        pattern = lambda x: [data.split('.')[0] for data in x]
        links.format(pattern)

        return [link[0] for link in links.rows]
    

    def getRoster(self) -> Scraper.Table:

        roster = []
        for row in self.table.rows:
            roster.append(row[0])
        
        return roster

    def getRosterLinks(self) -> Scraper.Table:
        links = []
        for row in self.getLinks().rows:
            links.append(row[0])

        return links

class LineScraper(Scraper):

    class LineSet:
        def __init__(self, data:tuple) -> None:
            self.name = data[0].split('(')[0].strip().replace(' ', '-')
            self.side = data[1]
            self.spread = float(data[2])
            self.spreadOdds = int(data[3])
            self.mlOdds = int(data[4])

        def __str__(self) -> str:
            return f'{self.name}: {self.spread}'
        
        def __repr__(self) -> str:
            return self.__str__()


    def __init__(self, home=None, away=None):

        super().__init__()
        self.LinesUrl = f'https://www.scoresandodds.com/ncaab'

        self.visit(self.LinesUrl) 

        self.table = self.getTable()

        with open('./datasets/ncaab/mapping.json', 'r') as fp:
            self.mappings = json.load(fp)
       

        if not (home is None and away is None):
            self.home = self.entry(home)
            self.away = self.entry(away)

    def _teams_are_set(self):
        return hasattr(self, 'home') and hasattr(self, 'away')

    def getTable(self) -> Scraper.Table:
        
        def extract(row):
            name = row.select_one('td div span.team-name a span').text.strip().lower()
            side = row['data-side']
            current_spread = row.select_one('td[data-field="current-spread"] span.data-value')
            current_spread_odds = row.select_one('td[data-field="current-spread"] small.data-odds')
            moneyline_odds = row.select_one('td[data-field="current-moneyline"] span.data-value')

            current_spread = current_spread.text.strip() if current_spread else None
            current_spread_odds = current_spread_odds.text.strip() if current_spread_odds else None
            moneyline_odds = moneyline_odds.text.strip() if moneyline_odds else None

            return (name, side, current_spread, current_spread_odds, moneyline_odds)


        table_html = self.soup.find(class_="container")
        table = Scraper.Table(table_html) if table_html else None

        pattern = lambda x: 'event-card-header' in x['class']
        table.drop(pattern)

        table.format(extract)

        pattern = lambda x: any(elem is None for elem in x)
        table.drop(pattern)
        
        pattern = lambda x: self.LineSet(x)
        table.format(pattern)

        return table

    def entry(self, name) -> LineSet:

        for entry in self.table.rows:
            if name == entry.name or self.mappings.get(entry.name) == name:
                return entry

        raise Exception(f'Teamname {name} not found in lines!')

    def spread(self):
       
        return self.home.spread

    def getMoneyLineOdds(self) -> tuple[int, int]:
      
        return self.home.mlOdds, self.away.mlOdds

    def getSpreadOdds(self) -> tuple[int, int]:
        return self.home.spreadOdds, self.away.spreadOdds

    def getTodaysGames(self) -> list[str]:

        games = []
        for i in range(len(self.table.rows))[::2]:
            game = (self.table.rows[i], self.table.rows[i+1])
            games.append(game)

        return games

    def getGame(self, team=None):
        if team is None:
            return self.home, self.away

class GameScraper(Scraper):

    def __init__(self, gamePage):
        super().__init__()
        self.visit(gamePage)

        self.home, self.away = self.generateTables() 

    def getTables(self):
        boxes = self.soup.find(id='boxes')

        away, home = list(boxes.find_all('table'))[::2]

        home = Scraper.Table(home)
        away = Scraper.Table(away)

                
        pattern = lambda x: x.th.get('scope') != 'row'
        home.drop(pattern)
        away.drop(pattern)

        pattern = lambda x: [str(data.text) for data in x.find_all(['th', 'td'])]
        home.format(pattern) 
        away.format(pattern)

        pattern = lambda x: x[0] == 'School Totals'
        home.drop(pattern)
        away.drop(pattern)

        pattern = lambda x: {x[0]: x[1:]}
        home.format(pattern)
        away.format(pattern)


        return away, home


    def generateTables(self): #TODO
        wrapper = self.soup.find(class_='scorebox')

        away, home =  [elem.find('a')['href'] for elem in wrapper.find_all('strong')]

        away = away.split('/')[3]
        home = home.split('/')[3]
        
        awayTable, homeTable = self.getTables()

        awayScore, homeScore = [int(data.text) for data in wrapper.find_all(class_='score')]

        date = wrapper.find(class_='scorebox_meta').find('div').text
        date = datetime.strptime(date, '%B %d, %Y')
        # Format the datetime object to the desired output format
        date = date.strftime('%Y-%m-%d')

        homeWine = "W" if homeScore > awayScore else "L"
        awayWin = "W" if awayScore > homeScore else "L"

        homePrepend = [date, home, 'H', away, 'REG', homeWine, None]
        awayPrepend = [date, away, '@', home, 'REG', awayWin, None]
        
        for player in awayTable.rows:
            name, stats = list(player.items())[0]
            stats = awayPrepend + stats
            player[name] = stats
            
        for player in homeTable.rows:
            name, stats = list(player.items())[0]
            stats = homePrepend + stats
            player[name] = stats

        awayMerged = {}
        homeMerged = {}
        for row in awayTable.rows:
            awayMerged.update(row)
        for row in homeTable.rows:
            homeMerged.update(row)

        away = {away: awayMerged}
        home = {home: homeMerged}
        
        return home, away


"""
SPECIAL HANDLERS

"""

class languageHandler(Handler):
    """
    Data handler for language modeling
    """

    class languagePreprocessor(Preprocessor):
        pass
    
    def __init__(self):
        super().__init__()


class simHandler(Handler):
    """
    Data handler for simulation
    """

    # Class data memebers
    teamsDir = 'test/teams' 
    
    class simPreprocessor(Preprocessor):
        pass

    def __init__(self):

        pass

    @classmethod
    def getTeam(cls, teamName: str) -> dict[str, list[list[str]]]:
        """
        Query the database for a particular team
        """
        file = os.path.join(cls.teamsDir, f'{teamName}.pkl')

        if not os.path.exists(file):
            raise Exception(f'The team {teamName} does not exist!!')

        with open(file, 'rb') as fp:
            players = pickle.load(fp)
            if players.get(teamName):
                return players
            else:
                return {teamName: players}
        
    @classmethod
    def updateTeam(cls, teamName):
        
        teamSc = NCAABTeamScraper(teamName)
        team = simHandler.getTeam(teamName)
        teamName = list(team.keys())[0]
        
        links = teamSc.gameLinks()
        schedule = teamSc.getSchedule()

        updates = []
        
        if list(team[teamName].keys())[0] == teamName:
            # TOO MUCH NESTING
            team = team[teamName]

        for player, stats in team[teamName].items():
            
            if len(stats.rows) >= 1:
            
                pattern = lambda x: 'Games' in x[0]
                stats.drop(pattern)

                playerLastUpdate = stats.rows[-1][0]
                playerLastUpdate = datetime.strptime(playerLastUpdate, '%Y-%m-%d').date()
                updates.append((player, playerLastUpdate))

        mostCurrent = max([update[1] for update in updates])

        updateQueue = [(datetime.strptime(row[0], '%Y-%m-%d').date(), row[2]) for row in schedule[0] if datetime.strptime(row[0], '%Y-%m-%d').date() > mostCurrent]
        
        if len(updateQueue) == 0:
            with open(f'test/teams/{teamName}.pkl', 'wb') as file:
                pickle.dump(team, file)
                print(f'updated team {teamName}')


        for row in links.rows:
            date, link, oppTeam = row[0][0], row[0][1], row[1]
            
            if (date, oppTeam) in updateQueue:
                gs = GameScraper(link)

                homeUpdates, awayUpdates = gs.generateTables()

                if teamName in list(homeUpdates.keys()):
                    homeTeamName = teamName
                    awayTeamName = list(awayUpdates.keys())[0]
                    away = simHandler.getTeam(awayTeamName)
                    home = team
                elif teamName in list(awayUpdates.keys()):
                    homeTeamName = list(homeUpdates.keys())[0]
                    awayTeamName = teamName
                    home = simHandler.getTeam(homeTeamName)
                    away = team
                else:
                    raise Exception('Could not find teamname in updates')

                for player, update in homeUpdates[homeTeamName].items():
                    if home[homeTeamName].get(player):
                        home[homeTeamName][player].rows.append(update)
                
                for player, update in awayUpdates[awayTeamName].items():
                    if away[awayTeamName].get(player):
                        away[awayTeamName][player].rows.append(update)
                
                with open(f'test/teams/{homeTeamName}.pkl', 'wb') as file:
                    pickle.dump(home, file)
                    print(f'updated team {homeTeamName}')
                with open(f'test/teams/{awayTeamName}.pkl', 'wb') as file:
                    print(f'updated team {awayTeamName}')
                    pickle.dump(away, file)

    @classmethod
    def exists(cls, teamName):
        file = os.path.join(cls.teamsDir, f'{teamName}.pkl')
        return os.path.exists(file)

class powerHandler(Handler):
    """
    Data handler for power rankings
    """
    class powerPreprocessor(Preprocessor):
        pass

    def __init__(self):
        super().__init__()

