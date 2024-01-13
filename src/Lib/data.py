"""
GENERAL

"""

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



