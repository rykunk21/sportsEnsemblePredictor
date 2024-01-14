"""
GENERAL

"""

import sqlite3
import requests
import re
from bs4 import BeautifulSoup
from typing import Any, Iterator, Optional

class Scraper:

    class Table:
        def __init__(self, htmlContent: Any) -> None:
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

            def _combine_headers(main_headers, over_headers):
                """Combines over headers and main headers, appending over header text to main headers."""
                return [
                    main_header + (f'_{over_headers[i]}' if over_headers[i] else '')
                    for i, main_header in enumerate(main_headers)
                ]

            table_header = self.soup.find('thead')
            if not table_header:
                return None

            over_headers = _extract_over_headers(table_header)

            # flatten over headers
            over_headers = [item for sublist in over_headers for item in sublist]

            main_headers = _extract_main_headers(table_header)

            return _combine_headers(main_headers, over_headers)[1:]

        def drop(self, pattern):
            self.rows = [
                row for row in self.rows
                if not pattern(row)
            ]

        def format(self, pattern):
            self.rows = [
                pattern(row) for row in self.rows
            ]


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
    def __init__(self, database):
        self.conn = sqlite3.connect(database)
        self.cursor = self.conn.cursor()

    def create(self, name, cols):
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {name} {cols}')
        self.conn.commit()

    def read(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def write(self, query, values):
        self.cursor.execute(query, values)
        self.conn.commit()

    def update(self, query, values):
        self.cursor.execute(query, values)
        self.conn.commit()

    def delete(self, query, values):
        self.cursor.execute(query, values)
        self.conn.commit()

    def close(self):
        self.conn.close()



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
    def __init__(self):
        pass

"""
Special Scrapers
"""

class NCAABTeamScraper(Scraper):

    def __init__(self, year):
        """
        Initializes the NCAABTeamScraper with a specific year.
        Sets up the scraper to point to the NCAAB teams URL for the given year
        and retrieves the team statistics table.
        """
        self.ncaabTeamsUrl = f'https://www.sports-reference.com/cbb/seasons/men/{year}-school-stats.html'
        tableId = 'basic_school_stats'

        super().__init__()
        self.visit(self.ncaabTeamsUrl)
        self.table = self.getTable(tableId)
    
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
    class simPreprocessor(Preprocessor):
        pass

    def __init__(self):
        super().__init__()


class powerHandler(Handler):
    """
    Data handler for power rankings
    """
    class powerPreprocessor(Preprocessor):
        pass

    def __init__(self):
        super().__init__()

