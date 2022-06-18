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

        if not src.exists():
            raise FileNotFoundError("Invalid source file path")
        elif not dst.is_dir():
            raise FileNotFoundError("Invalid destination directory path")

        if src.parent == dst:
            copied_fname = f"{src.stem}_copy{src.suffix}"
            dst = dst / copied_fname
            if dst.exists():
                index = len(list(dst.parent.glob(f"{dst.stem}*{dst.suffix}")))
                dst = dst.parent / f"{dst.stem}_{index + 1}{dst.suffix}"

        return pathlib.Path(shutil.copy2(src, dst))
