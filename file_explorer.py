import os


class FileExplorer:

    def get_content(self, path):
        """
        Return directory content with files and directories specified.

        Returns
        ---------------
        dict
            obj type: list of files/directories
        """

        content = {
            "files": [],
            "dirs": []
        }
        for obj in os.scandir(path):
            if obj.is_file():
                content["files"].append(obj.path)
            elif obj.is_dir():
                content["dirs"].append(obj.path)
        return content
