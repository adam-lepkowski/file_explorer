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
    current_obj : None or Path
        path to a source object for later use (move, copy)
    """

    def __init__(self):
        self.fe = FileExplorer()
        self.cache = Cache()
        self.current_obj = None

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

        Raises
        ---------------
        FileNotFoundError
            If path is not a directory
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

    def get_parent(self, path):
        """
        Get path parent directory.

        Parameters
        ---------------
        path : str
            path to child directory

        Returns
        ---------------
        Path
            path obj representing parent path

        Raises
        ---------------
        FileNotFoundError
            If path is not a directory
        """

        path = Path(path)
        if path.is_dir():
            return path.parent
        else:
            raise FileNotFoundError("Invalid directory path")

    def copy(self, directory, name):
        """
        Store obj path for later use.

        Parameters
        ---------------
        directory : str
            absolute path to file or dir stored for copy
        name : str
            file or dir name

        Raises
        ---------------
        FileNotFoundError
            If path is not a directory
        """

        path = Path(directory) / name
        if path.exists():
            self.current_obj = path
        else:
            raise FileNotFoundError("Target does not exist")

    def paste(self, dst):
        """
        Paste copied object.

        Parameters
        ---------------
        dst : str
            path to destination dir
        """

        if self.current_obj:
            src = self.current_obj
            self.fe.copy(src, dst)

    def is_valid_path(self, path):
        return Path(path).is_dir()
