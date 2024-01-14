"""
GENERAL

"""

import sqlite3
import requests
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

            return _combine_headers(main_headers, over_headers)


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

class DataBase:
    """
    Interface for interacting with and manipulating a database
    """
    def __init__(self, database):

        # Create a connection to the database (or create it if it doesn't exist)
        self.conn = sqlite3.connect(database)

        # Create a cursor object to execute SQL commands
        self.cursor = self.conn.cursor()

        
    def create(self, name, cols):
        # Create a table called 'users' with columns 'id', 'name', and 'age'
        self.cursor.execute(f'CREATE TABLE {name} {cols}')


    def read(self):
        pass

    def write(self):
        pass

    def close(self):
        """
        Close the connection
        """
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

