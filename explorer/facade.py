import os
from pathlib import Path

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

    def get_default_dir(self):
        """
        Get current user's home directory.

        Returns
        ---------------
        path : Path
            path to current user's home directory
        """

        path = Path(os.environ['userprofile'])
        return path
