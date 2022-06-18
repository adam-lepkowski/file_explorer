import unittest
from unittest.mock import patch, Mock

from file_explorer import FileExplorer


class TestGetContent(unittest.TestCase):

    def setUp(self):
        self.fe = FileExplorer()

    @patch("file_explorer.pathlib.Path.iterdir")
    def test_get_content(self, iterdir_mock):
        mocks = [Mock() for _ in range(4)]
        for i, mock in enumerate(mocks):
            mock.is_dir.return_value = True if i % 2 == 0 else False
            mock.is_file.return_value = False if i % 2 == 0 else True
            mock.__str__ = "dir_path" if i % 2 == 0 else "file_path"
        iterdir_mock.return_value = mocks
        result = self.fe.get_content(".")
        expected = {
            "files": [mocks[1], mocks[3]],
            "dirs": [mocks[0], mocks[2]]
        }
        self.assertEqual(expected, result)

    def test_get_content_invalid_path_raises_error(self):
        with self.assertRaises(FileNotFoundError):
            self.fe.get_content('invalid_path')

    @patch("file_explorer.pathlib.Path.iterdir")
    def test_get_content_empty_dir(self, iterdir_mock):
        iterdir_mock.return_value = []
        expected = {
            "files": [],
            "dirs": []
        }
        result = self.fe.get_content(".")
        self.assertEqual(expected, result)


class TestCopyFile(unittest.TestCase):

    def setUp(self):
        self.fe = FileExplorer()

    @patch("file_explorer.pathlib.Path.is_file")
    def test_src_not_file_raises_error(self, is_file_mock):
        with self.assertRaises(FileNotFoundError):
            is_file_mock.return_value = False
            src = "src/path"
            dst = "dst/path"
            self.fe.copy_file(src, dst)

    @patch("file_explorer.pathlib.Path.is_file")
    def test_dst_not_dir_raises_error(self, is_file_mock):
        with self.assertRaises(FileNotFoundError):
            is_file_mock.return_value = True
            src = "src/path"
            dst = "dst/path"
            self.fe.copy_file(src, dst)
