import pathlib
import shutil


class FileExplorer:

    def get_content(self, path):
        """
        Return directory content.

        Returns
        ---------------
        dict
            obj type: list of Path objects representing files/directories
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
            string representation of source file/directory
        dst : str
            string representation of destination directory
        src_type : {dir, file}
            string with src type (one of the above) to run appropriate checks

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
            raise ValueError("Invalid src_type")

        src = pathlib.Path(src)
        dst = pathlib.Path(dst)

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

        Returns
        ---------------
        Path
            Path object for the newly created file
        """

        src = pathlib.Path(src)
        dst = pathlib.Path(dst)

        if not src.is_file():
            raise FileNotFoundError("Invalid source file path")
        elif not dst.is_dir():
            raise FileNotFoundError("Invalid destination directory path")

        dst = dst / src.name
        if dst.exists():
            index = len(list(dst.parent.glob(f"{dst.stem}*{dst.suffix}")))
            dst = dst.parent / f"{src.stem}_copy_{index}{dst.suffix}"

        return pathlib.Path(shutil.copy2(src, dst))

    def copy_dir(self, src, dst):
        """
        Copy directory with it's content to a dst location.
        Add a suffix if directory already exists in dst.
        """

        src = pathlib.Path(src)
        dst = pathlib.Path(dst)

        if not src.is_dir():
            raise FileNotFoundError("Invalid source directory path")
        elif not dst.is_dir():
            raise FileNotFoundError("Invalid destination directory path")

        dst = dst / src.name
        if dst.exists():
            index = len(list(dst.parent.glob(f"{dst.stem}*")))
            dst = dst.parent / f"{src.stem}_copy_{index}"

        return pathlib.Path(shutil.copytree(src, dst))
