import pathlib
import shutil
import os


class FileExplorer:

    def get_content(self, path):
        """
        Return directory content.

        Parameters
        ---------------
        path : str
            dir path

        Returns
        ---------------
        dict
            obj type: list of Path objects representing files/directories

        Raises
        ---------------
        FileNotFoundError
            If path is not a directory
        """

        path = pathlib.Path(path)
        if path.is_dir():
            content = {
                "files": [],
                "dirs": []
            }
            for obj in path.iterdir():
                if obj.is_file():
                    content["files"].append(obj)
                elif obj.is_dir():
                    content["dirs"].append(obj)
            return content
        else:
            raise FileNotFoundError("Directory does not exist")

    def is_valid_path(self, src, dst, src_type):
        """
        Check if src and dst are valid paths to files/dirs and suitable to copy

        Parameters
        ---------------
        src : str
            path to source file/dir
        dst : str
            path to destination dir
        src_type : {dir, file}
            src type (one of the above) to run appropriate checks

        Returns
        ---------------
        tuple
            both Path objects (src, dst)

        Raises
        ---------------
        FileNotFoundError
            If the src file/dir or dst dir are invalid
        ValueError
            If the src_type is not in {file, dir}
        """

        if src_type not in ["file", "dir"]:
            msg = f"src_type should be 'file' or 'dir' not {src_type}"
            raise ValueError(msg)

        src = pathlib.Path(src) if not isinstance(src, pathlib.Path) else src
        dst = pathlib.Path(dst) if not isinstance(dst, pathlib.Path) else dst

        if src_type == "file" and not src.is_file():
            raise FileNotFoundError("Invalid source file path")
        elif src_type == "dir" and not src.is_dir():
            raise FileNotFoundError("Invalid source directory path")
        elif not dst.is_dir():
            raise FileNotFoundError("Invalid destination directory path")

        return src, dst

    def copy_file(self, src, dst):
        """
        Copy a file into a specified destination directory.
        Add a suffix if file already exists in dst

        Parameters
        ---------------
        src : str or Path
            path to source file
        dst : str or Path
            path to destination dir

        Returns
        ---------------
        Path
            Path object for the newly created file
        """

        src, dst = self.is_valid_path(src, dst, "file")

        dst = dst / src.name
        if dst.exists():
            index = len(list(dst.parent.glob(f"{dst.stem}*{dst.suffix}")))
            dst = dst.parent / f"{src.stem}_copy_{index}{dst.suffix}"

        return pathlib.Path(shutil.copy2(src, dst))

    def copy_dir(self, src, dst):
        """
        Copy directory with it's content to a dst location.
        Add a suffix if directory already exists in dst.

        Parameters
        ---------------
        src : str or Path
            path to source dir
        dst : str or Path
            path to destination dir

        Returns
        ---------------
        Path
            Path object for the newly created dir
        """

        src, dst = self.is_valid_path(src, dst, "dir")

        dst = dst / src.name
        if dst.exists():
            index = len(list(dst.parent.glob(f"{dst.stem}*")))
            dst = dst.parent / f"{src.stem}_copy_{index}"

        return pathlib.Path(shutil.copytree(src, dst))

    def copy(self, src, dst):
        """
        Copy file/dir into dst using copy_file/copy_dir depending on src type

        Parameters
        ---------------
        src : str
            path to source file/dir
        dst : str
            path to destination dir

        Returns
        ---------------
        Path
            Path object for the newly created file/dir

        Raises
        -------------
        FileNotFoundError
            If src path does not exist
        """

        src = pathlib.Path(src)
        dst = pathlib.Path(dst)

        if src.is_file():
            return self.copy_file(src, dst)
        elif src.is_dir():
            return self.copy_dir(src, dst)
        else:
            raise FileNotFoundError("Invalid src path")

    def move(self, src, dst):
        """
        Move a src file/dir to dst dir.

        Parameters
        ---------------
        src : str
            path to source file/dir
        dst : str
            path to destination dir

        Returns
        ---------------
        Path
            Path object for the newly created file/dir
        """

        moved = self.copy(src, dst)
        if moved:
            src = pathlib.Path(src)
            if src.is_file():
                src.unlink()
            elif src.is_dir():
                shutil.rmtree(src)
        return moved

    def rename(self, src, dst, prefix=None, suffix=None):
        """
        Rename src file/dir to dst. Dst should not have an extension.

        Parameters
        ---------------
        src : str or Path
            path to source file/dir
        dst : str or Path
            new file/dir name
        prefix : str
            add before dst - path/prefix_dst
        suffix : str
            add after dst stem, before extension - path/prefix_stem_suffix.ext

        Returns
        ---------------
        Path
            newly named file/dir path
        """

        if not isinstance(src, pathlib.Path):
            src = pathlib.Path(src)

        if not isinstance(dst, pathlib.Path):
            dst = pathlib.Path(dst)

        dst = src.parent / f"{dst.name}{src.suffix}"

        if prefix:
            dst = dst.parent / f"{prefix}_{dst.name}"

        if suffix:
            dst = dst.parent / f"{dst.stem}_{suffix}{dst.suffix}"

        return src.rename(dst)

    def rm(self, src):
        """
        Remove src file/dir.

        Parameters
        ---------------
        src : str or Path
            path to source file/dir

        Raises
        ---------------
        FileNotFoundError
            If src path does not exist
        """

        src = pathlib.Path(src) if not isinstance(src, pathlib.Path) else src

        if src.is_file():
            src.unlink()
        elif src.is_dir():
            shutil.rmtree(src)
        else:
            raise FileNotFoundError("Invalid src path")

        return None

    def open_file(self, src):
        """
        Open a file in associated application.

        Parameters
        ---------------
        src : str or Path
            path to source file
        """

        src = pathlib.Path(src) if not isinstance(src, pathlib.Path) else src

        if src.is_file():
            os.startfile(src)
