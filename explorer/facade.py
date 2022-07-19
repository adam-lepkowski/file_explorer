import os
import time
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

    def get_content(self, path):
        """
        Get directory content.

        Parameters
        ---------------
        path : Path or str
            dir path

        Returns
        ---------------
        list
            list of tuples with filename, modification datetime and obj type
        """

        content = self.fe.get_content(path)
        form = "%Y/%m/%d %H:%M:%S"
        result = []
        for type, objects in content.items():
            for obj in objects:
                mt = time.strftime(form, time.localtime(os.path.getmtime(obj)))
                row = obj.name, mt, type
                result.append(row)
        return result
