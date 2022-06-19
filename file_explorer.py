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

    def copy_file(self, src, dst):
        """
        Copy a file into a specified destination directory.
        Add a suffix if copying into the same directory.

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
