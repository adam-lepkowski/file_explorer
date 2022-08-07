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
    current_obj : list
        list of object awaiting further action - copy/move
    last_undo: None or dict
        last undone action. Prevent undo loops
    last_redo: None or dict
        last redone action. Prevent redo loops
    """

    def __init__(self):
        self.fe = FileExplorer()
        self.cache = Cache()
        self.current_obj = []
        self.last_undo = None
        self.last_redo = None

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

        items = []
        if self.current_obj:
            for obj in self.current_obj:
                src = obj["src"]
                new_obj = getattr(self.fe, obj["func"])(src, dst)
                item = {
                    "src": src,
                    "func": obj["func"],
                    "dst": Path(dst),
                    "new_obj": new_obj
                }
                items.append(item)
        self.cache.store(items)

    def is_valid_path(self, path):
        return Path(path).is_dir()

    def store_src(self, objs):
        """
        Store obj path for later use.

        Parameters
        ---------------
        objs : dict
            parent: parent directory
            names: src file/dir names selected
            func : {move, copy}
                file operation intended for src file
        Raises
        ---------------
        FileNotFoundError
            If file/dir does not exist
        """

        current = []
        for name in objs["names"]:
            path = Path(objs["parent"]) / str(name)
            if path.exists():
                current.append({"src": path, "func": objs["func"]})
            else:
                raise FileNotFoundError("Target does not exist")
        self.current_obj = current


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
        new_obj = getattr(self.fe, func)(src, dst)
        item = {
            "src": src,
            "func": func,
            "dst": Path(dst),
            "new_obj": new_obj
        }
        self.cache.store(item)

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
            new_obj = self.fe.rename(src, dst)
            item = {
                "src": src,
                "func": "rename",
                "dst": Path(dst),
                "new_obj": new_obj
            }
            self.cache.store(item)
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

    def undo(self):
        """
        Undo an action.
        """

        action = self.cache.get_current()
        if action and action != self.last_undo:
            if action["func"].lower() == "copy":
                self.fe.rm(action["new_obj"])
            elif action["func"].lower() == "move":
                src = action["new_obj"]
                dst = action["src"].parent
                new_name = src.stem
                prev_name = action["src"].stem
                moved_file = self.fe.move(src, dst)
                if prev_name != new_name:
                    self.fe.rename(moved_file, prev_name)
            elif action["func"].lower() == "rename":
                src = action["new_obj"]
                prev_name = action["src"].stem
                self.fe.rename(src, prev_name)
            self.last_undo = action
            self.last_redo = None
        self.cache.undo()

    def redo(self):
        """
        Redo an undone action.
        """

        action = self.cache.get_current()
        if action and action != self.last_redo:
            func = action["func"]
            src = action["src"]
            dst = action["dst"]
            getattr(self.fe, func)(src, dst)
            self.last_redo = action
            self.last_undo = None
        self.cache.redo()

    def clear_cache(self):
        """
        Reset cache attrs to default values
        """

        self.current_obj = None
        self.last_redo = None
        self.last_undo = None
        self.cache.clear()
