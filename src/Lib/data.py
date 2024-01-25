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

            def _combine_headers(over_headers, main_header):
                """Combines over headers and main headers, appending over header text to main headers."""
                return [
                    over_headers + (f'_{main_header[i]}' if main_header[i] else '')
                    for i, over_headers in enumerate(over_headers)
                ]

            def _clean_header_values(header):
                illegal_characters = ['.', '-', ' ', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '=', '{', '}', '[', ']', '|', '\\', '/', '?', '<', '>', "'", '¥', '¢', '£', '¬']
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

            combined_headers = _combine_headers(over_headers, main_headers)[1:] # eliminate id at position 0

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

    class Table:
        def __init__(self, name, cols) -> None:
            self.name = name
            self.cols = cols

        def __str__(self):
            col_str =  ', '.join([f'{key} {value}' for key, value in self.cols.items()])
            return f'{self.name} ({col_str})'

        def __repr__(self):
            return self.__str__()


    def __init__(self, database, **kwargs):

        
        self.conn = sqlite3.connect(database)
        self.cursor = self.conn.cursor()
        # initial table assignment
        

    def clear(self):
        for table in self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall():
            self.cursor.execute(f"DROP TABLE {table[0]};")
        self.conn.commit()

        
    def exists(self, table):
        return table in self.tableNames()

    def create(self, table):
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {table}')
        self.conn.commit()

    def retreive(self, query=None):
        if query is None:
            query = 'SELECT * FROM sqlite_master WHERE type="table"'
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def insert(self, values, table=None):
        self.conn.commit()

    def update(self, query, values):
        self.cursor.execute(query, values)
        self.conn.commit()

    def delete(self, query, values):
        self.cursor.execute(query, values)
        self.conn.commit()

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

