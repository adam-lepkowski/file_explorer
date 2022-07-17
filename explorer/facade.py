from explorer import FileExplorer, Cache


class Facade:
    """
    Facade for FileExplorer with Cache functionality.

    Attributes
    ---------------
    fe : FileExplorer
    cache : Cache
    """

    def __init__(self):
        self.fe = FileExplorer()
        self.cache = Cache()
