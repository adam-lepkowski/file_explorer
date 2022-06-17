import unittest
from unittest.mock import patch, Mock

from file_explorer import FileExplorer


class TestGetContent(unittest.TestCase):

    def setUp(self):
        self.fe = FileExplorer()

    @patch("file_explorer.os.scandir")
    def test_get_content(self, scandir_mock):
        mocks = [Mock() for _ in range(4)]
        for i, mock in enumerate(mocks):
            mock.is_dir.return_value = True if i % 2 == 0 else False
            mock.is_file.return_value = False if i % 2 == 0 else True
            mock.path = "dir_path" if i % 2 == 0 else "file_path"
        scandir_mock.return_value = mocks
        result = self.fe.get_content("path_not_relevant_to_test")
        expected = {
            "files": ["file_path", "file_path"],
            "dirs": ["dir_path", "dir_path"]
        }
        self.assertEqual(expected, result)
