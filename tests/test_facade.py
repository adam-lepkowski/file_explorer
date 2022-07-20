import unittest
from unittest.mock import patch
from pathlib import Path

from parameterized import parameterized

from explorer import Facade


class TestGetDefaultDir(unittest.TestCase):

    def setUp(self):
        self.facade = Facade()

    def test_get_default_dir(self):
        result = self.facade.get_default_dir()
        self.assertTrue(isinstance(result, Path))


class TestGetContent(unittest.TestCase):

    def setUp(self):
        self.facade = Facade()
        self.content = {
            "dirs": [Path("dir1")],
            "files": [Path("file1.py")]
        }

    @patch("explorer.facade.os.path.getmtime", return_value=1)
    @patch("explorer.facade.FileExplorer.get_content")
    def test_get_content(self, mock_explorer, mock_getmtime):
        mock_explorer.return_value = self.content
        expected = [
            ("dir1", "1970/01/01 01:00:01", "dirs"),
            ("file1.py", "1970/01/01 01:00:01", "files")
        ]
        result = self.facade.get_content("foo/bar")
        self.assertEqual(expected, result)
