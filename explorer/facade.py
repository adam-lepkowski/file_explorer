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
    current_obj : None or dict
        path: path to a source object for later use
        func: move or copy
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

    def paste(self, dst):
        """
        Paste copied object and cache action.

        Parameters
        ---------------
        dst : str
            path to destination dir
        """

        if self.current_obj:
            src = self.current_obj["src"]
            new_obj = getattr(self.fe, self.current_obj["func"])(src, dst)
            item = {
                "src": src,
                "func": self.current_obj["func"],
                "dst": dst,
                "new_obj": new_obj
            }
            self.cache.store(item)

    def is_valid_path(self, path):
        return Path(path).is_dir()

    def store_src(self, directory, name, func):
        """
        Store obj path for later use.

        Parameters
        ---------------
        directory : str
            absolute path to file or dir stored for copy
        name : str
            file or dir name
        func : {move, copy}
            file operation intended for src file

        Raises
        ---------------
        FileNotFoundError
            If path is not a directory
        """

        path = Path(directory) / str(name)
        if path.exists():
            self.current_obj = {"src": path, "func": func}
        else:
            raise FileNotFoundError("Target does not exist")

    def transfer(self, src, name, dst, func):
        """
        Transfer (copy/move) an object from src to dst.

        Parameters
        ---------------
        src : str
            path to source dir
        name : str
            name of file/directory to be transfered
        dst : str
            path to destination dir
        func : {move, copy}
            file operation intended for src file
        """

        src = Path(src) / str(name)
        getattr(self.fe, func)(src, dst)

    def rename(self, directory, name, new_name):
        """
        Rename a file or directory.

        Parameters
        ---------------
        directory : str
            path to source dir
        name : str
            name of file/directory to be renamed
        new_name : str
            new name for file or directory. File should not contain extension
        """

        src = Path(directory) / str(name)
        if src.exists():
            dst = Path(directory) / str(new_name)
            self.fe.rename(src, dst)
        else:
            raise FileNotFoundError("Invalid source directory path")

    def delete(self, directory, name):
        """
        Permanently delete a file or directory.

        Parameters
        ---------------
        directory : str
            path to source dir
        name : str
            name of file/directory to be deleted
        """

        target = Path(directory) / str(name)
        if target.exists():
            self.fe.rm(target)
